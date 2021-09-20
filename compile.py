from cx_Freeze import setup, Executable
import sys
import os

PYTHON_INSTALL_DIR = sys.exec_prefix
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

base = None
if sys.platform == "win32":
    base = "Win32GUI"

executables = [Executable("main.py", base=base, targetName='AnimationEditor.exe')]

packages = ["idna"]
options = {
    'build_exe': {
        'packages': packages,
        'include_files': [
            os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'),
            os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll'),
            'resources',
         ],
    },
}

setup(
    name="Peoplemon Animation Editor",
    options=options,
    version="1.0",
    description='Fuck Vince',
    executables=executables
)
