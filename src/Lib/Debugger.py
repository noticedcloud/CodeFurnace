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

from datetime import datetime

def error(*msg) -> None:
    time: datetime = datetime.now()
    print(F"[ \033[91mERROR\033[0m | \033[36m{time.hour}:{time.minute}:{time.second}\033[0m ]", *msg)

def warning(*msg) -> None:
    time: datetime = datetime.now()
    print(F"[ \033[93mWARNING\033[0m | \033[36m{time.hour}:{time.minute}:{time.second}\033[0m ]", *msg)

def Debug(*msg) -> None:
    time: datetime = datetime.now()
    print(F"[ \033[92mDEBUG\033[0m | \033[36m{time.hour}:{time.minute}:{time.second}\033[0m ]", *msg)

def info(*msg) -> None:
    time: datetime = datetime.now()
    print(F"[ \033[36mINFO\033[0m | \033[36m{time.hour}:{time.minute}:{time.second}\033[0m ]", *msg)