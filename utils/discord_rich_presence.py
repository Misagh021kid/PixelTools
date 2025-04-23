from pypresence import Presence
import time

CLIENT_ID = '1364139937892536362'

def init_discord():
    try:
        rpc = Presence(CLIENT_ID)
        rpc.connect()
        rpc.update(
            state="Version 0.0.2",
            details="Pentesting for MC Servers",
            start=time.time(),
            large_image="pixeltools",
            large_text="Minecraft Pentest Tool"
        )
        return rpc
    except Exception as e:
        print("Discord Rich Presence unavailable:", e)
