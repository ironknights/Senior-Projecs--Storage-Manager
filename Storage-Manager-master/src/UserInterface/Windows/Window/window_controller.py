"""Code written by Jacquesne Jones unless otherwise specified."""

from src.ErrorHandling import error as Err
import PySimpleGUI as Gui
from abc import ABC, abstractmethod

GLOBAL_TIMEOUT = 100    # TODO: Consider threading if delays occur


def error(msg):
    Gui.PopupError(msg)


# Abstract base class for windows that allow creation of new windows while open
class WindowController(ABC):
    open_windows = []
    DB = None
    current_user = None

    def __init__(self, view, title, database=None):
        if database:
            WindowController.DB = database
        elif not database and not WindowController.DB:  # Check if trying to load without initialization
            raise Err.NoDatabaseLoaded
        self.database = WindowController.DB
        self.tabs = None
        self.view = view(self, window_title=title)
        self.window = self.view.window

    def run(self):
        """Reads the window and processes all events for the window and any tabs

        :return Returns the result of the process_event function for the window as a whole"""
        if self.window:
            event, values = self.window.read(timeout=GLOBAL_TIMEOUT)
            if self.tabs:
                for tab in self.tabs.values():
                    tab.process_event(event, values)
            return self.process_event(event, values)
        else:
            raise Err.NoWindowObject

    def add_tab(self, name, tab_type):
        """Adds a new tab to the window"""
        if not self.tabs:
            self.tabs = {}
        self.tabs[name] = tab_type(self)

    def load_tabs(self):
        """Runs all tab load functions"""
        for tab in self.tabs.values():
            tab.load()

    def reload(self):
        """Creates a new window over the old one and closes the old one"""
        location = self.view.window.CurrentLocation()
        size = self.view.window.Size
        self.view.layout = self.view.create_layout()
        new_window = Gui.Window(self.view.title, self.view.layout,
                                location=location, size=size)
        new_window.Finalize()
        self.view.window.Close()
        self.view.window = new_window
        self.window = self.view.window

    @staticmethod
    def open(new_window):
        """Opens a new window and adds it to the running list of windows"""
        WindowController.open_windows.append(new_window)

    @staticmethod
    def refresh_all():
        """Refreshes all windows and tabs that are currently running, updating their data

        The intent is to always call this function whenever a change to the database occurs to make sure
        existing windows have up-to-date information for the user"""
        for window in WindowController.open_windows:
            if window.tabs:
                for tab in window.tabs:
                    tab.refresh()
            window.refresh()

    @staticmethod
    def popup(message, options=None, title=None):
        """Creates a simple popup window for the user"""
        if not options:
            options = ["Yes", "No"]
        buttons = []
        for button in options:
            buttons.append(Gui.B(button))
        layout = [
            [Gui.T(message)],
            buttons
        ]
        if not title:
            title = "Notice"
        window = Gui.Window(title, layout)
        event, values = window.read()
        window.close()
        return event

    @abstractmethod
    def load(self):
        """Loads any initial data for the window and is called manually.

        This function is not automatically called and can be moved depending on the implementation."""
        pass

    @abstractmethod
    def process_event(self, event, values):
        """Processes the return values from a read call."""
        pass

    @abstractmethod
    def refresh(self):
        """Updates all values on the window that can be changed that are dependent on the database."""
        pass

    @abstractmethod
    def shutdown(self):
        """Runs any necessary functions to safely shut down the window."""
        pass
