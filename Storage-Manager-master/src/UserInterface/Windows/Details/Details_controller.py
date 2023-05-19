"""Code written by Jacquesne Jones unless otherwise specified."""

from src.UserInterface.Windows.Window.window_controller import WindowController
from src.DatabaseORM.unit_orm import Unit
from src.DatabaseORM.tenant_orm import Tenant
from .Details_view import DetailsWindowView


class DetailsWindow(WindowController):
    """Shows the details for a given Unit or Tenant"""
    def __init__(self, controller, table_type, key, edit=False):
        skip_load = False
        self.table = table_type
        self.edit = edit
        self.key = key
        self.controller = controller
        if self.table == Unit:
            self.data = controller.database.UnitModel.get(key)
        elif self.table == Tenant:
            self.data = controller.database.TenantModel.get(key)
        else:
            skip_load = True
        super().__init__(DetailsWindowView, "Unit Details" if self.table == Unit else "Tenant Details")
        if not skip_load:
            self.load()

    def load(self):
        self.window = self.view.window

    def process_event(self, event, values):
        if event in (None, "Close"):
            return self.shutdown()
        elif event == "Edit":
            self.edit_switch()
        elif event == "Save":
            self.save_data(values)
        elif event in self.view.events:
            self.__text_edited(event, values)
        return True

    def refresh(self):
        self.view.transactions.refresh()
        self.view.histories.refresh()

    def shutdown(self):
        self.window.close()
        return False

    def edit_switch(self):
        """Changes the current mode and reloads the window."""
        # Switch edit mode and reload
        self.edit = not self.edit
        self.view.edit = not self.view.edit
        self.reload()

    def save_data(self, values):
        """Saves any changes and creates history updates if a value was changed."""
        items = [
            ("Last", "self.data.last"),
            ("First", "self.data.first"),
            ("Middle", "self.data.middle"),
            ("Address", "self.data.addr1"),
            ("Line 2", "self.data.addr2"),
            ("City", "self.data.city"),
            ("State", "self.data.state_string"),
            ("Zip", "self.data.zip"),
            ("Phone", "self.data.phone"),
            ("Cell", "self.data.cell"),
            ("Work", "self.data.work"),
            ("Email", "self.data.email"),
            ("License Number", "self.data.license_num"),
            ("License State", "self.data.license_state"),
            ("Lease #", "self.data.lease"),
            ("Company", "self.data.company"),
            ("Tax ID", "self.data.tax_id"),
            ("Gate Code", "self.data.gate_code"),
            ("Access", "self.data.access_id"),
            ("Never Lock", "self.data.never_lock"),
            ("Deactivate Gate", "self.data.deactivate_gate"),
            ("Web Access", "self.data.web_access"),
            ("Vehicle VIN", "self.data.vehicle_vin"),
            ("License Plate", "self.data.plate_num"),
            ("Vehicle State", "self.data.vehicle_state"),
            ("Insurance #", "self.data.insurance_num"),
            ("Lien Holder", "self.data.lien_holder"),
        ]
        # NOTE: This function uses eval() and exec() functions to evaluate and change
        # the database using the above list. Normally these functions are considered unsafe,
        # however, the list is a constant and does not involve user input so no manipulation
        # of commands is possible.
        for key, value in items:
            # Get value of secondary string
            val = eval(value)
            # This changes value to a string comparison
            if not val:
                val = ""
            if values[key] != val:
                # Update database value
                exec(f"{value} = values['{key}']")
                # Add history item
                self.database.TenantHistoryModel.new(
                    self.data,
                    "Update",
                    key,
                    values[key],
                    val
                )
                # Update internal data for text colors
                self.view.values[key] = values[key]
                self.window[f"_{key}_"](text_color='black')
                self.refresh_all()

    def __text_edited(self, event, values):
        """Modifies text colors depending on if the field has been modified."""
        # Change text color to red if different from original value, otherwise switch back to black
        if values[event] != self.view.values[event]:
            self.window[f"_{event}_"](text_color='red')
        else:
            self.window[f"_{event}_"](text_color='black')
