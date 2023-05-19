"""Code written by Deeptanshu Das unless otherwise specified."""

import PySimpleGUI as Gui
from src.UserInterface.Tabs.MainTab.MainTab_viewer import MainTabViewer
from src.DatabaseORM.sitemap_orm import MapUnit, MapLine
from src.DatabaseModel.sitemap_model import MapModel
from src.DatabaseORM.unit_orm import Unit

scalar = 5
Unit_spacing = 10



class MapsView(MainTabViewer):
    """Class for the MapsView"""

    def __init__(self, window, key, tab_title):
        super().__init__(window, key, tab_title)

    def create_layout(self):
        """This creates the Graph layouts that would represent the maps"""
        graph = Gui.Graph(canvas_size=(500, 500), graph_bottom_left=(0, 0), graph_top_right=(500, 500),
                          background_color=None, pad=None, change_submits=False, drag_submits=False,
                          enable_events=False,
                          key="Graphs", tooltip=None, right_click_menu=None, visible=True, float_values=False,
                          metadata=None)

        layout = [graph]

        return layout

    def draw_all_lines(self):
        """This method iterates over all the lines and draws lines on the canvas"""
        lines = self.window.database.MapModel.get_all_lines()
        for line in lines:
            self.draw_line(line)

    def draw_all_units(self):
        """This method iterates over all the units and draws units on the canvas"""
        units = self.window.database.MapModel.get_all_units()
        for unit in units:
            self.draw_unit_on_map(unit)

    def draw_line(self, map_line):
        """This function draws line on the canvas"""
        self.window.window["Graphs"].DrawLine((map_line.x1, map_line.y1), (map_line.x2, map_line.y2))

    def get_bottom_point(self, map_unit):
        """This function sets the bottom coordinates for the graphs"""
        x = map_unit.x + float(map_unit.unit.size.width) * scalar
        y = map_unit.y + float(map_unit.unit.size.width) * scalar
        return x, y

    def draw_unit_on_map(self, map_unit):
        """This function draws the units on the canvas"""
        bot_x, bot_y = self.get_bottom_point(map_unit)
        color = self.get_unit_color(map_unit.unit)

        var = map_unit.unit.identifier

        mid_x = ((map_unit.x + bot_x)/2)

        mid_y = ((map_unit.y + bot_y)/2)

        self.window.window["Graphs"].DrawRectangle(top_left=(map_unit.x, map_unit.y), bottom_right=(bot_x, bot_y), fill_color=color)
        self.window.window["Graphs"].DrawText(var, location=(mid_x, mid_y), text_location="center")

    @staticmethod
    def get_unit_color(map_unit):
        """This function gets the unit colors for either vacant or occupied units"""
        if map_unit.status == "Vacant":
            return 'green'
        elif map_unit.status == "Occupied":
            return 'grey'

    def create_tab(self):
        """Creates the tabs"""
        return Gui.Tab(self.title, [self.layout], key=self.key)

    def refresh(self):
        pass
