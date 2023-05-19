"""Code written by Jacquesne Jones unless otherwise specified."""

from src.UserInterface.Windows.Window.window_controller import WindowController
from .Links_view import LinkWindowView


class LinkWindow(WindowController):
    """Window to set and remove links between units."""
    def __init__(self, controller, key):
        self.unit = controller.database.UnitModel.get(key)
        super().__init__(LinkWindowView, "Link Units")
        self.add_links = []
        self.remove_links = []
        self.add_box_selected = None
        self.load()

    def load(self):
        self.window = self.view.window

    def process_event(self, event, values):
        if event in (None, "Cancel"):
            return self.shutdown()
        if event in ("_REMOVE_", "_CURRENT_BOX_"):
            self.change_link(values["_CURRENT_BOX_"],
                             self.add_links, self.remove_links, self.view.available, self.view.cur_links)
        elif event in ("_ADD_", "_ADD_BOX_"):
            self.change_link(values["_ADD_BOX_"],
                             self.remove_links, self.add_links, self.view.cur_links, self.view.available)
        elif event == "_LINK_":
            self.link_units()
        else:
            if values["_ADD_BOX_"] and self.add_box_selected != values["_ADD_BOX_"]:
                self.add_box_selected = values["_ADD_BOX_"]
                self.window["_SHOW_LINKS_"](self.view.show_links(values["_ADD_BOX_"]))
        return True

    def refresh(self):
        pass

    def shutdown(self):
        self.window.close()
        return False

    def change_link(self, values, old_items, new_items, new_list, old_list):
        """Changes link values depending on what has been changed"""
        for item in values:
            # If the item was already moved, just remove it, otherwise add it to the new list
            if item in old_items:
                old_items.remove(item)
            else:
                new_items.append(item)
            # Change lists
            new_list.append(item)
            old_list.remove(item)
        # Sort lists
        self.view.available.sort()
        self.view.cur_links.sort()
        # Update lists
        self.window["_ADD_BOX_"](self.view.available)
        self.window["_CURRENT_BOX_"](self.view.cur_links)

    def link_units(self):
        """Link specific units together"""
        # If nothing is left linked, remove self from groups as well
        if not self.view.cur_links:
            self.remove_links.append(self.unit.identifier)
        # Add self if adding to group
        if len(self.add_links) > 0:
            self.add_links.append(self.unit.identifier)
        # Remove orphaned group members

        self.database.UnitModel.update_links(self.add_links, self.remove_links)
        self.window.close()
