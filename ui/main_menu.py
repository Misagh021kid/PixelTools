import customtkinter as ctk
from ui.penetration_page import open_penetration_page
import urllib.request
from ui.mctools_page import open_mctools
import webbrowser
import platform
import socket


def show_main_menu(app):
    for widget in app.winfo_children():
        widget.destroy()

    def internet_connected():
        try:
            urllib.request.urlopen("http://google.com", timeout=2)
            return True
        except:
            return False

    if not internet_connected():
        error = ctk.CTkLabel(app, text="❌ No internet connection.", font=("OpenSans", 18), text_color="red")
        error.pack(pady=20)
        return

    title = ctk.CTkLabel(app, text="Pixel Tools (Main Menu)", font=("OpenSans", 26))
    title.pack(pady=40)

    mctool_btn = ctk.CTkButton(app, text="Minecraft Server Info", command=lambda: open_mctools(app), width=250, height=40, font=("OpenSans", 13), fg_color="#2a2a2a", hover_color="#0088ff")
    mctool_btn.pack(pady=10)

    pentest_btn = ctk.CTkButton(app, text="Minecraft Pentest", command=lambda: open_penetration_page(app), width=250, height=40, font=("OpenSans", 13), fg_color="#2a2a2a", hover_color="#0088ff")
    pentest_btn.pack(pady=10)
    sysinfo = f"""
    [+] System Info
    Platform: {platform.system()} {platform.release()}
    Machine: {platform.machine()}
    Hostname: {socket.gethostname()}
    IP: {socket.gethostbyname(socket.gethostname())}
    """.strip()

    console_box = ctk.CTkTextbox(app, height=120, width=550, font=("JetBrains Mono", 12), fg_color="#0e1116", text_color="#33ff66")
    console_box.pack(pady=25)
    console_box.insert(ctk.END, sysinfo)
    console_box.configure(state="disabled")
    github_icon = ctk.CTkLabel(app, text="💻", font=("OpenSans", 20), cursor="hand2")
    github_icon.place(relx=1.0, rely=1.0, x=-40, y=-10, anchor="se")
    github_icon.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/misaghx"))

    discord_icon = ctk.CTkLabel(app, text="🤝", font=("OpenSans", 20), cursor="hand2")
    discord_icon.place(relx=1.0, rely=1.0, x=-10, y=-10, anchor="se")
    discord_icon.bind("<Button-1>", lambda e: webbrowser.open("https://discord.gg/YOUR_SERVER"))