"""Code written by Jacquesne Jones unless otherwise specified."""

from sqlalchemy import String, Boolean, Column, Integer, ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from .base_orm import Base, TimeStamp
from src.DatabaseModel.format import get_state, get_state_num, name_last_first


class Tenant(Base):
    """Defines a tenant, including all their personal information and any connections to other data objects."""
    ssn = Column(String(9))
    last = Column(String)
    first = Column(String)
    middle = Column(String)
    addr1 = Column(String)
    addr2 = Column(String)
    city = Column(String)
    state_id = Column(Integer)
    zip = Column(String)
    country = Column(String)
    phone = Column(String)
    cell = Column(String)
    work = Column(String)
    email = Column(String)
    license_num = Column(String)
    license_state = Column(Integer)
    lease = Column(Integer)
    company = Column(String)
    tax_id = Column(String)
    alt_relationship = Column(String)
    alt_last = Column(String)
    alt_first = Column(String)
    alt_middle = Column(String)
    alt_addr1 = Column(String)
    alt_addr2 = Column(String)
    alt_city = Column(String)
    alt_state = Column(String)
    alt_zip = Column(String)
    alt_country = Column(String)
    alt_phone = Column(String)
    alt_cell = Column(String)
    alt_email = Column(String)
    gate_code = Column(Integer)
    access_id = Column(Integer, ForeignKey('accesstimes.id'))
    never_lock = Column(Boolean)
    deactivate_gate = Column(Boolean)
    web_access = Column(Boolean)
    cc_token = Column(String)
    vehicle_vin = Column(String)
    plate_num = Column(String)
    vehicle_state = Column(Integer)
    insurance_num = Column(String)
    lien_holder = Column(String)

    @hybrid_property
    def state(self):
        """Getter for the state, returning the state_id."""
        return self.state_id

    @state.setter
    def state(self, value):
        """Allows direct setting of state id by the name of the state."""
        self.state_id = get_state_num(value)

    @hybrid_property
    def state_string(self):
        """Gets the state by string instead of id.

        :return Two letter state name.
        """
        return get_state(self.state_id)

    @hybrid_property
    def state_string_long(self):
        """Gets the full state name instead of id.

        :return Full state name.
        """
        return get_state(self.state_id, long=True)

    @hybrid_property
    def fullname(self):
        """Gets a string of the person's name in the format Last, First, Middle Initial"""
        return name_last_first(self.last, self.first, self.middle)

    unit = relationship("Unit", back_populates='tenant')
    reservation = relationship('Reservation', back_populates='tenant')
    note = relationship('TenantNote', back_populates='tenant')
    transaction = relationship('Transaction', back_populates='tenant')
    history = relationship('TenantHistory', back_populates='tenant')
    access = relationship('AccessTime', back_populates='tenant')


class TenantNote(Base, TimeStamp):
    """A note for a specific tenant."""
    tenant_id = Column(Integer, ForeignKey('tenants.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    category_id = Column(Integer, ForeignKey('tenantnotecategories.id'))
    note = Column(String)

    tenant = relationship('Tenant', back_populates='note')
    category = relationship('TenantNoteCategory', back_populates='note')
    user = relationship('User', back_populates='tenant_note')


class TenantNoteCategory(Base):
    """Note categories for filtering."""
    category = Column(String)

    note = relationship('TenantNote', back_populates='category')
