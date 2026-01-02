import pythonnet
pythonnet.load("coreclr")

import clr
import threading
from os import getcwd

from Lib.Debugger import info, warning, error

class Scanner:
    def __init__(self) -> None:
        path = getcwd()
        clr.AddReference(f"{path}/Server/Exploits/NoticedCloud/.Scanner/Scanner.dll")

        from Scanner import PortScanner

        self.scanner = PortScanner()
        self.scanning = False
        self.scan_result = []
        self.commands: dict = {"exploit": "runs the exploit", "run": "runs the exploit"}
        self.RHOST: str = "0.0.0.0"
        self.START_PORT: int = 1
        self.END_PORT: int = 1000
        self.EXPLOIT: str = "Server/Exploits/NoticedCloud/"
        self._ports_scanned = 0

    def exec(self, command: str) -> any:
        if command.startswith("payload_gen"):
            self.payload_gen(command)
        elif command == "exploit" or command == "run":
            self.exploit()
        elif command == "":
            self.print_progress()
        else:
            return 1

    def set(self, *args, **kwargs) -> None:
        if "rhost" in args[0]:
            self.RHOST = args[0]["rhost"]
            info(f"RHOST set to {self.RHOST}")
        elif "start_port" in args[0]:
            self.START_PORT = int(args[0]["start_port"])
            info(f"START_PORT set to {self.START_PORT}")
        elif "end_port" in args[0]:
            self.END_PORT = int(args[0]["end_port"])
            info(f"END_PORT set to {self.END_PORT}")
        else:
            warning("Argument not valid")

    def get_options(self) -> dict:
        return {
            "rhost": self.RHOST,
            "start_port": self.START_PORT,
            "end_port": self.END_PORT
        }

    def options(self) -> None:
        print(f"""
{'CONTENT':<12} {'VALUE':<15} {'REQUIRED':<10}

{'-----------':<12} {'---------------':<15} {'----------':<10}

{'RHOST':<12} {self.RHOST:<15} {'True':<10}

{'START_PORT':<12} {self.START_PORT:<15} {'True':<10}
{'END_PORT':<12} {self.END_PORT:<15} {'True':<10}

""")

    def scan_thread(self):
        try:
            total_ports = self.END_PORT - self.START_PORT + 1
            self._ports_scanned = 0
            self.scan_result = []

            for port in range(self.START_PORT, self.END_PORT + 1):
                result = self.scanner.Scan(self.RHOST, port)
                self.scan_result.append((port, result))
                self._ports_scanned += 1

            self.scanning = False

        except Exception as e:
            import traceback
            traceback.print_exc()
            error(f"Errore durante la scansione: {e}")
            self.scanning = False


    def exploit(self) -> None:
        if not self.scanning:
            self.scanning = True
            th = threading.Thread(target=self.scan_thread, daemon=True)
            th.start()
            print("Scansione avviata! Premi Invio per vedere lo stato.")
            th.join()
            
        else:
            print("Scansione già in corso...")

    def print_progress(self):
        if not self.scanning:
            print("Nessuna scansione in corso.")
            return

        total_ports = self.END_PORT - self.START_PORT + 1
        percent = (self._ports_scanned / total_ports) * 100
        print(f"Scansione completata: {percent:.2f}% ({self._ports_scanned}/{total_ports} porte scansionate)")