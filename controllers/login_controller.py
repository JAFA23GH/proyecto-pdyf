import wx
from database.db import Database
from views.menu_view import MenuView
from views.login_view import LoginView
import bcrypt

class LoginController:
    def __init__(self, mediator=None):
        self.menu_view = None
        self.mediator = mediator
        self.db = Database()
        self.view = LoginView(self, None)
        self.view.Show()

        if self.mediator:
            self.mediator.add_component(self)  # Registrar el controlador en el mediador

    def receive(self, event):
        """Método para recibir notificaciones del mediador."""
        if event == "usuario_logueado":
            print("Notificación: Un usuario ha iniciado sesión.")
            # Realizar alguna acción en respuesta al inicio de sesión

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
        """Abre el menú y oculta la ventana de login."""
        self.view.Hide()  # Oculta la ventana de inicio de sesión
        self.menu_view = MenuView(self, user_id, nombre, rol, self.mediator)  # Almacenar la referencia
        self.menu_view.Show()  # Muestra la ventana del menú principal