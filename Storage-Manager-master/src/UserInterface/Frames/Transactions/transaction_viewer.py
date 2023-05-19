"""Code written by Jacquesne Jones unless otherwise specified."""

import PySimpleGUI as Gui


class TransactionView:
    def __init__(self, controller, transactions, widths=None, rows=None):
        self.controller = controller
        self.transactions = transactions
        self.col_widths = widths
        self.rows = rows
        self.view = self.create_view()

    def create_view(self):
        return Gui.Table(self.transactions,
                         headings=["Date", "Amount", "Category"],
                         col_widths=self.col_widths,
                         num_rows=self.rows,
                         key="_TRANSACTION_TABLE_",
                         justification='left',
                         auto_size_columns=False)
