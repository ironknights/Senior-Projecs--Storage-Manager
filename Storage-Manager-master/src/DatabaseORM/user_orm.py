"""Code written by Jacquesne Jones unless otherwise specified."""

from src.DatabaseORM.base_orm import Base, favorite_reports
from sqlalchemy import String, Boolean, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship


class User(Base):
    """Defines an user that has access to the program."""
    user_id = Column(String, unique=True)
    pw_hash = Column(String)
    permission_id = Column(Integer, ForeignKey('permissions.id'))
    default_tab = Column(String)

    unit_note = relationship('UnitNote', back_populates='user')
    tenant_note = relationship('TenantNote', back_populates='user')
    permission = relationship('Permission', back_populates='user')
    report_favorite = relationship('Report', secondary=favorite_reports, back_populates='user')
    unit_history = relationship('UnitHistory', back_populates='user')
    tenant_history = relationship('TenantHistory', back_populates='user')


class Permission(Base):
    """Defines a permission template that gives a user access to specific program functionality."""
    title = Column(String)
    create_template = Column(Boolean)
    ssn_reports = Column(Boolean)
    edit_rules = Column(Boolean)
    edit_forms = Column(Boolean)
    edit_reports = Column(Boolean)
    edit_inventory = Column(Boolean)
    edit_exceptions = Column(Boolean)
    manual_exceptions = Column(Boolean)
    allow_incomplete = Column(Boolean)

    user = relationship('User', back_populates='permission')
