# Standard imports
import customtkinter as ctk
import tkinter as tk
import os
import threading
from typing import Optional

# Local application imports
from app.ui.menus.SSH_action_menu import SSHActionMenu
from app.dialogs.edit_device import EditDeviceDialog
from app.config import PING_INTERVAL


class ConnectionButton(ctk.CTkFrame):
    def __init__(self, parent, app, ip_address, on_remove_connection_button_function, ping_log=False):
        super().__init__(parent, width=340, height=50, bg_color="transparent", fg_color="gray21", corner_radius=1)
        self._app = app
        self.ip_address = ip_address
        self.remove_connection_button = on_remove_connection_button_function
        self.ping_log = ping_log

        ip_address, device_name, username, password = self.device_info

        # Device name title
        self._device_name_label = ctk.CTkLabel(
            self, text=device_name, font=("Arial", 10, "bold"), fg_color="transparent",
            bg_color="transparent", text_color="white"
        )
        self._device_name_label.pack(side="left", pady=5)
        self._device_name_label.place(relx=0.02, rely=0.13, anchor=tk.W)

        # Delete device button
        delete_connection = ctk.CTkButton(
            self, text="X", width=15, height=15, fg_color="transparent", hover_color="gainsboro",
            text_color="red", corner_radius=0, command=self.delete_device)
        delete_connection.pack(pady=5)
        delete_connection.place(relx =0.01, rely=0.13, anchor=tk.CENTER)

        # todo improve edit button
        # Edit device button
        edit_connection = ctk.CTkButton(
            self, text="✏️", width=15, height=15, fg_color="transparent", hover_color="gainsboro",
            text_color="blue", corner_radius=0, command=self.edit_device)
        edit_connection.pack(pady=10)
        edit_connection.place(relx =0.05, rely=0.23, anchor=tk.CENTER)

        # SSH Commands menu
        menu = SSHActionMenu(self, self._app)
        menu.place(relx=0.95, rely=1.07, anchor=tk.SE)

        # Online/offline status label
        self.status_label = ctk.CTkLabel(
            self, text="Loading...", font=("Arial", 10), fg_color="transparent",
            bg_color="transparent", text_color="white"
        )
        self.status_label.pack(pady=5)
        self.status_label.place(relx=0.92, rely=0.229, anchor=tk.W)

        # Kick-start the update loop
        self._run_status_loop = True
        self.after(0, self.status_update_loop)

    @property
    def run_status_loop(self):
        return self._run_status_loop

    @run_status_loop.setter
    def run_status_loop(self, running: bool):
        """Pause/Resume the status update loop"""
        was_running = self._run_status_loop
        self._run_status_loop = running

        # If the update loop wasn't running before - start it now
        if running and not was_running:
            self.after(0, self.status_update_loop)

    def status_update_loop(self):
        if self._run_status_loop:
            threading.Thread(target=self._ping_and_update, daemon=True).start()
            self.after(PING_INTERVAL, self.status_update_loop)

    def _ping_and_update(self):
        response = os.system(f"ping -n 1 {self.ip_address} >nul")
        reachable = response == 0

        if self.ping_log:
            print(f'Pinged \'{self.device_info[1]}\'@{self.ip_address}: response \'{response}\'')

        self._device_name_label.configure(text=self._app.database.get_device_info_by_ip(self.ip_address)[1])

        self.after(0, lambda: self.online_appearance() if reachable else self.offline_appearance())

    @property
    def device_info(self):
        return self._app.database.get_device_info_by_ip(self.ip_address)

    def online_appearance(self):
        self.status_label.configure(text='● Online', text_color="green")

    def offline_appearance(self):
        self.status_label.configure(text='● Offline', text_color="red")

    def delete_device(self):
        print(f'Deleted device {self._app.database.get_device_info_by_ip(self.ip_address)[0]}@{self.ip_address}')
        self._app.database.delete_device_by_ip(self.ip_address)
        self.run_status_loop = False
        self.remove_connection_button(self)
        self.destroy()

    def update_button_data(self, new_ip: Optional[str] = None):
        if new_ip:
            self.ip_address = new_ip
        self._ping_and_update()

    def edit_device(self):
        EditDeviceDialog(self, self._app, self.update_button_data)
