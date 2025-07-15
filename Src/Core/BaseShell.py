import os

try:
    import readline
except ImportError:
    try:
        import pyreadline3 as readline
    except ImportError:
        readline = None

from Lib.Debugger import info, warning, error

from colorama import Fore, Style

def complete(self, text: str, state: int) -> None:
    buffer = readline.get_line_buffer()
    line = buffer.strip().split()

    completions: List[str] = []
    exploit_commands: List[str] = []

    if self.exploit is not None:
        exploit_commands = list(self.exploit.commands.keys())

    if not line:
        completions = ["use", "set", "show", "quit", "help"] + exploit_commands
    elif line[0] == "use":
        base = text.lower()
        completions = [e for e in self.exploits_list if e.lower().startswith(base)]
    elif line[0] == "cd":
        base = text.lower()
        folder_list: List[str] = [f for f in os.listdir() if os.path.isdir(os.path.join(f))]
        completions = [e for e in folder_list if e.lower().startswith(base)]
    elif line[0] == "show":
        options = ["options", "exploits", "payloads"]
        completions = [o for o in options if o.startswith(text)]
    elif line[0] == "set":
        if self.exploit is not None:
            try:
                opts = list(self.exploit.get_options().keys())
                if len(line) >= 2 and line[1].lower() == "payload":
                    completions = [p for p in self.payloads_list if p.lower().startswith(text.lower())]
                else:
                    completions = [o for o in opts if o.startswith(text.lower())]
            except Exception:
                pass

    else:
        completions = [
            cmd for cmd in ["use", "set", "show", "quit", "help", "getcwd", "cd"] + exploit_commands
            if cmd.lower().startswith(text.lower())
        ]

    return completions[state] if state < len(completions) else None

def check_read_line(self) -> None:
    global readline

    if readline is None:
        warning("Install readline, for better experience.")
        option = input("Do you want to install it automatically (Y/n)? ").lower()

        if not option or option.startswith('y'):
            lib_import = "pyreadline3" if os.name == "nt" else "readline"
            os.system(f"pip install {lib_import}")

            try:
                try:
                    import readline
                except ImportError:
                    import pyreadline3 as readline
            except Exception as e:
                error(f"Failed to import readline: {e}")
                return

        if readline:
            info(f"{lib_import} installed and imported successfully.")

            readline.set_completer_delims(" \t\n")
            readline.parse_and_bind("tab: complete")
            readline.set_completer(self.complete)

            if os.path.exists(self.HISTORY_FILE):
                readline.read_history_file(self.HISTORY_FILE)


def _do_help(self) -> None:
    exploit_commands = ""

    if self.exploit and self.exploit.commands:
        exploit_commands = '\n'.join(
            f"  {Fore.CYAN}{k:<12}{Style.RESET_ALL} {v}" for k, v in sorted(self.exploit.commands.items())
        )

    help_text = f"""{Fore.YELLOW}usage: {Fore.WHITE}[command] [options]{Style.RESET_ALL}

{Fore.YELLOW}commands:{Style.RESET_ALL}
  {Fore.GREEN}use <exploit>{Style.RESET_ALL}         Select an exploit module
  {Fore.GREEN}set <opt> <value>{Style.RESET_ALL}     Set an option for the current module
  {Fore.GREEN}show [type]{Style.RESET_ALL}           Show information (type = options, exploits, payloads)
  {Fore.GREEN}cd <folder>{Style.RESET_ALL}           Moves to a certain folder
  {Fore.GREEN}getcwd{Style.RESET_ALL}                Show current working directory
  {Fore.GREEN}quit{Style.RESET_ALL}                  Exit the framework

{Fore.YELLOW}show options:{Style.RESET_ALL}
  {Fore.GREEN}options{Style.RESET_ALL}     Show the current exploit's configurable options
  {Fore.GREEN}exploits{Style.RESET_ALL}    List all available exploits
  {Fore.GREEN}payloads{Style.RESET_ALL}    List all available payloads
"""

    print(help_text)

    if exploit_commands:
        print(
            f"\n{Fore.MAGENTA}exploit-specific commands ({self.exploit.__class__.__name__}):{Style.RESET_ALL}\n{exploit_commands}")

def execute(self, command: str) -> None:
    if command.startswith("use"):
        exploit = command.split()[1]
        result = self.use(exploit)

        if result:
            self.input = f"CodeFurnace exploit(\033[91m{exploit}\033[0m) >> "
        else:
            error("Exploit not found")
    elif command.startswith("set"):
        if self.exploit is None:
            error("Please specify an exploit before")
        else:
            action = command.split()[1]
            content = command.split()[2]
            self.set({f"{action.lower()}": f"{content}"})
    elif command.startswith("cd"):
        parts = command.split()
        if len(parts) == 2:
            os.chdir(parts[1])
            return
        elif len(parts) > 2:
            error("cd has no optional parameter called", parts[2])
            return
        os.chdir(os.path.expanduser("~"))
    elif command == "getcwd":
        print(os.getcwd())
    elif command.startswith("show"):
        subcmds = command.split()
        if len(subcmds) < 2:
            error("You must specify a subcommand: options, exploits, payloads")
            return

        sub = subcmds[1].lower()

        if sub == "options":
            if self.exploit is not None:
                self.options()
            else:
                error("You must specify an exploit before")
        elif sub == "exploits":
            self.print_items("Server/Exploits")
            self.load_exploits_list()
        elif sub == "payloads":
            self.print_items("Server/Payloads")

        else:
            error("You must use a valid subcommand: options, exploits, payloads")

    elif command == "help":
        self._do_help()

    else:
        content = 0

        if self.exploit:
            content = self.exploit.exec(command)

        if content == 1 or not self.exploit:
            command = f'powershell -NoProfile -Command "{command}"' if os.name == "nt" else command
            os.system(command)


def console(self) -> None:
    self.load_payloads_list()
    self.load_exploits_list()
    self.check_read_line()

    while True:
        try:
            command = input(self.input).strip()

            if command == "quit":
                info("Closing the app...")

                break

            self.execute(command)
        except KeyboardInterrupt:
            print()
        finally:
            self.save_history()