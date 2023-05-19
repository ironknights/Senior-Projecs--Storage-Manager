"""Code written by Jacquesne Jones unless otherwise specified."""

from src.UserInterface.Windows.Window.window_controller import Gui


class LoginView:        # Does NOT use WindowViewer as there is no database at time of login

    def __init__(self, loaded_db, username):
        self.loaded_db = loaded_db
        self.username = username
        self.layout = self.create_layout()
        self.window = self.create_window()

    def create_layout(self):
        text_size = 50
        layout = [
            [Gui.Text("Database: "), Gui.T(self.loaded_db, key="_DB_", size=(text_size, 1)), Gui.B("New", key="_NEW_"),
             Gui.FileBrowse("Change", file_types=(("SMDB", "*.db"), ("All Files", "*.*")), target="_DB_")],
            [Gui.Text("User Name"), Gui.InputText(self.username if self.username else "",
                                                  key="_USERNAME_", enable_events=True,
                                                  focus=True if not self.username else False,
                                                  size=(max(len(self.loaded_db), text_size + 9), 1))],
            [Gui.Text("Password  "), Gui.InputText(password_char="*",
                                                   key="_PASSWORD_", enable_events=True,
                                                   focus=True if self.username else False,
                                                   size=(max(len(self.loaded_db), text_size + 9), 1))],
            [Gui.Button("Login", disabled=True, bind_return_key=True), Gui.Button("Quit"), Gui.B("DEFAULT LOGIN")]
        ]
        return layout

    def create_window(self):
        return Gui.Window("Login", self.layout, use_default_focus=False)