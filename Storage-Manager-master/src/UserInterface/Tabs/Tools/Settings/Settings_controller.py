"""Code written by Jacquesne Jones unless otherwise specified."""

from src.UserInterface.Tabs.MainTab.MainTab_controller import MainTabController
from src.UserInterface.Tabs.Tools.Settings.Settings_view import SettingsTabView
from src.UserInterface.Windows.Window.window_controller import WindowController


class Settings(MainTabController):
    def __init__(self, window, key="_SETTINGS_", title="Settings"):
        super().__init__(window, key, SettingsTabView, title)

    def load(self):
        pass

    def process_event(self, event, values):
        if event == "_SAVE_DEFAULT_TAB_":
            self.save_tab(values["_DEFAULT_TAB_"])
        if event == "_SAVE_WEBSITE_":
            self.save_website(values["_WEBSITE_"])

    def refresh(self):
        pass

    def save_tab(self, tab):
        """Saves the new default tab setting to the database"""
        user = WindowController.current_user
        current_default = user.default_tab
        if tab != current_default:
            user.default_tab = tab
            self.window.database.session.commit()

    def save_website(self, website):
        """Saves the new website value to the database"""
        old_website = self.window.database.BusinessRuleModel.get_rule("Website")
        if old_website.value != website:
            old_website.value = website
            self.window.database.session.commit()
