# Standard imports
import customtkinter as tk

# Local application imports
from app.pages.home import HomePage
from app.services.user_data import UserData

class App(tk.CTk):
    """Application root, responsible for root level actions."""
    def __init__(self):
        super().__init__()
        self.title("PySSH")
        self.geometry("800x600")

        self.user_data = UserData()

        self.container = tk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)

        self.pages = {}
        self.show_page(HomePage)

    def show_page(self, page_class):
        """Change between pages."""
        # If the page hasn't been opened, initialize it.
        if page_class not in self.pages:
            page = page_class(self.container, self)
            self.pages[page_class] = page
            page.grid(row=0, column=0, sticky="nsew")

        # Display the page.
        self.pages[page_class].tkraise()


    def run(self):
        """Start the app."""
        self.mainloop()
