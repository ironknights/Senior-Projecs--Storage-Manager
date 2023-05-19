"""Code written by Jacquesne Jones unless otherwise specified."""

from src.UserInterface.Windows.Window.window_controller import Gui, WindowController
from src.UserInterface.Tabs.MainTab.MainTab_viewer import MainTabViewer


class EditRulesView(MainTabViewer):
    def __init__(self, window, key, tab_title):
        # Check if this should be disabled
        self.disabled = True if WindowController.current_user.permission.edit_rules == 0 else False
        super().__init__(window, key, tab_title)

    def create_layout(self):
        sales_tax = self.window.database.BusinessRuleModel.get_rule("Sales Tax")
        due_day = self.window.database.BusinessRuleModel.get_rule("Due Day")
        late_day = self.window.database.BusinessRuleModel.get_rule("Late Day")
        lien_day = self.window.database.BusinessRuleModel.get_rule("Lien Day")

        layout = [[Gui.T(f"Sales Tax: "), Gui.I(sales_tax.value, key="_BR_SALES_TAX_", disabled=self.disabled)],
                  [Gui.T(f"Due Day: "), Gui.I(due_day.value, key="_BR_DUE_DAY_", disabled=self.disabled)],
                  [Gui.T(f"Late Day: "), Gui.I(late_day.value, key="_BR_LATE_DAY_", disabled=self.disabled)],
                  [Gui.T(f"Lien Day: "), Gui.I(lien_day.value, key="_BR_LIEN_DAY_", disabled=self.disabled)],
                  [Gui.B("Save", key="_BR_SAVE_CHANGES_", disabled=self.disabled)]]
        return layout

    def create_tab(self):
        return Gui.Tab(self.title, self.layout, key=self.key)
