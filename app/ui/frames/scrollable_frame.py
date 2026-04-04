from customtkinter import CTkScrollableFrame

class ScrollableFrame(CTkScrollableFrame):
    @property
    def canvas(self):
        # Allow public access to a private attribute and centralise the risk of access.
        return self._parent_canvas
