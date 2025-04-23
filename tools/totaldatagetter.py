from mcstatus import JavaServer
import socket
import time
from datetime import datetime
import whois
import re
from utils.threading_util import threaded, typing_lock
import dns.resolver, dns.reversename


def type_output(output_box, text, app):
    with typing_lock:
        output_box.configure(state="normal")
        output_box.delete("1.0", "end")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        header = f"PXTOOL - {timestamp}\n(c) Misagh | github.com/misagh021kid\n\n"
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
def scan_port(host, output_box, app):
    port = 25565
    try:
        with socket.create_connection((host, port), timeout=3):
            text = f"[✔] Port {port} is OPEN!"
    except:
        text = f"[✖] Port {port} is CLOSED or FILTERED!"
    type_output(output_box, text, app)


@threaded
def resolve_ip(host, output_box, app):
    try:
        ip = socket.gethostbyname(host)
        text = f"[✔] Resolved IP: {ip}"
    except Exception as e:
        text = f"[✖] IP Resolution Failed:\n{str(e)}"
    type_output(output_box, text, app)


@threaded
def reverse_dns(host, output_box, app):
    try:
        ip = socket.gethostbyname(host)
        rev_name = dns.reversename.from_address(ip)
        try:
            answers = dns.resolver.resolve(rev_name, "PTR")
            hostname = str(answers[0]).rstrip('.')
            text = f"[✔] Reverse DNS: {hostname}"
        except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
            text = f"[ℹ] No PTR record for IP {ip}"
    except Exception as e:
        text = f"[✖] Reverse DNS Failed:\n{e}"
    
    type_output(output_box, text, app)


@threaded
def whois_lookup(host, output_box, app):
    try:
        w = whois.whois(host)
        text = f"[✔] WHOIS Info:\nDomain: {w.domain_name}\nRegistrar: {w.registrar}\nCreation: {w.creation_date}"
    except Exception as e:
        text = f"[✖] WHOIS Lookup Failed:\n{str(e)}"
    type_output(output_box, text, app)


@threaded
def fast_scan(host, output_box, app):
    timestamp = datetime.now().strftime("%H:%M:%S")
    try:
        server = JavaServer.lookup(host)
        status = server.status()
        motd = status.description
        if isinstance(motd, dict):
            motd = motd.get("text", "")
        motd = re.sub(r'§[0-9a-fk-or]', '', motd, flags=re.IGNORECASE)

        version = status.version.name
        protocol = status.version.protocol
        latency = status.latency

        ip = socket.gethostbyname(host)

        log = [
            f"[{timestamp}] IP: {ip}:{25565}",
            f"[{timestamp}] MOTD: {motd}",
            f"[{timestamp}] Version: {version}",
            f"[{timestamp}] PROTOCOL: {protocol}",
            f"[{timestamp}] PING: {latency:.2f} ms",
        ]

        output = "\n".join(log)

    except Exception as e:
        output = f"[{timestamp}] Scan Failed:\n{str(e)}"

    type_output(output_box, output, app)
