# Standard imports
import customtkinter as ctk
import tkinter as tk
import os

# Local application imports
from app.dialogs.add_device import AddDeviceDialog
from app.ui.buttons.connection_button import ConnectionWidget

class HomePage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)

        self._app = app

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        add_device_frame = ctk.CTkFrame(self, height=50)
        add_device_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        add_device_frame.grid_columnconfigure(1, weight=1)

        add_device_button = ctk.CTkButton(
            add_device_frame,
            text="+",
            font=("Arial", 25, "bold"),
            command=self.on_add_device,
            height=50,
            width = 50
        )
        add_device_button.grid(row=0, column=0, padx=10, pady=10)

        add_device_label = ctk.CTkLabel(
            add_device_frame,
            text="Add Device",
            font=("Arial", 25, "bold")
        )
        add_device_label.grid(row=0, column=1, sticky="w")

        self.device_container = ctk.CTkScrollableFrame(self)
        self.device_container.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.conn_btn_class = ConnectionWidget

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
            self.create_connection_button(connection["ip_address"])

    def create_connection_button(self, ip_address: str):
        # find the IP corresponding to this device match by index in devices.json
        ConnectionWidget()
