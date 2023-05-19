"""Code written by Jacquesne Jones unless otherwise specified."""

from src.UserInterface.Tabs.MainTab.MainTab_controller import MainTabController
from src.UserInterface.Tabs.Tools.EditRules.EditRules_view import EditRulesView


class EditRules(MainTabController):
    def __init__(self, window, key="_EDIT_RULES_", title="Edit Rules"):
        super().__init__(window, key, EditRulesView, title)

    def load(self):
        pass

    def process_event(self, event, values):
        if event == "_BR_SAVE_CHANGES_":
            self.save_changes(values)

    def save_changes(self, values):
        """Saves all values to their current state"""
        items = [
            ("_BR_SALES_TAX_", "Sales Tax"),
            ("_BR_DUE_DAY_", "Due Day"),
            ("_BR_LATE_DAY_", "Late Day"),
            ("_BR_LIEN_DAY_", "Lien Day"),
        ]
        # Go ahead and change all values since the list is short, no need to store previous values
        for key, value in items:
            self.window.database.BusinessRuleModel.get_rule(value).value = values[key]
        self.window.database.session.commit()

    def refresh(self):
        pass
