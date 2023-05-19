"""Code written by Jacquesne Jones unless otherwise specified."""

from .base_orm import Base, TimeStamp
from sqlalchemy import String, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship


class UnitHistory(Base, TimeStamp):
    """Histories for units."""
    unit_id = Column(Integer, ForeignKey('units.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    category_id = Column(Integer, ForeignKey('historycategories.id'))
    field_changed = Column(String)
    new_value = Column(String)
    old_value = Column(String)

    unit = relationship('Unit', back_populates='history')
    user = relationship('User', back_populates='unit_history')
    category = relationship('HistoryCategory', back_populates='unit')


class TenantHistory(Base, TimeStamp):
    """Histories for tenants."""
    tenant_id = Column(Integer, ForeignKey('tenants.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    category_id = Column(Integer, ForeignKey('historycategories.id'))
    field_changed = Column(String)
    new_value = Column(String)
    old_value = Column(String)

    tenant = relationship('Tenant', back_populates='history')
    user = relationship('User', back_populates='tenant_history')
    category = relationship('HistoryCategory', back_populates='tenant')


class HistoryCategory(Base):
    """Categories used by histories."""
    category = Column(String)

    unit = relationship('UnitHistory', back_populates='category')
    tenant = relationship('TenantHistory', back_populates='category')
