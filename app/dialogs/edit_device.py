# Standard imports
from typing import Callable

# Local application imports
from app.dialogs.base_device_input import BaseDeviceInput

class EditDeviceDialog(BaseDeviceInput):
    def __init__(self, parent, app, on_edit: Callable, get_ip_address: Callable, set_ip_address: Callable):
        self._parent = parent
        self._app = app
        self._on_edit = on_edit
        self._get_ip_address = get_ip_address
        self._set_ip_address = set_ip_address

        self.old_state = self._app.database.get_connection_info_by_ip(self._get_ip_address())

        defaults = {
            "ip_address": self.old_state[0],
            "device_name": self.old_state[1],
            "username": self.old_state[2],
            "password": self.old_state[3],
        }

        super().__init__(self._parent, self.edit_device, 'Edit Device', defaults=defaults)

    def edit_device(self, ip_address, device_name, username, password):
        new_state = (ip_address, device_name, username, password)
        if new_state == self.old_state:
            self.destroy()
            return

        self._app.database.update_connection_by_ip(
            self.old_state[0], ip_address, device_name, username, password
        )
        self._set_ip_address(ip_address)
        self._on_edit()
        self.destroy()
