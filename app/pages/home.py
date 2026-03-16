# Standard imports
import customtkinter as ctk
import tkinter as tk
import os

# Local application imports
from app.dialogs.add_device import AddDeviceDialog

class HomePage(ctk.CTkFrame):
    def __init__(self, parent, app):
        self._parent = parent
        self._app = app

        super().__init__(self._parent)

        # -- Add Device button --
        add_device_placeholder_frame = ctk.CTkFrame(self, width=340, height=50, bg_color="transparent",
                                                    fg_color="gray21", corner_radius=1)
        add_device_placeholder_frame.pack(pady=5)
        add_device_placeholder_frame.pack_propagate(False)

        add_device_placeholder_button = ctk.CTkButton(add_device_placeholder_frame, text="+",
                                                      font=("Arial", 25, "bold"), height=30, width=30,
                                                      command=self.on_add_device, bg_color="transparent",
                                                      fg_color="royalblue", hover_color="royalblue4", corner_radius=5)
        add_device_placeholder_button.pack(pady=10)
        add_device_placeholder_button.place(relx=0.08, rely=0.5, anchor=tk.CENTER)

        add_device_placeholder_label = ctk.CTkLabel(add_device_placeholder_frame, text="Add Device",
                                                    font=("Arial", 20, "bold"), fg_color="transparent",
                                                    bg_color="transparent", text_color="white")
        add_device_placeholder_label.pack(pady=10)
        add_device_placeholder_label.place(relx=0.3, rely=0.5, anchor=tk.CENTER)

        self._init_buttons()

    def on_add_device(self):
        AddDeviceDialog(self, self._app, self.on_connection_creation)

    def on_connection_creation(self, connection):
        # todo create button for the device
        self.create_connection_button(connection)
        pass

    def _init_buttons(self):
        connections = self._app.database.get_all_connections()
        for connection in connections:
            self.create_connection_button(connection)

    def create_connection_button(self, connection: dict):
        # find the IP corresponding to this device match by index in devices.json
        ip = connection['ip_address']

        response = os.system(f"ping -n 1 {ip}")
        if response == 0:
            print(f"{ip} is reachable")
            device_online(key)
        else:
            print(f"{ip} is not reachable")
            device_offline(key)
