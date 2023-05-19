"""Code written by Jacquesne Jones unless otherwise specified."""

from .transaction_viewer import TransactionView
from src.DatabaseModel.format import date_format, price_format


class TransactionFrame:
    """Adds a frame used to show the transactions of a given Unit and Tenant."""
    def __init__(self, controller, unit=None, tenant=None, widths=None, rows=None):
        self.controller = controller
        self.unit = unit
        self.tenant = tenant
        self.transactions = self.get_table_list()
        self.view = TransactionView(controller, self.transactions,
                                    widths=widths, rows=rows).view

    def refresh(self):
        self.transactions = self.get_table_list()
        self.controller.window["_TRANSACTION_TABLE_"](self.transactions)

    def get_table_list(self):
        transactions = self.controller.database.TransactionModel.get_all(unit=self.unit, tenant=self.tenant)
        if transactions.count() == 0:
            return [[]]
        else:
            transaction_list = []
            for transaction in transactions:
                # Format: Date, Value, Category
                transaction_list.append([date_format(transaction.created),
                                         price_format(transaction.amount), transaction.category.category])
            return transaction_list
