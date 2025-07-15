import os

try:
    import readline
except ImportError:
    try:
        import pyreadline3 as readline
    except ImportError:
        readline = None

from Lib.Template import Template

from typing import Optional, List

class CodeFurnace:
    def __init__(self) -> None:
        self.exploit: Optional[Template] = None
        self.input: str = "CodeFurnace >> "
        self.exploits_list: List[str] = []
        self.payloads_list: List[str] = []
        self.original_path: str = os.getcwd()
        self.HISTORY_FILE: str = "history.txt"

        if readline:
            readline.set_completer_delims(" \t\n")
            readline.parse_and_bind("tab: complete")
            readline.set_completer(self.complete)

            if os.path.exists(self.HISTORY_FILE):
                readline.read_history_file(self.HISTORY_FILE)