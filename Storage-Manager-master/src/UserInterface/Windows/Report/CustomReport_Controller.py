# Author's Notes ######################################################################################################
"""
Program: SOLO
File Purpose: Custom Report Window Viewer
Language: Python 3
Author: Cameron Howard
"""


# Imports #############################################################################################################
from src.UserInterface.Windows.Window.window_controller import WindowController
from src.UserInterface.Windows.Report.CustomReport_View import CustomReportWindowView


# Class Definition ####################################################################################################
class CustomReportWindow(WindowController):
    # Self Init
    def __init__(self, table_list, table_fields, default_table, menu_option):
        self.tables = table_list
        self.table_choices = table_fields
        self.default_table = default_table
        self.report = menu_option
        super().__init__(CustomReportWindowView, "Custom Report")
        self.load()

    # Load
    def load(self):
        pass

    # Process Events
    def process_event(self, event, values):
        if not event:
            return self.shutdown()

        # Table selected from combobox
        if event == '_REPORT_SELECTED_':
            table = values['_REPORT_SELECTED_']
            table_num = self.tables.index(table)

            # Update the listbox with the correct fields for the table
            self.window.Element('_FIELDS_').Update(values=self.table_choices[table_num])

        # Save button pressed
        elif event == '_SAVE_REPORT_':
            # Check for selection
            if len(values['_FIELDS_']) != 0:
                filter_vals = values['_REPORT_SELECTED_']

                # Create the modified string
                for items in values['_FIELDS_']:
                    filter_vals += ';' + items

                # Update the database and close the window
                self.database.ReportModel.update_database(self.report, filter_vals)
                self.shutdown()

            # Otherwise, do nothing
            else:
                print('Select values!')

        return True

    # Refresh
    def refresh(self):
        pass

    # Shutdown
    def shutdown(self):
        self.window.close()
        return False
