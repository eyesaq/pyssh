import os
import json

# utility functions for the SSH GUI application

# writes device info to devices.json
def write_name_json(data, filename="devices.json"):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

# writes ip to ips.json
def write_ip_json(data2, filename="ips.json"):
    with open(filename, "w") as f:
        json.dump(data2, f, indent=4)

#writes usernames to usernames.json
def write_username_json(data3, filename="usernames.json"):
    with open(filename, "w") as f:
        json.dump(data3, f, indent=4)

#writes pwds to passwords.json
def write_password_json(data4, filename="passwords.json"):
    with open(filename, "w") as f:
        json.dump(data4, f, indent=4 )

