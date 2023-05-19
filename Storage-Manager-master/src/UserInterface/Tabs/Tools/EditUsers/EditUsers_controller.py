"""Code written by Jacquesne Jones unless otherwise specified."""

from src.UserInterface.Tabs.MainTab.MainTab_controller import MainTabController
from src.UserInterface.Tabs.Tools.EditUsers.EditUsers_view import EditUsersView


class EditUsers(MainTabController):
    def __init__(self, window, key="_EDIT_USERS_", title="Edit Users"):
        super().__init__(window, key, EditUsersView, title)

    def load(self):
        pass

    def process_event(self, event, values):
        pass

    def refresh(self):
        pass
