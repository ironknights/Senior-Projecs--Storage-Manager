"""Code written by Jacquesne Jones unless otherwise specified."""

from .base_orm import Base, TimeStamp, inventory_waivers
from sqlalchemy import String, Boolean, Column, Integer, ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from src.DatabaseModel.format import price_format


class Transaction(Base, TimeStamp):
    """A monetary transaction.

    Transactions, unlike most database objects, can be associated with multiple tables. A transaction may
    have a unit, a tenant, or both.

    The reason for this is to allow the same data type to be used in three different scenarios. The most
    common scenario is when a transaction has a unit and tenant. This means that the charge is to a specific unit,
    such as rent or a fee, for a particular customer.

    By having both pieces of data it's much easier to keep track of transactions where a unit is rented to tenant
    without having to filter out old unit data. It also allows for a single customer to have multiple units and
    track their payments and charges to each unit individually.

    The last two scenarios is where a charge is only to a customer with no unit, or charged to an unknown customer.
    This is useful to keep track of inventory charges, such as selling locks to customers. The inventory can be
    sold without needing to assign it to a specific unit or even customer in the case of walk-in sales. Inventory
    sales can then be tracked easily by any transaction that lacks a unit.
    """
    unit_id = Column(Integer, ForeignKey('units.id'))
    tenant_id = Column(Integer, ForeignKey('tenants.id'))
    category_id = Column(Integer, ForeignKey('transactioncategories.id'))
    amount = Column(String)

    @hybrid_property
    def category_string(self):
        """Used to easily get access to the category name."""
        return self.category.category

    @hybrid_property
    def amount_string(self):
        """Returns the price in dollar format for use in the UI."""
        return price_format(self.amount)

    unit = relationship('Unit', back_populates='transaction')
    tenant = relationship('Tenant', back_populates='transaction')
    category = relationship('TransactionCategory', back_populates='transaction')


class TransactionCategory(Base):
    """Defines the type of category."""
    category = Column(String)

    transaction = relationship('Transaction', back_populates='category')


class Inventory(Base):
    """Used to track inventory."""
    title = Column(String)
    price = Column(String)
    quantity = Column(Integer)
    taxed = Column(Boolean)

    waiver = relationship('RuleException', secondary=inventory_waivers, back_populates='free_inventory')
