"""Code written by Jacquesne Jones unless otherwise specified."""

from .base_orm import Base, TimeStamp
from sqlalchemy import String, Column, Integer, ForeignKey, DateTime
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from src.DatabaseModel.format import price_format, name_last_first


class Unit(Base):
    """Defines a unit, which can be any sort of rental area including outdoor lots."""
    identifier = Column(String, unique=True)
    order = Column(Integer, unique=True)
    tenant_id = Column(Integer, ForeignKey('tenants.id'))
    size_id = Column(Integer, ForeignKey('unitrules.id'))
    link_group = Column(Integer)
    reserved_date = Column(DateTime)
    reserved_by = Column(Integer, ForeignKey('reservations.id'))

    @hybrid_property  # property than can handle both sql statements and python statements
    def status(self):
        """Calculates the status of unit."""
        if not self.tenant:
            return "Vacant"
        elif self.reserved_by:
            return "Reserved"
        else:
            return "Occupied"

    @hybrid_property
    def size_string(self):
        return self.size.size_string

    @hybrid_property
    def price_string(self):
        return self.size.price_string

    tenant = relationship('Tenant', back_populates='unit')
    size = relationship('UnitRule', back_populates='unit')
    reserved = relationship('Reservation', back_populates='unit')
    note = relationship('UnitNote', back_populates='unit')
    transaction = relationship('Transaction', back_populates='unit')
    history = relationship('UnitHistory', back_populates='unit')
    map = relationship('MapUnit', back_populates='unit', uselist=False)


class UnitRule(Base):
    """Defines the price, category, and size of the unit."""
    category_id = Column(Integer, ForeignKey('unitcategories.id'))
    length = Column(String)
    width = Column(String)
    floor = Column(Integer)
    price = Column(String)

    @hybrid_property
    def size_string(self):
        """Returns the size in a formatted string."""
        width = float(self.width)
        length = float(self.length)
        if width % 1 == 0:
            txt_width = f'{width:.0f}'
        else:
            txt_width = f'{width:.1f}'
        if length % 1 == 0:
            txt_length = f'{length:.0f}'
        else:
            txt_length = f'{length:.1f}'
        return self.category.cat_format.replace('{width}', txt_width).replace('{length}', txt_length)

    @hybrid_property
    def price_string(self):
        return price_format(self.price)

    unit = relationship('Unit', back_populates='size')
    category = relationship('UnitCategory', back_populates='rule')


class UnitCategory(Base):
    """The category of the unit, such as indoor or outdoor, and the format of the size for the UI."""
    category = Column(String)
    cat_format = Column(String)

    rule = relationship('UnitRule', back_populates='category')


class Reservation(Base, TimeStamp):
    """Defines reservation data for a unit."""
    existing_id = Column(Integer, ForeignKey('tenants.id'))
    last = Column(String)
    first = Column(String)
    middle = Column(String)
    phone = Column(String)
    email = Column(String)

    @hybrid_property
    def fullname(self):
        return name_last_first(self.last, self.first, self.middle)

    unit = relationship('Unit', back_populates='reserved')
    tenant = relationship('Tenant', back_populates='reservation')


class UnitNote(Base, TimeStamp):
    """Notes for units."""
    unit_id = Column(Integer, ForeignKey('units.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    details = Column(String)

    unit = relationship('Unit', back_populates='note')
    user = relationship('User', back_populates='unit_note')

