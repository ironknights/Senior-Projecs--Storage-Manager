"""Code written by Jacquesne Jones unless otherwise specified."""

import PySimpleGUI as Gui


class HistoryView:
    def __init__(self, controller, items, widths=None, rows=None):
        self.controller = controller
        self.items = items
        self.col_widths = widths
        self.rows = rows
        self.view = self.create_view()

    def create_view(self):
        """Creates the table view to embed in other objects."""
        return Gui.Table(self.items,
                         headings=["Date", "Category", "Field", "New Value", "Original"],
                         col_widths=self.col_widths,
                         num_rows=self.rows,
                         key="_HISTORY_TABLE_",
                         justification='left',
                         auto_size_columns=False)
