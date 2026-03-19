# Standard imports
import customtkinter as ctk
import tkinter as tk
import os
import time
import threading

# Local application imports
from app.ui.menus.SSH_action_menu import SSHActionMenu


class ConnectionButton(ctk.CTkFrame):
    def __init__(self, parent, app, ip_address, connection_buttons):
        self._parent = parent
        self._app = app
        self.ip_address = ip_address
        self.connection_buttons = connection_buttons

        # Pause or continue the status update loop.
        self.status_loop_running = True

        super().__init__(self._parent, width=340, height=50, bg_color="transparent", fg_color="gray21", corner_radius=1)

        ip_address, device_name, username, password = self.device_info

        # Device name title
        device_name_label = ctk.CTkLabel(
            self, text=device_name, font=("Arial", 10, "bold"), fg_color="transparent",
            bg_color="transparent", text_color="white"
        )
        device_name_label.pack(pady=5)
        device_name_label.place(relx=0.05, rely=0.13, anchor=tk.W)

        # Delete device button
        delete_connection = ctk.CTkButton(
            self, text="X", width=15, height=15, fg_color="transparent", hover_color="gainsboro",
            text_color="red", corner_radius=0, command=self.delete_device)
        delete_connection.pack(pady=5)
        delete_connection.place(relx =0.02, rely=0.13, anchor=tk.CENTER)

        # Online/offline status label
        self.status_label = ctk.CTkLabel(
            self, text="Wait...", font=("Arial", 10), fg_color="transparent",
            bg_color="transparent", text_color="green"
        )
        self.status_label.pack(pady=5)
        self.status_label.place(relx=0.85, rely=0.229, anchor=tk.W)

        # SSH Commands menu.
        menu = SSHActionMenu(self, self._app, self.ip_address)
        menu.place(relx=0.95, rely=1.07, anchor=tk.SE)

        threading.Thread(target=self.status_update_loop).start()

    def status_update_loop(self):
        while True:
            if self.status_loop_running:
                self.update_online_status()
                time.sleep(5)

    def update_online_status(self):
        if self.ping():
            self.online_appearance()
        else:
            self.offline_appearance()

    def ping(self):
        response = os.system(f"ping -n 1 {self.ip_address}")

        if response == 0:
            print(f"{self.ip_address} is reachable")
            return True
        else:
            print(f"{self.ip_address} is not reachable ({response})")
            return False

    @property
    def device_info(self):
        return self._app.database.get_device_info_by_ip(self.ip_address)

    def online_appearance(self):
        self.status_label.configure(text='● Online')

    def offline_appearance(self):
        self.status_label.configure(text='● Offline')

    def destroy(self):
        if self in self.connection_buttons:
            self.connection_buttons.remove(self)
        super().destroy()

    def delete_device(self):
        print(f'Deleted device {self._app.database.get_field_by_ip(self.ip_address, 'device_name')}@{self.ip_address}')
        self._app.database.delete_device_by_ip(self.ip_address)
        self.destroy()
