"""Code written by Deeptanshu Das unless otherwise specified."""

import PySimpleGUI as Gui
from src.UserInterface.Tabs.MainTab.MainTab_viewer import MainTabViewer
from src.DatabaseORM.unit_orm import Unit

GRAPH_SIZE = (100, 100)
DATA_SIZE = (300, 300)


class OperationsView(MainTabViewer):
    """Operations view class"""

    def __init__(self, window, key, tab_title):
        self.num_units = 0
        super().__init__(window, key, tab_title)


    def create_layout(self):
        """This function creates the dashboard layout"""
        units_frame = self.create_button_frame("Units",
                                               ("Unit List", "Move In", "Move Out", "Transfers", "Reservations"), 6)
        tenants_frame = self.create_button_frame("Tenants", ("Tenant List", "Wait List", "Emails",
                                                             "Calls", "Texts", "Letters"), 6)
        payments_frame = self.create_button_frame("Payments", ("Make Payment", "Invoicing", "Auto Payments",
                                                               "Credit/Debit", "Merchandise"), 6)
        end_of_day_frame = self.create_button_frame("End of Day", ("Trial Deposit", "Daily Close", "Backup"), 6)

        # Getting the number of occupied units

        all_units = self.window.database.session.query(Unit)

        num_occupied = 0

        occupied_percentage = 0

        for unit in all_units:
            self.num_units += 1
            if unit.status == "Occupied":
                num_occupied += 1

        # print("Total units:", self.num_units)
        #
        # print("Total occupied:", num_occupied)

        if self.num_units>0:
            occupied_percentage = (num_occupied / self.num_units) * 100

        # Getting the unit available size

        units_unoccupied_a = 0
        units_unoccupied_b = 0
        units_unoccupied_c = 0
        units_unoccupied_d = 0
        units_unoccupied_e = 0
        units_unoccupied_f = 0
        units_unoccupied_g = 0
        units_unoccupied_h = 0

        for unit in all_units:
            if unit.status == "Vacant":
                if unit.size_string == "5x5":
                    units_unoccupied_a += 1
                if unit.size_string == "5x10":
                    units_unoccupied_b += 1
                if unit.size_string == "10x10":
                    units_unoccupied_c += 1
                if unit.size_string == "10x15":
                    units_unoccupied_d += 1
                if unit.size_string == "10x20":
                    units_unoccupied_e += 1
                if unit.size_string == "20 ft.":
                    units_unoccupied_f += 1
                if unit.size_string == "35 ft.":
                    units_unoccupied_g += 1
                if unit.size_string == "40 ft.":
                    units_unoccupied_h += 1

        # Table element

        table_contents = []

        table = [Gui.Table(table_contents, headings=["Unit", "Name", "Phone", "Due"],
                           num_rows=10, col_widths=[10, 20, 15, 10], bind_return_key=True,
                           auto_size_columns=False, alternating_row_color='#97FFFF', vertical_scroll_only=True,
                           justification='right', hide_vertical_scroll=False, background_color="Light Blue",
                           visible_column_map=[True, True, True, True], key="_TABLE_")]

        # Graph element

        graph = Gui.Graph(canvas_size=(120, 120), graph_bottom_left=(0, 0), graph_top_right=(120, 120),
                          background_color=None, pad=None, change_submits=False, drag_submits=False,
                          enable_events=False,
                          key="Graph", tooltip=None, right_click_menu=None, visible=True, float_values=False,
                          metadata=None)

        # The dashboard units

        dashboard_frame = [Gui.Frame("Dashboard", [[Gui.Text(f"Occupied Units : {occupied_percentage} %"), graph],
                                                   [Gui.Text(f"Available 5x5 units : {units_unoccupied_a}")],
                                                   [Gui.Text(f"Available 5x10 units : {units_unoccupied_b}")],
                                                   [Gui.Text(f"Available 10x10 units : {units_unoccupied_c}")],
                                                   [Gui.Text(f"Available 10x15 units : {units_unoccupied_d}")],
                                                   [Gui.Text(f"Available 10x20 units : {units_unoccupied_e}")],
                                                   [Gui.Text(f"Available 20 ft. units : {units_unoccupied_f}")],
                                                   [Gui.Text(f"Available 35 ft. units : {units_unoccupied_g}")],
                                                   [Gui.Text(f"Available 40 ft. units : {units_unoccupied_h}")],
                                                   [Gui.Text(f"Pending Phone Payments")],
                                                   table, ])]

        layout = [[units_frame, tenants_frame, payments_frame, end_of_day_frame], dashboard_frame]

        return layout

    # -------------------------------------------------------------------------------------
    # This section coded by Jacquesne Jones
    def create_tab(self):
        return Gui.Tab(self.title, self.layout, key=self.key)

    @staticmethod
    def create_button_frame(frame, buttons, total):
        # Get maximum size to determine button width
        pad_text_size = 14
        max_width = 0
        for btn in buttons:
            if len(btn) > max_width:
                max_width = len(btn)
        # Create layout frame
        layout = [[Gui.Button(item,
                              key=f"_{frame.upper().replace(' ', '_')}_{item.upper().replace(' ', '_')}_",
                              size=(max_width, 1))] for item in buttons]
        layout += [[Gui.T(" ", key=f"{frame}{num}", auto_size_text=False, size=(1, 1),
                          font=('Helvetica', pad_text_size))]
                   for num in range(total - len(buttons))]
        frame = Gui.Frame(frame, layout, key=f"_{frame.upper().replace(' ', '_')}_")
        return frame
    # -------------------------------------------------------------------------------------
