from database.db import Database

class auditoriaModel:
    def __init__(self):
        self.db = Database()

    def obtener_auditorias(self):
        """Obtiene todas las auditorías de la base de datos."""
        query = "SELECT id, caso_id, accion, fecha, usuario_id FROM Auditorias"
        return self.db.fetch_all(query)