from models.usuario import UsuarioModel
from views.gestionar_usuarios_view import GestionarUsuariosView


class GestionarUsuariosController:
    def __init__(self, menu_view):
        self.model = UsuarioModel()
        self.menu_view = menu_view

    def mostrar_ventana(self, vista):
        if vista == "GestionarUser":
            self.ventana = GestionarUsuariosView(None, controller=self, menu_view=self.menu_view)
        self.ventana.Show()

    def obtener_usuarios(self):
        """Obtiene todos los usuarios de la base de datos."""
        return self.model.obtener_usuarios()

    def agregar_usuario(self, nombre, usuario, contraseña, rol):
        """Agrega un nuevo usuario a la base de datos."""
        return self.model.agregar_usuario(nombre, usuario, contraseña, rol)

    def editar_usuario(self, usuario_id, nombre, usuario, rol):
        """Edita un usuario existente en la base de datos."""
        return self.model.editar_usuario(usuario_id, nombre, usuario, rol)

    def eliminar_usuario(self, usuario_id):
        """Elimina un usuario de la base de datos."""
        return self.model.eliminar_usuario(usuario_id)