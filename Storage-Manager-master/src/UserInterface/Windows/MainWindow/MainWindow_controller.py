"""Code written by Jacquesne Jones unless otherwise specified."""

from src.UserInterface.Windows.Window.window_controller import WindowController, Gui, error
from src.UserInterface.Windows.MainWindow.MainWindow_view import MainWindowView
from src.Encryption.crypto import Access
from src.DatabaseORM.unit_orm import Unit
from src.DatabaseORM.tenant_orm import Tenant
from src.BusinessAutomation.automation import OperationsModel


class MainWindow(WindowController):
    """Defines the main window of the program.

    This window is a singleton and should only be created once. If closed all other windows are closed as well
    and the program shuts down. This is the window where the database is loaded and maintained.
    """
    def __init__(self, database, window_title, user, password):
        WindowController.current_user = database.UserModel.get_by_name(user)
        super().__init__(MainWindowView, window_title, database)
        self.operations = OperationsModel(database)
        self.failed = False
        if self.verify(user, password):
            self.load()
        else:
            self.failed_login()

    def verify(self, user, password):
        """Verifies is a given password matches the hash for the selected username"""
        pw_hash = self.database.UserModel.get_by_name(user).pw_hash
        return Access.verify_hash(password, pw_hash)

    def failed_login(self):
        """Let the user know the password failed and let the calling function know this window failed to login"""
        self.failed = True
        Gui.PopupError("Username or password is incorrect, please try again.", title="Could not verify user")

    def load(self):
        self.window.Finalize()
        self.load_tabs()
        # Change tab if default is different
        if WindowController.current_user.default_tab == "Reports":
            self.window["_TG_MAIN_"].Widget.select(1)
        # INITIALIZATION PROCESSES
        # This includes any automation of business rules designed to run at program start
        self.run_automated_tasks()
        # MAIN PROGRAM LOOP
        # This first runs the main window, then checks if it's closed. If not, it runs all other open windows
        # in the order they were opened. If any window is closed, it removes it from the open windows to free up
        # space in the list.
        while self.run():   # First Read Call
            for window in WindowController.open_windows:
                if not window.run():
                    WindowController.open_windows.remove(window)

    def process_event(self, event, values):
        # Rerun all automated tasks every hour to make sure program stays up to date while running a long time
        if self.operations.check_hourly_events():
            self.run_automated_tasks()
        # Now continue with event processing
        if event in (None, "Quit::_FILE_"):
            return self.shutdown()
        # Check for menu event
        if "::" in event:
            self.process_menu(event, values)
        return True

    def process_menu(self, event, values):
        """Processes the top menu items specifically"""
        if event == "Add Unit::_DEBUG_":
            values, index = self.view.debug_add_unit_popup()
            if values:
                err = self.database.new(
                    Unit(
                        identifier=values["_IDENTIFIER_"],
                        tenant_id=values["_TENANT_"],
                        size_id=index))
                if err == "err_unique":
                    error(f"Unit name {values['_IDENTIFIER_']} is already in use.")
        elif event == "Add Tenant::_DEBUG_":
            values = self.view.debug_add_tenant_popup()
            if values:
                self.database.new(
                    Tenant(
                        ssn=values["_SSN_"],
                        last=values["_LNAME_"],
                        first=values["_FNAME_"],
                        middle=values["_MNAME_"],
                        addr1=values["_ADDR1_"],
                        addr2=values["_ADDR2_"],
                        city=values["_CITY_"],
                        state=values["_STATE_"],
                        zip=values["_ZIP_"],
                        phone=values["_PHONE_"],
                        email=values["_EMAIL_"]
                    )
                )
        elif event == "Add User::_DEBUG_":
            Gui.popup("Working")
        elif event == "Add Transaction::_DEBUG_":
            values = self.view.debug_add_transaction_popup()
            if values:
                unit = None
                tenant = None
                if values["_UNIT_"]:
                    unit = self.database.UnitModel.get(values["_UNIT_"])
                if values["_TENANT_"]:
                    tenant = self.database.TenantModel.get(values["_TENANT_"])
                self.database.TransactionModel.new(
                    values["_AMOUNT_"], values["_CATEGORY_"], unit=unit, tenant=tenant)
        elif event == "Add History::_DEBUG_":
            values = self.view.debug_add_history_popup()
            if values:
                if values["_TYPE_"] == "Unit":
                    unit = self.database.UnitModel.get(values["_ID_"])
                    self.database.UnitHistoryModel.new(
                        unit, values["_CATEGORY_"], values["_FIELD_"],
                        values["_NEW_VALUE_"], values["_OLD_VALUE_"])
                else:
                    tenant = self.database.TenantModel.get(values["_ID_"])
                    self.database.TenantHistoryModel.new(
                        tenant, values["_CATEGORY_"], values["_FIELD_"],
                        values["_NEW_VALUE_"], values["_OLD_VALUE_"])
        elif event == "WIPE DB::_DEBUG_":
            if self.view.confirm_popup("Are you sure you want to completely wipe the database? This cannot be undone!"):
                self.database.wipe()

    def refresh(self):
        pass

    def shutdown(self):
        """Function to close down the program."""
        print("Shutting down...")
        self.window.close()
        exit(0)
        return False

    def run_automated_tasks(self):
        """Runs all upkeep tasks and checks."""
        print(f"Automated tasks run at {self.operations.last_time_check.ctime()}")
        self.operations.charge_units(self.database.BusinessRuleModel.get_rule("Due Day").value)
