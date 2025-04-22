import customtkinter as ctk
import threading
from tools.portscanner import portscanner
from tools.fakeproxy import fakeproxy
from tools.botflood import bot_attack

def open_penetration_page(app):
    from ui.main_menu import show_main_menu
    for widget in app.winfo_children():
        widget.destroy()

    ctk.CTkButton(
        app, text="← Back", width=80, font=("OpenSans", 14),
        fg_color="#2a2a2a", hover_color="#2a2a2a",
        command=lambda: show_main_menu(app)
    ).place(x=10, y=10)

    ctk.CTkLabel(app, text="Minecraft Penetration Tools", font=("OpenSans", 24)).pack(pady=20)

    entry = ctk.CTkEntry(app, placeholder_text="play.example.com", width=300, font=("OpenSans", 14))
    entry.pack(pady=5)

    btn_frame = ctk.CTkFrame(app, fg_color="#1a1a1a")
    btn_frame.pack(pady=15)

    def update_output(msg):
        output_box.configure(state="normal")
        output_box.delete("1.0", "end")
        output_box.insert("end", msg + "\n")
        output_box.configure(state="disabled")

    def run_portscanner():
        host = entry.get()
        output_box.configure(state="normal")
        output_box.delete("1.0", "end")
        output_box.insert("end", f"[+] Starting scan on {host}...\n")
        output_box.configure(state="disabled")
        threading.Thread(target=lambda: portscanner(host, output_box, app)).start()

    def dummy_output(msg):
        output_box.configure(state="normal")
        output_box.delete("1.0", "end")
        output_box.insert("end", f"[✔] {msg}")
        output_box.configure(state="disabled")

    tools = [
        ("Port Scanner", run_portscanner),
        ("FakeProxy", lambda: fakeproxy(entry.get(), output_box, app)),
        ("Server Chart", lambda: dummy_output("Exploits deployed...")),
        ("Bots Attack", lambda: bot_attack(entry.get(), output_box, app)),
    ]

    for i, (name, cmd) in enumerate(tools):
        ctk.CTkButton(
            btn_frame, text=name, command=cmd, width=200,
            font=("OpenSans", 13), fg_color="#2a2a2a", hover_color="#0088ff"
        ).grid(row=i, column=0, padx=10, pady=5)

    global output_box
    output_box = ctk.CTkTextbox(
        app, height=200, width=550, font=("JetBrains Mono", 12),
        fg_color="#0e1116", text_color="#33ff66"
    )
    output_box.pack(pady=15)
    output_box.insert(ctk.END, "[+] Select a tool to begin.")
    output_box.configure(state="disabled")
