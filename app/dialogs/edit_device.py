# Standard imports
from typing import Callable

# Local application imports
from app.dialogs.base_device_input import BaseDeviceInput

class EditDeviceDialog(BaseDeviceInput):
    def __init__(self, parent, app, ip_address):
        self._parent = parent
        self._app = app

        self.old_state = self._app.database.get_device_info_by_ip(ip_address)

        defaults = {
            "ip_address": self.old_state[0],
            "device_name": self.old_state[1],
            "username": self.old_state[2],
            "password": self.old_state[3],
        }

        super().__init__(self._parent, self._app.database.update_device_by_ip, 'Edit Device', defaults=defaults)
