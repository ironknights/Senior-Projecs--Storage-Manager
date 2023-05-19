"""Code written by Jacquesne Jones unless otherwise specified."""

from src.UserInterface.Windows.Window.window_controller import Gui
from src.DatabaseORM.unit_orm import Unit
from src.DatabaseORM.tenant_orm import Tenant
from src.UserInterface.Windows.Window.window_viewer import WindowViewer
from src.UserInterface.Frames.Transactions.transaction_controller import TransactionFrame
from src.UserInterface.Frames.History.history_controller import HistoryFrame


class DetailsWindowView(WindowViewer):
    """View for details window."""
    def __init__(self, controller, window_title=None):
        self.table = controller.table
        self.edit = controller.edit
        self.data = controller.data
        self.transactions = None
        self.histories = None
        self.values = {}
        self.items = []
        self.events = []
        super().__init__(controller, window_title)

    def create_layout(self):
        # Clear all old data if it exists when creating layout
        self.values.clear()
        self.items.clear()
        self.events.clear()
        # Create layout based on details type
        if self.table == Unit:
            self.transactions = TransactionFrame(self.controller,
                                                 unit=self.data,
                                                 widths=[10, 10, 17],
                                                 rows=5)
        else:
            self.transactions = TransactionFrame(self.controller,
                                                 tenant=self.data,
                                                 widths=[15, 15, 30],
                                                 rows=5)
        # Create history frame
        self.histories = HistoryFrame(self.controller,
                                      data=self.data,
                                      widths=[10, 10, 10, 10, 10],
                                      rows=5)
        if self.table == Unit:
            return self.__create_unit_layout()
        elif self.table == Tenant:
            return self.__create_tenant_layout()
        else:
            self.title = "INVALID ITEM"
            return [[Gui.T("No data!!!")]]

    def create_window(self):
        return Gui.Window(self.title, self.layout)

    def __create_unit_layout(self):
        self.items = [
            ("Unit", self.data.identifier),
            ("Size", self.data.size_string),
            ("Status", self.data.status),
            ("Rate", self.data.price_string),
            ("Tenant", self.data.tenant.fullname if self.data.tenant else ""),
            ("Reservation", self.data.reserved_by)
        ]
        photo_frame = Gui.Frame("Photos", [
            [Gui.T(" " * 10)], [Gui.T(" " * 10)], [Gui.T(" " * 10)]])
        frame, size = self.__generate_data_frame()
        layout = [
            [Gui.Column([[Gui.Frame("Unit", frame)],
                         [self.transactions.view],
                         [Gui.T(' ' * ((size * 3) + 26)), Gui.B("Close")]]),
             Gui.Column([[photo_frame],
                         [self.histories.view]])]
        ]
        return layout

    def __create_tenant_layout(self):
        self.items = [
            ("Last", self.data.last),
            ("First", self.data.first),
            ("Middle", self.data.middle),
            ("Address", self.data.addr1),
            ("Line 2", self.data.addr2),
            ("City", self.data.city),
            ("State", self.data.state_string),
            ("Zip", self.data.zip),
            ("Phone", self.data.phone),
            ("Cell", self.data.cell),
            ("Work", self.data.work),
            ("Email", self.data.email),
            ("License Number", self.data.license_num),
            ("License State", self.data.license_state),
            ("Lease #", self.data.lease),
            ("Company", self.data.company),
            ("Tax ID", self.data.tax_id),
            ("Gate Code", self.data.gate_code),
            ("Access", self.data.access_id),
            ("Never Lock", self.data.never_lock),
            ("Deactivate Gate", self.data.deactivate_gate),
            ("Web Access", self.data.web_access),
            ("Vehicle VIN", self.data.vehicle_vin),
            ("License Plate", self.data.plate_num),
            ("Vehicle State", self.data.vehicle_state),
            ("Insurance #", self.data.insurance_num),
            ("Lien Holder", self.data.lien_holder),
        ]
        photo_frame = Gui.Frame("Photos", [
            [Gui.T(" " * 10)], [Gui.T(" " * 10)], [Gui.T(" " * 10)]])
        frame, size = self.__generate_data_frame()
        if self.edit:
            button_bar = [Gui.B("Edit"), Gui.B("Save"), Gui.T(' ' * ((size * 3) + 14)), Gui.B("Close")]
        else:
            button_bar = [Gui.B("Edit"), Gui.T(' ' * ((size * 3) + 16)), Gui.B("Close")]
        layout = [
            [Gui.Column([[Gui.Frame("Tenant", frame)],
                         [self.transactions.view],
                         button_bar]),
             Gui.Column([[photo_frame],
                         [self.histories.view]])]
        ]
        return layout

    def __generate_data_frame(self, num_columns=2, label_width=None, field_width=None):
        frame = []
        # If no width is set, find largest width and set to that
        if not label_width or not field_width:
            largest_label = 0
            largest_field = 0
            for item in self.items:
                # Assign list of possible events for use in controller
                self.events.append(f"{item[0]}")
                # Get longest length
                label_length = len(str(item[0]))
                field_length = len(str(item[1]))
                if label_length > largest_label:
                    largest_label = label_length
                if field_length > largest_field:
                    largest_field = field_length
            # Only set if not manually set already
            if not label_width:
                label_width = largest_label + 1
            if not field_width:
                field_width = largest_field + 1
        edit_type = Gui.Input if self.edit else Gui.Text
        for index in range(0, len(self.items) - 2, 2):
            row = [
                Gui.T(f"{self.items[index][0]}:", size=(label_width, 1),
                      key=f"_{self.items[index][0]}_"),
                edit_type(f"{self.items[index][1] if self.items[index][1] else ''}", size=(field_width, 1),
                          key=f"{self.items[index][0]}",
                          enable_events=True),
                Gui.T(f"{self.items[index+1][0]}:", size=(label_width, 1),
                      key=f"_{self.items[index+1][0]}_"),
                edit_type(f"{self.items[index+1][1] if self.items[index+1][1] else ''}", size=(field_width, 1),
                          key=f"{self.items[index+1][0]}",
                          enable_events=True)
            ]
            frame.append(row)
            # Add values if necessary
            if self.edit:
                self.values[self.items[index][0]] = self.items[index][1] if self.items[index][1] else ''
                self.values[self.items[index+1][0]] = self.items[index+1][1] if self.items[index][1] else ''
        # Check if last line had even or odd number of values, if odd, don't include last line
        if (len(self.items) / 2).is_integer():
            row = [
                Gui.T(f"{self.items[len(self.items) - 2][0]}:", size=(label_width, 1),
                      key=f"_{self.items[len(self.items) - 2][0]}_"),
                edit_type(f"{self.items[len(self.items) - 2][1] if self.items[len(self.items) - 2][1] else ''}",
                          size=(field_width, 1),
                          key=f"{self.items[len(self.items) - 2][0]}",
                          enable_events=True),
                Gui.T(f"{self.items[len(self.items) - 1][0]}:", size=(label_width, 1),
                      key=f"_{self.items[len(self.items) - 1][0]}_"),
                edit_type(f"{self.items[len(self.items) - 1][1] if self.items[len(self.items) - 1][1] else ''}",
                          size=(field_width, 1),
                          key=f"{self.items[len(self.items) - 1][0].upper()}",
                          enable_events=True)
            ]
            if self.edit:
                self.values[self.items[len(self.items) - 2][0]] = \
                    self.items[len(self.items) - 2][1] if self.items[len(self.items) - 2][1] else ''
                self.values[self.items[len(self.items) - 1][0]] = \
                    self.items[len(self.items) - 1][1] if self.items[len(self.items) - 1][1] else ''
        else:
            row = [
                Gui.T(f"{self.items[len(self.items) - 1][0]}:", size=(label_width, 1),
                      key=f"_{self.items[len(self.items) - 1][0]}_"),
                edit_type(f"{self.items[len(self.items) - 1][1] if self.items[len(self.items) - 2][1] else ''}",
                          size=(field_width, 1),
                          key=f"{self.items[len(self.items) - 1][0]}",
                          enable_events=True)
            ]
            if self.edit:
                self.values[self.items[len(self.items) - 1][0]] = self.items[len(self.items) - 1][1] if self.items[len(self.items) - 1][1] else ''
        frame.append(row)
        size = label_width + field_width
        return frame, size
