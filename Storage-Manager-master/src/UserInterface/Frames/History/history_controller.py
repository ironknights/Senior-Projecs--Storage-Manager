"""Code written by Jacquesne Jones unless otherwise specified."""

from .history_viewer import HistoryView
from src.DatabaseModel.format import date_format
from src.DatabaseORM.unit_orm import Unit
from src.DatabaseORM.tenant_orm import Tenant


class HistoryFrame:
    """Adds a frame that shows the history of a given Unit or Tenant object."""
    def __init__(self, controller, data=None, widths=None, rows=None):
        """Frame init

        :param controller: The controller of the frame (object creating it).
        :param data: The Unit or Tenant to get the history of.
        :param widths: How wide to make the frame in characters.
        :param rows: How many rows to show before scrolling.
        """
        self.controller = controller
        self.data = data
        self.items = self.get_table_list()
        self.view = HistoryView(controller, self.items, widths=widths, rows=rows).view

    def refresh(self):
        self.items = self.get_table_list()
        self.controller.window["_HISTORY_TABLE_"](self.items)

    def get_table_list(self):
        """Generates a table of all history for the data object."""
        items = None
        if type(self.data) == Unit:
            items = self.controller.database.UnitHistoryModel.get_all(self.data)
        elif type(self.data) == Tenant:
            items = self.controller.database.TenantHistoryModel.get_all(self.data)
        else:
            print("FATAL ERROR")
            exit(-1)
        if items and items.count() == 0:
            return [[]]
        else:
            history_list = []
            for history in items:
                # Format: Date, Category, Field, New Value, Original
                history_list.append([date_format(history.created),
                                     history.category.category,
                                     history.field_changed,
                                     history.new_value,
                                     history.old_value])
            return history_list
