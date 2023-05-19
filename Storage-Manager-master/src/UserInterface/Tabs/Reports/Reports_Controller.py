# Author's Notes ######################################################################################################
"""
Program: SOLO
File Purpose: Reports Tab Controller
Language: Python 3
Author: Cameron Howard
"""


# Imports #############################################################################################################
import csv
from src.UserInterface.Tabs.MainTab.MainTab_controller import MainTabController
from src.UserInterface.Tabs.Reports.Reports_View import ReportsView
from src.UserInterface.Windows.Report.Report_Controller import ReportWindow

padding = 25


# Class Definition ####################################################################################################
# Export CSV
def to_csv(table):
    writer = csv.writer(open('report.csv', 'w'))
    for row in table:
        writer.writerow(row)


class Reports(MainTabController):
    # Self Init
    def __init__(self, window, key="_REPORTS_", title=f"{' ' * padding}Reports{' ' * padding}"):
        super().__init__(window, key, ReportsView, title)
        self.load()

    # Load
    def load(self):
        # Do nothing
        pass

    # Process Events
    def process_event(self, event, values):
        # Check for appropriate event trigger
        if event == '_LOAD_REPORT_' or event == '_EXPORT_':
            menu_option = (values['_REPORT_OPTIONS_'][0]).replace('_', '')
            report = self.window.database.ReportModel.get_report(menu_option)

            # Check that report is valid
            if len(report) != 0:
                search_filter = [sf.filter_string for sf in report]
                category = [sf.category for sf in report]

                # Check that it is actually a report, not just a category
                if category[0] != 'Main' and len(search_filter[0]) != 0:
                    # Execute the search_filter sql statement
                    with self.window.database.engine.connect() as con:
                        result = con.execute(search_filter[0])
                        table_headers = result.keys()
                        table_values = [[value for column, value in row.items()] for row in result]

                        # If valid, open report or export it
                        if len(table_values) != 0:
                            if event == '_LOAD_REPORT_':
                                self.open(ReportWindow(table_headers, table_values))

                            elif event == '_EXPORT_':
                                table = [table_headers]
                                for item in table_values:
                                    table.append(item)

                                to_csv(table)

    # Refresh
    def refresh(self):
        # Do nothing
        pass
