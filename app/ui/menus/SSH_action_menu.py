# Standard imports
import tkinter as tk
import subprocess
import paramiko
import threading
import customtkinter as ctk


class SSHActionMenu(ctk.CTkButton):
    def __init__(self, parent, app):
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

        self._parent = parent
        self._app = app

        self.menu = tk.Menu(self, tearoff=0, bg="gray10", fg="white", relief="flat", bd=0)
        self['menu'] = self.menu

        self.menu.add_command(label="Reboot", command=self.reboot)
        self.menu.add_command(label="Shutdown", command=self.shutdown)
        self.menu.add_command(label="SSH", command=self.start_ssh)

    def _open_menu(self):
        x = self.winfo_rootx()
        y = self.winfo_rooty() + self.winfo_height()
        self.menu.tk_popup(x, y)

    @property
    def device_info(self):
        return self._app.database.get_connection_info_by_ip(self._parent.ip_address)

    def start_ssh(self):
        threading.Thread(target=self._ssh_thread).start()

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
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ip_address, device_name, username, password = self.device_info

        ssh.connect(ip_address, username=username, password=password)
        stdin, stdout, stderr = ssh.exec_command("sudo shutdown -r now")
        output = stdout.readlines()

        print(f'\nRebooting \'{device_name}\'@{ip_address}\n')

        for line in output:
            print(line.strip())

        print(f'\n\'{device_name}\'@{ip_address} reboot operation ended\n')

    def shutdown(self):
        threading.Thread(target=self._shutdown_thread).start()

    def _shutdown_thread(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ip_address, device_name, username, password = self.device_info

        ssh.connect(ip_address, username=username, password=password)
        stdin, stdout, stderr = ssh.exec_command("sudo shutdown now")
        output = stdout.readlines()

        print(f'\nShutting down \'{device_name}\'@{ip_address}\n')

        for line in output:
            print(line.strip())

        print(f'\n\'{device_name}\'@{ip_address} shut down operation ended\n')
