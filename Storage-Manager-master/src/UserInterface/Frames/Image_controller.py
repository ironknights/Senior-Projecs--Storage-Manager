"""Code written by Deeptanshu Das unless otherwise specified."""

import zipfile
from zipfile import ZipFile
from src.UserInterface.Frames.Image_viewer import ImageViewer
import PySimpleGUI as sg
import os
from src.DatabaseORM.unit_orm import Unit
from src.DatabaseORM.tenant_orm import Tenant
import ntpath


# TODO: Bring up the browse files option
# TODO: Add the files to the Container(zip)
# TODO: Make sub-folders in the zip file - Tenant or Unit
# TODO: Store the zip file in the same directory


class ImageController:
    """Base class for Image Controller"""

    def __init__(self, data_object, images):
        # Load the function to load all the images
        self.viewer = ImageViewer(images)
        self.fname = None
        self.data_object = data_object

    def process_event(self, event, values):
        """processes the add functionality"""

        # If event is in "Add" bring up the browse files option
        if event == "Add":
            self.fname = sg.Window('Image Browser',
                                  [[sg.Text('Image to add')],
                                   [sg.In(), sg.FileBrowse()],
                                   [sg.Open(), sg.Cancel()]]).read(close=True)[1][0]

            if not self.fname:
                sg.popup("Cancel", "No filename supplied")
                # raise SystemExit("Cancelling: no filename supplied")
            else:
                sg.popup('The filename you chose was', self.fname)

                self.image_save()

    def image_save(self):
        """This method saves the images into a zip file. The zip file is stored
        in a container fashion. The images are stored in terms of their unit id and
        their unit names. Once stored it will be stored sequentially with files"""
        if type(self.data_object) == Unit:
            with ZipFile('Images.zip', 'a') as myzip:
                var = self.data_object.id
                end = ntpath.basename(self.fname)
                myzip.write(os.path.join('Images.zip', self.fname), "Unit/" + str(var) + "/Images/" + end, zipfile.ZIP_DEFLATED)

                # myzip.write(self.fname, "Unit/" + str(var) + self.fname, zipfile.ZIP_DEFLATED)
                myzip.close()

        elif type(self.data_object) == Tenant:
            with ZipFile('Images.zip', 'a') as myzip:
                var = self.data_object.id
                end = ntpath.basename(self.fname)
                myzip.write(os.path.join('Images.zip', self.fname), "Tenant/" + str(var) + "/Image/" + end, zipfile.ZIP_DEFLATED)

                # myzip.write(self.fname, "Tenant/" + str(var) + self.fname, zipfile.ZIP_DEFLATED)
                myzip.close()


    def image_load(self):
     """
     loop through the images

     self.images = read all images from Images.zip
    for image in self.images:
        img_list.append(Gui.Image(image, enable_events=True, size=(360, 330)))

     :return:
     """






