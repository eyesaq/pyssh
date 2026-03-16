# Standard libraries
import os
import tkinter as tk
import json
#from PIL import Image, ImageTk
import threading
import customtkinter as ctk

# Local application imports
from app.services.write_functions import write_name_json, write_ip_json, write_username_json, write_password_json
from app.services.ssh_functions import ssh, reboot, shutdown


def clear_entry_fields(*fields):
    for field in fields:
        field.delete(0, tk.END)

def create_device_button(device):
    key = device.lower()
    
    #i use subprocess and threading for ts. so i dont need it now but im too lazy to delete it 
    def open_device():
        path = os.path.join("Devices", f"{key}.bat")
        try:
            os.startfile(path)
        except Exception as e:
            print(f"Failed to start {path}: {e}")

    #offline device gui look
    def device_offline(key):
        get_ip()

        global new_label_frame
        new_label_frame = ctk.CTkFrame(device_container, width=340, height=50, bg_color="transparent", fg_color="gray21", corner_radius=1)
        new_label_frame.pack(pady=5)
        new_label_frame.pack_propagate(False)

        new_label = ctk.CTkLabel(new_label_frame, text=key, font=("Arial", 10, "bold"), fg_color="transparent", bg_color="transparent", text_color="white")
        new_label.pack(pady=5)
        new_label.place(relx=0.05, rely=0.13, anchor=tk.W)

        offline_label = ctk.CTkLabel(new_label_frame, text="● Offline", font=("Arial", 10), fg_color="transparent", bg_color="transparent", text_color="red")
        offline_label.pack(pady=5)
        offline_label.place(relx=0.85, rely=0.229, anchor=tk.W)

        delete_button = ctk.CTkButton(new_label_frame, text="X", width=15, height=15, fg_color="transparent", hover_color="gainsboro", text_color="red", corner_radius=4, command=lambda frame=new_label_frame, device_key=key: delete_device(frame, device_key))
        delete_button.pack(pady=5)
        delete_button.place(relx =0.02, rely=0.13, anchor=tk.CENTER)

        ip_address_label = ctk.CTkLabel(new_label_frame, text=ip_address_name)
        ip_address_label.pack(pady=5)

    #online device gui look
    def device_online(key):
        get_ip()
        get_username(get_ip_index)
        get_password(get_ip_index)

        global new_label_frame
        new_label_frame = ctk.CTkFrame(device_container, width=340, height=50, bg_color="transparent", fg_color="gray21", corner_radius=1)
        new_label_frame.pack(pady=5)
        new_label_frame.pack_propagate(False)

        new_label = ctk.CTkLabel(new_label_frame, text=key, font=("Arial", 10, "bold"), fg_color="transparent", bg_color="transparent", text_color="white")
        new_label.pack(pady=5)
        new_label.place(relx=0.05, rely=0.13, anchor=tk.W)

        #menu for ssh controls
        menu = tk.Menubutton(new_label_frame, text="⋯", font=("Arial", 25), bg="gray21",fg="white" ,activebackground="gray21", activeforeground="gray", relief="flat", bd=0, highlightthickness=0, highlightbackground="gray21", highlightcolor="gray21")
        menu.place(relx=0.95, rely=1.07, anchor=tk.SE)
        menu.menu = tk.Menu(menu, tearoff=0, bg="gray10", fg="white", relief="flat", bd=0)
        menu["menu"] = menu.menu
        menu.menu.add_command(label="Reboot", command=lambda ip_address_name=ip_address_name, username_name=username_name, password_name=password_name: reboot(ip_address_name, username_name, password_name))
        menu.menu.add_command(label="Shutdown", command=lambda ip_address_name=ip_address_name, username_name=username_name, password_name=password_name: shutdown(ip_address_name, username_name, password_name))
        menu.menu.add_command(label="SSH", command=lambda username=username_name, ip_address=ip_address_name: threading.Thread(target=lambda: ssh(username, ip_address)).start())

        online_label = ctk.CTkLabel(new_label_frame, text="● Online", font=("Arial", 10), fg_color="transparent", bg_color="transparent", text_color="green")
        online_label.pack(pady=5)
        online_label.place(relx=0.85, rely=0.229, anchor=tk.W)

        delete_button = ctk.CTkButton(new_label_frame, text="X", width=15, height=15, fg_color="transparent", hover_color="gainsboro", text_color="red", corner_radius=0, command=lambda frame=new_label_frame, device_key=key: delete_device(frame, device_key))
        delete_button.pack(pady=5)
        delete_button.place(relx =0.02, rely=0.13, anchor=tk.CENTER)

        ip_address_label = ctk.CTkLabel(new_label_frame, text=ip_address_name, bg_color="transparent")
        ip_address_label.pack(pady=5)


    def get_ip():
        with open("../../data/devices.json") as f:
            devices = json.load(f).get("devices", [])
        global get_ip_index
        get_ip_index = [d.lower() for d in devices].index(key.lower())

        with open("../../data/ips.json") as f:
            ips = json.load(f).get("ips", [])

        global ip_address_name
        ip_address_name = ips[get_ip_index]
        
    def get_username(get_ip_index):
        index = get_ip_index
        with open("../../data/usernames.json") as f:
            usernames = json.load(f).get("usernames", [])
        global username_name
        username_name = usernames[index]

    def get_password(get_ip_index):
        index = get_ip_index
        with open("../../data/passwords.json") as f:
            passwords = json.load(f).get("passwords", [])
        global password_name
        password_name = passwords[index]


    def delete_device(frame, device_key):
        frame.destroy()

        #open json
        with open("../../data/devices.json") as f:
            devices = json.load(f).get("devices", [])

        #get index of the key
        index = [d.lower() for d in devices].index(device_key.lower())
        #remove the key from the json
        print(devices)
        del devices[index]
        print(f"edit: {devices}")
        if device_key.lower() not in [d.lower() for d in devices]:
            print(f"{device_key} removed from devices.json")
        else:
            print(f"Failed to remove {device_key} from devices.json")

        #write to the json file
        with open("../../data/devices.json", "w") as f:
            json.dump({"devices": devices}, f, indent=4)

        #same shit just for ip ips.json
        with open("../../data/ips.json") as f:
            ips = json.load(f).get("ips", [])

        ip_key = ips[index]

        print(ips)
        del ips[index]
        print(f"edit: {ips}")

        if ip_key not in ips:
            print(f"{ip_key} removed from ips.json")
        else:
            print(f"Failed to remove {ip_key} from ips.json")

        with open("../../data/ips.json", "w") as f:
            json.dump({"ips": ips}, f, indent=4)

        #same for Username.json

        with open("../../data/usernames.json") as f:
            usernames = json.load(f).get("usernames", [])
        
        usernames_key = usernames[index]

        print(usernames)
        del usernames[index]
        print(f"edit: {usernames}")
        
        if usernames_key not in usernames:
            print(f"{usernames_key} removed from usernames.json")
        else:
            print(f"Failed to remove {usernames_key} from usernames.json")

        with open("../../data/usernames.json", "w") as f:
           json.dump({"usernames": usernames}, f, indent=4)

        #same for Password.json
        with open("../../data/passwords.json") as f:
            passwords = json.load(f).get("passwords", [])

        passwords_key = passwords[index]

        print(passwords)
        del passwords[index]
        print(f"edit: {passwords}")

        if passwords_key not in passwords:
            print(f"{passwords_key} removed from passwords.json")
        else:
            print(f"Failed to remove {passwords_key} from passwords.json")
        
        with open("../../data/passwords.json", "w") as f:
            json.dump({"passwords": passwords}, f, indent=4)

    #checks for change in device online status and changes widget accordingly 
    def device_status_check(online, ip, key, new_label_frame):
        if not new_label_frame.winfo_exists():
            return

        print("Checking status...")
        response = os.system(f"ping -n 1 {ip}")

        if response == 0:
            print(f"{ip} is reachable")
            check_online = True
        else:
            print(f"{ip} is not reachable")
            check_online = False

        if check_online != online:
            print("Status change detected, Refreshing...")
            for widget in device_container.winfo_children():
                widget.destroy()
            load_devices()
            online = check_online
        else:
            print("No status change")

        #schedule next check in 5 seconds
        window.after(5000, lambda: device_status_check(online, ip, key, new_label_frame))

    #find the IP corresponding to this device match by index in devices.json
    try:
        with open("../../data/devices.json") as f:
            devices = json.load(f).get("devices", [])
        with open("../../data/ips.json") as f:
            ips = json.load(f).get("ips", [])
        try:
            idx = devices.index(key)
            ip = ips[idx] if idx < len(ips) else None
        except ValueError:
            ip = None
    except Exception:
        ip = None

    if ip:
        response = os.system(f"ping -n 1 {ip}")
        if response == 0:
            print(f"{ip} is reachable")
            device_online(key)
        else:
            print(f"{ip} is not reachable")
            device_offline(key)
    else:
        print(f"No IP found for {key}; skipping ping")
        device_offline(key)

#gets info from the entry fields and calls the functions to create batch file and write to json
def use_variables(device_name, ip_address, user, frame, password):
    #get the values from the entry fields without whitespace
    name_raw = device_name.get().strip()
    ip = ip_address.get().strip()
    user_val = user.get().strip()
    password = password.get()


    if not name_raw or not ip or not user_val:
        print("Device fields are empty - cannot create device")
        empty_label = tk.Label(frame, text="feilds cannot be empty", font=("Arial", 10), fg="red", bg="gray20")
        empty_label.pack(pady=5)
        empty_label.place(relx=0.5, rely=0.75, anchor=tk.CENTER)  
        return None
    elif ip.isalpha():
        print("Enter a valid IP address - cannot be alphabetic")
        ip_label = tk.Label(frame, text="Enter a valid IP address", font=("Arial", 10), fg="red", bg="gray20")
        ip_label.pack(pady=5)
        ip_label.place(relx=0.5, rely=0.75, anchor=tk.CENTER)  
        return None

    key = name_raw.lower()
    key2 = ip.lower()
    key3 = user_val.lower()
    key4 = password

    #clears the error message if there is one in a super awful way, should be fixed in the future
    clear_label = tk.Label(frame, text="                                                            ",
                            font=("Arial", 10), bg="gray20")
    clear_label.pack(pady=5)
    clear_label.place(relx=0.5, rely=0.75, anchor=tk.CENTER)

    #writes ip to ips.json
    try:
        with open("../../data/ips.json") as json_file:
            data2 = json.load(json_file)
    except Exception:
        data2 = {"ips": []}
    
    if key2 not in data2.get("ips", []):
        data2.setdefault("ips", []).append(key2)
        write_ip_json(data2)
        print(f"IP {key2} added to ips.json")
    else:
        print(f"IP {key2} already in ips.json")

    #write device name to devices.json 
    try:
        with open("../../data/devices.json") as json_file:
            data = json.load(json_file)
    except Exception:
        data = {"devices": []}

    if key.lower() not in [d.lower() for d in data.get("devices", [])]:
        data.setdefault("devices", []).append(key)
        write_name_json(data)
        print(f"Device {key} added to devices.json")
    else:
        print(f"Device {key} already in devices.json")

    #writes username to usernames.json
    try:
        with open("../../data/usernames.json") as json_file:
            data3 = json.load(json_file)
    except Exception:
        data3 = {"usernames": []}
    
    if key3 not in data3.get("usernames", []):
        data3.setdefault("usernames", []).append(key3)
        write_username_json(data3)
        print(f"Username {key3} added to usernames.json")
    else:
        print(f"Username {key3} already in usernames.json")

    #writes passwords to passwords.json
    try: 
        with open("../../data/passwords.json") as json_file:
            data4 = json.load(json_file)
    except Exception:
        data4 = {"passwords": []}

    data4.setdefault("passwords", []).append(key4)
    write_password_json(data4)
    print(f"Password {key4} added to passwords.json")
    
    #add the button to the ui with name
    create_device_button(name_raw)
    clear_entry_fields(device_name, ip_address, user)
    return key

#creates buttons on startup
def load_devices(filename="devices.json"):
    try:
        with open(filename) as f:
            data = json.load(f)
            for device in data.get("devices", []):
            
                create_device_button(device)
    except FileNotFoundError:
        print(f"{filename} not found; starting with no devices")
    except Exception as e:
        print(f"Error loading devices: {e}")

def add_device_window():

    add_device_win = ctk.CTkToplevel(window)
    add_device_win.title("Add Device")
    add_device_win.geometry("250x350")

    frame = ctk.CTkFrame(add_device_win, width=200, height=300, bg_color="transparent", fg_color="gray20", corner_radius=1)
    frame.pack(pady=10)
    frame.pack_propagate(False)
    frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    label = tk.Label(frame, text="  Add Device  ", font=("Arial", 16, "bold",), fg="white", bg="gray20",)
    label.pack(pady=20)
    label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

    #ip address entry field
    ip_address = ctk.CTkEntry(frame, placeholder_text="ip address", placeholder_text_color="gray50",corner_radius=5)
    ip_address.pack(pady=10)
    ip_address.place(relx=0.5, rely=0.37, anchor=tk.CENTER)

    #username entry field
    user = ctk.CTkEntry(frame, placeholder_text="username", placeholder_text_color="gray50",corner_radius=5)
    user.pack(pady=10)
    user.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    #device name entry field
    device_name = ctk.CTkEntry(frame, placeholder_text="device name", placeholder_text_color="gray50",corner_radius=5)
    device_name.pack(pady=10)
    device_name.place(relx=0.5, rely=0.24, anchor=tk.CENTER)

    password = ctk.CTkEntry(frame, placeholder_text="password", placeholder_text_color="gray50",corner_radius=5)
    password.pack(pady=10)
    password.place(relx=0.5, rely=0.63, anchor=tk.CENTER)

    #button to add device calls all the goyslop when clicked
    variable_button = ctk.CTkButton(frame, text="Add Device",font=("Arial", 13, "bold"), command=lambda: add_device_win.destroy() if use_variables(device_name, ip_address, user, frame, password) else None, bg_color="transparent", fg_color="royalblue", hover_color="royalblue4", corner_radius=5)
    variable_button.pack(pady=10)
    variable_button.place(relx=0.5, rely=0.76, anchor=tk.CENTER)


def main_window():

    #main frontend window
    global window
    window = ctk.CTk()
    window.title("Python SSH")
    window.geometry("650x450")

    #a placeholder frame to make the add device button look good ig
    add_device_placeholder_frame = ctk.CTkFrame(window, width=340, height=50, bg_color="transparent", fg_color="gray21", corner_radius=1)
    add_device_placeholder_frame.pack(pady=5)
    add_device_placeholder_frame.pack_propagate(False)
    
    #contains all device widgets and allows you to scroll if widgest exceed size of frame
    global device_container
    device_container = ctk.CTkScrollableFrame(window, fg_color="transparent", height=300, width=340)
    device_container.pack
    device_container.place(relx=0.229, rely=0.13)
    device_container._scrollbar.configure(width=11)

    #add device button
    add_device_placeholder_button = ctk.CTkButton(add_device_placeholder_frame, text="+", font=("Arial", 25, "bold"), height=30, width=30, command=add_device_window, bg_color="transparent", fg_color="royalblue", hover_color="royalblue4", corner_radius=5)
    add_device_placeholder_button.pack(pady=10)
    add_device_placeholder_button.place(relx=0.08, rely=0.5, anchor=tk.CENTER)

    #add device label
    add_device_placeholder_label = ctk.CTkLabel(add_device_placeholder_frame, text="Add Device", font=("Arial", 20, "bold"), fg_color="transparent", bg_color="transparent", text_color="white")
    add_device_placeholder_label.pack(pady=10)
    add_device_placeholder_label.place(relx=0.3, rely=0.5, anchor=tk.CENTER)

    load_devices()
    window.mainloop()

main_window()

