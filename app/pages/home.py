# Standard imports
import customtkinter as ctk
import tkinter as tk

# Local application imports
from app.dialogs.add_device import AddDeviceDialog
from app.ui.buttons.connection_button import ConnectionButton

class HomePage(ctk.CTkFrame):
    def __init__(self, parent, app):
        self._parent = parent
        self._app = app

        super().__init__(self._parent)

        self.connection_buttons = []

        # -- Add Device button --
        add_device_frame = ctk.CTkFrame(self, width=340, height=50, bg_color="transparent",
                                                    fg_color="gray21", corner_radius=1)
        add_device_frame.pack(pady=5)
        add_device_frame.pack_propagate(False)

        add_device_button = ctk.CTkButton(add_device_frame, text="+",
                                                      font=("Arial", 25, "bold"), height=30, width=30,
                                                      command=self.on_add_device, bg_color="transparent",
                                                      fg_color="royalblue", hover_color="royalblue4", corner_radius=5)
        add_device_button.pack(pady=10)
        add_device_button.place(relx=0.08, rely=0.5, anchor=tk.CENTER)

        add_device_label = ctk.CTkLabel(add_device_frame, text="Add Device",
                                                    font=("Arial", 20, "bold"), fg_color="transparent",
                                                    bg_color="transparent", text_color="white")
        add_device_label.pack(pady=10)
        add_device_label.place(relx=0.3, rely=0.5, anchor=tk.CENTER)

        self._init_buttons()

    def on_add_device(self):
        AddDeviceDialog(self, self._app, self.create_connection_button)

    def _init_buttons(self):
        for ip_address in self._app.database.get_all_ip_addresses():
            self.create_connection_button(ip_address)

    def create_connection_button(self, ip_address: str):
        connection_button = ConnectionButton(self, self._app, ip_address, self.connection_buttons)
        connection_button.pack(pady=5)
        connection_button.pack_propagate(False)

        self.connection_buttons.append(connection_button)
