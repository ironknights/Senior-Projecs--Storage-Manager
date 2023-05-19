# Author's Notes ######################################################################################################
"""
Program: SOLO
File Purpose: Edit Reports Tab Viewer
Language: Python 3
Author: Cameron Howard
"""


# Imports #############################################################################################################
from src.UserInterface.Tabs.MainTab.MainTab_controller import MainTabController
from src.UserInterface.Tabs.Tools.EditReports.EditReports_View import EditReportsView
from src.UserInterface.Windows.Report.CustomReport_Controller import CustomReportWindow
from src.UserInterface.Windows.Report.NewReport_Controller import NewReportWindow


# Class Definition ####################################################################################################
class EditReports(MainTabController):
    def __init__(self, window, key="_EDIT_REPORTS_", title="Edit Reports"):
        super().__init__(window, key, EditReportsView, title)
        self.load()

    def load(self):
        pass

    def process_event(self, event, values):
        # Report selected
        if event == '_EDIT_REPORT_OPTIONS_':
            tables = []
            table_values = []

            # Get the list of tables / fields from database
            tables_list = self.window.database.ReportModel.get_tables_list()
            for table in tables_list:
                col_vals = []
                tables.append(table.name)
                for col in table.c:
                    col_vals.append(col.name)
                table_values.append(col_vals)

            # Format variables
            menu_option = (values['_EDIT_REPORT_OPTIONS_'][0]).replace('_', '')
            report_fields = self.window.database.ReportModel.get_report_fields(menu_option)
            default = report_fields[0]

            self.open(CustomReportWindow(tables, table_values, default, menu_option))

        # Otherwise, open creation window
        elif event == '_CREATE_NEW_':
            self.open(NewReportWindow())

    def refresh(self):
        pass
