# Standard imports
from typing import Callable

# Local application imports
from app.dialogs.base_device_input import BaseDeviceInput

class AddDeviceDialog(BaseDeviceInput):
    def __init__(self, parent, app, on_connection_creation: Callable):
        self._parent = parent
        self._app = app
        self._on_connection_creation = on_connection_creation

        super().__init__(self._parent, self.save_device, 'Add Device')

    def save_device(self, ip_address, device_name, username, password):
        self._app.database.add_connection(ip_address, device_name, username, password)
        print(f"Saved connection: {device_name} @ {ip_address}")

        self._on_connection_creation(ip_address)
