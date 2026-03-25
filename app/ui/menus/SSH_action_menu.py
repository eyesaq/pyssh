# Standard imports
import tkinter as tk
import subprocess
import paramiko
import threading
import customtkinter as ctk
from typing import Callable


class SSHActionMenu(ctk.CTkButton):
    def __init__(self, parent, app, get_device_info: Callable):
        menu_icon = app.icons.menu_button
        w, h = menu_icon.cget('size')

        super().__init__(
            parent,
            image=menu_icon,
            text='',
            width=w,
            height=h,
            fg_color="transparent",
            hover_color="gainsboro",
            command=self._open_menu
        )

        self._get_device_info = get_device_info
        self._app = app

        self.menu = tk.Menu(self, tearoff=0, bg="gray10", fg="white", relief="flat", bd=0)

        self.menu.add_command(label="Reboot", command=self.reboot)
        self.menu.add_command(label="Shutdown", command=self.shutdown)
        self.menu.add_command(label="SSH", command=self.start_ssh)

    def _open_menu(self):
        x = self.winfo_rootx()
        y = self.winfo_rooty() + self.winfo_height()
        self.menu.tk_popup(x, y)

    @property
    def device_info(self):
        return self._get_device_info

    def start_ssh(self):
        threading.Thread(target=self._ssh_thread).start()

    def _run_ssh_command(self, command: str, action_name: str):
        ssh = paramiko.SSHClient()
        try:
            ip_address, device_name, username, password = self.device_info
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ip_address, username=username, password=password)
            _, stdout, _ = ssh.exec_command(command)

            print(f'\n{action_name} \'{device_name}\'@{ip_address}\n')
            for line in stdout.readlines():
                print(line.strip())

        finally:
            ssh.close()

    def _ssh_thread(self):
        ip_address, device_name, username, password = self.device_info

        ssh_command = f"ssh {username}@{ip_address}"
        try:
            subprocess.run(["cmd", "/c", ssh_command])
        except Exception as e:
            print(f"Failed to connect to {ip_address}\n{e}")

    def reboot(self):
        threading.Thread(target=self._reboot_thread).start()

    def _reboot_thread(self):
        self._run_ssh_command("sudo shutdown -r now", 'reboot')

    def shutdown(self):
        threading.Thread(target=self._shutdown_thread).start()

    def _shutdown_thread(self):
        self._run_ssh_command("sudo shutdown now", 'shutdown')
