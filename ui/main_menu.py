import customtkinter as ctk
from ui.penetration_page import open_penetration_page
from ui.mctools_page import open_mctools
import urllib.request
import webbrowser
import platform
import socket
import time
import threading
import requests
import os
import sys

def show_main_menu(app):
    for widget in app.winfo_children():
        widget.destroy()

    def check_internet():
        try:
            start = time.time()
            urllib.request.urlopen("http://google.com", timeout=2)
            delay = time.time() - start
            if delay < 0.5:
                return "Good"
            else:
                return "Poor Connection"
        except:
            return "No Connection"

    def update_internet_status():
        def check():
            net_status = check_internet()
            app.after(0, lambda: update_ui_internet(net_status))

        def update_ui_internet(net_status):
            net_label.configure(text=f"Internet: {net_status}")
            net_label.configure(text_color={
                "Good": "green",
                "Poor Connection": "orange",
                "No Connection": "red"
            }.get(net_status, "gray"))

            is_active = net_status != "No Connection"
            mctool_btn.configure(state="normal" if is_active else "disabled")
            pentest_btn.configure(state="normal" if is_active else "disabled")

        threading.Thread(target=check, daemon=True).start()

    def check_for_updates():
        def update():
            try:
                response = requests.get("https://api.github.com/repos/Misagh021kid/Pixeltools/releases/latest").json()
                if "tag_name" not in response:
                    return lambda: append_console("\n[!] No releases found on GitHub.\n")

                latest_version = response["tag_name"]
                current_version = "v0.0.1"

                if latest_version != current_version:
                    download_url = next(asset["browser_download_url"]
                                        for asset in response["assets"]
                                        if asset["name"].endswith(".exe"))

                    def step1(): append_console(f"\n[+] New version available: {latest_version}. Downloading update...\n")
                    def step2(): append_console("[+] Update downloaded. Replacing current file...\n")

                    r = requests.get(download_url, stream=True)
                    with open("PixelTools_new.exe", "wb") as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)

                    return lambda: (
                        step1(),
                        step2(),
                        replace_file()
                    )
                else:
                    return lambda: append_console("\n[✓] You already have the latest version.\n")

            except Exception as e:
                return lambda: append_console(f"\n[!] Update check failed: {e}\n")

        def replace_file():
            new_file = os.path.abspath("PixelTools_new.exe")
            old_file = sys.argv[0]
            os.remove(old_file)
            os.rename(new_file, old_file)
            os.execv(old_file, sys.argv)

        def append_console(text):
            console_box.configure(state="normal")
            console_box.insert(ctk.END, text)
            console_box.configure(state="disabled")

        def thread_task():
            result_func = update()
            app.after(0, result_func)

        threading.Thread(target=thread_task, daemon=True).start()

    # UI Elements
    title = ctk.CTkLabel(app, text="Pixel Tools (Main Menu)", font=("OpenSans", 26))
    title.pack(pady=40)

    mctool_btn = ctk.CTkButton(app, text="Minecraft Server Info", command=lambda: open_mctools(app),
                               width=250, height=40, font=("OpenSans", 13), fg_color="#2a2a2a", hover_color="#0088ff")
    mctool_btn.pack(pady=10)

    pentest_btn = ctk.CTkButton(app, text="Minecraft Pentest", command=lambda: open_penetration_page(app),
                                width=250, height=40, font=("OpenSans", 13), fg_color="#2a2a2a", hover_color="#0088ff")
    pentest_btn.pack(pady=10)

    sysinfo = f"""
    [+] System Info
    Platform: {platform.system()} {platform.release()}
    Machine: {platform.machine()}
    Hostname: {socket.gethostname()}
    IP: {socket.gethostbyname(socket.gethostname())}
    """.strip()

    status_bar = ctk.CTkFrame(app, height=30, fg_color="transparent")
    status_bar.pack(side="bottom", fill="x", pady=5, padx=10)

    version_label = ctk.CTkLabel(status_bar, text="v0.0.2", font=("OpenSans", 12))
    version_label.pack(side="left")

    internet_frame = ctk.CTkFrame(status_bar, fg_color="transparent")
    internet_frame.pack(side="top")

    net_label = ctk.CTkLabel(internet_frame, text="Checking...", font=("OpenSans", 12))
    net_label.pack(side="left", padx=5)

    refresh_btn = ctk.CTkButton(internet_frame, text="⟳", width=30, height=24, font=("OpenSans", 14),
                                 command=update_internet_status, fg_color="#2a2a2a", hover_color="#0088ff")
    refresh_btn.pack(side="left")

    update_internet_status()

    console_box = ctk.CTkTextbox(app, height=120, width=550, font=("JetBrains Mono", 12),
                                 fg_color="#0e1116", text_color="#33ff66")
    console_box.pack(pady=25)
    console_box.insert(ctk.END, sysinfo)
    console_box.configure(state="disabled")

    update_btn = ctk.CTkButton(app, text="Check for Updates", command=check_for_updates,
                               width=200, height=30, font=("OpenSans", 12),
                               fg_color="#2a2a2a", hover_color="#00bb66")
    update_btn.pack(pady=(0, 5))

    github_icon = ctk.CTkLabel(app, text="⭐", font=("OpenSans", 20), cursor="hand2")
    github_icon.place(relx=1.0, rely=1.0, x=-40, y=-10, anchor="se")
    github_icon.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/misagh021kid/Pixeltools"))

    discord_icon = ctk.CTkLabel(app, text="🔌", font=("OpenSans", 20), cursor="hand2")
    discord_icon.place(relx=1.0, rely=1.0, x=-10, y=-10, anchor="se")
    discord_icon.bind("<Button-1>", lambda e: webbrowser.open("https://discord.gg/JyHTwWD5M3"))
