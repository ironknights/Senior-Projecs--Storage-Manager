"""Code written by Jacquesne Jones unless otherwise specified."""

from src.UserInterface.Windows.Window.window_controller import Gui
from src.UserInterface.Tabs.MainTab.MainTab_viewer import MainTabViewer
from src.UserInterface.Tabs.Tools.Settings.Settings_controller import Settings
from src.UserInterface.Tabs.Tools.EditReports.EditReports_controller import EditReports
from src.UserInterface.Tabs.Tools.EditUsers.EditUsers_controller import EditUsers
from src.UserInterface.Tabs.Tools.EditUnits.EditUnits_controller import EditUnits
from src.UserInterface.Tabs.Tools.EditRules.EditRules_controller import EditRules


class ToolsTabView(MainTabViewer):
    def __init__(self, window, key, tab_title):
        super().__init__(window, key, tab_title)

    def create_layout(self):
        self.window.add_tab("Settings", Settings)
        self.window.add_tab("EditReports", EditReports)
        self.window.add_tab("EditUsers", EditUsers)
        self.window.add_tab("EditUnits", EditUnits)
        self.window.add_tab("EditRules", EditRules)
        layout = [Gui.Column([[Gui.TabGroup([[
            self.window.tabs["Settings"].tab,
            self.window.tabs["EditReports"].tab,
            self.window.tabs["EditUsers"].tab,
            self.window.tabs["EditUnits"].tab,
            self.window.tabs["EditRules"].tab,
        ]])]])]
        return layout

    def create_tab(self):
        return Gui.Tab(self.title, [self.layout], key=self.key)
