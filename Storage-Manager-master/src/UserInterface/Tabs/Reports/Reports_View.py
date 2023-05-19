# Author's Notes ######################################################################################################
"""
Program: SOLO
File Purpose: Reports Tab Viewer
Language: Python 3
Author: Cameron Howard
"""


# Imports #############################################################################################################
import PySimpleGUI as Gui
from src.UserInterface.Tabs.MainTab.MainTab_viewer import MainTabViewer


# Class Definition ####################################################################################################
class ReportsView(MainTabViewer):
    # Self Init
    def __init__(self, window, key, tab_title):
        self.report_categories = []
        self.report_menu = []
        super().__init__(window, key, tab_title)

    # Create Window Layout
    def create_layout(self):
        # Declare and populate the treedata with all the menu options
        treedata = Gui.TreeData()

        # Load the report categories
        result = self.window.database.ReportModel.get_menu_categories()
        self.report_categories = [option.title for option in result]

        # Load the report menu
        for name in self.report_categories:
            result = self.window.database.ReportModel.get_menu_options(name)
            m = [option.title for option in result]
            self.report_menu.append(m)

        # Load treedata
        for category, menu in zip(self.report_categories, self.report_menu):
            # Put the menu header, then remove it from the list
            header = category
            treedata.Insert("", '_' + header + '_', header, [header])

            # The options within each menu
            for option in menu:
                treedata.Insert('_' + header + '_', '_' + option + '_', option, [option])

        # Create and return the layout for the window
        layout = [
            [Gui.Button('Load', key='_LOAD_REPORT_'), Gui.Button('Export', key='_EXPORT_')],
            [Gui.Text('Select a report.')],
            [Gui.Tree(data=treedata, headings=[], auto_size_columns=True, num_rows=30, show_expanded=True,
                      col0_width=25, key='_REPORT_OPTIONS_', enable_events=True, change_submits=True)]
        ]

        return layout

    # Create Tab
    def create_tab(self):
        return Gui.Tab(self.title, self.layout, key=self.key)
