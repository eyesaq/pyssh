from PIL import Image
import customtkinter as ctk
from pathlib import Path

class Icons:
    def __init__(self):
        self._icons_path = Path('data/icons')

        self.delete_button = self._load('delete_button.jpg')
        self.edit_button = self._load('edit_button.png')
        self.menu_button = self._load('menu_button.png')

    def _load(self, file_name, size=(10, 10)):
        return ctk.CTkImage(
            light_image=Image.open(self._icons_path/file_name),
            dark_image=Image.open(self._icons_path/file_name),
            size=size
        )
