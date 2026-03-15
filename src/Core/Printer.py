import os
def options(self) -> None:
    if self.exploit is not None:
        self.exploit.options()
    else:
        warning("Please specify an exploit")
def print_items(self, directory: str) -> None:
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d != '__pycache__' and not d.startswith("_")]
        if "payload.json" in files:
            rel_path = os.path.relpath(root, directory)
            path = rel_path.replace("\\", "/")
            print(path)
            continue
        for file in files:
            if file.endswith(".py"):
                rel_path = os.path.relpath(os.path.join(root, file), directory)
                path = rel_path.replace("\\", "/").replace(".py", "")
                print(path)
            elif file.endswith(".json"):
                if file == "payload.json": continue
                rel_path = os.path.relpath(os.path.join(root, file), directory)
                path = rel_path.replace("\\", "/").replace(".json", "")
                print(path)
