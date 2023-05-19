"""Code written by Jacquesne Jones unless otherwise specified."""

from src.UserInterface.Tabs.MainTab.MainTab_controller import MainTabController
from src.UserInterface.Tabs.Tools.Tools_view import ToolsTabView

padding = 25


class Tools(MainTabController):
    def __init__(self, window, key="_TOOLS_", title=f"{' ' * padding}Tools{' ' * padding}"):
        super().__init__(window, key, ToolsTabView, title)
        self.load()

    def load(self):
        pass

    def process_event(self, event, values):
        pass

    def refresh(self):
        pass
