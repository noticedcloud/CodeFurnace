import json
import os
import subprocess
import shlex
from typing import Dict, Any, List
from Core.IModule import IModule
from Lib.Debugger import info, warning, error
class GenericAdapter(IModule):
    """
    Adapter for modules defined by a JSON manifest.
    Wraps external executables (Rust, Go, C++, etc.)
    """
    def __init__(self, manifest_path: str) -> None:
        self.manifest_path = manifest_path
        self.base_dir = os.path.dirname(manifest_path)
        try:
            with open(manifest_path, 'r') as f:
                self.metadata = json.load(f)
        except Exception as e:
            error(f"Failed to load manifest {manifest_path}: {e}")
            self.metadata = {}
        self.options_config = self.metadata.get("options", {})
        self.current_options = {k: v for k, v in self.options_config.items()}
    @property
    def type(self) -> str:
        return self.metadata.get("type", "exploit")
    @property
    def commands(self) -> dict:
        raw_commands = self.metadata.get("commands", {})
        if isinstance(raw_commands, dict):
            formatted = {}
            for k, v in raw_commands.items():
                if isinstance(v, dict):
                    formatted[k] = v.get("description", "No description")
                else:
                    formatted[k] = v
            return formatted
        return {"exploit": "Run the module"}
    @property
    def ai_commands(self) -> list:
        return self.metadata.get("ai_commands", [])
    def get_metadata(self) -> Dict[str, Any]:
        return self.metadata
    def get_options(self) -> Dict[str, Any]:
        return self.current_options
    def set(self, options: Dict[str, str]) -> None:
        for key, value in options.items():
            key_upper = key.upper()
            found = False
            for opt_name in self.current_options:
                if opt_name.upper() == key_upper:
                    self.current_options[opt_name] = value
                    info(f"{opt_name} => {value}")
                    found = True
                    break
            if not found:
                warning(f"Option {key} not found.")
    def exploit(self) -> None:
        if "exploit" in self.commands:
            self.exec("exploit")
        elif "run" in self.commands:
            self.exec("run")
        else:
            legacy_cmd = self.metadata.get("command", "")
            if legacy_cmd:
                self._run_shell_cmd(legacy_cmd)
            else:
                warning("No 'exploit' or 'run' command defined.")
    def exec(self, command: str) -> Any:
        raw_commands = self.metadata.get("commands", {})
        target_cmd_data = raw_commands.get(command)
        if not target_cmd_data:
            warning(f"Command '{command}' not defined in manifest.")
            return
        execution_string = ""
        if isinstance(target_cmd_data, dict):
            execution_string = target_cmd_data.get("command", "")
        else:
            if command in ["exploit", "run"]:
                execution_string = self.metadata.get("command", "")
        if not execution_string:
            warning(f"No execution string found for '{command}'")
            return
        self._run_shell_cmd(execution_string)
    def _run_shell_cmd(self, cmd_template: str):
        final_cmd = cmd_template
        for opt, val in self.current_options.items():
            final_cmd = final_cmd.replace(f"{{{{{opt}}}}}", str(val))
        info(f"Executing: {final_cmd}")
        try:
            process = subprocess.Popen(
                final_cmd, 
                shell=True,
                cwd=self.base_dir, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                text=True
            )
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    print(output.strip())
            rc = process.poll()
            if rc != 0:
                err = process.stderr.read()
                if err:
                    error(f"Module execution failed: {err}")
        except Exception as e:
            error(f"Execution error: {e}")
