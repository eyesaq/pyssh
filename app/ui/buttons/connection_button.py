# Standard imports
from ipaddress import ip_address

import customtkinter as ctk
import tkinter as tk

# Local application imports

class ConnectionButton(ctk.CTkButton):
    def __init__(self, parent, connection):
        self._parent = parent
        self.connection = connection

        ip_address = self.connection['ip_address']
        device_name = self.connection['device_name']

        get_username(get_ip_index)
        get_password(get_ip_index)

        # == GUI ==
        new_label_frame = ctk.CTkFrame(
            self._parent, width=340, height=50, bg_color="transparent",
            fg_color="gray21", corner_radius=1
        )
        new_label_frame.pack(pady=5)
        new_label_frame.pack_propagate(False)

        new_label = ctk.CTkLabel(
            new_label_frame, text=device_name, font=("Arial", 10, "bold"),
            fg_color="transparent", bg_color="transparent", text_color="white"
        )
        new_label.pack(pady=5)
        new_label.place(relx=0.05, rely=0.13, anchor=tk.W)

        #menu for ssh controls
        menu = tk.Menubutton(
            new_label_frame, text="⋯", font=("Arial", 25), bg="gray21",
            fg="white", activebackground="gray21", activeforeground="gray",
            relief="flat", bd=0, highlightthickness=0,
            highlightbackground="gray21", highlightcolor="gray21"
        )
        menu.place(relx=0.95, rely=1.07, anchor=tk.SE)

        menu.menu = tk.Menu(menu, tearoff=0, bg="gray10", fg="white", relief="flat", bd=0)
        menu["menu"] = menu.menu

        menu.menu.add_command(label="Reboot", command=lambda ip_address_name=ip_address_name, username_name=username_name, password_name=password_name: reboot(ip_address_name, username_name, password_name))
        menu.menu.add_command(label="Shutdown", command=lambda ip_address_name=ip_address_name, username_name=username_name, password_name=password_name: shutdown(ip_address_name, username_name, password_name))
        menu.menu.add_command(label="SSH", command=lambda username=username_name, ip_address=ip_address_name: threading.Thread(target=lambda: ssh(username, ip_address)).start())

        online_label = ctk.CTkLabel(
            new_label_frame, text="● Online", font=("Arial", 10), fg_color="transparent",
            bg_color="transparent", text_color="green"
        )
        online_label.pack(pady=5)
        online_label.place(relx=0.85, rely=0.229, anchor=tk.W)

        delete_button = ctk.CTkButton(
            new_label_frame, text="X", width=15, height=15, fg_color="transparent", hover_color="gainsboro",
            text_color="red", corner_radius=0,
            command=lambda frame=new_label_frame, device_key=device_name: delete_device(frame, device_key))
        delete_button.pack(pady=5)
        delete_button.place(relx =0.02, rely=0.13, anchor=tk.CENTER)

        ip_address_label = ctk.CTkLabel(new_label_frame, text=ip_address_name, bg_color="transparent")
        ip_address_label.pack(pady=5)
