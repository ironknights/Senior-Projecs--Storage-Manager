# Author's Notes ######################################################################################################
"""
Program: SOLO
File Purpose: Report Window Viewer
Language: Python 3
Author: Cameron Howard

Note:
    This window can be turned into a table within the main window once PySimpleGUI implements header
    changes in their table update. Or by using a different GUI framework that can handle such updates.
"""


# Imports #############################################################################################################
from src.UserInterface.Windows.Window.window_controller import Gui
from src.UserInterface.Windows.Window.window_viewer import WindowViewer


# Class Definition ####################################################################################################
class ReportWindowView(WindowViewer):
    # Self Init
    def __init__(self, controller, window_title=None):
        self.data = controller.table_data
        self.headers = controller.table_headers
        super().__init__(controller, window_title)

    # Create Window Layout
    def create_layout(self):
        layout = [
            [Gui.Table(self.data, headings=self.headers, bind_return_key=True, pad=10, num_rows=30,
                       alternating_row_color='#97FFFF', justification='center', key="_REPORT_TABLE_")]
        ]

        return layout

    # Create Window
    def create_window(self):
        return Gui.Window(self.title, self.layout, resizable=True)
