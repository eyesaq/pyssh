import customtkinter as ctk
import tkinter as tk
from typing import Callable

class AddDeviceDialog(ctk.CTkToplevel):
    def __init__(self, parent, app, on_connection_creation: Callable):
        self._parent = parent
        self._app = app
        self._on_connection_creation = on_connection_creation

        super().__init__(self._parent)

        self.title("Add Device")
        self.geometry("250x350")

        # -- Main container --
        container_frame = ctk.CTkFrame(
            self, width=200, height=300, bg_color="transparent",
            fg_color="gray20", corner_radius=1
        )
        container_frame.pack(pady=10)
        container_frame.pack_propagate(False)
        container_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # -- Header --
        header_label = tk.Label(
            container_frame, text="  Add Device  ",
            font=("Arial", 16, "bold",), fg="white", bg="gray20"
        )
        header_label.pack(pady=20)
        header_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

        # -- IP Address entry field --
        self.ip_address_entry = ctk.CTkEntry(
            container_frame, placeholder_text="ip address",
            placeholder_text_color="gray50", corner_radius=5
        )
        self.ip_address_entry.pack(pady=10)
        self.ip_address_entry.place(relx=0.5, rely=0.37, anchor=tk.CENTER)

        # -- Username entry field --
        self.username_entry = ctk.CTkEntry(
            container_frame, placeholder_text="username",
            placeholder_text_color="gray50", corner_radius=5
        )
        self.username_entry.pack(pady=10)
        self.username_entry.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # -- Device Name entry field --
        self.device_name_entry = ctk.CTkEntry(
            container_frame, placeholder_text="device name",
            placeholder_text_color="gray50", corner_radius=5
        )
        self.device_name_entry.pack(pady=10)
        self.device_name_entry.place(relx=0.5, rely=0.24, anchor=tk.CENTER)

        # -- Password entry field --
        self.password_entry = ctk.CTkEntry(
            container_frame, placeholder_text="password",
            placeholder_text_color="gray50", corner_radius=5
        )
        self.password_entry.pack(pady=10)
        self.password_entry.place(relx=0.5, rely=0.63, anchor=tk.CENTER)

        # -- Variable button --
        self.variable_button = ctk.CTkButton(
            container_frame, text="Add Device", font=("Arial", 13, "bold"),
            command=self.save_device, bg_color="transparent",
            fg_color="royalblue", hover_color="royalblue4", corner_radius=5
        )
        self.variable_button.pack(pady=10)
        self.variable_button.place(relx=0.5, rely=0.76, anchor=tk.CENTER)

    def save_device(self):
        # Retrieve inputs
        ip_address = self.ip_address_entry.get()
        device_name = self.device_name_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Validate inputs
        if not self._validate_entries(ip_address, device_name, username, password):
            return  # todo if validation fails

        # Normalize inputs
        normalized_ip_address = ip_address.lower().strip()
        normalized_device_name = device_name.lower().strip()
        normalized_username = username.lower().strip()
        normalized_password = password

        # Hash plaintext passwords
        normalized_hashed_password = self._hash_password(normalized_password)

        # Add the new connection to the database
        self._app.database.add_connection(normalized_ip_address,
                                          normalized_device_name,
                                          normalized_username,
                                          normalized_hashed_password)
        print(f"Saved connection: {device_name} @ {ip_address}")

        # add the button to the ui with name
        self._on_connection_creation(device_name)

        self.destroy()

    def _validate_entries(self, ip_address, device_name, username, password):
        pass    # todo validation logic
        return True

    def _hash_password(self, password):
        # todo hash plaintext
        return password
