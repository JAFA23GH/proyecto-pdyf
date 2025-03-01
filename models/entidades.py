from database.db import Database

class EntidadModel:
    def __init__(self):
        self.db = Database()

    def obtener_entidades(self):
        """Obtiene todas las entidades de la base de datos, incluyendo información del investigador."""
        query = """
        SELECT e.id, e.tipo_brecha, e.tipo_proyecto, e.proceso_corregido, e.procesos_realizado,
               u.nombre AS investigador, e.empresa, e.subtipo_ficha, e.tipo_irregularidad,
               e.subtipo_irregularidad, e.procedencia_casos
        FROM Entidades e
        JOIN Usuarios u ON e.investigador_id = u.id
        """
        return self.db.fetch_all(query)

    def agregar_entidad(self, tipo_brecha, tipo_proyecto, proceso_corregido, procesos_realizado,
                        investigador_id, empresa, subtipo_ficha, tipo_irregularidad,
                        subtipo_irregularidad, procedencia_casos):
        """Agrega una nueva entidad a la base de datos."""
        query = """
        INSERT INTO Entidades (tipo_brecha, tipo_proyecto, proceso_corregido, procesos_realizado,
                               investigador_id, empresa, subtipo_ficha, tipo_irregularidad,
                               subtipo_irregularidad, procedencia_casos)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        return self.db.execute(query, (tipo_brecha, tipo_proyecto, proceso_corregido, procesos_realizado,
                                       investigador_id, empresa, subtipo_ficha, tipo_irregularidad,
                                       subtipo_irregularidad, procedencia_casos))

    def editar_entidad(self, entidad_id, tipo_brecha, tipo_proyecto, proceso_corregido, procesos_realizado,
                       investigador_id, empresa, subtipo_ficha, tipo_irregularidad,
                       subtipo_irregularidad, procedencia_casos):
        """Edita una entidad existente en la base de datos."""
        query = """
        UPDATE Entidades
        SET tipo_brecha = ?, tipo_proyecto = ?, proceso_corregido = ?, procesos_realizado = ?,
            investigador_id = ?, empresa = ?, subtipo_ficha = ?, tipo_irregularidad = ?,
            subtipo_irregularidad = ?, procedencia_casos = ?
        WHERE id = ?
        """
        return self.db.execute(query, (tipo_brecha, tipo_proyecto, proceso_corregido, procesos_realizado,
                                       investigador_id, empresa, subtipo_ficha, tipo_irregularidad,
                                       subtipo_irregularidad, procedencia_casos, entidad_id))

    def eliminar_entidad(self, entidad_id):
        """Elimina una entidad de la base de datos."""
        query = "DELETE FROM Entidades WHERE id = ?"
        return self.db.execute(query, (entidad_id,))
