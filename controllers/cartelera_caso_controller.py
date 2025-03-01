from models.cartelera import CarteleraModel
from views.cartelera_caso_view import CarteleraCasoView

class CarteleraCasosController:
    def __init__(self, menu_view):
        self.model = CarteleraModel()  # Instancia del modelo
        self.menu_view = menu_view  # Referencia a la vista del menú anterior

    def mostrar_ventana(self, vista):
        """Muestra la ventana de consulta de casos."""
        if vista == "Consultar":
            self.ventana = CarteleraCasoView(None, controller=self, menu_view=self.menu_view)
        self.ventana.Show()

    def obtener_casos(self):
        """Obtiene todos los casos de la base de datos."""
        return self.model.obtener_casos()