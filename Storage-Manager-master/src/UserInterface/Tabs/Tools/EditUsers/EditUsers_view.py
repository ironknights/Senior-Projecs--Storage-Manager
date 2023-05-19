"""Code written by Jacquesne Jones unless otherwise specified."""

from src.UserInterface.Windows.Window.window_controller import Gui
from src.UserInterface.Tabs.MainTab.MainTab_viewer import MainTabViewer


class EditUsersView(MainTabViewer):
    def __init__(self, window, key, tab_title):
        super().__init__(window, key, tab_title)

    def create_layout(self):
        layout = [Gui.T("NOT IMPLEMENTED")]
        return layout

    def create_tab(self):
        return Gui.Tab(self.title, [self.layout], key=self.key)
