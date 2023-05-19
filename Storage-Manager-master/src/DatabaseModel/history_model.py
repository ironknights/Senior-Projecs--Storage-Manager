"""Code written by Jacquesne Jones unless otherwise specified."""

from .base_model import BaseModel
from src.DatabaseORM.history_orm import UnitHistory, TenantHistory, HistoryCategory
from src.UserInterface.Windows.Window.window_controller import WindowController


class UnitHistoryModel(BaseModel):
    """The model for unit histories."""
    def new(self, unit, category, field, new_val, old_val):
        """Creates a new unit history and saves it to the database.

                :param unit: The Unit object the history applies to.
                :param category: String category of the history.
                :param field: What field is being changed.
                :param new_val: The new data being stored.
                :param old_val: The old data that existed before the change.
                """
        # Get category for assignment
        new_category = self.database.UnitHistoryModel.get_category_by_name(category)
        # Create new transaction and add values
        new_history = UnitHistory()
        new_history.user = WindowController.current_user
        new_history.unit = unit
        new_history.category = new_category
        new_history.field_changed = field
        new_history.new_value = new_val
        new_history.old_value = old_val
        # Add new transaction
        self.session.add(new_history)
        self.session.commit()

    def get_category_list(self):
        """Gets a list of all history categories."""
        return self.session.query(HistoryCategory)

    def get_category_by_name(self, name):
        """Gets a specific category based on the name of that category.

                :param name: String category to get.
                """
        return self.session.query(HistoryCategory).filter(HistoryCategory.category == name).one()

    def get_all(self, unit):
        """Gets all unit histories for a specific unit in descending order."""
        return self.session.query(UnitHistory).filter(UnitHistory.unit == unit)\
            .order_by(UnitHistory.created.desc())


class TenantHistoryModel(BaseModel):
    """The model for tenant histories"""
    def new(self, tenant, category, field, new_val, old_val):
        """Creates a new tenant history and saves it to the database.

                :param tenant: The Tenant object the history applies to.
                :param category: String category of the history.
                :param field: What field is being changed.
                :param new_val: The new data being stored.
                :param old_val: The old data that existed before the change.
                """
        # Get category for assignment
        new_category = self.database.TenantHistoryModel.get_category_by_name(category)
        # Create new transaction and add values
        new_history = TenantHistory()
        new_history.user = WindowController.current_user
        new_history.tenant = tenant
        new_history.category = new_category
        new_history.field_changed = field
        new_history.new_value = new_val
        new_history.old_value = old_val
        # Add new transaction
        self.session.add(new_history)
        self.session.commit()

    def get_category_list(self):
        """Gets a list of all history categories."""
        return self.session.query(HistoryCategory)

    def get_category_by_name(self, name):
        """Gets a specific category based on the name of that category.

                :param name: String category to get.
                """
        return self.session.query(HistoryCategory).filter(HistoryCategory.category == name).one()

    def get_all(self, tenant):
        """Gets all tenant histories for a specific tenant in descending order."""
        return self.session.query(TenantHistory).filter(TenantHistory.tenant == tenant)\
            .order_by(TenantHistory.created.desc())

    # This code by Emerson Havener
    def get_by_tenant(self, tenant_id):
        hostories = self.session.query(TenantHistory).filter(
            TenantHistory.tenant_id == tenant_id)
        return hostories