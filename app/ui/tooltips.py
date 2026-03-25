import customtkinter as ctk

class CTkToolTip:
    def __init__(self, widget, text, delay=500):
        self.widget = widget
        self.text = text
        self.delay = delay
        self.tooltip_window = None
        self.after_id = None

        widget.bind("<Enter>", self.schedule)
        widget.bind("<Leave>", self.hide)

    def schedule(self, event=None):
        self.after_id = self.widget.after(self.delay, self.show)

    def show(self):
        if self.tooltip_window or not self.text:
            return

        x = self.widget.winfo_rootx() + self.widget.winfo_width() + 5
        y = self.widget.winfo_rooty() + 5

        self.tooltip_window = tw = ctk.CTkToplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.geometry(f"+{x}+{y}")

        label = ctk.CTkLabel(
            tw,
            text=self.text,
            fg_color="transparent",
            text_color="white",
            corner_radius=6,
            padx=8,
            pady=4
        )
        label.pack()

    def hide(self, event=None):
        if self.after_id:
            self.widget.after_cancel(self.after_id)
            self.after_id = None

        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None
