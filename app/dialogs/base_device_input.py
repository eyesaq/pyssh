# Standard imports
import customtkinter as ctk
import tkinter as tk
from typing import Callable, Optional

class BaseDeviceInput(ctk.CTkToplevel):
    def __init__(self, parent, on_completion_function: Callable, title: str, defaults: Optional[dict] = None):
        self._parent = parent
        self.process_function = on_completion_function
        self.defaults = defaults or {}

        super().__init__(self._parent)

        self.title(title)
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
            container_frame, text=f"  {title}  ",
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
        self.ip_address_entry.place(relx=0.5, rely=0.24, anchor=tk.CENTER)
        if "ip_address" in self.defaults:
            self.ip_address_entry.insert(0, self.defaults["ip_address"])

        # -- Device Name entry field --
        self.device_name_entry = ctk.CTkEntry(
            container_frame, placeholder_text="device name",
            placeholder_text_color="gray50", corner_radius=5
        )
        self.device_name_entry.pack(pady=10)
        self.device_name_entry.place(relx=0.5, rely=0.37, anchor=tk.CENTER)
        if "device_name" in self.defaults:
            self.device_name_entry.insert(0, self.defaults["device_name"])

        # -- Username entry field --
        self.username_entry = ctk.CTkEntry(
            container_frame, placeholder_text="username",
            placeholder_text_color="gray50", corner_radius=5
        )
        self.username_entry.pack(pady=10)
        self.username_entry.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        if "username" in self.defaults:
            self.username_entry.insert(0, self.defaults["username"])

        # -- Password entry field --
        self.password_entry = ctk.CTkEntry(
            container_frame, placeholder_text="password",
            placeholder_text_color="gray50", corner_radius=5
        )
        self.password_entry.pack(pady=10)
        self.password_entry.place(relx=0.5, rely=0.63, anchor=tk.CENTER)
        if "password" in self.defaults:
            self.password_entry.insert(0, self.defaults["password"])

        # -- Completion button --
        self.variable_button = ctk.CTkButton(
            container_frame, text=title, font=("Arial", 13, "bold"),
            command=self.process_inputs, bg_color="transparent",
            fg_color="royalblue", hover_color="royalblue4", corner_radius=5
        )
        self.variable_button.pack(pady=10)
        self.variable_button.place(relx=0.5, rely=0.76, anchor=tk.CENTER)

    def retrieve_normalized_inputs(self):
        # Retrieve inputs
        ip_address = self.ip_address_entry.get()
        device_name = self.device_name_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Validate inputs
        invalid_input = self._validate_entries(ip_address, device_name, username, password)
        if invalid_input:
            self._bad_validation(invalid_input)
            return

        # Normalize inputs
        normalized_ip_address = ip_address.lower().strip()
        normalized_device_name = device_name.lower().strip()
        normalized_username = username.lower().strip()
        normalized_password = password

        return normalized_ip_address, normalized_device_name, normalized_username, normalized_password

    def _bad_validation(self, error_message):
        pass    # todo if validation fails

    def process_inputs(self):
        normalized_inputs = self.retrieve_normalized_inputs()
        if normalized_inputs:
            self.process_function(*normalized_inputs)
            self.destroy()

    def _validate_entries(self, ip_address, device_name, username, password):
        return  # todo validation logic
