"""Code written by Jacquesne Jones unless otherwise specified."""

from src.UserInterface.Tabs.MainTab.MainTab_controller import MainTabController
from src.UserInterface.Tabs.Tools.EditUnits.EditUnits_view import EditUnitsView


class EditUnits(MainTabController):
    def __init__(self, window, key="_EDIT_UNITS_", title="Edit Units"):
        super().__init__(window, key, EditUnitsView, title)

    def load(self):
        pass

    def process_event(self, event, values):
        pass

    def refresh(self):
        pass
