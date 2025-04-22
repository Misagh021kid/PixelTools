import customtkinter as ctk
import re
from logic.network_tools import check_status, dns_lookup, scan_port

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

    btn1 = ctk.CTkButton(frame, text="Check Server Status", command=lambda: check_status(entry.get(), output_box, app), width=180, font=("OpenSans", 13), fg_color="#2a2a2a", hover_color="#0088ff")
    btn1.grid(row=0, column=0, padx=10, pady=5)

    btn2 = ctk.CTkButton(frame, text="DNS Lookup", command=lambda: dns_lookup(entry.get(), output_box, app), width=180, font=("OpenSans", 13), fg_color="#2a2a2a", hover_color="#0088ff")
    btn2.grid(row=1, column=0, padx=10, pady=5)

    btn3 = ctk.CTkButton(frame, text="Scan Port 25565", command=lambda: scan_port(entry.get(), output_box, app), width=180, font=("OpenSans", 13), fg_color="#2a2a2a", hover_color="#0088ff")
    btn3.grid(row=2, column=0, padx=10, pady=5)


# logic/network_tools.py
from mcstatus import JavaServer
import dns.resolver
import socket
import time
from datetime import datetime
from utils.threading_util import threaded, typing_lock

def type_output(output_box, text, app):
    with typing_lock:
        output_box.configure(state="normal")
        output_box.delete("1.0", "end")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        header = f"MSC - {timestamp}\n(c) Misagh & ChatGPT | github.com/misaghx\n\n"
        output_box.insert("end", header)
        app.update()
        time.sleep(0.01)
        for line in text.splitlines():
            output_box.insert("end", f"> {line}\n")
            output_box.see("end")
            app.update()
            time.sleep(0.2)
        output_box.configure(state="disabled")

@threaded
def check_status(host, output_box, app):
    try:
        server = JavaServer.lookup(host)
        status = server.status()
        motd = status.description.strip() if isinstance(status.description, str) else status.description.get("text", "")
        motd = re.sub(r'§[0-9a-fk-or]', '', motd, flags=re.IGNORECASE)
        text = f"[✔] Server is Online\n[✔] MOTD: {motd}\n[✔] Players: {status.players.online}/{status.players.max}\n[✔] Ping: {status.latency:.2f} ms"
    except Exception as e:
        text = f"[✖] Server Offline or Error:\n{str(e)}"
    type_output(output_box, text, app)

@threaded
def scan_port(host, output_box, app):
    port = 25565
    try:
        with socket.create_connection((host, port), timeout=3):
            text = f"[✔] Port {port} is OPEN!"
    except:
        text = f"[✖] Port {port} is CLOSED or FILTERED!"
    type_output(output_box, text, app)

@threaded
def dns_lookup(host, output_box, app):
    try:
        result = dns.resolver.resolve(host, 'A')
        ips = ", ".join([ip.to_text() for ip in result])
        text = f"[✔] DNS Lookup for {host}:\n{ips}"
    except Exception as e:
        text = f"[✖] DNS Lookup Failed:\n{str(e)}"
    type_output(output_box, text, app)