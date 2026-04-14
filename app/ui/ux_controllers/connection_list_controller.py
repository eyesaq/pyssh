# Local application imports
from app.ui.buttons.connection_button import ConnectionButton

class ConnectionListController:
    def __init__(self, app, home_page):
        self._app = app
        self._home = home_page

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
        btn = self.currently_selected_button
        if btn is None:
            return

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
    @property
    def currently_selected_button_index(self):
        for index, button in enumerate(self._home.connection_buttons):
            if button.highlighted:
                return index
        return None

    @property
    def currently_selected_button(self):
        for button in self._home.connection_buttons:
            if button.highlighted:
                return button
        return None

    def select_button(self, index):
        self.clear_selection()

        btn = self._home.connection_buttons[index]
        btn.highlighted = True
        btn.focus_set()
        self._home.scroll_into_view(btn)

    def move_selection(self, increment_value: int):
        buttons = self._home.connection_buttons
        if not buttons:
            return

        # Deselect old selection
        previous_selection = self.currently_selected_button_index
        self.clear_selection()

        # Compute new index
        if previous_selection is None:
            target_index = 0
        else:
            target_index = (previous_selection + increment_value) % len(buttons)

        self.select_button(target_index)

    def clear_selection(self):
        selected_button = self.currently_selected_button
        if selected_button:
            selected_button.highlighted = False

    def on_connection_button_click(self, button):
        if self.currently_selected_button is None:
            return

        if button.highlighted:
            return

        self.clear_selection()

    # ---------------------------
    # State synchronisation
    # ---------------------------
    def on_connection_button_removed(self, button):
        buttons = self._home.connection_buttons

        # Deselect old selection
        previous_selection = self.currently_selected_button_index
        self.clear_selection()

        if previous_selection is not None and len(buttons) > 1:
            if button is buttons[previous_selection]:
                if previous_selection == 0:
                    self.select_button(1)

                # Select one button up if a button in the middle is deleted.
                else:
                    self.select_button(previous_selection - 1)
