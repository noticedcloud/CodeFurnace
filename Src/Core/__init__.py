from .BaseShell import complete, execute,check_read_line, console, _do_help
from .HistoryManager import save_history
from .ModuleLoader import use, set, load_exploits_list, load_payloads_list
from .Printer import print_items, options
from .CodeFurnace import CodeFurnace
from .AIHandler import get_response, handle_response

# BASE SHELL

CodeFurnace.execute = execute
CodeFurnace.complete = complete
CodeFurnace.check_read_line = check_read_line
CodeFurnace.console = console
CodeFurnace._do_help = _do_help

# HISTORY MANAGER

CodeFurnace.save_history = save_history

# MODULE LOADER

CodeFurnace.use = use
CodeFurnace.set = set
CodeFurnace.load_exploits_list = load_exploits_list
CodeFurnace.load_payloads_list = load_payloads_list

# PRINTER

CodeFurnace.print_items = print_items
CodeFurnace.options = options

# AI HANDLER
CodeFurnace.handle_response = handle_response
CodeFurnace.get_response = get_response