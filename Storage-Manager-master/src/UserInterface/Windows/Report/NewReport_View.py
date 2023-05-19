# Author's Notes ######################################################################################################
"""
Program: SOLO
File Purpose: New Report Window Viewer
Language: Python 3
Author: Cameron Howard
"""


# Imports #############################################################################################################
from src.UserInterface.Windows.Window.window_controller import Gui
from src.UserInterface.Windows.Window.window_viewer import WindowViewer


# Class Definition ####################################################################################################
class NewReportWindowView(WindowViewer):
    # Self Init
    def __init__(self, controller, window_title=None):
        super().__init__(controller, window_title)

    # Create Window Layout
    def create_layout(self):
        # Create and return the layout for the window
        layout = [
            [Gui.Text('Enter report title: '),
             Gui.InputText()],
            [Gui.Text('Enter report category: '),
             Gui.InputText()],
            [Gui.Text('Enter report description: '),
             Gui.InputText()],
            [Gui.Button('Save', key='_SAVE_NEW_')]
        ]

        return layout

    # Create Window
    def create_window(self):
        return Gui.Window(self.title, self.layout, resizable=True)
