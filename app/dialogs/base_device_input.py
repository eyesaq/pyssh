# Standard imports
import socket
import customtkinter as ctk
import tkinter as tk
import ipaddress
from typing import Callable, Optional
from functools import partial
import re


class BaseDeviceInput(ctk.CTkToplevel):
    def __init__(self, parent, on_completion_function: Callable, title: str, fast_field_overwrite: bool = True, defaults: Optional[dict] = None):
        super().__init__(parent)
        self.process_function = on_completion_function
        self.fast_field_overwrite = fast_field_overwrite
        self.defaults = defaults or {}

        self.title(title)
        self.geometry("250x420")  # Increased to accommodate error labels

        # -- Main container --
        self.container_frame = ctk.CTkFrame(
            self, width=220, height=390, bg_color="transparent",
            fg_color="gray20", corner_radius=1
        )
        self.container_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # -- Header --
        header_label = tk.Label(
            self.container_frame, text=f"  {title}  ",
            font=("Arial", 16, "bold"), fg="white", bg="gray20"
        )
        header_label.place(relx=0.5, rely=0.07, anchor=tk.CENTER)

        # Each field is paired with an error label beneath it
        # rely positions are spaced to leave room for error labels
        self.ip_address_entry, self.ip_address_error = self._make_field(
            "ip address", "ip_address", rely=0.18
        )
        self.device_name_entry, self.device_name_error = self._make_field(
            "device name", "device_name", rely=0.33
        )
        self.username_entry, self.username_error = self._make_field(
            "username", "username", rely=0.48
        )
        self.password_entry, self.password_error = self._make_field(
            "password", "password", rely=0.63
        )

        # -- Completion button --
        self.action_button = ctk.CTkButton(
            self.container_frame, text=title, font=("Arial", 13, "bold"),
            command=self.process_inputs, bg_color="transparent",
            fg_color="royalblue", hover_color="royalblue4", corner_radius=5
        )
        self.action_button.place(relx=0.5, rely=0.83, anchor=tk.CENTER)

        self.bind("<Map>", self._on_map)

    def _make_field(self, placeholder: str, default_key: str, rely: float):
        """Create an entry field and its paired error label, returning both."""
        entry = ctk.CTkEntry(
            self.container_frame, placeholder_text=placeholder,
            placeholder_text_color="gray50", corner_radius=5
        )
        entry.place(relx=0.5, rely=rely, anchor=tk.CENTER)
        if default_key in self.defaults:
            entry.insert(0, self.defaults[default_key])

        error_label = ctk.CTkLabel(
            self.container_frame, text="", font=("Arial", 10),
            text_color="red", fg_color="transparent", height=8
        )
        error_label.place(relx=0.5, rely=rely + 0.07, anchor=tk.CENTER)

        return entry, error_label

    def _on_map(self, event):
        self.unbind("<Map>")
        self._init_ux()

    def _init_ux(self):
        self.lift()
        self.focus_force()
        self.grab_set()

        self._fields = [
            self.ip_address_entry,
            self.device_name_entry,
            self.username_entry,
            self.password_entry,
        ]

        self._error_labels = {
            self.ip_address_entry: self.ip_address_error,
            self.device_name_entry: self.device_name_error,
            self.username_entry: self.username_error,
            self.password_entry: self.password_error,
        }

        self.bind("<Escape>", lambda e: self.destroy())
        self.ip_address_entry.focus()

        for idx, field in enumerate(self._fields):
            field.bind("<Return>", partial(self._on_enter, idx))
            field.bind("<Down>", partial(self._focus_next, idx))
            field.bind("<Up>", partial(self._focus_prev, idx))
            if self.fast_field_overwrite:
                field.bind("<FocusIn>", partial(self._select_all, field))

    def _select_all(self, field, event=None):
        field.select_range(0, tk.END)
        field.icursor(tk.END)

    def retrieve_inputs(self):
        ip_address = self.ip_address_entry.get()
        device_name = self.device_name_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

        errors = self._validate_entries(ip_address, device_name, username, password)
        if errors:
            self._bad_validation(errors)
            return None

        return ip_address, device_name, username, password

    def _reset_field(self, field, event=None):
        field.configure(border_color="gray30")
        self._error_labels[field].configure(text="")

    def _bad_validation(self, errors: dict):
        first_error_field = None

        for field, field_errors in errors.items():
            if field_errors:
                if first_error_field is None:
                    first_error_field = field
                field.configure(border_color="red")
                self._error_labels[field].configure(text=field_errors[0])
                field.bind("<FocusIn>", partial(self._reset_field, field))
                self.focus()
            else:
                self._error_labels[field].configure(text="")

    def process_inputs(self):
        inputs = self.retrieve_inputs()
        if inputs:
            self.process_function(*inputs)

    def _validate_entries(self, ip_address, device_name, username, password):
        errors = {
            self.ip_address_entry: [],
            self.device_name_entry: [],
            self.username_entry: [],
            self.password_entry: []
        }

        # Presence checks
        if not ip_address.strip():
            errors[self.ip_address_entry].append("IP address is required")
        if not device_name.strip():
            errors[self.device_name_entry].append("Device name is required")
        if not username.strip():
            errors[self.username_entry].append("Username is required")
        if not password.strip():
            errors[self.password_entry].append("Password is required")

        # Device name length
        if len(device_name) > 25:
            errors[self.device_name_entry].append("Device name must be 25 characters or fewer")

        # Username validation
        if username and not re.fullmatch(r"[A-Za-z0-9_.-]+", username):
            errors[self.username_entry].append("Username contains invalid characters")
        if username.startswith("-"):
            errors[self.username_entry].append("Username cannot start with '-'")

        # Password validation
        if " " in password:
            errors[self.password_entry].append("Password cannot contain spaces")

        # IP / Hostname validation
        if ip_address.strip():
            try:
                ipaddress.ip_address(ip_address)
            except ValueError:
                try:
                    socket.gethostbyname(ip_address)
                except socket.error:
                    errors[self.ip_address_entry].append(f"'{ip_address}' is not a valid IP or hostname")

        return errors if any(errors.values()) else None

    def _focus_next(self, index, event=None):
        if index < len(self._fields) - 1:
            self._fields[index + 1].focus()

    def _focus_prev(self, index, event=None):
        if index > 0:
            self._fields[index - 1].focus()

    def _on_enter(self, index, event=None):
        if index < len(self._fields) - 1:
            self._fields[index + 1].focus()
        else:
            self.action_button.invoke()
