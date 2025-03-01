from models.disciplinario import disciplinaModel
from views.gestionar_disciplinario_view import VentanaGestionardisciplinario


class GestionardisciplinarioController:
    def __init__(self, menu_view):
        self.model = disciplinaModel()  # Instancia del modelo
        self.menu_view = menu_view  # Referencia a la vista del menú

    def mostrar_ventana(self, vista):
        """
        Muestra la ventana de gestión de disciplinario.
        """
        if vista == "Negar":
            self.ventana = VentanaGestionardisciplinario(None, controller=self, menu_view=self.menu_view)
        self.ventana.Show()

    def obtener_disciplinario(self):
        """
        Obtiene todos los registros de la tabla disciplinario.
        """
        return self.model.obtener_disciplinario()

    def agregar_disciplinario(self, usuario_id, equipo_id, estatus, Estado_Equip, fecha_incidente, descripcion=None):
        """
        Agrega un nuevo registro a la tabla disciplinario.
        """
        return self.model.agregar_disciplinario(usuario_id, equipo_id, estatus, Estado_Equip, fecha_incidente, descripcion)

    def editar_disciplinario(self, disciplinario_id, usuario_id, equipo_id, estatus, Estado_Equip, fecha_incidente, descripcion=None):
        """
        Edita un registro existente en la tabla disciplinario.
        """
        return self.model.editar_disciplinario(disciplinario_id, usuario_id, equipo_id, estatus, Estado_Equip, fecha_incidente, descripcion)

    def eliminar_disciplinario(self, disciplinario_id):
        """
        Elimina un registro de la tabla disciplinario.
        """
        return self.model.eliminar_disciplinario(disciplinario_id)

    def obtener_usuarios(self):
        """Obtiene una lista de usuarios con su id y nombre."""
        return self.model.obtener_usuarios()  # Suponiendo que el modelo tiene este método

    def obtener_equipos(self):
        """Obtiene una lista de equipos con su id y nombre/serial."""
        return self.model.obtener_equipos()  # Suponiendo que el modelo tiene este método