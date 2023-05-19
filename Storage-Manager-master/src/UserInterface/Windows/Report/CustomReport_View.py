# Author's Notes ######################################################################################################
"""
Program: SOLO
File Purpose: Custom Report Window Viewer
Language: Python 3
Author: Cameron Howard
"""


# Imports #############################################################################################################
from src.UserInterface.Windows.Window.window_controller import Gui
from src.UserInterface.Windows.Window.window_viewer import WindowViewer


# Class Definition ####################################################################################################
class CustomReportWindowView(WindowViewer):
    # Self Init
    def __init__(self, controller, window_title=None):
        self.table_list = controller.tables
        self.table_fields = controller.table_choices
        self.default = controller.default_table
        self.report = controller.report
        super().__init__(controller, window_title)

    # Create Window Layout
    def create_layout(self):
        if len(self.default) == 0:
            self.default = self.table_list[0]
        index = self.table_list.index(self.default)
        fields = self.table_fields[index]

        # Create and return the layout for the window
        layout = [
            [Gui.Text('Select a table: '),
             Gui.Combo(self.table_list, key='_REPORT_SELECTED_', enable_events=True, default_value=self.default)],
            [Gui.Text('Select fields: '),
             Gui.Listbox(values=fields, select_mode=Gui.LISTBOX_SELECT_MODE_MULTIPLE, size=(10, 8), key='_FIELDS_',
                         enable_events=True)],
            [Gui.Button('Save', key='_SAVE_REPORT_')]
        ]

        return layout

    # Create Window
    def create_window(self):
        return Gui.Window(self.title, self.layout, resizable=True)
