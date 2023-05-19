"""Code written by Deeptanshu Das unless otherwise specified."""

from src.UserInterface.Tabs.MainTab.MainTab_controller import MainTabController
from src.UserInterface.Tabs.Operations.Operations_viewer import OperationsView
from src.UserInterface.Windows.Lookup.Lookup_controller import LookupWindow
from src.UserInterface.Windows.Payment.Payment_controller import PaymentWindow
import random


padding = 25

BAR_WIDTH = 10
BAR_SPACING = 15
EDGE_OFFSET = 3
# GRAPH_SIZE = (30, 30)
# DATA_SIZE = (30, 30)


class Operations(MainTabController):
    """Operations class"""
    def __init__(self, window, key="_OPERATIONS_", title=f"{' ' * padding}Operations{' ' * padding}"):
        super().__init__(window, key, OperationsView, title)

    def load(self):

     """ Loads the bar graphs"""

     values = [self.view.num_units, 8]
     for i, graph_value in enumerate(values):
        #graph_value = random.randint(0, 60)
        self.window.window["Graph"].DrawRectangle(top_left=(i * BAR_SPACING + EDGE_OFFSET, graph_value),
                        bottom_right=(i * BAR_SPACING + EDGE_OFFSET + BAR_WIDTH, 0), fill_color='blue')
        self.window.window["Graph"].DrawText(text=graph_value, location=(i * BAR_SPACING + EDGE_OFFSET + 15, graph_value + 10))

    def process_event(self, event, values):
        # -------------------------------------------------------------------------------------
        # This section coded by Jacquesne Jones
        if event == "_UNITS_UNIT_LIST_":
            self.open(LookupWindow("units"))
        elif event == "_TENANTS_TENANT_LIST_":
            self.open(LookupWindow("tenants"))
        elif event == "_UNITS_MOVE_IN_":
            self.open(LookupWindow("move_in"))
        elif event == "_PAYMENTS_MAKE_PAYMENT_":
            self.open(LookupWindow("tenants"))
        # -------------------------------------------------------------------------------------

    def refresh(self):
        """Refreshes all windows and tabs"""
        # if data changed on back-end what will happen on the operations
        pass
