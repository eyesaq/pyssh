# Local application imports
from app.ui.buttons.connection_button import ConnectionButton

class ConnectionListController:
    def __init__(self, app, home_page):
        self._app = app
        self._home = home_page

        self._selected_index = None

        self._bind_keyboard()
        self._bind_mouse()

    # ---------------------------
    # Keyboard bindings
    # ---------------------------
    def _bind_keyboard(self):
        # --- Change selection ---
        self._app.bind("<Up>", lambda e: self.move_selection(-1))
        self._app.bind("<Down>", lambda e: self.move_selection(1))

        # --- Add Device shortcut ---
        self._app.bind("<a>", lambda e: self._home.on_add_device())
        self._app.bind("<A>", lambda e: self._home.on_add_device())

    def _invoke(self, action):
        if self._selected_index is None:
            return

        btn = self._home.connection_buttons[self._selected_index]

        if action == "edit":
            btn.edit_connection_button.invoke()
        elif action == "delete":
            btn.delete_connection_button.invoke()
        elif action == "menu":
            btn.menu_button.invoke()

    # ---------------------------
    # Mouse bindings
    # ---------------------------
    def _bind_mouse(self):
        mouse_events = [
            "<Button-1>",
            "<Button-2>",
            "<Button-3>",
            "<B1-Motion>",
            "<ButtonRelease-1>",
        ]

        for ev in mouse_events:
            self._app.bind(ev, self._handle_click_outside_selection, add="+")

    def _handle_click_outside_selection(self, event):
        widget = event.widget

        # Ignore clicks on buttons or their children
        parent = widget
        while parent is not None:
            if isinstance(parent, ConnectionButton):
                return
            parent = getattr(parent, "master", None)

        self.clear_selection()

    # ---------------------------
    # Selection logic
    # ---------------------------
    def move_selection(self, direction):
        buttons = self._home.connection_buttons
        if not buttons:
            return

        # Unhighlight old
        if self._selected_index is not None:
            buttons[self._selected_index].highlighted = False

        # Compute new index
        if self._selected_index is None:
            self._selected_index = 0
        else:
            self._selected_index = (self._selected_index + direction) % len(buttons)

        btn = buttons[self._selected_index]
        btn.highlighted = True
        btn.focus_set()

        self._home.scroll_into_view(btn)

    def clear_selection(self):
        if self._selected_index is not None:
            self._home.connection_buttons[self._selected_index].highlighted = False
            self._selected_index = None

    def on_button_click(self, button):
        if self._selected_index is None:
            return

        if button.highlighted:
            return

        self.clear_selection()
