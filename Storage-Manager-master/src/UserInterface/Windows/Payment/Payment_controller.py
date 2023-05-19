"""Code written by Emerson Havener unless otherwise specified."""

from src.UserInterface.Windows.Window.window_controller import WindowController, Err
from .Payment_view import PaymentView
from src.UserInterface.Frames.Image_controller import ImageController
from src.DatabaseORM.transaction_orm import Transaction


class PaymentWindow(WindowController):
    payableRentChargeBalance = 0.00
    payableLateFeeBalance = 0.00

    def __init__(self, tenant, transactions, histories):
        self.tenant = tenant
        self.transactions = transactions
        self.histories = histories
        self.img_controller = ImageController([], tenant)
        self.selected_balances = []
        super().__init__(PaymentView, "Payment")
        self.load()

    def load(self):
        self.window = self.view.window

    def process_event(self, event, values):
        if event != "__TIMEOUT__":
            print(f"Event: {event}")

        if event in (None, "Cancel"):
            return self.shutdown()

        self.img_controller.process_event(event, values)

        if "_TOGGLE_BALANCE_id=" in event:
            self.toggleBalance(event[19:])

        if event == "Make Payment":
            self.makePayment(values)

        return True

    def refresh(self):
        self.view.refresh()

    def shutdown(self):
        self.window.close()
        return False

    def makePayment(self, values):
        print('values', values)
        if values and values["_RENT_PAYMENT_"] and float(values["_RENT_PAYMENT_"]) > 0:
            transactionToUpdate = self.selected_balances.pop()
            updatedTransaction = self.database.TransactionModel.pay(
                transactionToUpdate.id, float(values["_RENT_PAYMENT_"]))
            self.view.dispay_loader()
            self.window['_RENT_PAYMENT_'].update('')
            self.refresh()

    def toggleBalance(self, id):
        balance = self.database.TransactionModel.get(id)
        if balance not in self.selected_balances:
            self.selected_balances.append(balance)
            if balance.category_string == "Rent Charge":
                self.payableRentChargeBalance = self.payableRentChargeBalance + \
                    (-1 * float(balance.amount))
            elif balance.category_string == "Late Fee":
                self.payableLateFeeBalance = self.payableLateFeeBalance + \
                    (-1 * float(balance.amount))

        else:
            if balance.category_string == "Rent Charge":
                self.payableRentChargeBalance = self.payableRentChargeBalance + \
                    float(balance.amount)
            elif balance.category_string == "Late Fee":
                self.payableLateFeeBalance = self.payableLateFeeBalance + \
                    float(balance.amount)
            self.selected_balances.remove(balance)

        self.refresh()

        formattedPayableRentChargeBalance = format(
            self.payableRentChargeBalance, '.2f')
        formattedPayableLateFeeBalance = format(
            self.payableLateFeeBalance, '.2f')

        self.window['_PAYABLE_RENT_CHARGE_TEXT_'].update(
            f'${formattedPayableRentChargeBalance}')
        self.window['_PAYABLE_LATE_FEE_TEXT_'].update(
            f'${formattedPayableLateFeeBalance}')

        print('formattedPayableRentChargeBalance',
              formattedPayableRentChargeBalance)
        print('formattedPayableLateFeeBalance', formattedPayableLateFeeBalance)

        return
