import wx
from database.db import Database
from views.menu_view import MenuView
from views.login_view import LoginView
import bcrypt

class LoginController:
    def __init__(self):
        self.db = Database()
        self.view = LoginView(self, None)
        self.view.Show()

    def validar_login(self, usuario, contraseña):
        """Valida las credenciales del usuario."""
        query = "SELECT id, nombre, contraseña, rol FROM Usuarios WHERE usuario = ?"
        result = self.db.fetch_all(query, (usuario,))

        if result:
            user_id, nombre, hashed_password, rol = result[0]

            if bcrypt.checkpw(contraseña.encode('utf-8'), hashed_password):
                print("Login exitoso")
                self.abrir_menu_view(user_id, nombre, rol)
            else:
                wx.MessageBox("Contraseña incorrecta", "Error", wx.OK | wx.ICON_ERROR)
        else:
            wx.MessageBox("Usuario no encontrado", "Error", wx.OK | wx.ICON_ERROR)

    def abrir_menu_view(self, user_id, nombre, rol):
        """Abre el menú y cierra la ventana de login."""
        self.view.Close()
        menu_view = MenuView(self, user_id, nombre, rol, None)
        menu_view.Show()
