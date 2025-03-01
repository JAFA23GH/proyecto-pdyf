from models.entidades import EntidadModel
from views.gestionar_entidades_view import VentanaGestionarEntidades


class GestionarEntidadesController:
    def __init__(self, menu_view):
        self.model = EntidadModel()
        self.menu_view = menu_view

    def mostrar_ventana(self, vista):
        if vista == "Gestionar":
            self.ventana = VentanaGestionarEntidades(None, controller=self, menu_view=self.menu_view)
        self.ventana.Show()

    def obtener_entidades(self):
        """Obtiene todos los entidades de la base de datos."""
        return self.model.obtener_entidades()

    def agregar_entidades(self, nombre, entidad, contraseña, rol):
        """Agrega un nuevo entidad a la base de datos."""
        return self.model.agregar_entidad(nombre, entidad, contraseña, rol)

    def editar_entidades(self, entidad_id, nombre, entidad, rol):
        """Edita un entidad existente en la base de datos."""
        return self.model.editar_entidad(entidad_id, nombre, entidad, rol)

    def eliminar_entidades(self, entidad_id):
        """Elimina un entidad de la base de datos."""
        return self.model.eliminar_entidad(entidad_id)