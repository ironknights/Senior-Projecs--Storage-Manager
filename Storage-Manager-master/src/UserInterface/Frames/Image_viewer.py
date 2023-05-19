"""Code written by Deeptanshu Das unless otherwise specified."""

import PySimpleGUI as Gui


class ImageViewer:
    """class Image  """

    def __init__(self, images):
        self.images = []
        self.view = self.create_view()

    # @staticmethod
    def create_view(self):
        """Creates the image viewing Gui"""
        img_list = []
        for image in self.images:
            img_list.append(Gui.Image(image, enable_events=True, size=(360, 330)))

        button = [Gui.B("Add"), Gui.B("Load"), Gui.B("Remove")]

        column_var = [img_list]

        column = [Gui.Column(column_var, scrollable=True, size=(370, 180))]

        layout = [column, button]

        return Gui.Frame("Images", layout, size=(200, 200))


