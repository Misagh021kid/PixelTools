import sys
import subprocess
import importlib.util
import platform

MIN_VERSION = (3, 10)
RECOMMENDED = "3.11"

required_packages = [
    "customtkinter",
    "PIL",
    "pypresence",
    "requests",
    "mcstatus",
    "whois",
    "pyinstaller",
]

builtin_modules = [
    "threading", "tkinter", "datetime", "time", "os", "sys", "socket",
    "platform", "webbrowser", "urllib.request", "re", "struct", "random"
]

def check_python_version():
    if sys.version_info < MIN_VERSION:
        print(f"[❌] Python {MIN_VERSION[0]}.{MIN_VERSION[1]} or higher is required.")
        sys.exit(1)
    else:
        print(f"[✔] Python version {platform.python_version()} detected (Recommended: {RECOMMENDED})")

def install_package(package):
    print(f"[➕] Installing '{package}'...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def check_and_install():
    for module in builtin_modules:
        try:
            __import__(module)
            print(f"[✔] Built-in module '{module}' is available.")
        except ImportError:
            print(f"[⚠] Missing built-in module '{module}' (unusual)")

    for package in required_packages:
        if importlib.util.find_spec(package) is None:
            install_package(package)
        else:
            print(f"[✔] '{package}' is already installed.")

def build_exe():
    print("[🚀] Building the project to EXE using PyInstaller...")
    subprocess.call([
        "pyinstaller",
        "--noconfirm",
        "--onefile",
        "--windowed",
        "--name", "PixelTools",
        "--icon", "assets/icon.ico",
        "main.py"
    ])
    print("[✅] Build completed! Check the /dist folder for your executable.")

if __name__ == "__main__":
    print("[🧱] Starting build process for PixelTools...\n")
    check_python_version()
    check_and_install()
    build_exe()
