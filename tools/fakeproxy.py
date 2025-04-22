import socket
import threading
from utils.threading_util import threaded
import struct

@threaded
def fakeproxy(target_host, output_box, app):
    FAKEPROXY_PORT = 25565

    def update_output(text):
        output_box.configure(state="normal")
        output_box.insert("end", f"{text}\n")
        output_box.see("end")
        output_box.configure(state="disabled")
        app.update()

    def read_varint(data):
        num = 0
        for i in range(5):
            byte = data[i]
            num |= (byte & 0x7F) << (7 * i)
            if not (byte & 0x80):
                return num, i + 1
        return 0, 0

    def parse_packet(data, direction):
        try:
            length, offset = read_varint(data)
            packet_id, pid_len = read_varint(data[offset:])
            full_offset = offset + pid_len

            # Check only in login state packets
            if packet_id == 0x01 and direction == "Server → Client":
                update_output("[SECURITY] Server → Client: Encryption Request (public key, verify token...)")
            elif packet_id == 0x01 and direction == "Client → Server":
                update_output("[SECURITY] Client → Server: Encryption Response (encrypted secret key...)")
            elif packet_id == 0x00 and direction == "Client → Server":
                update_output("[LOGIN] Client sent Login Start (username, etc.)")
            elif packet_id == 0x02 and direction == "Server → Client":
                update_output("[LOGIN] Server sent Login Success (UUID, username)")
            elif packet_id == 0x03 and direction == "Server → Client":
                update_output("[INFO] Server set compression threshold.")
        except Exception as e:
            update_output(f"[!] Error parsing packet: {e}")

    def handle_client(client_socket):
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.connect((target_host, 25565))
            update_output("[✔] Connected to the real server.")

            def forward(source, destination, label):
                while True:
                    try:
                        data = source.recv(4096)
                        if not data:
                            break
                        parse_packet(data, label)
                        destination.sendall(data)
                    except Exception as e:
                        update_output(f"[!] Error forwarding {label}: {e}")
                        break

            threading.Thread(target=forward, args=(client_socket, server_socket, "Client → Server")).start()
            threading.Thread(target=forward, args=(server_socket, client_socket, "Server → Client")).start()

        except Exception as e:
            update_output(f"[!] Connection error: {e}")

    def start_fakeproxy():
        proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        proxy_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        proxy_socket.bind(('', FAKEPROXY_PORT))
        proxy_socket.listen(5)

        update_output(f"[+] FakeProxy started on port localhost:{FAKEPROXY_PORT}")
        update_output(f"[+] Forwarding to real server {target_host}:25565")

        while True:
            client_socket, addr = proxy_socket.accept()
            update_output(f"[⇆] Client connected: {addr}")
            threading.Thread(target=handle_client, args=(client_socket,)).start()

    update_output(f"[•] Starting FakeProxy for {target_host}...")
    threading.Thread(target=start_fakeproxy).start()
