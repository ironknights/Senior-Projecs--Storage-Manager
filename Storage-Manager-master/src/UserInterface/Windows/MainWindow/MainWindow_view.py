"""Code written by Jacquesne Jones unless otherwise specified."""

from src.UserInterface.Windows.Window.window_controller import Gui
from src.DatabaseModel.format import state_list
from src.UserInterface.Windows.Window.window_viewer import WindowViewer
from src.UserInterface.Tabs.Operations.Operations_controller import Operations
from src.UserInterface.Tabs.Tools.Tools_controller import Tools
from src.UserInterface.Tabs.Reports.Reports_Controller import Reports
from src.UserInterface.Tabs.Maps.Maps_Controller import Maps


class MainWindowView(WindowViewer):
    def __init__(self, controller, window_title=None):
        if not window_title:
            self.title = "SOLO Storage Manager"
        else:
            self.title = window_title
        self.tabs = controller.tabs
        super().__init__(controller, self.title)

    def create_layout(self):
        top_menu = self.create_menu()
        self.controller.add_tab("Operations", Operations)
        self.controller.add_tab("Reports", Reports)
        self.controller.add_tab("Tools", Tools)
        self.controller.add_tab("Maps", Maps)
        layout = [
            [Gui.MenuBar(top_menu)],
            [Gui.TabGroup([[
                self.controller.tabs["Operations"].tab,
                self.controller.tabs["Reports"].tab,
                self.controller.tabs["Tools"].tab,
                self.controller.tabs["Maps"].tab,
            ]], tab_location="top", key="_TG_MAIN_")]
        ]
        return layout

    def create_window(self):
        return Gui.Window(self.title, self.layout, margins=(20, 20), resizable=True)

    @staticmethod
    def create_menu():
        """Generates the layout for the top bar menu"""
        layout = [
            ["&File", ["&Quit::_FILE_"]],
            ["&Debug", ["Add &Unit::_DEBUG_", "Add &Tenant::_DEBUG_", "Add U&ser::_DEBUG_",
                        "Add T&ransaction::_DEBUG_", "Add &History::_DEBUG_", "&WIPE DB::_DEBUG_"]]
        ]
        return layout

    def debug_add_unit_popup(self):
        """Debug popup to add a new unit"""
        sizes = self.database.UnitModel.get_sizes()
        layout = [
            [Gui.T("Name:", size=(6, 1)), Gui.In(key="_IDENTIFIER_")],
            [Gui.T("Size:", size=(6, 1)), Gui.Combo(self.database.UnitModel.list_sizes(), size=(43, 1), key="_SIZE_")],
            [Gui.T("Tenant ID:", size=(6, 1)), Gui.In(key="_TENANT_")],
            [Gui.Submit(), Gui.Cancel()]
        ]
        window = Gui.Window("Add New Unit", layout)
        event, values = window.read()
        if event in (None, "Cancel"):
            window.close()
            return None, None
        else:
            window.close()
            size_id = sizes[values["_SIZE_"]]
            return values, size_id

    @staticmethod
    def debug_add_tenant_popup():
        """Debug popup to add a new tenant"""
        layout = [
            [Gui.T("SSN:", size=(10, 1)), Gui.In(key="_SSN_")],
            [Gui.T("Last Name:", size=(10, 1)), Gui.In(key="_LNAME_")],
            [Gui.T("First Name:", size=(10, 1)), Gui.In(key="_FNAME_")],
            [Gui.T("Middle Name:", size=(10, 1)), Gui.In(key="_MNAME_")],
            [Gui.T("Address:", size=(10, 1)), Gui.In(key="_ADDR1_")],
            [Gui.T("Address 2:", size=(10, 1)), Gui.In(key="_ADDR2_")],
            [Gui.T("City:", size=(10, 1)), Gui.In(key="_CITY_")],
            [Gui.T("State:", size=(10, 1)), Gui.Combo(state_list(), size=(5, 1), key="_STATE_")],
            [Gui.T("Zip Code:", size=(10, 1)), Gui.In(key="_ZIP_")],
            [Gui.T("Phone:", size=(10, 1)), Gui.In(key="_PHONE_")],
            [Gui.T("Email:", size=(10, 1)), Gui.In(key="_EMAIL_")],
            [Gui.Submit(), Gui.Cancel()]
        ]
        window = Gui.Window("Add New Tenant", layout)
        event, values = window.read()
        if event in (None, "Cancel"):
            window.close()
            return None
        else:
            window.close()
            return values

    def debug_add_transaction_popup(self):
        """Debug popup to add a new tenant"""
        categories = self.database.TransactionModel.get_category_list()
        category_list = []
        for category in categories:
            category_list.append(category.category)
        layout = [
            [Gui.T("Amount:", size=(10, 1)), Gui.In(key="_AMOUNT_")],
            [Gui.T("Unit_ID:", size=(10, 1)), Gui.In(key="_UNIT_")],
            [Gui.T("Tenant_ID:", size=(10, 1)), Gui.In(key="_TENANT_")],
            [Gui.T("Category:", size=(10, 1)), Gui.Combo(category_list, key="_CATEGORY_")],
            [Gui.Submit(), Gui.Cancel()]
        ]
        window = Gui.Window("Add New Transaction", layout)
        event, values = window.read()
        if event in (None, "Cancel"):
            window.close()
            return None
        else:
            window.close()
            return values

    def debug_add_history_popup(self):
        """Debug popup to add a new tenant"""
        categories = self.database.UnitHistoryModel.get_category_list()
        category_list = []
        for category in categories:
            category_list.append(category.category)
        layout = [
            [Gui.T("Field:", size=(10, 1)), Gui.In(key="_FIELD_")],
            [Gui.T("New Value:", size=(10, 1)), Gui.In(key="_NEW_VALUE_")],
            [Gui.T("Old Value:", size=(10, 1)), Gui.In(key="_OLD_VALUE_")],
            [Gui.T("ID:", size=(10, 1)), Gui.In(key="_ID_")],
            [Gui.T("Type:", size=(10, 1)), Gui.Combo(["Unit", "Tenant"],
                                                     default_value="Unit", key="_TYPE_")],
            [Gui.T("Category:", size=(10, 1)), Gui.Combo(category_list, key="_CATEGORY_")],
            [Gui.Submit(), Gui.Cancel()]
        ]
        window = Gui.Window("Add New Transaction", layout)
        event, values = window.read()
        if event in (None, "Cancel"):
            window.close()
            return None
        else:
            window.close()
            return values

    @staticmethod
    def confirm_popup(msg):
        """Creates a confirmation popup window.

                :return: True if confirmed, false otherwise."""
        layout = [
            [Gui.T(msg)],
            [Gui.B("Confirm"), Gui.Cancel()]
        ]
        window = Gui.Window("Are you sure?", layout)
        event, values = window.read()
        if event == "Confirm":
            window.close()
            return True
        else:
            window.close()
            return False
