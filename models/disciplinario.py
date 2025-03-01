from database.db import Database

class disciplinaModel:
    def __init__(self):
        self.db = Database()

    def obtener_disciplinario(self):
        """Obtiene todos los registros de disciplinario de la base de datos."""
        query = """
        SELECT d.id, u.nombre AS nombre_usuario, e.nombre AS nombre_equipo, 
               d.estatus, d.Estado_Equip, d.fecha_incidente
        FROM disciplinario d
        JOIN Usuarios u ON d.usuario_id = u.id
        JOIN equipos e ON d.equipo_id = e.id
        """
        resultados = self.db.fetch_all(query)  # Suponiendo que fetch_all devuelve una lista de tuplas

        # Convertir tuplas a diccionarios
        registros = []
        columnas = ['id', 'nombre_usuario', 'nombre_equipo', 'estatus', 'Estado_Equip', 'fecha_incidente']
        for resultado in resultados:
            registro = dict(zip(columnas, resultado))
            registros.append(registro)

        return registros

    def agregar_disciplinario(self, usuario_id, equipo_id, estatus, Estado_Equip, fecha_incidente, descripcion=None):
        """
        Agrega un nuevo registro a la tabla disciplinario.
        """
        query = """
        INSERT INTO disciplinario (usuario_id, equipo_id, estatus, Estado_Equip, fecha_incidente, descripcion)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        return self.db.execute(query, (usuario_id, equipo_id, estatus, Estado_Equip, fecha_incidente, descripcion))

    def editar_disciplinario(self, disciplinario_id, usuario_id, equipo_id, estatus, Estado_Equip, fecha_incidente, descripcion=None):
        """
        Edita un registro existente en la tabla disciplinario.
        """
        query = """
        UPDATE disciplinario
        SET usuario_id = ?, equipo_id = ?, estatus = ?, Estado_Equip = ?, fecha_incidente = ?, descripcion = ?
        WHERE id = ?
        """
        return self.db.execute(query, (usuario_id, equipo_id, estatus, Estado_Equip, fecha_incidente, descripcion, disciplinario_id))

    def eliminar_disciplinario(self, disciplinario_id):
        """
        Elimina un registro de la tabla disciplinario.
        """
        query = "DELETE FROM disciplinario WHERE id = ?"
        return self.db.execute(query, (disciplinario_id,))

    def obtener_usuarios(self):
        """Obtiene una lista de usuarios con su id y nombre."""
        query = "SELECT id, nombre FROM Usuarios"
        return self.db.fetch_all(query)

    def obtener_equipos(self):
        """Obtiene una lista de equipos con su id y nombre/serial."""
        query = "SELECT id, nombre, serial FROM equipos"
        return self.db.fetch_all(query)