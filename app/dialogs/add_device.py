# Standard imports
from typing import Callable

# Local application imports
from app.dialogs.base_device_input import BaseDeviceInput

class AddDeviceDialog(BaseDeviceInput):
    def __init__(self, parent, app, on_connection_creation: Callable):
        super().__init__(parent, self.save_device, 'Add Device')
        self._app = app
        self._on_connection_creation = on_connection_creation

    def save_device(self, ip_address, device_name, username, password):
        if self._app.database.ip_exists(ip_address):
            print(f"IP address '{ip_address}' is already assigned to another device")
            self.raise_validation_error(self.ip_address_entry,"IP already exists in database")
        else:
            self._app.database.add_connection(ip_address, device_name, username, password)
            print(f"Saved connection: '{device_name}'@'{ip_address}'")
            self._on_connection_creation(ip_address)
            self.destroy()
