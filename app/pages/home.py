# Standard imports
import customtkinter as ctk

# Local application imports
from app.dialogs.add_device import AddDeviceDialog
from app.ui.buttons.connection_button import ConnectionButton
from app.config import PING_LOG
from app.ui.ux_controllers.connection_list_controller import ConnectionListController


class HomePage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self._app = app

        # List of ConnectionButton widgets
        self.connection_buttons = []

        top_banner_frame = ctk.CTkFrame(
            self, width=340, height=50,
            bg_color="transparent", fg_color="gray21"
        )
        top_banner_frame.pack(padx=5, pady=5, fill="x")
        top_banner_frame.pack_propagate(False)

        left_banner_container = ctk.CTkFrame(
            top_banner_frame,
            fg_color="transparent",
            bg_color="transparent"
        )
        left_banner_container.place(x=10, y=1) 

        add_device_icon = self._app.icons.add_button
        w, h = add_device_icon.cget("size")

        add_device_button = ctk.CTkButton(
            left_banner_container,
            text="",
            image=add_device_icon,
            fg_color="transparent",
            hover_color="gray20",
            width=w,
            height=h,
            command=self.on_add_device
        )
        add_device_button.pack(side="left", padx=(0, 8))

        add_device_label = ctk.CTkLabel(
            left_banner_container,
            text="Add Device",
            font=("Arial", 20, "bold"),
            text_color="white",
            fg_color="transparent"
        )
        add_device_label.pack(side="left")

        header_label = ctk.CTkLabel(
            top_banner_frame,
            text="PySSH",
            font=("Roboto", 40, "bold"),
            text_color="white",
            fg_color="transparent"
        )
        header_label.place(x=-10, rely=0.5, relx=1.0, anchor="e")

        self.devices_scroll_frame = ctk.CTkScrollableFrame(self)
        self.devices_scroll_frame.pack(
            padx=10, pady=10, fill="both", expand=True
        )

        # No devices label
        self.no_devices_label = ctk.CTkLabel(
            self.devices_scroll_frame._parent_canvas,
            bg_color='transparent',
            text="No Devices",
            font=("Arial", 18, "bold"),
            text_color="gray60"
        )

        # Load existing devices
        self._init_buttons()

        # Attach UX controller
        self.ux_controller = ConnectionListController(app, self)

    # ---------------------------------------------------------
    # GUI Commands
    # ---------------------------------------------------------

    def scroll_into_view(self, widget):
        """Smooth scroll animation (controller calls this)."""
        canvas = self.devices_scroll_frame._parent_canvas

        widget_y = widget.winfo_rooty()
        canvas_y = canvas.winfo_rooty()
        canvas_h = canvas.winfo_height()

        if canvas_y <= widget_y <= canvas_y + canvas_h - widget.winfo_height():
            return

        bbox = canvas.bbox(widget)
        if not bbox:
            return

        target = bbox[1] / canvas.bbox("all")[3]
        current = canvas.yview()[0]
        delta = (target - current) / 8

        def animate(i=0):
            if i < 8:
                canvas.yview_moveto(current + delta * i)
                canvas.after(10, lambda: animate(i + 1))

        animate()

    # ---------------------------------------------------------
    # Device management
    # ---------------------------------------------------------

    def _init_buttons(self):
        for ip_address in self._app.database.get_all_ip_addresses():
            self.create_connection_button(ip_address, ping_log=PING_LOG)
        self.update_no_device_label()

    def create_connection_button(self, ip_address: str, ping_log=False):
        btn = ConnectionButton(
            self.devices_scroll_frame,
            self._app,
            ip_address,
            self.remove_connection_button,
            ping_log=ping_log
        )
        btn.pack(pady=5, fill="x", expand=True)
        btn.pack_propagate(False)

        # Controller handles click behavior
        btn.bind("<Button-1>", lambda e, b=btn: self.ux_controller.on_button_click(b))

        self.connection_buttons.append(btn)
        self.update_no_device_label()

    def remove_connection_button(self, button):
        if button in self.connection_buttons:
            self.connection_buttons.remove(button)
            self.update_no_device_label()

    def update_no_device_label(self):
        if len(self.connection_buttons) == 0:
            self.no_devices_label.lift()
            self.no_devices_label.place(relx=0.5, rely=0.5, anchor='center')
        else:
            self.no_devices_label.place_forget()

    # ---------------------------------------------------------
    # Dialogs
    # ---------------------------------------------------------

    def on_add_device(self):
        AddDeviceDialog(self, self._app, self.create_connection_button)

