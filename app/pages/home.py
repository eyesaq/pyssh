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

        # Make frame expandable
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # -- Add Device frame --
        add_device_frame = ctk.CTkFrame(
            self,
            height=50,
            fg_color="gray21",
            corner_radius=1
        )
        add_device_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10,)
        add_device_frame.grid_columnconfigure(1, weight=1)

        # Button "+"
        add_device_button = ctk.CTkButton(
            add_device_frame,
            text="+",
            font=("Arial", 25, "bold"),
            height=30,
            width=30,
            command=self.on_add_device,
            fg_color="royalblue",
            hover_color="royalblue4",
            corner_radius=5
        )
        add_device_button.grid(row=0, column=0, padx=10, pady=10)

        # Label
        add_device_label = ctk.CTkLabel(
            add_device_frame,
            text="Add Device",
            font=("Arial", 20, "bold"),
            text_color="white"
        )
        add_device_label.grid(row=0, column=1, sticky="w", padx=10)

        # -- Scrollable device container --
        self.device_container = ctk.CTkScrollableFrame(self, corner_radius=1,)
        self.device_container.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))

        self.device_container.grid_columnconfigure(0, weight=1)

        self._init_buttons()

    def on_add_device(self):
        AddDeviceDialog(self, self._app, self.create_connection_button)

    def _init_buttons(self):
        for ip_address in self._app.database.get_all_ip_addresses():
            self.create_connection_button(ip_address)

    def create_connection_button(self, ip_address: str):
        connection_button = ConnectionButton(
            self.device_container,
            self._app,
            ip_address,
            self.connection_buttons
        )

        row_index = len(self.connection_buttons)

        connection_button.grid(
            row=row_index,
            column=0,
            sticky="ew",
            padx=5,
            pady=5
        )

        self.connection_buttons.append(connection_button)
