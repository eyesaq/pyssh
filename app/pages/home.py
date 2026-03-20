# Standard imports
import customtkinter as ctk
import tkinter as tk

# Local application imports
from app.dialogs.add_device import AddDeviceDialog
from app.ui.buttons.connection_button import ConnectionButton
from app.config import PING_LOG

class HomePage(ctk.CTkFrame):
    def __init__(self, parent, app):
        self._parent = parent
        self._app = app

        super().__init__(self._parent)

        self._connection_buttons = []

        # -- Add Device button --
        add_device_frame = ctk.CTkFrame(self, width=340, height=50, bg_color="transparent",
                                                    fg_color="gray21", corner_radius=1)
        add_device_frame.pack(pady=5, fill="x")
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


        self.devices_scroll_frame = ctk.CTkScrollableFrame(self)
        self.devices_scroll_frame.pack(pady=10, fill="both", expand=True)

        # --- Default no device label ---
        self.no_devices_label = ctk.CTkLabel(
            self.devices_scroll_frame,  # todo change the parent so the label isn't pressed upwards
            text="No devices",
            font=("Arial", 18, "bold"),
            text_color="gray60"
        )
        self.no_devices_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self._init_buttons()

        self.after(10, self._init_ux)

    def _init_ux(self):
        # --- Focus ---
        self.focus_set()

        # --- Add Device Shortcut ---
        self._app.bind("<a>", lambda e: self.on_add_device())
        self._app.bind("<A>", lambda e: self.on_add_device())

    def _init_buttons(self):
        for ip_address in self._app.database.get_all_ip_addresses():
            self.create_connection_button(ip_address, ping_log=PING_LOG)

    def remove_connection_button(self, button):
        if button in self._connection_buttons:
            self._connection_buttons.remove(button)
            self._on_connection_buttons_change()

    def _on_connection_buttons_change(self):
        if len(self._connection_buttons) == 0:
            self.no_devices_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        else:
            self.no_devices_label.place_forget()

    def on_add_device(self):
        AddDeviceDialog(self, self._app, self.create_connection_button)

    def create_connection_button(self, ip_address: str, ping_log=False):
        connection_button = ConnectionButton(
            self.devices_scroll_frame,
            self._app,
            ip_address,
            self.remove_connection_button,
            ping_log=ping_log
        )
        connection_button.pack(pady=5, fill="x", expand=True)
        connection_button.pack_propagate(False)

        self._connection_buttons.append(connection_button)
        self._on_connection_buttons_change()
