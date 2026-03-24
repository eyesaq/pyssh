# Standard imports
from typing import Callable

# Local application imports
from app.dialogs.base_device_input import BaseDeviceInput

class EditDeviceDialog(BaseDeviceInput):
    def __init__(self, parent, app, update_data: Callable):
        self._parent = parent
        self._app = app
        self._update_button_data = update_data

        self.old_state = self._app.database.get_connection_info_by_ip(self._parent.ip_address)

        defaults = {
            "ip_address": self.old_state[0],
            "device_name": self.old_state[1],
            "username": self.old_state[2],
            "password": self.old_state[3],
        }

        super().__init__(self._parent, self.edit_device, 'Edit Device', defaults=defaults)

    def edit_device(self, ip_address, device_name, username, password):
        self._app.database.update_connection_by_ip(self.old_state[0], ip_address, device_name, username, password)
        if ip_address != self.old_state[0]:
            self._update_button_data(new_ip=ip_address)
