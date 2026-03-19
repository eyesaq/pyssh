# Standard imports
import customtkinter as ctk
import tkinter as tk
import os
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

        super().__init__(parent, width=340, height=50, bg_color="transparent", fg_color="gray21", corner_radius=1)

        ip_address, device_name, username, password = self.device_info

        # Device name title
        device_name_label = ctk.CTkLabel(
            self, text=device_name, font=("Arial", 10, "bold"), fg_color="transparent",
            bg_color="transparent", text_color="white"
        )
        device_name_label.pack(side="left", pady=5)
        device_name_label.place(relx=0.02, rely=0.13, anchor=tk.W)

        # Delete device button
        delete_connection = ctk.CTkButton(
            self, text="X", width=15, height=15, fg_color="transparent", hover_color="gainsboro",
            text_color="red", corner_radius=0, command=self.delete_device)
        delete_connection.pack(pady=5)
        delete_connection.place(relx =0.01, rely=0.13, anchor=tk.CENTER)

        # SSH Commands menu.
        menu = SSHActionMenu(self, self._app, self.ip_address)
        menu.place(relx=0.95, rely=1.07, anchor=tk.SE)

         # Online/offline status label
        self.status_label = ctk.CTkLabel(
            self, text="Loading...", font=("Arial", 10), fg_color="transparent",
            bg_color="transparent", text_color="white"
        )
        self.status_label.pack(pady=5)
        self.status_label.place(relx=0.92, rely=0.229, anchor=tk.W)

        #removes delay
        self.after(1, self.status_update_loop)

    def status_update_loop(self):
        if self.status_loop_running:
            # run ping in a separate thread
            threading.Thread(target=self._ping_and_update, daemon=True).start()
            # schedule next update
            self.after(5000, self.status_update_loop)

    def _ping_and_update(self):
        # ping the device in this thread
        response = os.system(f"ping -n 1 {self.ip_address} >nul")
        reachable = response == 0

        # update the GUI safely in the main thread
        self.after(0, lambda: self.online_appearance() if reachable else self.offline_appearance())
        

    @property
    def device_info(self):
        return self._app.database.get_device_info_by_ip(self.ip_address)

    def online_appearance(self):
        self.status_label.configure(text='● Online', text_color="green")

    def offline_appearance(self):
        self.status_label.configure(text='● Offline', text_color="red")

    def destroy(self):
        if self in self.connection_buttons:
            self.connection_buttons.remove(self)
        super().destroy()

    def delete_device(self):
        print(f'Deleted device {self._app.database.get_field_by_ip(self.ip_address, 'device_name')}@{self.ip_address}')
        self._app.database.delete_device_by_ip(self.ip_address)
        self.destroy()
