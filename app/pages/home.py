# Standard imports
import customtkinter as ctk

# Local application imports
from app.dialogs.add_device import AddDeviceDialog
from app.ui.buttons.connection_button import ConnectionButton
from app.config import PING_LOG

class HomePage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self._app = app

        self._selected_index = None
        self._connection_buttons = []

        # -- Top banner --
        top_banner_frame = ctk.CTkFrame(self, width=340, height=50, bg_color="transparent", fg_color="gray21")
        top_banner_frame.pack(padx=5, pady=5, fill="x")
        top_banner_frame.pack_propagate(False)

        # -- Add device button --
        add_device_button = ctk.CTkButton(
            top_banner_frame, text="+", font=("Arial", 25, "bold"), command=self.on_add_device,
            bg_color="transparent", fg_color="royalblue", hover_color="royalblue4", corner_radius=5
        )
        add_device_button.place(relwidth=0.05, relheight=0.7, relx=0.01, rely=0.5, anchor='w')

        # -- Add device label --
        add_device_label = ctk.CTkLabel(
            top_banner_frame, text="Add Device", font=("Arial", 20, "bold"),
            fg_color="transparent", bg_color="transparent", text_color="white"
        )
        add_device_label.place(relx=0.07, rely=0.5, anchor='w')

        # -- Header label --
        header_label = ctk.CTkLabel(
            top_banner_frame, text="PySSH", font=("Roboto", 40, "bold"),
            fg_color="transparent", bg_color="transparent", text_color="white"
        )
        header_label.place(relx=0.95, rely=0.5, anchor='e')

        self.devices_scroll_frame = ctk.CTkScrollableFrame(self)
        self.devices_scroll_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # --- Default no device label ---
        self.no_devices_label = ctk.CTkLabel(
            self.devices_scroll_frame._parent_canvas,
            bg_color='transparent',
            text="No Devices",
            font=("Arial", 18, "bold"),
            text_color="gray60"
        )
        self._init_buttons()
        self._init_ux()

    def _init_ux(self):
        # --- Focus ---
        self.focus_set()

        # --- Add Device Shortcut ---
        self._app.bind("<a>", lambda e: self.on_add_device())
        self._app.bind("<A>", lambda e: self.on_add_device())

        # --- Connection button selection ---
        self._app.bind("<Up>", lambda e: self._move_selection(-1))
        self._app.bind("<Down>", lambda e: self._move_selection(1))

        # Mouse actions that should clear selection
        mouse_events = [
            "<Button-1>",  # left click
            "<Button-2>",  # middle click
            "<Button-3>",  # right click
            "<B1-Motion>",  # dragging
            "<ButtonRelease-1>",
        ]

        for ev in mouse_events:
            self._app.bind(ev, self._maybe_clear_selection, add="+")

    def _move_selection(self, direction):
        if not self._connection_buttons:
            return

        # Deselect old button
        if self._selected_index is not None:
            self._connection_buttons[self._selected_index].highlighted = False

        # Start at first button
        if self._selected_index is None:
            self._selected_index = 0
        else:
            # Loop back around
            self._selected_index = (self._selected_index + direction) % len(self._connection_buttons)

        btn = self._connection_buttons[self._selected_index]
        btn.highlighted = True
        btn.focus_set()

        # Smooth scroll
        self._scroll_into_view_smooth(btn)

    def _maybe_clear_selection(self, event):
        widget = event.widget

        # If click is on a ConnectionButton, let _on_button_click handle it
        if isinstance(widget, ConnectionButton):
            return

        # If click is inside a child of a ConnectionButton, also let _on_button_click handle it
        parent = widget
        while parent is not None:
            if isinstance(parent, ConnectionButton):
                return
            parent = getattr(parent, "master", None)

        # Otherwise clear selection
        if self._selected_index is not None:
            self._connection_buttons[self._selected_index].highlighted = False
            self._selected_index = None

    def _scroll_into_view_smooth(self, widget, steps=8):
        canvas = self.devices_scroll_frame._parent_canvas

        # Get widget and canvas positions
        widget_y = widget.winfo_rooty()
        canvas_y = canvas.winfo_rooty()
        canvas_h = canvas.winfo_height()

        # If widget is already fully visible, do nothing
        if canvas_y <= widget_y <= canvas_y + canvas_h - widget.winfo_height():
            return

        # Compute target scroll fraction
        bbox = canvas.bbox(widget)
        if not bbox:
            return
        target = bbox[1] / canvas.bbox("all")[3]

        # Smooth animation
        current = canvas.yview()[0]
        delta = (target - current) / steps

        def animate(i=0):
            if i < steps:
                canvas.yview_moveto(current + delta * i)
                canvas.after(10, lambda: animate(i + 1))

        animate()

    def _init_buttons(self):
        for ip_address in self._app.database.get_all_ip_addresses():
            self.create_connection_button(ip_address, ping_log=PING_LOG)
        self.update_no_device_label()

    def remove_connection_button(self, button):
        if button in self._connection_buttons:
            self._connection_buttons.remove(button)
            self.update_no_device_label()

    def update_no_device_label(self):
        if len(self._connection_buttons) == 0:
            self.no_devices_label.lift()  # Bring above scroll frame
            self.no_devices_label.place(relx=0.5, rely=0.5, anchor='center')
        else:
            self.no_devices_label.place_forget()

    def on_add_device(self):
        AddDeviceDialog(self, self._app, self.create_connection_button)

    def _on_button_click(self, button):
        # If nothing is selected, clicking a button clears nothing
        if self._selected_index is None:
            return

        # If this button is the selected one, keep selection
        if button.highlighted:
            return

        # Otherwise clicking a different button clears selection
        self._connection_buttons[self._selected_index].highlighted = False
        self._selected_index = None

    def create_connection_button(self, ip_address: str, ping_log=False):
        connection_button = ConnectionButton(
            self.devices_scroll_frame,
            self._app,
            ip_address,
            self.remove_connection_button,
            ping_log=ping_log
        )
        connection_button.pack(pady=5, fill="x", expand=True)
        connection_button.pack_propagate(False)

        connection_button.bind("<Button-1>", lambda e, b=connection_button: self._on_button_click(b))

        self._connection_buttons.append(connection_button)
        self.update_no_device_label()
