from database.db import Database

class CarteleraModel:
    def __init__(self):
        self.db = Database()

    def obtener_casos(self):
        """Obtiene todos los casos de la base de datos."""
        query = """
            SELECT investigador, fecha_inicio, nro_expediente, tipo, 
                   descripcion_modus_operandi, actuaciones_acciones, 
                   conclusiones_recomendaciones, estatus 
            FROM Casos
        """
        return self.db.fetch_all(query)