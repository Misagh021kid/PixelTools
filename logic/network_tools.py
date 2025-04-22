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