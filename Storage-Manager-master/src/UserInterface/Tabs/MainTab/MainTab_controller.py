"""Code written by Jacquesne Jones unless otherwise specified."""

from abc import ABC, abstractmethod


class MainTabController(ABC):
    """Abstract base class for tabs."""
    def __init__(self, window, key, view_type, tab_title=None):
        self.view = view_type(window, key, tab_title)
        self.layout = self.view.layout
        self.tab = self.view.tab
        self.key = key
        self.window = window

    def run(self, event, values):
        """Tab run simply runs the process event function via the window."""
        self.process_event(event, values)

    def open(self, new_window):
        """Opens a new window."""
        self.window.open(new_window)

    def refresh_all(self):
        """Refreshes all windows and tabs."""
        self.window.refresh_all()

    def popup(self, message, options=None, title=None):
        """Creates a popup message and returns the result."""
        return self.window.popup(message, options, title)

    @abstractmethod
    def load(self):
        """Load runs after the window is finalized so you can update and use drawing functions at this point."""
        pass

    @abstractmethod
    def process_event(self, event, values):
        """Processes any events for the tab."""
        pass

    @abstractmethod
    def refresh(self):
        """Contains all update code for the tab."""
        pass
