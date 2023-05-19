"""Code written by Deeptanshu Das unless otherwise specified."""

from src.UserInterface.Tabs.MainTab.MainTab_controller import MainTabController
from src.UserInterface.Tabs.Maps.Maps_viewer import MapsView
from src.UserInterface.Windows.Lookup.Lookup_controller import LookupWindow

padding = 25


class Maps(MainTabController):
    """Maps controller class"""
    def __init__(self, window, key="_MAPS_", title=f"{' ' * padding}Maps{' ' * padding}"):
        super().__init__(window, key, MapsView, title)
       # self.load()

    def load(self):
        """Loads the draw_all_units and draw_all_lines methods"""

        self.view.draw_all_units()
        self.view.draw_all_lines()

    def process_event(self, event, values):
        """Processes the events"""
        pass

    @staticmethod
    def make_vertical(title):
        """Making the tabs"""
        new_title = ""
        for letter in title:
            new_title += f"{letter}\n"
        return new_title

    def refresh(self):
        """Refreshes all windows and tabs"""
        # if data changed on back-end what will happen on the operations
        pass



