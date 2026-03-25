# Standard imports
import customtkinter as tk

# Local application imports
from app.pages.home import HomePage
from app.storage.user_data import UserDataDir
from app.storage.database import Database
from app.storage.icons import Icons

class App(tk.CTk):
    """Application root, responsible for root level actions."""
    def __init__(self):
        super().__init__()
        self.title("PySSH")
        self.geometry("800x600")
        self.lift()

        self.user_data_dir = UserDataDir()
        self.database = Database(self.user_data_dir)
        self.icons = Icons()

        self.container = tk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

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

        print(f"Switched page to {page_class.__name__}")


    def run(self):
        """Start the app."""
        self.mainloop()