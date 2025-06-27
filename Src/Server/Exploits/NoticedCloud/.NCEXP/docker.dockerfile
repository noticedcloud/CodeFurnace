FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y python3 python3-venv python3-pip

RUN pip install pyinstaller pillow GPUtil psutil opencv-python keyboard

WORKDIR /app

COPY {{filename}}.py .

CMD ["pyinstaller", "--onefile", "{{filename}}.py", "--icon=Lib/icon.ico", "--name", "{{filename}}", "--hidden-import", "GPUtil", "--hidden-import", "PIL"]