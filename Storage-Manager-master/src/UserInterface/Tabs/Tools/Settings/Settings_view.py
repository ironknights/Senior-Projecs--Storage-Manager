"""Code written by Jacquesne Jones unless otherwise specified."""

from src.UserInterface.Windows.Window.window_controller import Gui
from src.UserInterface.Tabs.MainTab.MainTab_viewer import MainTabViewer
from src.UserInterface.Windows.Window.window_controller import WindowController


class SettingsTabView(MainTabViewer):
    def __init__(self, window, key, tab_title):
        super().__init__(window, key, tab_title)

    def create_layout(self):
        user = WindowController.current_user.user_id
        default_tab = WindowController.current_user.default_tab
        website = self.window.database.BusinessRuleModel.get_rule("Website").value
        layout = [
            [Gui.T("Current User: "), Gui.T(f"{user}")],
            [Gui.T("Default Tab on Load: "),
             Gui.Combo(["Operations", "Reports"], default_value=default_tab, key="_DEFAULT_TAB_"),
             Gui.B("Save", key="_SAVE_DEFAULT_TAB_")],
            [Gui.T("Website: "), Gui.I(default_text=website, key="_WEBSITE_"),
             Gui.B("Save", key="_SAVE_WEBSITE_")],
            [Gui.T("Printer Settings: "), Gui.B("Open", key="_PRINT_SETTINGS_")],
            [Gui.T("Gate Settings: "), Gui.B("Open", key="_GATE_SETTINGS_")]
        ]
        return layout

    def create_tab(self):
        return Gui.Tab(self.title, self.layout, key=self.key)
