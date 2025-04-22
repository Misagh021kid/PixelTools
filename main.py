import customtkinter as ctk
from ui.main_menu import show_main_menu
from assets.theme_config import configure_theme
import tkinter as tk
from PIL import Image, ImageTk
from utils.discord_rich_presence import init_discord

if __name__ == "__main__":
    root = ctk.CTk()
    icon_image = Image.open("assets/icon.png")
    icon = ImageTk.PhotoImage(icon_image)
    root.iconphoto(True, icon)
    rpc = init_discord()
    configure_theme()
    app = ctk.CTk()
    app.geometry("600x500")
    app.title("Pixel Tools")
    show_main_menu(app)
    app.mainloop()
if rpc:
    rpc.close()