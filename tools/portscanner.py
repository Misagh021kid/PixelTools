import socket
import threading
from utils.threading_util import threaded

@threaded
def portscanner(host, output_box, app):
    open_ports = []
    start_port = 20
    end_port = 25565
    total = end_port - start_port + 1
    checked = 0
    lock = threading.Lock()

    def update_output(text):
        output_box.configure(state="normal")
        output_box.delete("1.0", "end")
        output_box.insert("end", f"{text}\n")
        output_box.see("end")
        output_box.configure(state="disabled")
        app.update()

    def update_progress(text):
        output_box.configure(state="normal")
        output_box.delete("end-2l", "end-1l")  # حذف خط قبلی بار پیشرفت
        output_box.insert("end", f"{text}\n")
        output_box.see("end")
        output_box.configure(state="disabled")
        app.update()

    update_output(f"[+] Starting scan on {host}...")

    def scan_port(port):
        nonlocal checked
        try:
            with socket.create_connection((host, port), timeout=0.5):
                with lock:
                    open_ports.append(port)
        except:
            pass
        finally:
            with lock:
                checked += 1
                percent = int((checked / total) * 100)
                bar = '█' * (percent // 5) + '░' * (20 - (percent // 5))
                update_progress(f"[{bar} {percent}%] Scanning port {port}...")

    threads = []
    for port in range(start_port, end_port + 1):
        t = threading.Thread(target=scan_port, args=(port,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    if open_ports:
        update_output(f"\n[✔] Open ports on {host}:\n{', '.join(map(str, open_ports))}")
    else:
        update_output(f"\n[✖] No open ports found on {host}.")
