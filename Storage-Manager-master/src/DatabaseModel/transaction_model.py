"""Code written by Jacquesne Jones unless otherwise specified."""

from .base_model import BaseModel
from src.DatabaseORM.transaction_orm import Transaction, TransactionCategory
from sqlalchemy import and_
from src.UserInterface.Windows.Window.window_controller import WindowController


class TransactionModel(BaseModel):
    def new(self, amount, category, unit=None, tenant=None, debit=False):
        """Creates a new unit history and saves it to the database.

                        :param amount: String that can be converted to a positive float for the amount to charge
                        :param category: String category of the transaction.
                        :param unit: What unit this transaction is associated with, default None.
                        :param tenant: What tenant this transaction is associated with, default None.
                        :param debit: Boolean check to covert to negative value for debits.
                        """
        # Get category for assignment
        new_category = self.database.TransactionModel.get_category_by_name(
            category)
        # Create new transaction and add values
        new_transaction = Transaction()
        new_transaction.user = WindowController.current_user
        # Convert to negative if necessary
        if debit:
            neg_amount = -float(amount)
            amount = str(neg_amount)
        new_transaction.amount = amount
        new_transaction.unit = unit
        new_transaction.tenant = tenant
        new_transaction.category = new_category
        # Add new transaction
        self.session.add(new_transaction)
        self.session.commit()

    def get_category_list(self):
        """Gets a list of all transaction categories."""
        return self.session.query(TransactionCategory)

    def get_category_by_name(self, name):
        """Gets a specific category based on the name of that category.

                        :param name: String category to get.
                        """
        return self.session.query(TransactionCategory).filter(TransactionCategory.category == name).one()

    def get_all(self, unit=None, tenant=None):
        """Gets all Transactions for a given unit, tenant, both, or every transaction"""
        if unit and tenant:
            return self.session.query(Transaction).filter(and_(Transaction.unit == unit, Transaction.tenant == tenant))\
                .order_by(Transaction.created.desc())
        elif unit and not tenant:
            return self.session.query(Transaction).filter(Transaction.unit == unit)\
                .order_by(Transaction.created.desc())
        elif tenant and not unit:
            return self.session.query(Transaction).filter(Transaction.tenant == tenant)\
                .order_by(Transaction.created.desc())
        else:
            return self.session.query(Transaction)\
                .order_by(Transaction.created.desc())

    def get_last_charge(self, unit):
        """Gets the last rent charge made to the unit"""
        return self.session.query(Transaction).filter(Transaction.unit == unit)\
            .order_by(Transaction.created.desc()).first()

    def make_payment_on_unit(self, unit, amount):
        """Makes a payment for a given unit"""
        pass

    def add_rent_charge(self, unit, amount):
        """Adds a new rent charge on a unit.

        :param unit: The unit to charge.
        :param amount: A positive number string that can be converted to a float."""
        tenant = unit.tenant
        self.new(amount, "Rent Charge", unit=unit, tenant=tenant, debit=True)

    # -------------------------------------------------------------------------------------
    # This section coded by Emerson Havener
    def pay(self, transaction_id, amount):
        transaction = self.session.query(Transaction).get(transaction_id)
        transaction.amount = float(transaction.amount) + amount
        self.session.commit()
        self.session.flush()

    def get_by_tenant(self, tenant_id):
        transactions = self.session.query(Transaction).filter(
            Transaction.tenant_id == tenant_id)
        return transactions
    # -------------------------------------------------------------------------------------


class InventoryModel(BaseModel):
    pass
