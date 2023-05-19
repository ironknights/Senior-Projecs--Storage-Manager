"""Code written by Jacquesne Jones unless otherwise specified."""

from src.UserInterface.Windows.Window.window_controller import WindowController, Gui
from src.UserInterface.Windows.Lookup.Lookup_view import LookupWindowView
from src.UserInterface.Windows.Details.Details_controller import DetailsWindow
from src.UserInterface.Windows.Links.Links_controller import LinkWindow
from src.UserInterface.Windows.MoveIn.MoveIn_controller import MoveIn
from src.UserInterface.Windows.Payment.Payment_controller import PaymentWindow


class LookupWindow(WindowController):
    """Opens a window that shows a list of all units or tenants, or a filtered move in list."""
    def __init__(self, lookup_type, filters=None):
        self.lookup = lookup_type
        super().__init__(LookupWindowView, "Lookup")
        self.window_filters = filters if filters else ""
        self.search = ""
        self.filter = "All" if lookup_type == "units" else None
        self.load()

    def load(self):
        # Load finalizes the window to set default filters and update
        self.window.Finalize()
        self.view.table_contents = self.__filter(
            {"_SEARCH_": "", "_FILTER_": "All"})
        self.window["_TABLE_"](self.view.table_contents)

    def process_event(self, event, values):
        if not event:
            return self.shutdown()
        if event in ("_TABLE_", "Details") and values["_TABLE_"]:
            key = self.view.table_contents[values["_TABLE_"][0]][0]
            self.open(DetailsWindow(self, self.view.table_type, key))
        elif event == "Edit" and values["_TABLE_"]:
            key = self.view.table_contents[values["_TABLE_"][0]][0]
            self.open(DetailsWindow(self, self.view.table_type, key, edit=True))
        elif event == "Link/Unlink" and values["_TABLE_"]:
            key = self.view.table_contents[values["_TABLE_"][0]][0]
            self.open(LinkWindow(self, key))
        # -------------------------------------------------------------------------------------
        # This section coded by Emerson Havener
        elif event == "Select" and values["_TABLE_"]:
            selectedIndex = self.view.table_contents[values["_TABLE_"][0]][0]
            unit = self.database.UnitModel.get(selectedIndex)
            self.open(MoveIn(unit))
            return self.shutdown()

        elif event == "Make Payment" and values["_TABLE_"]:
            selectedIndex = self.window.read()[1]["_TABLE_"][0] + 1
            print('selected index', selectedIndex)
            tenant = self.database.TenantModel.get(selectedIndex)
            transactions = self.database.TransactionModel.get_by_tenant(
                selectedIndex)
            histories = self.database.TenantHistoryModel.get_by_tenant(
                selectedIndex)
            self.open(PaymentWindow(tenant, transactions, histories))
            return self.shutdown()
        elif event == "Make Payment " and values["_TABLE_"]:
            selectedIndex = self.window.read()[1]["_TABLE_"][0] + 1
            print('selected index', selectedIndex)
            unit = self.database.UnitModel.get(selectedIndex)
            tenant = unit.tenant
            transactions = self.database.TransactionModel.get_by_tenant(
                tenant.id)
            histories = self.database.TenantHistoryModel.get_by_tenant(
                tenant.id)
            self.open(PaymentWindow(tenant, transactions, histories))
            return self.shutdown()
        elif event == "Move In":
            selectedIndex = self.view.table_contents[values["_TABLE_"][0]][0]
            unit = self.database.UnitModel.get(selectedIndex)
            self.open(MoveIn(unit))
        # -------------------------------------------------------------------------------------
        elif event in ("_SEARCH_", "_FILTER_"):
            self.search = values["_SEARCH_"]
            if self.lookup == "unit":
                self.filter = values["_FILTER_"]
            self.view.table_contents = self.__filter(values)
            self.window["_TABLE_"](self.view.table_contents)
        # If the user presses escape, clear the search bar
        elif event == "Escape:27":
            self.window["_SEARCH_"]("")
            self.search = ""
            if self.lookup == "unit":
                self.window["_FILTER_"]("All")
                self.filter = "All"
            self.refresh()
        return True

    def refresh(self):
        if self.lookup == "tenants":
            data = self.database.TenantModel.get_list()
            self.view.table_all = self.view.get_tenant_table_data(data)
        else:
            data = self.database.UnitModel.get_list()
            self.view.table_all = self.view.get_unit_table_data(data)
        self.view.table_contents = self.__filter(
            {"_SEARCH_": self.search, "_FILTER_": self.filter})
        self.window["_TABLE_"](self.view.table_contents)

    def shutdown(self):
        self.window.close()
        return False

    @staticmethod
    def __generate_buttons(buttons, btn_size):
        """Generates a button stack for top bar"""
        bar = []
        for btn in buttons:
            bar.append(Gui.B(btn, size=btn_size))
        return bar

    def __filter(self, values):
        """Creates a filtered version of the main table and returns it"""
        filtered_table = []
        search = values["_SEARCH_"].strip().casefold()
        for item in self.view.table_all:
            item_strings = item[1:]
            for val in item_strings:
                if search in val.casefold() and self.window_filters in val.casefold() and \
                        (self.lookup == "tenants" or (values["_FILTER_"] == item_strings[2] if self.filter else False)
                         or (values["_FILTER_"] == "All" if self.filter else True)):
                    filtered_table.append(item)
                    break
        return filtered_table
