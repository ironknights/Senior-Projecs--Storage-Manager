"""Code written by Jacquesne Jones unless otherwise specified."""

from .base_orm import Base, favorite_reports
from sqlalchemy import String, Boolean, Column
from sqlalchemy.orm import relationship


class Report(Base):
    """A report used for analyzing data.

    The design of a report is for easy data access.
    title, category, and description are primarily used to display information to the user and organize the table.
    filter_string and filter_values define the SQL statement used to pull information for the report.
    contain_ssn is a flag used to restrict access to reports with potentially sensitive information from those
    not authorized to access it.
    """
    title = Column(String, unique=True)
    category = Column(String)
    description = Column(String)
    filter_string = Column(String)
    filter_values = Column(String)
    contains_ssn = Column(Boolean)

    user = relationship('User', secondary=favorite_reports, back_populates='report_favorite')


class Form(Base):
    """Forms are graphical templates used for mass mailing and to format reports in PDF or doc output."""
    title = Column(String)
    category = Column(String)
    filename = Column(String)
