import os
import importlib

from Lib.Debugger import info, warning, error

def use(self, exploit_path: str) -> bool:
    file_path = f"Server/Exploits/{exploit_path}.py"

    if not os.path.exists(file_path):
        return False

    module_path = exploit_path.replace("/", ".")
    class_name = module_path.split(".")[-1]

    try:
        module = importlib.import_module(f"Server.Exploits.{module_path}")
        self.exploit = getattr(module, class_name)()
        return True
    except Exception as e:
        error(f"Failed to load exploit: {e}")
        return False


def set(self, *args) -> None:
    self.exploit.set(args[0])

def load_exploits_list(self) -> None:
    self.exploits_list.clear()
    for root, dirs, files in os.walk("Server/Exploits"):
        dirs[:] = [d for d in dirs if d != '__pycache__' and not d.startswith("_")]
        for file in files:
            if file.endswith(".py"):
                rel_path = os.path.relpath(os.path.join(root, file), "Server/Exploits")
                path = rel_path.replace("\\", "/").replace(".py", "")
                self.exploits_list.append(path)


def load_payloads_list(self) -> None:
    self.payloads_list.clear()
    for root, dirs, files in os.walk("Server/Payloads"):
        dirs[:] = [d for d in dirs if d != '__pycache__' and not d.startswith("_")]
        for file in files:
            if file.endswith(".py"):
                rel_path = os.path.relpath(os.path.join(root, file), "Server/Payloads")
                path = rel_path.replace("\\", "/").replace(".py", "")
                self.payloads_list.append(path)