from models.auditoria import auditoriaModel
from views.consultar_auditoria_view import ConsultarAuditoriaView

class GestionarauditoriasController:
    def __init__(self, menu_view):
        self.model = auditoriaModel()  # Instancia del modelo
        self.menu_view = menu_view  # Referencia a la vista del menú anterior

    def mostrar_ventana(self, vista):
        """Muestra la ventana de consulta de auditorías."""
        if vista == "Auditar":
            self.ventana = ConsultarAuditoriaView(None, controller=self, menu_view=self.menu_view)
        self.ventana.Show()

    def obtener_auditorias(self):
        """Obtiene todas las auditorías de la base de datos."""
        return self.model.obtener_auditorias()