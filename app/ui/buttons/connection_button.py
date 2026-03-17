# Standard imports
from ipaddress import ip_address

import customtkinter as ctk
import tkinter as tk
import threading
from app.pages.home import HomePage

# Local application imports


class ConnectionButton(ctk.CTkButton):
    def __init__(self, parent, app, ip_address, online_status, device_container):
        self._parent = parent
        self._app = app
        self.ip_address = ip_address
        self.online_status = online_status
        self.device_container = device_container

    def set_online_status(self, online_status: bool):
        pass

        # == GUI ==
        # == Online device widget ==
    def online_connection_widget(self):
        # Gets device info from database
        device_name = self._app.database.get_field_by_ip(self.ip_address, "device_name")
        username = self._app.database.get_field_by_ip(self.ip_address, "username")
        password = self._app.database.get_field_by_ip(self.ip_address, "password")
        
        # Frame - add device_container to home.py
        online_connection_frame = ctk.CTkFrame(self.device_container, width=340, height=50, bg_color="transparent", fg_color="gray21", corner_radius=1)
        online_connection_frame.pack(pady=5)
        online_connection_frame.pack_propagate(False)

        # Nameplate
        new_label = ctk.CTkLabel(online_connection_frame, text=device_name, font=("Arial", 10, "bold"), fg_color="transparent", bg_color="transparent", text_color="white")
        new_label.pack(pady=5)
        new_label.place(relx=0.05, rely=0.13, anchor=tk.W)

        # Shows online status
        online_label = ctk.CTkLabel(online_connection_frame, text="● Online", font=("Arial", 10), fg_color="transparent", bg_color="transparent", text_color="green")
        online_label.pack(pady=5)
        online_label.place(relx=0.85, rely=0.229, anchor=tk.W)

        # Menu for ssh controls - reboot, shutdown and ssh functions need to be added
        menu = tk.Menubutton(online_connection_frame, text="⋯", font=("Arial", 25), bg="gray21",fg="white" ,activebackground="gray21", activeforeground="gray", relief="flat", bd=0, highlightthickness=0, highlightbackground="gray21", highlightcolor="gray21")
        menu.place(relx=0.95, rely=1.07, anchor=tk.SE)
        menu.menu = tk.Menu(menu, tearoff=0, bg="gray10", fg="white", relief="flat", bd=0)
        menu["menu"] = menu.menu
        menu.menu.add_command(label="Reboot", command=lambda ip_address = self.ip_address, username=username, password=password: reboot(ip_address, username, password))
        menu.menu.add_command(label="Shutdown", command=lambda ip_address = self.ip_address, username=username, password=password: shutdown(ip_address, username, password))
        menu.menu.add_command(label="SSH", command=lambda username=username, ip_address=self.ip_address: threading.Thread(target=lambda: ssh(username, ip_address)).start())

        # Needs delete device function - now using ip address instead of key
        delete_connection = ctk.CTkButton(online_connection_frame, text="X", width=15, height=15, fg_color="transparent", hover_color="gainsboro", text_color="red", corner_radius=0, command=lambda frame=online_connection_frame, ip_address = self.ip_address: delete_device(frame, ip_address))
        delete_connection.pack(pady=5)
        delete_connection.place(relx =0.02, rely=0.13, anchor=tk.CENTER)

        # Shows ip label
        ip_address_label = ctk.CTkLabel(online_connection_frame, text=self.ip_address, bg_color="transparent")
        ip_address_label.pack(pady=5)

        # ==Online device widget==
    def offline_connection_widget(self):
        # Gets device info from database
        device_name = self._app.database.get_field_by_ip(self.ip_address, "device_name")

        # Frame - add device_container to home.py
        offline_connection_frame = ctk.CTkFrame(self.device_container, width=340, height=50, bg_color="transparent", fg_color="gray21", corner_radius=1)
        offline_connection_frame.pack(pady=5)
        offline_connection_frame.pack_propagate(False)

        # Nameplate
        new_label = ctk.CTkLabel(offline_connection_frame, text=device_name, font=("Arial", 10, "bold"), fg_color="transparent", bg_color="transparent", text_color="white")
        new_label.pack(pady=5)
        new_label.place(relx=0.05, rely=0.13, anchor=tk.W)

        # Shows online status
        offline_label = ctk.CTkLabel(offline_connection_frame, text="● Offline", font=("Arial", 10), fg_color="transparent", bg_color="transparent", text_color="red")
        offline_label.pack(pady=5)
        offline_label.place(relx=0.85, rely=0.229, anchor=tk.W)

        # Needs delete device function - now using ip address instead of key
        delete_connection = ctk.CTkButton(offline_connection_frame, text="X", width=15, height=15, fg_color="transparent", hover_color="gainsboro", text_color="red", corner_radius=4, command=lambda frame=offline_connection_frame, ip_address = self.ip_address: delete_device(frame, ip_address))
        delete_connection.pack(pady=5)
        delete_connection.place(relx =0.02, rely=0.13, anchor=tk.CENTER)

        # Shows ip label
        ip_address_label = ctk.CTkLabel(offline_connection_frame, text=self.ip_address, bg_color="transparent")
        ip_address_label.pack(pady=5)


