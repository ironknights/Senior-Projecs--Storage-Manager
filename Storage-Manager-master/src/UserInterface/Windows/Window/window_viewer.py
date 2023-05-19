"""Code written by Jacquesne Jones unless otherwise specified."""

from abc import ABC, abstractmethod


class WindowViewer(ABC):

    def __init__(self, controller, window_title):
        self.controller = controller
        self.database = controller.database
        if not window_title:
            self.title = ""
        else:
            self.title = window_title
        self.layout = self.create_layout()
        self.window = self.create_window()

    @abstractmethod
    def create_layout(self):
        """Create the main window layout and return it."""
        pass

    @abstractmethod
    def create_window(self):
        """Create a new window object for the main window and return it."""
        pass
