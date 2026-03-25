# Standard imports
import customtkinter as ctk
import os
import threading
from typing import Optional

# Local application imports
from app.ui.menus.SSH_action_menu import SSHActionMenu
from app.dialogs.edit_device import EditDeviceDialog
from app.config import PING_INTERVAL


class ConnectionButton(ctk.CTkFrame):
    def __init__(self, parent, app, ip_address, on_remove_connection_button_function, ping_log=False):
        super().__init__(parent, width=340, height=50, bg_color="transparent", fg_color="gray21")
        self._app = app
        self.ip_address = ip_address
        self.remove_connection_button = on_remove_connection_button_function
        self.ping_log = ping_log

        self._highlighted = False
        self.bind_ids = {}

        ip_address, device_name, username, password = self.device_info

        # Toolbox buttons container
        toolbox_frame = ctk.CTkFrame(self)
        toolbox_frame.place(
            relx=0.0, rely=1.0, anchor="sw", relwidth=0.1,
            relheight=0.4, x=5, y=-5
        )

        # Delete device button
        delete_icon = self._app.icons.delete_button
        w, h = delete_icon.cget('size')

        self.delete_connection_button = ctk.CTkButton(
            toolbox_frame, image=delete_icon, text='', fg_color="transparent",
            hover_color="gainsboro", command=self.delete_device, width=w, height=h
        )
        self.delete_connection_button.place(anchor='center', relx=0.2, rely=0.5)

        # Edit device button
        edit_icon = self._app.icons.edit_button
        w, h = edit_icon.cget('size')

        self.edit_connection_button = ctk.CTkButton(
            toolbox_frame, image=edit_icon, text= '', fg_color="transparent",
            hover_color="gainsboro", command=self.edit_device, width=w, height=h
        )
        self.edit_connection_button.place(anchor='center', relx=0.5, rely=0.5)

        # SSH Commands menu
        self.menu_button = SSHActionMenu(toolbox_frame, self._app, self.device_info)
        self.menu_button.place(relx=0.8, rely=0.5, anchor='center')

        # Device name title
        self._device_name_label = ctk.CTkLabel(
            self, text=device_name, font=("Arial", 15, "bold"), fg_color="transparent",
            bg_color="transparent", text_color="white", height=10
        )
        self._device_name_label.place(x=5, y=2, relx=0.0, rely=0.0, anchor='nw')

        # Online/offline status label
        w, h = self._app.icons.online_indicator.cget('size')

        self.status_label = ctk.CTkLabel(self, text="", image=None, width=w, height=h)
        self.status_label.place(relx=0.97, rely=0.5, anchor='center')

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
        self._device_name_label.configure(text=self._app.database.get_connection_info_by_ip(self.ip_address)[1])

        response = os.system(f"ping -n 1 {self.ip_address} >nul")
        reachable = response == 0

        if self.ping_log:
            print(f'Pinged \'{self.device_info[1]}\'@{self.ip_address}: response \'{response}\'')

        self.after_idle(lambda: self.online_appearance() if reachable else self.offline_appearance())

    @property
    def device_info(self):
        return self._app.database.get_connection_info_by_ip(self.ip_address)

    @property
    def highlighted(self):
        return self._highlighted

    @highlighted.setter
    def highlighted(self, highlight: bool):
        if highlight:
            self.configure(border_width=2, border_color="white")

            self.bind_ids["<e>"] = self._app.bind("<e>", lambda e: self.edit_connection_button.invoke())
            self.bind_ids["<Delete>"] = self._app.bind("<Delete>", lambda e: self.delete_connection_button.invoke())
            self.bind_ids["<m>"] = self._app.bind("<m>", lambda e: self.menu_button.invoke())
        else:
            if self.bind_ids:
                for sequence, bind_id in self.bind_ids.items():
                    self._app.unbind(sequence, bind_id)
                self.bind_ids = {}
            self.configure(border_width=0)

        self._highlighted = highlight

    def online_appearance(self):
        self.status_label.configure(image=self._app.icons.online_indicator)

    def offline_appearance(self):
        self.status_label.configure(image=self._app.icons.offline_indicator)

    def delete_device(self):
        print(f'Deleted device {self._app.database.get_connection_info_by_ip(self.ip_address)[0]}@{self.ip_address}')
        self._app.database.delete_connection_by_ip(self.ip_address)
        self.run_status_loop = False
        self.remove_connection_button(self)
        self.destroy()

    def update_button_data(self, new_ip: Optional[str] = None):
        if new_ip:
            self.ip_address = new_ip
        self._ping_and_update()

    def edit_device(self):
        EditDeviceDialog(self, self._app, self.update_button_data)
