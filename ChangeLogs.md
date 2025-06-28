# Changelog

## 01/05/2025 – v0.4

### 🆕 Added
- Introduced `CHANGELOG.md`.

### ✏️ Changes in [`cmrconsole.py`](Src/cmrconsole.py)
- Replaced `exec` with `importlib` in the `Use` method.
- Removed `PrintExploits` and `PrintPayloads` methods.
- Added `PrintItems` function to list exploits and payloads.
- Reworked the `show` command to support subcommands.
- Added autocompletion for exploit names.

### ✏️ Changes in [`NCEXP.py`](Src/Server/Exploits/NoticedCloud/NCEXP.py)
- Added `_load_template` and `_load_imports` helper functions.

## 03/05/2025 - v0.6

### 🆕 Added
- Introduced `requirements.txt`.

### ✏️ Changes in [`cmrconsole.py`](Src/cmrconsole.py)
- Reworked the autocompletion.
- Removed `run`, `exploit` and `payload_gen` commands.
- Reworked the else statement for the commands.
- Reworked the `show` command to support exploit commands.

### ✏️ Changes in [`NCEXP.py`](Src/Server/Exploits/NoticedCloud/NCEXP.py)
- Added exploit commands.
- Added `exec` function to run exploit commands.
- Added `run`, `exploit` and `payload_gen` commands.

### ✏️ Changes in [`Template.py`](Src/Lib/Template.py)
- Added `exec` function.

## 03/05/2025 - v0.7

### ✏️ Changes in [`cmrconsole.py`](Src/cmrconsole.py)
- Fixed the autocompletion.

## 12/06/2025 - v0.7.1

### ✏️ Changes in [`Server/Windows/reverse_tcp.py`](Src/Server/Payloads/Windows/NoticedCloud/reverse_tcp.py) / [`Server/Linux/reverse_tcp.py`](Src/Server/Payloads/Windows/NoticedCloud/reverse_tcp.py)
- Reworked the main logic for better stability and performance.
- Improved payload handling and connection management.
- Cleaned up the code structure for easier maintenance.
- Renamed code style: class names now follow PascalCase, while functions and variables follow snake_case.

### ✏️ Changes in [`Client/Windows/reverse_tcp.py`](Src/Client/Payloads/Windows/NoticedCloud/reverse_tcp.py) / Changes in [`Client/Linux/reverse_tcp.py`](Src/Client/Payloads/Windows/NoticedCloud/reverse_tcp.py)
- Reworked the main logic for better stability and performance.
- Cleaned up the code structure for easier maintenance.
- Renamed code style: class names now follow PascalCase, while functions and variables follow snake_case.

### ✏️ Changes in [`Debugger.py`](Src/Lib/Debugger.py)
- Renamed code style: class names now follow PascalCase, while functions and variables follow snake_case.

### ✏️ Changes in [`Server/Windows/reverse_tcp.py`](Src/Server/Payloads/Windows/NoticedCloud/reverse_tcp.py) / [`Server/Linux/reverse_tcp.py`](Src/Server/Payloads/Windows/NoticedCloud/reverse_tcp.py)
- Slightly cleaned up the code structure for easier maintenance.
- Renamed code style: class names now follow PascalCase, while functions and variables follow snake_case.

## 27/06/2025 - v0.7.2

### 🆕 Added
- Introduced [`CodeFurnace.py`](Src/Core/CodeFurnace.py).

### 🚚 Moved
- Moved the `CodeFurnace` class from [`cmrconsole.py`](Src/cmrconsole.py) to [`CodeFurnace.py`](Src/Core/CodeFurnace.py) to improve code structure.

### ✏️ Changes in [`CodeFurnace.py`](Src/Core/CodeFurnace.py)
- Corrected typos in the `CodeFurnace` class.
- Implemented command history support using up/down arrow keys.

### ✏️ Changes in [`cmrconsole.py`](Src/cmrconsole.py)
- Removed the `CodeFurnace` class.

## 27/06/2025 - v0.7.3

### ✏️ Changes in [`CodeFurnace.py`](Src/Core/CodeFurnace.py)
- Improved help command with clearer, color-coded output and dynamic exploit commands display.

### ✏️ Changes in [`NCEXP.py`](Src/Exploits/NoticedCloud/NCEXP.py)
- Improved `options` function output with better formatting and aligned columns for readability.