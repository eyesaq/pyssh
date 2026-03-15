import customtkinter as ctk

class HomePage(ctk.CTkFrame):
    def __init__(self, parent, app):
        self._parent = parent
        self._app = app

        super().__init__(self._parent)