"""Code written by Jacquesne Jones unless otherwise specified."""

from .base_orm import Base, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship


class MapUnit(Base):
    """Defines the map data for an existing unit.

    MapUnits are connected to Unit objects and add some additional data for the purpose of drawing the map.
    The design is that one corner of the rectangle is set using an (x, y) coordinate on a graph. The size of the
    drawing is based on the physical size of the unit defined in UnitRules.

    The rotation values allow the user to skew and rotate the unit.
    unit_rotation defines the angle in degrees of the unit as a whole, so a rotation of 45 would draw a trapezoid
    rather than a square for a 5x5 unit.
    base_rotation defines the rotation of the base, turning the entire object. A rotation of 45 here would draw
    a diamond rather than a square for a 5x5 unit.
    """
    unit_id = Column(Integer, ForeignKey('units.id'))
    x = Column(Integer)
    y = Column(Integer)
    unit_rotation = Column(Integer)
    base_rotation = Column(Integer)

    unit = relationship('Unit', back_populates='map')


class MapLine(Base):
    """Draws basic lines on the map.

    The idea behind line drawing is to allow the user to build an interactive map of the facility. These
    lines are static drawings that can be used to indicate facility borders, such as fences and gates,
    as well as other obstacles, road limits, etc.

    They use a simple two-point line drawing mechanism, with (x1, y1) being one end of the line and (x2, y2)
    being the other point.
    """
    x1 = Column(Integer)
    y1 = Column(Integer)
    x2 = Column(Integer)
    y2 = Column(Integer)
