import customtkinter as ctk
import tkinter as tk
import threading


class ConnectionButton(ctk.CTkFrame):
    def __init__(self, parent, app, ip_address, online_status):
        super().__init__(parent, height=50, fg_color="gray21", corner_radius=1)

        self._app = app
        self.ip_address = ip_address
        self.online_status = online_status

        # Layout config
        self.grid_columnconfigure(2, weight=1)  # middle expands

        self.build_widget()

    def build_widget(self):
        if self.online_status:
            self.online_connection_widget()
        else:
            self.offline_connection_widget()

    # =========================
    # ONLINE
    # =========================
    def online_connection_widget(self):
        device_name = self._app.database.get_field_by_ip(self.ip_address, "device_name")
        username = self._app.database.get_field_by_ip(self.ip_address, "username")
        password = self._app.database.get_field_by_ip(self.ip_address, "password")

        # Delete button (left)
        delete_btn = ctk.CTkButton(
            self,
            text="X",
            width=20,
            height=20,
            fg_color="transparent",
            hover_color="gainsboro",
            text_color="red",
            command=lambda: delete_device(self, self.ip_address)
        )
        delete_btn.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        # Device name
        name_label = ctk.CTkLabel(
            self,
            text=device_name,
            font=("Arial", 10, "bold"),
            text_color="white"
        )
        name_label.grid(row=0, column=1, sticky="w")

        # Status
        status_label = ctk.CTkLabel(
            self,
            text="● Online",
            text_color="green",
            font=("Arial", 10)
        )
        status_label.grid(row=0, column=2, sticky="e", padx=5)

        # IP label (below name)
        ip_label = ctk.CTkLabel(self, text=self.ip_address)
        ip_label.grid(row=1, column=1, sticky="w")

        # Menu (right)
        menu_btn = tk.Menubutton(
            self,
            text="⋯",
            font=("Arial", 16),
            bg="gray21",
            fg="white",
            relief="flat",
            bd=0
        )
        menu_btn.grid(row=0, column=3, rowspan=2, sticky="e", padx=5)

        menu = tk.Menu(menu_btn, tearoff=0, bg="gray10", fg="white")
        menu_btn["menu"] = menu

        menu.add_command(
            label="Reboot",
            command=lambda: reboot(self.ip_address, username, password)
        )
        menu.add_command(
            label="Shutdown",
            command=lambda: shutdown(self.ip_address, username, password)
        )
        menu.add_command(
            label="SSH",
            command=lambda: threading.Thread(
                target=lambda: ssh(username, self.ip_address)
            ).start()
        )

    # =========================
    # OFFLINE
    # =========================
    def offline_connection_widget(self):
        device_name = self._app.database.get_field_by_ip(self.ip_address, "device_name")

        # Delete button
        delete_btn = ctk.CTkButton(
            self,
            text="X",
            width=20,
            height=20,
            fg_color="transparent",
            hover_color="gainsboro",
            text_color="red",
            command=lambda: delete_device(self, self.ip_address)
        )
        delete_btn.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        # Name
        name_label = ctk.CTkLabel(
            self,
            text=device_name,
            font=("Arial", 10, "bold"),
            text_color="white"
        )
        name_label.grid(row=0, column=1, sticky="w")

        # Status
        status_label = ctk.CTkLabel(
            self,
            text="● Offline",
            text_color="red",
            font=("Arial", 10)
        )
        status_label.grid(row=0, column=2, sticky="e", padx=5)

        # IP
        ip_label = ctk.CTkLabel(self, text=self.ip_address)
        ip_label.grid(row=1, column=1, sticky="w")