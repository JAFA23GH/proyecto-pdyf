from database.db import Database

class UsuarioModel:
    def __init__(self):
        self.db = Database()

    def obtener_usuarios(self):
        """Obtiene todos los usuarios de la base de datos."""
        query = "SELECT id, nombre, usuario, contraseña, rol FROM Usuarios"
        return self.db.fetch_all(query)

    def agregar_usuario(self, nombre, usuario, contraseña, rol):
        """Agrega un nuevo usuario a la base de datos."""
        query = "INSERT INTO Usuarios (nombre, usuario, contraseña, rol) VALUES (?, ?, ?, ?)"
        return self.db.execute(query, (nombre, usuario, contraseña, rol))

    def editar_usuario(self, usuario_id, nombre, usuario, rol):
        """Edita un usuario existente en la base de datos."""
        query = "UPDATE Usuarios SET nombre = ?, usuario = ?, rol = ? WHERE id = ?"
        return self.db.execute(query, (nombre, usuario, rol, usuario_id))

    def eliminar_usuario(self, usuario_id):
        """Elimina un usuario de la base de datos."""
        query = "DELETE FROM Usuarios WHERE id = ?"
        return self.db.execute(query, (usuario_id,))