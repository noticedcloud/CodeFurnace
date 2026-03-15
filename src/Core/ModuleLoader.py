import os
import importlib
import inspect
from Core.IModule import IModule
from Core.GenericAdapter import GenericAdapter
from Core.PayloadAdapter import PayloadAdapter
from Core.IPayload import IPayload
from Lib.Debugger import info, warning, error
def use(self, exploit_path: str) -> bool:
    file_py = f"Server/Exploits/{exploit_path}.py"
    file_json = f"Server/Exploits/{exploit_path}.json"
    if os.path.exists(file_json):
        try:
            self.exploit = GenericAdapter(file_json)
            if hasattr(self.exploit, "get_metadata"):
                try:
                    meta = self.exploit.get_metadata()
                    if "name" in meta and "version" in meta:
                        info(f"Loaded {meta['name']} (v{meta['version']}) [Polyglot]")
                except:
                    pass
            return True
        except Exception as e:
            error(f"Failed to load polyglot exploit: {e}")
            return False
    if not os.path.exists(file_py):
        return False
    module_path = exploit_path.replace("/", ".")
    class_name = module_path.split(".")[-1]
    try:
        module = importlib.import_module(f"Server.Exploits.{module_path}")
        if not hasattr(module, class_name):
            error(f"Class {class_name} not found in {module_path}")
            return False
        exploit_class = getattr(module, class_name)
        if not issubclass(exploit_class, IModule) and exploit_class.__name__ != "NCEXP":
             warning(f"Warning: {class_name} does not inherit from IModule. Some features may break.")
        self.exploit = exploit_class()
        if hasattr(self.exploit, "get_metadata"):
            try:
                meta = self.exploit.get_metadata()
                if "name" in meta and "version" in meta:
                    info(f"Loaded {meta['name']} (v{meta['version']})")
            except:
                pass
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
            elif file.endswith(".json"):
                rel_path = os.path.relpath(os.path.join(root, file), "Server/Exploits")
                path = rel_path.replace("\\", "/").replace(".json", "")
                self.exploits_list.append(path)
def load_payloads_list(self) -> None:
    self.payloads_list.clear()
    for root, dirs, files in os.walk("Server/Payloads"):
        dirs[:] = [d for d in dirs if d != '__pycache__' and not d.startswith("_")]
        if "payload.json" in files:
            rel_path = os.path.relpath(root, "Server/Payloads")
            path = rel_path.replace("\\", "/") 
            self.payloads_list.append(path)
            continue 
        for file in files:
            if file.endswith(".py"):
                rel_path = os.path.relpath(os.path.join(root, file), "Server/Payloads")
                path = rel_path.replace("\\", "/").replace(".py", "")
                self.payloads_list.append(path)
def load_payload_module(payload_path: str) -> IPayload:
    """
    Loads a payload module given its relative path (e.g. Windows/reverse_tcp)
    """
    dir_path = f"Server/Payloads/{payload_path}"
    manifest_path = os.path.join(dir_path, "payload.json")
    if os.path.exists(manifest_path):
        try:
            return PayloadAdapter(manifest_path)
        except Exception as e:
            error(f"Failed to load payload manifest: {e}")
            return None
    file_path = f"Server/Payloads/{payload_path}.py"
    if os.path.exists(file_path):
        module_path = payload_path.replace("/", ".")
        try:
            module = importlib.import_module(f"Server.Payloads.{module_path}")
            class_name = module_path.split(".")[-1]
            if not hasattr(module, class_name):
                 error(f"Class {class_name} not found in {module_path}")
                 return None
            payload_class = getattr(module, class_name)
            return payload_class()
        except Exception as e:
            error(f"Failed to load python payload: {e}")
            return None
    return None
