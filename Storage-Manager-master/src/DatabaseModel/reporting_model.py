# Author's Notes ######################################################################################################
"""
Program: SOLO
File Purpose: Report Database Model
Language: Python 3
Author: Cameron Howard
"""


# Imports #############################################################################################################
from .base_model import BaseModel
from src.DatabaseORM.reporting_orm import Report
from sqlalchemy import MetaData


# Class Definition ####################################################################################################
class ReportModel(BaseModel):
    # Report Menu Categories
    def get_menu_categories(self):
        return self.session.query(Report).filter(Report.category == 'Main').all()

    # Report Menu Options
    def get_menu_options(self, category_name):
        return self.session.query(Report).filter(Report.category == category_name).all()

    # Get Report
    def get_report(self, report_title):
        return self.session.query(Report).filter_by(title=report_title).all()

    # Report Fields
    def get_report_fields(self, title):
        filter_vals = self.session.query(Report).filter(Report.title == title).all()

        # If the search contains something, split the modified string into a list and return
        if len(filter_vals) != 0:
            filt = [f.filter_values for f in filter_vals]
            return [str(x) for x in filt[0].split(';')]

        return []

    # Generate Report Search String
    def generate_search(self, report_title):
        search_values = self.get_report_fields(report_title)
        search_string = 'select'
        table = search_values[0]

        search_values.pop(0)

        for item in search_values:
            search_string += (' ' + item + ',')

        search_string = search_string[:-1]
        search_string += ' from ' + table

        return search_string

    # Update Report Table
    def update_database(self, title, field_string):
        self.session.query(Report).filter(Report.title == title).\
            update({Report.filter_values: field_string})
        self.session.commit()

        search_string = self.generate_search(title)
        self.session.query(Report).filter(Report.title == title).\
            update({Report.filter_string: search_string})
        self.session.commit()

    # Add New Report
    def add_report(self, title, category, description):
        new_report = Report(
            title=title,
            category=category,
            description=description,
            filter_string='',
            filter_values='',
            contains_ssn=False
        )

        self.session.add(new_report)
        self.session.commit()

    # Get Table List
    def get_tables_list(self):
        m = MetaData()
        m.reflect(self.database.engine)
        return m.tables.values()


class FormModel(BaseModel):
    pass
