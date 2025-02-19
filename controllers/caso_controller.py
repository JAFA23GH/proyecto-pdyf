from views.caso_view import CasoView
from models.caso import Caso

class CasoController:
    def __init__(self):
        self.view = CasoView(None)
        self.view.Show()

    def guardar_caso(self, tipo, descripcion, fecha_inicio, estatus, investigador_id):
        caso = Caso(None, tipo, descripcion, fecha_inicio, estatus, investigador_id)
        caso.save()