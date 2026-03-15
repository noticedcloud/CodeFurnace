import json
import os
import subprocess
import shutil
from typing import Dict, Any
from Core.IPayload import IPayload
from Lib.Debugger import info, warning, error
class PayloadAdapter(IPayload):
    """
    Adapter for payloads defined by a JSON manifest.
    Handles compilation of external source code (Rust, Go, C++, etc.)
    """
    def __init__(self, manifest_path: str) -> None:
        self.manifest_path = manifest_path
        self.base_dir = os.path.dirname(manifest_path)
        try:
            with open(manifest_path, 'r') as f:
                self.metadata = json.load(f)
        except Exception as e:
            error(f"Failed to load payload manifest {manifest_path}: {e}")
            self.metadata = {}
    @property
    def type(self) -> str:
        return self.metadata.get("type", "stageless")
    def generate(self, options: Dict[str, Any]) -> str:
        target_os = options.get("OS", "").lower()
        suffix = ""
        if target_os in ["l", "rl", "linux"]:
            suffix = "_linux"
        elif target_os in ["w", "rw", "windows"]:
            suffix = "_windows"
        build_cmd_template = self.metadata.get(f"build_command{suffix}") or self.metadata.get("build_command", "")
        output_file = self.metadata.get(f"output_file{suffix}") or self.metadata.get("output_file", "payload.exe")
        if not build_cmd_template:
            error("No build_command defined in payload manifest.")
            return ""
        final_cmd = build_cmd_template
        for key, val in options.items():
            final_cmd = final_cmd.replace(f"{{{{{key}}}}}", str(val))
        info(f"Compiling payload with: {final_cmd}")
        try:
            process = subprocess.run(
                final_cmd,
                shell=True,
                cwd=self.base_dir,
                capture_output=True,
                text=True
            )
            if process.returncode != 0:
                error(f"Compilation failed:\n{process.stderr}")
                return ""
            info("Compilation successful.")
            abs_output_path = os.path.join(self.base_dir, output_file)
            if not os.path.exists(abs_output_path):
                error(f"Expected output file not found at {abs_output_path}")
                return ""
            return abs_output_path
        except Exception as e:
            error(f"Error during payload generation: {e}")
            return ""
