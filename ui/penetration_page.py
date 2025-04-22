import customtkinter as ctk
from tools.portscanner import portscanner
from tools.fakeproxy import fakeproxy
import threading

def open_penetration_page(app):
    from ui.main_menu import show_main_menu
    for widget in app.winfo_children():
        widget.destroy()

    back_btn = ctk.CTkButton(app, text="← Back", width=80, command=lambda: show_main_menu(app), font=("OpenSans", 14), fg_color="#2a2a2a", hover_color="#2a2a2a")
    back_btn.place(x=10, y=10)

    title = ctk.CTkLabel(app, text="Minecraft Penetration Tools", font=("OpenSans", 24))
    title.pack(pady=20)

    entry = ctk.CTkEntry(app, placeholder_text="play.example.com", width=300, font=("OpenSans", 14))
    entry.pack(pady=5)

    btn_frame = ctk.CTkFrame(app, fg_color="#1a1a1a")
    btn_frame.pack(pady=15)
    def run_portscanner():
        host = entry.get()

        def update_output(msg):
            output_box.configure(state="normal")
            output_box.delete("1.0", "end")
            output_box.insert("end", msg + "\n")
            output_box.configure(state="disabled")

        output_box.configure(state="normal")
        output_box.delete("1.0", "end")
        output_box.insert("end", f"[+] Starting scan on {host}...\n")
        output_box.configure(state="disabled")

        threading.Thread(target=lambda: portscanner(host, update_output)).start()




    tools = [
        ("Easy Scans", run_portscanner),
        ("FakeProxy", lambda: fakeproxy(entry.get(), output_box, app)),
        ("Plugin Exploits", lambda: dummy_output("Exploits deployed...")),
        ("Bots Attack", lambda: dummy_output("Bot attack simulation running..."))
    ]

    for i, (name, cmd) in enumerate(tools):
        btn = ctk.CTkButton(btn_frame, text=name, command=cmd, width=200, font=("OpenSans", 13), fg_color="#2a2a2a", hover_color="#0088ff")
        btn.grid(row=i, column=0, padx=10, pady=5)

    global output_box
    output_box = ctk.CTkTextbox(app, height=200, width=550, font=("JetBrains Mono", 12), fg_color="#0e1116", text_color="#33ff66")
    output_box.pack(pady=15)
    output_box.insert(ctk.END, "[+] Select a tool to begin.")
    output_box.configure(state="disabled")


def dummy_output(msg):
    output_box.configure(state="normal")
    output_box.delete("1.0", "end")
    output_box.insert("end", f"[✔] {msg}")
    output_box.configure(state="disabled")