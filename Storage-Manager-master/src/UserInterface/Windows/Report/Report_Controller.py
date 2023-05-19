# Author's Notes ######################################################################################################
"""
Program: SOLO
File Purpose: Report Window Viewer
Language: Python 3
Author: Cameron Howard
"""


# Imports #############################################################################################################
from src.UserInterface.Windows.Window.window_controller import WindowController
from src.UserInterface.Windows.Report.Report_View import ReportWindowView


# Class Definition ####################################################################################################
class ReportWindow(WindowController):
    # Self Init
    def __init__(self, headers, data):
        self.table_headers = headers
        self.table_data = data
        super().__init__(ReportWindowView, "Report")
        self.load()

    # Load
    def load(self):
        pass

    # Process Events
    def process_event(self, event, values):
        if not event:
            return self.shutdown()
        return True

    # Refresh
    def refresh(self):
        pass

    # Shutdown
    def shutdown(self):
        self.window.close()
        return False
