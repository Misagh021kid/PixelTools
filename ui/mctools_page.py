import customtkinter as ctk
import re
from logic.network_tools import (
    check_status,
    scan_port,
    resolve_ip,
    reverse_dns,
    whois_lookup
)

def open_mctools(app):
    from ui.main_menu import show_main_menu
    for widget in app.winfo_children():
        widget.destroy()

    back_btn = ctk.CTkButton(app, text="← Back", width=80, command=lambda: show_main_menu(app), font=("OpenSans", 14), fg_color="#2a2a2a", hover_color="#0088ff")
    back_btn.place(x=10, y=10)

    label = ctk.CTkLabel(app, text="Pixel Tools (SV Info)", font=("OpenSans", 24))
    label.pack(pady=15)

    entry = ctk.CTkEntry(app, placeholder_text="play.example.com", width=300, font=("OpenSans", 14))
    entry.pack(pady=5)

    frame = ctk.CTkFrame(app, fg_color="#1a1a1a")
    frame.pack(pady=10)

    output_box = ctk.CTkTextbox(app, height=200, width=550, font=("JetBrains Mono", 12), fg_color="#0e1116", text_color="#33ff66")
    output_box.pack(pady=15)
    output_box.insert(ctk.END, "[+] Waiting for command...")
    output_box.configure(state="disabled")

    buttons = [
        ("Check Server Status", check_status),
        ("Scan Port 25565", scan_port),
        ("Resolve IP", resolve_ip),
        ("Reverse DNS", reverse_dns),
        ("WHOIS Lookup", whois_lookup),
    ]

    for index, (text, command) in enumerate(buttons):
        row, col = divmod(index, 2)
        btn = ctk.CTkButton(
            frame,
            text=text,
            command=lambda c=command: c(entry.get(), output_box, app),
            width=180,
            font=("OpenSans", 13),
            fg_color="#2a2a2a",
            hover_color="#0088ff"
        )
        btn.grid(row=row, column=col, padx=10, pady=5)
