# Standard imports
import customtkinter as ctk
from tkinter import messagebox
import os
import threading
from typing import Optional

# Local application imports
from app.ui.menus.SSH_action_menu import SSHActionMenu
from app.dialogs.edit_device import EditDeviceDialog
from app.config import PING_INTERVAL
from app.ui.tooltips import CTkToolTip


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
            relx=0.0, rely=1.0, anchor="sw", relwidth=0.15,
            relheight=0.4, x=5, y=-5
        )

        # Delete device button
        delete_icon = self._app.icons.red_delete_button
        w, h = delete_icon.cget('size')

        self.delete_connection_button = ctk.CTkButton(
            toolbox_frame, image=delete_icon, text='', fg_color="transparent",
            hover_color="gray13", command=self.delete_connection, width=w, height=h
        )
        self.delete_connection_button.place(anchor='center', relx=0.2, rely=0.5)
        CTkToolTip(self.delete_connection_button, "Delete")

        # Edit device button
        edit_icon = self._app.icons.white_edit_button
        w, h = edit_icon.cget('size')

        self.edit_connection_button = ctk.CTkButton(
            toolbox_frame, image=edit_icon, text= '', fg_color="transparent",
            hover_color="gray13", command=self.edit_device, width=w, height=h
        )
        self.edit_connection_button.place(anchor='center', relx=0.5, rely=0.5)
        CTkToolTip(self.edit_connection_button, "Edit")

        # SSH Commands menu
        self.menu_button = SSHActionMenu(toolbox_frame, self._app, self.device_info)
        self.menu_button.place(relx=0.8, rely=0.5, anchor='center')
        CTkToolTip(self.menu_button, "SSH options")

        # Device name title
        self._device_name_label = ctk.CTkLabel(
            self, text=device_name, font=("Arial", 15, "bold"), fg_color="transparent",
            bg_color="transparent", text_color="white", height=10
        )
        self._device_name_label.place(x=5, y=2, relx=0.0, rely=0.0, anchor='nw')

        # Connection details
        top_right_status_frame = ctk.CTkFrame(self, fg_color="transparent", bg_color="transparent")
        top_right_status_frame.place(relx=1, rely=0.0, anchor="ne", x=-1.5, y=2)

        self._ip_address_label = ctk.CTkLabel(top_right_status_frame, text=ip_address)
        self._ip_address_label.pack(side="left", padx=(0, 5))

        self.status_label = ctk.CTkLabel(top_right_status_frame, text="○", fg_color="transparent")
        self.status_label.pack(side="left", padx=(0, 5))

        # Kick-start the update loop
        self._run_status_loop = True
        self.after_idle(self._init_update_loop)

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
            self.after_idle(self._init_update_loop)

    def _init_update_loop(self):
        if self._run_status_loop:
            threading.Thread(target=lambda: self._run_ping_cycle(reschedule=True), daemon=True).start()

    def _run_ping_cycle(self, reschedule: bool = False):
        response = os.system(f"ping -n 1 {self.ip_address} >nul")
        reachable = response == 0
        if self.ping_log:
            print(f'Pinged \'{self.device_info[1]}\'@{self.ip_address}: response \'{response}\'')
        self.after_idle(lambda: self._apply_ping_result_cycle(reachable, reschedule))

    def _apply_ping_result_cycle(self, reachable: bool, reschedule: bool):
        if not self.winfo_exists():
            return

        self._refresh_labels()
        self.online_appearance() if reachable else self.offline_appearance()

        if self._run_status_loop and reschedule:
            self.after(PING_INTERVAL, self._init_update_loop)

    def refresh(self):
        if not self.winfo_exists():
            return
        self._refresh_labels()
        threading.Thread(target=self._run_ping_cycle, daemon=True).start()

    def _refresh_labels(self):
        self._ip_address_label.configure(text=self.device_info[0])
        self._device_name_label.configure(text=self.device_info[1])

    @property
    def device_info(self):
        return self._app.database.get_connection_info_by_ip(self.ip_address)

    @property
    def highlighted(self):
        return self._highlighted

    @highlighted.setter
    def highlighted(self, highlight: bool):
        if highlight:
            self.configure(border_width=1, border_color="#8EBBFF")

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
        self.status_label.configure(text="●", text_color="green")

    def offline_appearance(self):
        self.status_label.configure(text="●", text_color="red")

    def delete_connection(self, force_delete: bool = False):
        device_name = self.device_info[1]
        if force_delete:
            confirmation = True
        else:
            confirmation = messagebox.askyesno("Confirm Delete", f"Delete '{device_name}'?")

        if confirmation:
            self._app.database.delete_connection_by_ip(self.ip_address)
            self.run_status_loop = False
            self.remove_connection_button(self)
            self.destroy()

    def apply_new_ip(self, new_ip: Optional[str] = None):
        if new_ip:
            self.ip_address = new_ip
        self.refresh()

    def edit_device(self):
        EditDeviceDialog(self, self._app, self.apply_new_ip)
