"""Code written by Emerson Havener unless otherwise specified."""

from src.UserInterface.Windows.Window.window_controller import Gui
from src.UserInterface.Windows.Window.window_viewer import WindowViewer
from src.UserInterface.Frames.Transactions.transaction_controller import TransactionFrame
from src.UserInterface.Frames.History.history_controller import HistoryFrame
from src.DatabaseModel.format import date_format
import time
import tkinter


class PaymentView(WindowViewer):
    inputSize = (15, 1)
    labelSize = (15, 1)

    def __init__(self, controller, window_title=None):
        self.tenant = controller.tenant
        self.transactions = controller.transactions
        self.histories = controller.histories
        self.image_viewer_frame = controller.img_controller.viewer
        super().__init__(controller, window_title)

    def refresh(self):
        pass

    def create_layout(self):
        tenant_address = [
            [Gui.Text(f'{self.tenant.last}, {self.tenant.first}',
                      size=(64, 1))],
            [Gui.Text(self.tenant.addr1, size=(64, 1))],
            [Gui.Text(
                f'{self.tenant.city}, {self.tenant.state_string}, {self.tenant.zip}', size=(64, 1))],
        ]

        tenant_vehicle = [
            [Gui.Text(f'VIN: {self.tenant.vehicle_vin}')],
            [Gui.Text(f'License Plate: {self.tenant.plate_num}')],
            [Gui.Text(f'State: {self.tenant.vehicle_state}')],
            [Gui.Text(f'Insurance #: {self.tenant.insurance_num}')],
            [Gui.Text(f'Lien Holder: {self.tenant.lien_holder}')]
        ]

        tenant_access = [
            [Gui.Text(f'Web Access: {self.tenant.web_access}')],
            [Gui.Text(f'Gate Code: {self.tenant.gate_code}')],
            [Gui.Text(f'Access Time: {self.tenant.access_id}')],
            [Gui.Text(f'Never Lock: {self.tenant.never_lock}')],
            [Gui.Text(f'Deactivate: {self.tenant.deactivate_gate}')]
        ]

        tenant_notes = [
            # [Gui.Text(f'Notes: {self.tenant.notes}')],
        ]

        tenant = Gui.TabGroup([[Gui.Tab('Address', tenant_address), Gui.Tab(
            'Vehicle', tenant_vehicle), Gui.Tab('Access', tenant_access), Gui.Tab('Notes', tenant_notes)]])

        photos = self.image_viewer_frame.view

        notes = []

        balances = []

        for transaction in self.transactions:
            if (float(transaction.amount) < 0):
                balances.append([Gui.Checkbox(
                    f'{date_format(transaction.created)}    {transaction.amount_string}    {transaction.category_string}', key=f'_TOGGLE_BALANCE_id={transaction.id}', enable_events=True)])

        balance_details = [],

        payment_form = [
            Gui.Column([
                [Gui.Text('')],
                [Gui.Text('Rent')],
                [Gui.Text('Deposit')],
                [Gui.Text('Late Fee')],
                [Gui.Text('PLien Fee')],
                [Gui.Text('Lien Fee')],
                [Gui.Text('Credit')],
                [Gui.Text('Insurance')],
                [Gui.Text('Cut Lock')],
                [Gui.Text('Advertising')],
                [Gui.Text('Total')]
            ]),
            Gui.Column([
                [Gui.Text('Due')],
                [Gui.Text(f'${self.controller.payableRentChargeBalance}',
                          key='_PAYABLE_RENT_CHARGE_TEXT_', size=self.inputSize)],
                [Gui.Text('$0.00', size=self.inputSize)],
                [Gui.Text(f'${self.controller.payableLateFeeBalance}',
                          key='_PAYABLE_LATE_FEE_TEXT_', size=self.inputSize)],
                [Gui.Text('$0.00', size=self.inputSize)],
                [Gui.Text('$0.00', size=self.inputSize)],
                [Gui.Text('$0.00', size=self.inputSize)],
                [Gui.Text('$0.00', size=self.inputSize)],
                [Gui.Text('$0.00', size=self.inputSize)],
                [Gui.Text('$0.00', size=self.inputSize)],
                [Gui.Text('$0.00', size=self.inputSize)],
            ]),
            Gui.Column([
                [Gui.Text('Payment')],
                [Gui.Input(key='_RENT_PAYMENT_', size=self.inputSize)],
                [Gui.Input(key='_DEPOSIT_PAYMENT_', size=self.inputSize)],
                [Gui.Input(key='_LATE_FEE_', size=self.inputSize)],
                [Gui.Input(key='_PLIEN_FEE_', size=self.inputSize)],
                [Gui.Input(key='_LIEN_FEE_', size=self.inputSize)],
                [Gui.Input(key='_CREDIT_', size=self.inputSize)],
                [Gui.Input(key='_INSURANCE_', size=self.inputSize)],
                [Gui.Input(key='_CUT_LOCK_', size=self.inputSize)],
                [Gui.Input(key='_ADVERTISING_', size=self.inputSize)],
                [Gui.Input(key='_TOTAL_', size=self.inputSize)],
            ])
        ]

        transactions = TransactionFrame(self.controller,
                                        tenant=self.tenant,
                                        widths=[30, 30, 64],
                                        rows=5).view

        histories = HistoryFrame(self.controller,
                                 data=self.tenant,
                                 widths=[10, 10, 10, 10, 10],
                                 rows=5).view

        return [
            [
                Gui.Column([
                    [tenant],
                    [photos],
                    notes
                ]),
                Gui.Column([
                    [Gui.Frame("Payable Balances", [
                        [Gui.Column(
                            balances
                        )]
                    ])],
                    notes
                ]),
                Gui.Column([
                    [Gui.Frame("Make Payment", [
                        payment_form,
                        [Gui.Button('Make Payment', size=(48, 2))],
                    ])]
                ])
            ],
            [
                transactions
            ]
        ]

    def create_window(self):
        return Gui.Window(self.title, self.layout)

    def create_popup(self):
        Gui.Popup('Payment processed!')

    def dispay_loader(self):
        win = tkinter.Tk()
        print('starting')
        win.config(cursor="wait")
        time.sleep(7)
        win.config(cursor="")
        win.destroy()
        self.create_popup()
        print("done")
        self.refresh()
        return
