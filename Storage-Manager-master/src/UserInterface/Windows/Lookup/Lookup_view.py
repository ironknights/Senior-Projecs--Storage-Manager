"""Code written by Jacquesne Jones unless otherwise specified."""

from src.UserInterface.Windows.Window.window_controller import Gui, error
from src.DatabaseORM.unit_orm import Unit
from src.DatabaseORM.tenant_orm import Tenant
from src.UserInterface.Windows.Window.window_viewer import WindowViewer


class LookupWindowView(WindowViewer):

    def __init__(self, controller, window_title=None):
        self.table_type = None
        self.table_contents = []
        self.lookup_type = controller.lookup
        super().__init__(controller, window_title)
        # Get the full table for filtering
        self.table_all = self.table_contents

    def create_layout(self):
        table = []
        top_bar = []
        data = []
        btn_size = (12, 2)
        if self.lookup_type == "units":
            self.table_type = Unit
            search_layout = [Gui.T("Search"), Gui.In(key="_SEARCH_", enable_events=True), Gui.T("Filters:"),
                             Gui.Combo(["All", "Vacant", "Occupied", "Reserved"], default_value="All",
                                       key="_FILTER_", enable_events=True)]
            data = self.database.UnitModel.get_list()
            self.title = "Units"
            top_bar = self.__generate_buttons(
                ("Make Payment ", "Details", "Link/Unlink",
                 "Notes", "Move In", "Move Out"),
                btn_size)
        elif self.lookup_type == "move_in":
            self.table_type = Unit
            search_layout = [Gui.T("Search"), Gui.In(
                key="_SEARCH_", enable_events=True)]
            data = self.database.UnitModel.get_list()
            self.title = "Move In"
            top_bar = [Gui.B("Cancel", size=btn_size), Gui.T(
                ' ' * 104), Gui.B("Select", size=btn_size)]
        elif self.lookup_type == "tenants":
            self.table_type = Tenant
            search_layout = [Gui.T("Search"), Gui.In(
                key="_SEARCH_", enable_events=True)]
            self.title = "Tenants"
            data = self.database.TenantModel.get_list()
            top_bar = self.__generate_buttons(
                ("Make Payment", "Details", "Edit", "Notes", "Ledger",
                 "Photos", "Auto Payment", "Notices", "Rates"),
                btn_size)
            self.table_contents = self.get_tenant_table_data(data)
            table = [Gui.Table(self.table_contents, headings=["ID", "Unit", "Name", "Phone", "Email"],
                               num_rows=20, col_widths=[1, 10, 25, 15, 42], bind_return_key=True,
                               auto_size_columns=False, alternating_row_color='#97FFFF', justification='left',
                               visible_column_map=[False, True, True, True, True], key="_TABLE_")]
        else:
            search_layout = []
            error("Invalid lookup type passed to Lookup object")
        if self.lookup_type in ("units", "move_in"):
            self.table_contents = self.get_unit_table_data(data)
            table = [Gui.Table(self.table_contents, headings=["ID", "Unit", "Size", "Status", "Rent", "Tenant"],
                               num_rows=20, col_widths=[1, 10, 10, 15, 10, 16], bind_return_key=True,
                               auto_size_columns=False, alternating_row_color='#97FFFF', justification='left',
                               visible_column_map=[False, True, True, True, True, True], key="_TABLE_")]
        return [
            top_bar,
            search_layout,
            table
        ]

    def create_window(self):
        return Gui.Window(self.title, self.layout, resizable=True, return_keyboard_events=True)

    @staticmethod
    def __generate_buttons(buttons, btn_size):
        """Generates a button stack for top bar"""
        bar = []
        for btn in buttons:
            bar.append(Gui.B(btn, size=btn_size))
        return bar

    @staticmethod
    def get_tenant_table_data(data):
        table_contents = []
        for item in data:
            table_contents.append([item.id, f"{item.unit[0].identifier}{'+' if len(item.unit) > 1 else ''}"
                                   if item.unit else "", item.fullname, item.phone, item.email])
        return table_contents

    def get_unit_table_data(self, data):
        table_contents = []
        for item in data:
            if (self.lookup_type == "move_in" and item.status == "Vacant") or self.lookup_type == "units":
                table_contents.append([item.id, item.identifier, item.size_string, item.status,
                                       item.price_string, item.tenant.fullname if item.tenant else ""])
        return table_contents
