"""Code written by Jacquesne Jones unless otherwise specified."""

from src.UserInterface.Windows.Window.window_controller import Gui
from src.UserInterface.Windows.Window.window_viewer import WindowViewer


class LinkWindowView(WindowViewer):
    def __init__(self, controller, window_title=None):
        self.unit = controller.unit
        self.cur_links = controller.database.UnitModel.get_link_list(self.unit)
        self.available = controller.database.UnitModel.get_unlinked_list(self.unit)
        self.link_list = []
        self.link_text = "   Currents links"
        super().__init__(controller, window_title)

    def create_layout(self):
        column1 = [
            [Gui.T(f"Current links for {self.unit.identifier}:")],
            [Gui.Listbox(self.cur_links, size=(20, 20), key="_CURRENT_BOX_",
                         bind_return_key=True)]
        ]
        text_width = 1
        column2 = [
            [Gui.T("Search:")],
            [Gui.T(" " * text_width)],
            [Gui.T(" " * text_width)],
            [Gui.T(" " * text_width)],
            [Gui.B("<<", key="_ADD_")],
            [Gui.B(">>", key="_REMOVE_")]
        ]
        column3 = [
            [Gui.I(key="_SEARCH_", size=(20, 1)), Gui.T(self.link_text, key="_CURRENT_LINK_", size=(20, 1))],
            [Gui.Listbox(self.available, size=(20, 20), key="_ADD_BOX_",
                         bind_return_key=True),
             Gui.Listbox(self.link_list, key="_SHOW_LINKS_", size=(20, 20), background_color="grey")]
        ]
        layout = [
            [Gui.Column(column1), Gui.Column(column2), Gui.Column(column3)],
            [Gui.B("Link", key="_LINK_"), Gui.B("Cancel")]
        ]
        return layout

    def create_window(self):
        return Gui.Window("Link", self.layout)

    def show_links(self, values):
        """Updates links when changed"""
        unit = self.database.UnitModel.get_by_name(values[0])
        link_list = self.database.UnitModel.get_link_list(unit)
        self.window["_SHOW_LINKS_"](link_list)
        self.window["_CURRENT_LINK_"](f"{self.link_text} for {values[0]}")
