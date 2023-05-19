"""Code written by Jacquesne Jones unless otherwise specified."""

from datetime import datetime
from sqlalchemy import Table, Column, Integer, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base, declared_attr


class Base(object):
    """This is a custom base class for the ORM that establishes common parameters for all ORM objects."""
    @declared_attr
    def __tablename__(cls):
        """This generates a table name based on the ORM class name.

        The table names attempt to be human readable for easy development. First, the names are converted to
        lowercase. Then they are made plural.

        For example, UnitHistory is made lowercase (unithistory), then the y is removed (unithistor), and
        finally ies is added, for a final table name of (unithistories).

        If the name already had an 's' at the end, it would simply return the lowercase name,
        otherwise it adds an 's'. For example, BusinessRule becomes businessrules.
        """
        name = cls.__name__.lower()
        # If the class name ends in 'y' then remove the y and add 'ies', otherwise just add an 's' if not already
        # ending in s
        if name[-1] == 'y':
            return f"{name[:-1]}ies"
        elif name[-1] == 's':
            return name
        else:
            return f"{name}s"

    # All ORM objects have an integer autonumber primary key called id.
    id = Column(Integer, primary_key=True)

    def __repr__(self):
        return ""


class TimeStamp(object):
    """This class adds a time stamp to classes that need to be logged at a certain time.

    This is mainly used for histories and transactions, but can be added as an parent class to any ORM
    class that needs a time stamp.
    """
    created = Column(DateTime, default=datetime.now())


# Assigns the custom base class for use in the ORM.
Base = declarative_base(cls=Base)


# Association tables for many-to-many relationships
favorite_reports = Table('favorite_reports', Base.metadata,
                         Column('report_id', ForeignKey('reports.id'), primary_key=True),
                         Column('user_id', ForeignKey('users.id'), primary_key=True))

fee_waivers = Table('fee_waivers', Base.metadata,
                    Column('exception', ForeignKey('ruleexceptions.id'), primary_key=True),
                    Column('fee_id', ForeignKey('fees.id'), primary_key=True))

inventory_waivers = Table('inventory_waivers', Base.metadata,
                          Column('exception', ForeignKey('ruleexceptions.id'), primary_key=True),
                          Column('inventory_id', ForeignKey('inventories.id'), primary_key=True))


