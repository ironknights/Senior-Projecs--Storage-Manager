"""Code written by Emerson Havener unless otherwise specified."""

from src.UserInterface.Windows.Window.window_controller import Gui
from src.UserInterface.Windows.Window.window_viewer import WindowViewer
from src.DatabaseModel.format import state_list
import os

cwd = os.getcwd()


class MoveInView(WindowViewer):
    inputSize = (20, 1)
    labelSize = (15, 1)
    checkboxPadding = ((105, 0), (0, 0))
    vehicleInputsDisabled = False

    def __init__(self, controller, window_title=None):
        self.unit = controller.unit
        self.frame = controller.img_controller.viewer
        super().__init__(controller, window_title)

    def create_layout(self):
        primary = [
            [Gui.Text(text='Last name', size=self.labelSize), Gui.Input(
                size=self.inputSize, key='_LAST_')],
            [Gui.Text(text='M', size=self.labelSize), Gui.Input(
                size=self.inputSize, key='_MIDDLE_')],
            [Gui.Text(text='First name', size=self.labelSize), Gui.Input(
                size=self.inputSize, key='_FIRST_')],
            [Gui.Text(text='Address', size=self.labelSize), Gui.Input(
                size=self.inputSize, key='_ADDR1_')],
            [Gui.Text(text='Line 2', size=self.labelSize), Gui.Input(
                size=self.inputSize, key='_ADDR2_')],
            [Gui.Text(text='City', size=self.labelSize), Gui.Input(
                size=self.inputSize, key='_CITY_')],
            [Gui.Text(text='State', size=self.labelSize), Gui.Combo(
                values=(list(state_list(long=True))), size=self.inputSize, key='_STATE_ID_')],
            [Gui.Text(text='Zip Code', size=self.labelSize), Gui.Input(
                size=self.inputSize, key='_ZIP_')],
            [Gui.Text(text='Country', size=self.labelSize), Gui.Combo(
                values=('United\ States'), size=self.inputSize, key='_COUNTRY_')],
            [Gui.Text(text='Cell', size=self.labelSize), Gui.Input(
                size=self.inputSize, key='_CELL_')],
            [Gui.Text(text='Phone', size=self.labelSize), Gui.Input(
                size=self.inputSize, key='_PHONE_')],
            [Gui.Text(text='Email', size=self.labelSize), Gui.Input(
                size=self.inputSize, key='_EMAIL_')],
            [Gui.Text(text='Company', size=self.labelSize), Gui.Input(
                size=self.inputSize, key='_COMPANY_')],
            [Gui.Checkbox('Web Access', size=self.inputSize,
                          pad=self.checkboxPadding, key='_WEB_ACCESS_')]
        ]

        alternate = [
            [Gui.Text(text='Last name', size=self.labelSize), Gui.Input(
                size=self.inputSize, key='_ALT_LAST_')],
            [Gui.Text(text='M', size=self.labelSize), Gui.Input(
                size=self.inputSize, key='_ALT_MIDDLE_')],
            [Gui.Text(text='First name', size=self.labelSize), Gui.Input(
                size=self.inputSize, key='_ALT_FIRST_')],
            [Gui.Text(text='Address', size=self.labelSize), Gui.Input(
                size=self.inputSize, key='_ALT_ADDR1_')],
            [Gui.Text(text='Line 2', size=self.labelSize), Gui.Input(
                size=self.inputSize, key='_ALT_ADDR2_')],
            [Gui.Text(text='City', size=self.labelSize), Gui.Input(
                size=self.inputSize, key='_ALT_CITY_')],
            [Gui.Text(text='State', size=self.labelSize), Gui.Combo(
                values=(list(state_list(long=True))), size=self.inputSize, key='_ALT_STATE_')],
            [Gui.Text(text='Zip Code', size=self.labelSize), Gui.Input(
                size=self.inputSize, key='_ALT_ZIP_')],
            [Gui.Text(text='Country', size=self.labelSize), Gui.Combo(
                values=('United States'), size=self.inputSize, key='_ALT_COUNTRY_')],
            [Gui.Text(text='Cell', size=self.labelSize), Gui.Input(
                size=self.inputSize, key='_ALT_CELL_')],
            [Gui.Text(text='Phone', size=self.labelSize), Gui.Input(
                size=self.inputSize, key='_ALT_PHONE_')],
            [Gui.Text(text='Email', size=self.labelSize), Gui.Input(
                size=self.inputSize, key='_ALT_EMAIL_')]
        ]

        layout = Gui.TabGroup([[Gui.Tab('Primary', primary), Gui.Tab(
            'Alternate', alternate)]])

        return [
            [
                Gui.Button('Cancel', size=(12, 2)),
                Gui.Text(f'Unit: {self.unit.identifier}'),
                Gui.Text(f'Size: {self.unit.size_string}'),
                Gui.Text(f'Price: {self.unit.price_string}'),
                Gui.Button('Submit', size=(12, 2))
            ],
            [
                Gui.Column([[layout]]),
                Gui.Column([
                    [Gui.Frame("Details", [
                        [Gui.Text(text='Drivers License', size=self.labelSize), Gui.Input(size=self.inputSize, justification='left',
                                                                                          key='_LICENSE_NUM_')],
                        [Gui.Text(text='State', size=self.labelSize), Gui.Combo(
                            values=(list(state_list(long=True))), size=self.inputSize, key='_LICENSE_STATE_')],
                        [Gui.Text(text='SSN', size=self.labelSize), Gui.Input(size=self.inputSize,
                                                                              key='_SSN_')],
                        [Gui.Text(text='Lease Number', size=self.labelSize), Gui.Input(size=self.inputSize,
                                                                                       key='_LEASE_')],
                        [Gui.Text(text='Tax ID', size=self.labelSize), Gui.Input(size=self.inputSize,
                                                                                 key='_TAX_ID_', disabled=True)]
                    ])],
                    [Gui.Frame("Gate", [
                        [Gui.Text(text='Gate Code', size=self.labelSize), Gui.Input(size=self.inputSize,
                                                                                    key='_GATE_CODE_')],
                        [Gui.Text(text='Access Time', size=self.labelSize), Gui.Combo(
                            values=('24-Hour'), size=self.inputSize, key='_ACCESS_')],
                        [Gui.Checkbox(
                            'Never Lock', size=self.inputSize, pad=self.checkboxPadding, key='_NEVER_LOCK_')],
                        [Gui.Checkbox(
                            'Deactivate', size=self.inputSize, pad=self.checkboxPadding, key='_DEACTIVATE_GATE_')]
                    ])]
                ]),
                Gui.Column([
                    [self.frame.view],
                    [Gui.Frame("Vehicle", [
                        [Gui.Text(text='VIN', size=self.labelSize), Gui.Input(size=self.inputSize,
                                                                              key='_VEHICLE_VIN_', disabled=True)],
                        [Gui.Text(text='License Plate', size=self.labelSize), Gui.Input(size=self.inputSize,
                                                                                        key='_PLATE_NUM_', disabled=True)],
                        [Gui.Text(text='State', size=self.labelSize), Gui.Input(size=self.inputSize,
                                                                                key='_VEHICLE_STATE_', disabled=True)],
                        [Gui.Text(text='Insurance Number', size=self.labelSize), Gui.Input(size=self.inputSize,
                                                                                           key='_INSURANCE_NUM_', disabled=True)],
                        [Gui.Text(text='Lien Holder', size=self.labelSize), Gui.Input(size=self.inputSize,
                                                                                      key='_LIEN_HOLDER_', disabled=True)]
                    ])],
                ])
            ]
        ]

    def create_window(self):
        return Gui.Window(self.title, self.layout)
