# Author's Notes ######################################################################################################
"""
Program: SOLO
File Purpose: New Report Window Controller
Language: Python 3
Author: Cameron Howard
"""


# Imports #############################################################################################################
from src.UserInterface.Windows.Window.window_controller import WindowController
from src.UserInterface.Windows.Report.NewReport_View import NewReportWindowView


# Class Definition ####################################################################################################
class NewReportWindow(WindowController):
    # Self Init
    def __init__(self):
        super().__init__(NewReportWindowView, "New Report")
        self.load()

    # Load
    def load(self):
        pass

    # Process Events
    def process_event(self, event, values):
        if not event:
            return self.shutdown()

        if event == '_SAVE_NEW_':
            title = str(values[0])
            category = str(values[1])
            desc = str(values[2])

            if len(title) == 0 or len(category) == 0:
                print('Enter in values!')

            else:
                self.database.ReportModel.add_report(title, category, desc)
                self.shutdown()

        return True

    # Refresh
    def refresh(self):
        pass

    # Shutdown
    def shutdown(self):
        self.window.close()
        return False
