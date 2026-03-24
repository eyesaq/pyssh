# Standard imports
import customtkinter as ctk
import tkinter as tk
from typing import Callable, Optional

class BaseDeviceInput(ctk.CTkToplevel):
    def __init__(self, parent, on_completion_function: Callable, title: str, defaults: Optional[dict] = None):
        super().__init__(parent)
        self.process_function = on_completion_function
        self.defaults = defaults or {}

        self.title(title)
        self.geometry("250x350")

        # -- Main container --
        container_frame = ctk.CTkFrame(
            self, width=200, height=300, bg_color="transparent",
            fg_color="gray20", corner_radius=1
        )
        container_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # -- Header --
        header_label = tk.Label(
            container_frame, text=f"  {title}  ",
            font=("Arial", 16, "bold",), fg="white", bg="gray20"
        )
        header_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

        # -- IP Address entry field --
        self.ip_address_entry = ctk.CTkEntry(
            container_frame, placeholder_text="ip address",
            placeholder_text_color="gray50", corner_radius=5
        )
        self.ip_address_entry.place(relx=0.5, rely=0.24, anchor=tk.CENTER)
        if "ip_address" in self.defaults:
            self.ip_address_entry.insert(0, self.defaults["ip_address"])

        # -- Device Name entry field --
        self.device_name_entry = ctk.CTkEntry(
            container_frame, placeholder_text="device name",
            placeholder_text_color="gray50", corner_radius=5
        )
        self.device_name_entry.place(relx=0.5, rely=0.37, anchor=tk.CENTER)
        if "device_name" in self.defaults:
            self.device_name_entry.insert(0, self.defaults["device_name"])

        # -- Username entry field --
        self.username_entry = ctk.CTkEntry(
            container_frame, placeholder_text="username",
            placeholder_text_color="gray50", corner_radius=5
        )
        self.username_entry.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        if "username" in self.defaults:
            self.username_entry.insert(0, self.defaults["username"])

        # -- Password entry field --
        self.password_entry = ctk.CTkEntry(
            container_frame, placeholder_text="password",
            placeholder_text_color="gray50", corner_radius=5
        )
        self.password_entry.place(relx=0.5, rely=0.63, anchor=tk.CENTER)
        if "password" in self.defaults:
            self.password_entry.insert(0, self.defaults["password"])

        # -- Completion button --
        self.action_button = ctk.CTkButton(
            container_frame, text=title, font=("Arial", 13, "bold"),
            command=self.process_inputs, bg_color="transparent",
            fg_color="royalblue", hover_color="royalblue4", corner_radius=5
        )
        self.action_button.place(relx=0.5, rely=0.76, anchor=tk.CENTER)

        self.bind("<Map>", self._on_map)

    def _on_map(self, event):
        self.unbind("<Map>")
        self._init_ux()

    def _init_ux(self):
        # --- Focus and modal behavior ---
        self.lift()
        self.focus_force()
        self.grab_set()

        # --- Field order for keyboard navigation ---
        self._fields = [
            self.ip_address_entry,
            self.device_name_entry,
            self.username_entry,
            self.password_entry,
        ]

        # Start focused on the IP field
        self.ip_address_entry.focus()

        # Bind navigation keys
        for idx, field in enumerate(self._fields):
            field.bind("<Return>", lambda e, i=idx: self._on_enter(i))
            field.bind("<Down>", lambda e, i=idx: self._focus_next(i))
            field.bind("<Up>", lambda e, i=idx: self._focus_prev(i))

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

    def _focus_next(self, index):
        # Move down unless we're already at the last field
        if index < len(self._fields) - 1:
            self._fields[index + 1].focus()

    def _focus_prev(self, index):
        # Move up unless we're at the first field
        if index > 0:
            self._fields[index - 1].focus()

    def _on_enter(self, index):
        # Enter moves down, but on the last field it submits
        if index < len(self._fields) - 1:
            self._fields[index + 1].focus()
        else:
            self.action_button.invoke()
