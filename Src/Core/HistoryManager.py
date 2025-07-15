try:
    import readline
except ImportError:
    try:
        import pyreadline3 as readline
    except ImportError:
        readline = None

def save_history(self) -> None:
    readline.write_history_file(self.original_path + "/" + self.HISTORY_FILE)