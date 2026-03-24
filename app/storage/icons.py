from PIL import Image
import customtkinter as ctk

class Icons:
    def __init__(self):
        self.edit_button = self._load("data/icons/edit_button.png")

    def _load(self, path, size=(20, 20)):
        return ctk.CTkImage(
            light_image=Image.open(path),
            dark_image=Image.open(path),
            size=size
        )
