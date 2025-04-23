import requests
import zipfile
import io
import os
import sys
import shutil
import subprocess
import time

REPO_OWNER = "Misagh021kid"
REPO_NAME = "Pixeltools"
EXE_NAME = "PixelTools.exe"
VERSION_FILE = "version.txt"

def get_current_version():
    with open(VERSION_FILE, "r") as f:
        return f.read().strip()

def get_latest_release():
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases/latest"
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        return data["tag_name"], data["zipball_url"]
    return None, None

def download_and_replace(download_url):
    print("[INFO] Downloading latest release...")
    r = requests.get(download_url)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall("update_tmp")

    # Search for the new exe inside the extracted folder
    extracted_folder = os.path.join("update_tmp", os.listdir("update_tmp")[0])
    new_exe_path = None

    for root, dirs, files in os.walk(extracted_folder):
        for file in files:
            if file.lower() == EXE_NAME.lower():
                new_exe_path = os.path.join(root, file)
                break

    if not new_exe_path:
        print("[ERROR] New executable not found in release!")
        return False

    # Rename current exe to .old
    print("[INFO] Replacing old version...")
    os.rename(EXE_NAME, EXE_NAME + ".old")

    # Move the new exe to replace the old one
    shutil.copy2(new_exe_path, EXE_NAME)

    # Clean up
    shutil.rmtree("update_tmp")

    print("[✓] Update complete. Launching new version...")
    subprocess.Popen([EXE_NAME])
    return True

def main():
    print("[INFO] Checking for updates...")
    current = get_current_version()
    latest, download_url = get_latest_release()

    if latest and current != latest:
        print(f"[INFO] New version available: {latest}")
        if download_and_replace(download_url):
            sys.exit()
        else:
            print("[ERROR] Update failed.")
    else:
        print("[✓] You are already on the latest version.")

if __name__ == "__main__":
    main()
