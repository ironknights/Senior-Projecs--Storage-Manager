"""Code written by Jacquesne Jones unless otherwise specified."""

from abc import ABC, abstractmethod


class MainTabViewer(ABC):
    """Abstract base class for tab views."""
    def __init__(self, window, key, tab_title=None):
        if not tab_title:
            self.title = "NONE"
        else:
            self.title = tab_title
        self.window = window
        self.key = key
        self.layout = self.create_layout()
        self.tab = self.create_tab()

    @abstractmethod
    def create_layout(self):
        """Create the main tab layout and return it."""
        pass

    @abstractmethod
    def create_tab(self):
        """Create a new tab object for the window and return it."""
        pass
