"""Code written by Jacquesne Jones unless otherwise specified."""

import PySimpleGUI as Gui
from src.DatabaseModel.database_model import Database
from src.UserInterface.Windows.Login.Login_controller import Login
from src.UserInterface.Windows.MainWindow.MainWindow_controller import MainWindow

MAX_TRIES = 5   # Defines the number of failed password attempts before the program shuts down automatically


def main():
    Gui.theme(new_theme="DefaultNoMoreNagging")
    tries = 0
    while True:
        # Open the login window and check to make sure an attempt to log in was made
        log_window = Login()
        if not log_window.username or not log_window.password:
            exit(0)
        else:
            log_window.close()
        # Set values for the main program based on what was gathered by the login window
        db = Database(log_window.loaded_db)
        user = log_window.username
        password = log_window.password
        # Create the main window and initialize it
        main_window = MainWindow(db, "SOLO Storage Manager", user, password)
        # If the password was incorrect delete the windows and start the whole process over
        if main_window.failed and tries < MAX_TRIES:
            tries += 1
            del log_window
            del main_window
        else:
            print("Main Window closed")
            break


if __name__ == "__main__":
    main()
