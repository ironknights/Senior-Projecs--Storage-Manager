"""Code written by Jacquesne Jones unless otherwise specified."""

from src.UserInterface.Windows.Window.window_controller import Gui
from src.DatabaseModel.database_model import *
from .Login_view import LoginView


class Login:    # Does not use WindowController as a base class because database is not yet loaded

    def __init__(self):
        settings = self.load_settings()
        self.loaded_db = settings[0]
        self.username = settings[1] if settings[1] != "None" else ""
        self.password = None
        self.view = LoginView(self.loaded_db, self.username)
        self.window = self.view.window
        values = self.load()
        if values:
            if "_USERNAME_" in values.keys():
                self.username = values["_USERNAME_"]
            if "_PASSWORD_" in values.keys():
                self.password = values["_PASSWORD_"]
            if "Change" in values.keys() and values["Change"]:
                self.loaded_db = values["Change"]

    def __repr__(self):
        return self.loaded_db, self.username, self.password

    def __str__(self):
        return f"db: {self.loaded_db}, username: {self.username}, password: {self.password}"

    @staticmethod
    def load_settings():
        """Gets settings from local file"""
        # First check if settings is already created, if not, create a default file:
        if not os.path.exists("../settings.cfg"):
            file = open("../settings.cfg", "w+")
            file.writelines([
                "DB: None\n",
                "User: None"
            ])
            return "None", "None"
        else:
            file = open("../settings.cfg", "r")
            values = file.readline().rstrip(), file.readline().rstrip()
            file.close()
            # Break up values and strip out early text
            db = values[0].partition("DB: ")[2]
            # Check if path exists, if not, don't try and load a non-existent file
            if not os.path.exists(db):
                db = "None"
            user = values[1].partition("User: ")[2]
            return db, user

    def close(self):
        """Close the window and save settings"""
        file = open("../settings.cfg", "w")    # Overwrite file with new data
        file.writelines([
            f"DB: {self.loaded_db}\n",
            f"User: {self.username if self.username else 'None'}"
        ])
        self.window.close()

    def load(self):
        while True:
            event, values = self.window.read()
            if event in (None, "Quit"):
                self.window.close()
                return None
            if event == "_NEW_":
                popup = Gui.Window("New Database", [
                    [Gui.T("Name:"), Gui.In(key="_NAME_")],
                    [Gui.Submit(), Gui.Cancel()]
                ])
                pop_event, pop_values = popup.read()
                if pop_event in (None, "Cancel"):
                    popup.close()
                else:
                    new_name = pop_values["_NAME_"] if pop_values["_NAME_"] else "database"
                    # Add trailing .db or local path if needed
                    if ".db" not in new_name:
                        new_name += ".db"
                    if '\\' not in new_name and '/' not in new_name:
                        new_name = os.path.join(os.getcwd(), new_name)
                    # Generate new empty database and update window
                    Database(new_name)
                    self.loaded_db = new_name
                    self.window["_DB_"](new_name)
                    popup.close()
            if event == "Login" and values["_USERNAME_"] and values["_PASSWORD_"]:
                return values
            # Debug skip for admin account
            if event == "DEFAULT LOGIN":
                values["_USERNAME_"] = "admin"
                values["_PASSWORD_"] = "password"
                return values
            # Enable login button once both username and password contain values, disable otherwise
            if event in ("_USERNAME_", "_PASSWORD_"):
                if values["_USERNAME_"] and values["_PASSWORD_"]:
                    self.window["Login"](disabled=False)
                else:
                    self.window["Login"](disabled=True)
