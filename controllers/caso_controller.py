from views.caso_view import CasoView

class CasoController:
    def __init__(self, user_id, rol):
        self.user_id = user_id
        self.rol = rol
        self.view = CasoView(self)  # Vista para registrar caso
        self.view.Show()

    def registrar_caso(self):
        tipo_caso = self.view.obtener_tipo_caso()  # Método para obtener tipo de caso

        # Factory Method para crear el caso
        caso = self.crear_caso(tipo_caso)
        if caso:
            self.view.mostrar_formulario(caso)  # Muestra formulario específico

    def crear_caso(self, tipo_caso):
        """Crea una instancia de caso según el tipo."""
        if tipo_caso == 'Gestión':
            return GestionCaso()
        elif tipo_caso == 'Reclamo':
            return ReclamoCaso()
        elif tipo_caso == 'Caso':
            return CasoGeneral()
        else:
            wx.MessageBox("Tipo de caso no válido", "Error", wx.OK | wx.ICON_ERROR)
            return None