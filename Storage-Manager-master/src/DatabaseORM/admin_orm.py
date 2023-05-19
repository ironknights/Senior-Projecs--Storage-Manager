"""Code written by Jacquesne Jones unless otherwise specified."""

from .base_orm import Base, fee_waivers, inventory_waivers
from sqlalchemy import String, Column, Integer, DateTime
from sqlalchemy.orm import relationship


class BusinessRule(Base):
    """Contains rule/value pairs used by the database to establish business rules.

    While these values are not hard-coded the use of them usually is. For example, a rule/value pair
    is the Sales Tax and a number. If there is no Sales Tax rule/value pair the program will crash on load
    as this key is always used.

    The required rule/value pairs for program operation are initialized in src/DatabaseModel/database_model.py
    in the __initialize function.
    """
    rule = Column(String)
    value = Column(String)


class Fee(Base):
    """Defines a fee or charge used by the business rules. These can be waived via rule exceptions."""
    title = Column(String)
    amount = Column(String)
    percent = Column(Integer)

    waiver = relationship('RuleException', secondary=fee_waivers, back_populates='waived_fee')


class RuleException(Base):
    """Defines an exception template for modifying fees and inventory changes normally charged to customers."""
    title = Column(String)
    price_adjustment = Column(String)
    percent_adjustment = Column(Integer)
    months = Column(Integer)
    recurring_months = Column(Integer)

    free_inventory = relationship('Inventory', secondary=inventory_waivers, back_populates='waiver')
    waived_fee = relationship('Fee', secondary=fee_waivers, back_populates='waiver')


class AccessTime(Base):
    """Defines the access times a tenant is allowed to enter the facility."""
    title = Column(String)
    start_time = Column(DateTime)
    end_time = Column(DateTime)

    tenant = relationship("Tenant", back_populates="access")
