import customtkinter as tk

class App(tk.CTk):
    """CTk root for the entire application"""
    def __init__(self):
        super().__init__()
        self.title("PySSH")

    def run(self):
        self.mainloop()
