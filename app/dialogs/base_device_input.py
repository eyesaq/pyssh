# Standard imports
import customtkinter as ctk
import tkinter as tk
from typing import Callable, Optional
from functools import partial

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
        self.lift()
        self.focus_force()
        self.grab_set()

        self._fields = [
            self.ip_address_entry,
            self.device_name_entry,
            self.username_entry,
            self.password_entry,
        ]

        self.ip_address_entry.focus()

        for idx, field in enumerate(self._fields):
            field.bind("<Return>", partial(self._on_enter, idx))
            field.bind("<Down>", partial(self._focus_next, idx))
            field.bind("<Up>", partial(self._focus_prev, idx))

    def retrieve_normalized_inputs(self):
        # Retrieve inputs
        ip_address = self.ip_address_entry.get()
        device_name = self.device_name_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Validate inputs
        invalid_inputs = self._validate_entries(ip_address, device_name, username, password)
        if invalid_inputs:
            self._bad_validation(invalid_inputs['main_error_message'], invalid_inputs['invalid_fields'])
            return

        # Normalize inputs
        normalized_ip_address = ip_address.lower().strip()
        normalized_device_name = device_name.lower().strip()
        normalized_username = username.lower().strip()
        normalized_password = password

        return normalized_ip_address, normalized_device_name, normalized_username, normalized_password

    def _reset_border(self, field):
        field.configure(border_color="gray30")

    def _bad_validation(self, main_error_message: str, invalid_fields: tuple[ctk.CTkEntry,...]):
        for invalid_field in invalid_fields:
            invalid_field.configure(border_color="red")
            invalid_field.bind("<FocusIn>", partial(self._reset_border, invalid_field))

        print(f'Validation Error: {main_error_message}')
        # todo add a warning dialog

    def process_inputs(self):
        normalized_inputs = self.retrieve_normalized_inputs()
        if normalized_inputs:
            self.process_function(*normalized_inputs)
            self.destroy()

    def _validate_entries(self, ip_address, device_name, username, password):
        # todo validation logic
        #return {'main_error_message': 'PLACEHOLDER', 'invalid_fields': (self.ip_address_entry,)}
        return None

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
