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

## 05/08/2025 - v1.0.0

### 🆕 Added
- Introduced [`__init__.py`](Src/Core/__init__.py).
- Introduced [`BaseShell.py`](Src/Core/BaseShell.py).
- Introduced [`HistoryManager.py`](Src/Core/HistoryManager.py).
- Introduced [`ModuleLoader.py`](Src/Core/ModuleLoader.py).
- Introduced [`Printer.py`](Src/Core/Printer.py).
- Introduced [`AIHandler.py`](Src/Core/AIHandler.py).

### 🚚 Moved
- Moved the `complete`, `check_read_line`, `_do_help` and `execute` functions from [`CodeFurnace.py`](Src/Core/CodeFurnace.py) to [`BaseShell.py`](Src/Core/BaseShell.py) to improve code structure.
- Moved the `save_history` function from [`CodeFurnace.py`](Src/Core/CodeFurnace.py) to [`HistoryManager.py`](Src/Core/HistoryManager.py) to improve code structure.
- Moved the `use`, `set`, `load_exploits_list` and `load_payloads_list` functions from [`CodeFurnace.py`](Src/Core/CodeFurnace.py) to [`ModuleLoader.py`](Src/Core/ModuleLoader.py) to improve code structure.
- Moved the `options` and `print_items` functions from [`CodeFurnace.py`](Src/Core/CodeFurnace.py) to [`Printer.py`](Src/Core/Printer.py) to improve code structure.

### ✏️ Renamed
- Renamed [`.NCEXP`](Src/Exploits/NoticedCloud/.NCEXP) -> [`_NCEXP`](Src/Exploits/NoticedCloud/_NCEXP)

### ✏️ Changes in [`CodeFurnace.py`](Src/Core/CodeFurnace.py)
- Removed all functions.

### ✏️ Changes in [`BaseShell.py`](Src/Core/BaseShell.py)
- Updated the `console` method to support multiple commands in a single input using `;` as a separator.
- Added error handling to prevent crashes when executing invalid commands.

## 02/01/2026 - v2.0.0

### 🆕 Added
- Introduced [`cert_gen.py`](src/cert_gen.py) for automatic self-signed certificate generation.
- Integrated automated certificate generation into `CodeFurnace` startup.
- Added `keylogger_stop` command to clients and server.

### ✏️ Changes in [`NCEXP.py`](src/Server/Exploits/NoticedCloud/NCEXP.py) / [`AsyncServer.py`](src/Core/AsyncServer.py)
- Implemented **TLS Encryption** for all secure communications.
- Implemented **XOR Encryption** layer for command/response obfuscation.
- Updated `AsyncServer` to support SSL/TLS listeners.
- Added `screenshot` command support with encrypted binary protocol (Fixing large size errors).
- Added `keylogger_dump` support with formatted output and file redirection.
- Fixed critical syntax errors and removed duplicate method definitions.

### ✏️ Changes in [`main.rs`](src/Client/Payloads/Rust/reverse_shell/src/main.rs)
- Implemented **Certificate Pinning** (Embedded `server.crt`, removed reliance on system roots).
- Implemented custom XOR encryption for all network traffic.
- Fixed `handle_screenshot` to properly encrypt image length and data (Fixing "Protocol Error").
- Fixed `main` loop syntax (missing closing brace).
- Updated compilation dependencies (`rustls`, `image`, `rustls-pemfile`).
- Fixed logic error in command matching (comparing plaintext vs plaintext).

### 🗑️ Removed / Cleaned
- **Removed all comments** from the entire codebase (`.py` and `.rs` files).
- Removed build artifacts (`target/`, `__pycache__`, `kk.bin`, etc.) to clean repository.
