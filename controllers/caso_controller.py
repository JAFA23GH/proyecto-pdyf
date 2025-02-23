from patterns.factory import ModelFactory
from views.caso_view import VentanaRegistro
from  views.asignar_caso_view import VentanaAsignar
from  views.modificar_caso_view import VentanaModificar
from datetime import datetime
import wx

class CasoController:
    def __init__(self, user_id, rol, menu_view):
        self.user_id = user_id
        self.rol = rol
        self.menu_view = menu_view  # Guarda la referencia de la ventana del menú
        self.modelo = ModelFactory.create_model('Caso') # Se instancia el modelo



    def mostrar_ventana(self, vista):
        if vista=="registro":
            self.ventana = VentanaRegistro(None, controlador=self, usuario=self.user_id, rol=self.rol)
        elif vista=="asignar":
            self.ventana = VentanaAsignar(None, controlador=self, usuario=self.user_id, rol=self.rol)
        elif vista=="modificar":
            self.ventana = VentanaModificar(None, controlador=self, usuario=self.user_id, rol=self.rol)
        self.ventana.Show()


    def registrar_caso(self, vista):
        """Obtiene los datos desde la vista y los guarda en la base de datos."""
        campos_requeridos = ["Nro. Expediente", "Fecha de inicio", "Móvil afectado",
                             "Tipo de irregularidad", "Objetivo / Agraviado", "Descripción Modus Operandi",
                             "Conclusiones / Recomendaciones"]

        # Verificar que los campos requeridos no estén vacíos (excepto investigador si es administrador)
        for campo in campos_requeridos:
            if campo != "Investigador" and not vista.text_ctrls[campo].GetValue().strip():
                wx.MessageBox(f"El campo '{campo}' es requerido.", "Error", wx.OK | wx.ICON_ERROR)
                return

        # Obtener el investigador
        if vista.rol == "Administrador":
            investigador = vista.investigador_combo.GetValue()  # Puede estar vacío
        else:
            investigador = vista.usuario  # Se llena automáticamente y no se puede cambiar

        investigador_id = self.modelo.obtener_id_investigador(investigador)
        if vista.rol == "Administrador" and not investigador_id:
            wx.MessageBox(f"No se encontró el investigador '{investigador}'.", "Error", wx.OK | wx.ICON_ERROR)
            return

        # Validar fecha
        fecha_inicio_str = vista.text_ctrls["Fecha de inicio"].GetValue()
        try:
            fecha_inicio = datetime.strptime(fecha_inicio_str, '%d/%m/%Y').date().strftime('%Y-%m-%d')
        except ValueError:
            wx.MessageBox("Formato de fecha incorrecto.", "Error", wx.OK | wx.ICON_ERROR)
            return

        # Crear caso con Factory Method
        tipo_caso = vista.tipo_caso_radiobox.GetStringSelection()
        caso = self.crear_caso(tipo_caso)
        if not caso:
            return

        # Determinar el estatus
        estatus = "Asignado" if vista.rol == "Investigador" else "Abierto"

        if estatus=="Abierto":
            investigador=""


        # Guardar en la base de datos
        datos = [
            tipo_caso, vista.text_ctrls["Nro. Expediente"].GetValue(),
            investigador, fecha_inicio, vista.text_ctrls["Móvil afectado"].GetValue(), investigador_id, estatus
        ]
        exito, mensaje = self.modelo.guardar_caso(datos)
        wx.MessageBox(mensaje, "Información", wx.OK | wx.ICON_INFORMATION)

    """def crear_caso(self, tipo_caso):
        # Factory Method: Crea una instancia de caso según el tipo.
        if tipo_caso == 'Gestión':
            return GestionCaso()
        elif tipo_caso == 'Reclamo':
            return ReclamoCaso()
        elif tipo_caso == 'Caso':
            return CasoGeneral()
        else:
            wx.MessageBox("Tipo de caso no válido", "Error", wx.OK | wx.ICON_ERROR)
            return None"""

    def obtener_investigadores(self):
        """Obtiene la lista de investigadores desde el modelo."""
        return self.modelo.obtener_investigadores()

    def obtener_casos_abiertos(self, investigador_id):
        """Obtiene la lista de casos desde el modelo."""
        return self.modelo.obtener_casos_abiertos(investigador_id)

    def obtener_datos_expediente(self, expediente):
        """Obtiene los datos del expediente específico."""
        return self.modelo.obtener_datos_expediente(expediente)

    def asignar_investigador(self, expediente, investigador_id, investigador):
        """Asigna un investigador a un caso específico."""
        return self.modelo.asignar_investigador(expediente, investigador, investigador_id)

    def obtener_id_investigador(self, nombre):
        """Obtiene el ID del investigador."""
        return self.modelo.obtener_id_investigador(nombre)
