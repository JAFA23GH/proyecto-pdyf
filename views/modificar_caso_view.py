import wx
from datetime import datetime

class VentanaModificar(wx.Frame):
    def __init__(self, parent, controlador, usuario, rol, menu_view=None):
        super(VentanaModificar, self).__init__(parent)
        self.SetTitle("Modificar Caso")
        self.SetSize((600, 800))
        self.controlador = controlador  # Referencia al controlador
        self.usuario = usuario
        self.rol = rol
        self.menu_view = menu_view
        self.text_ctrls = {}
        self.original_values = {}
        panel = wx.ScrolledWindow(self)
        panel.SetScrollRate(5, 5)
        vbox = wx.BoxSizer(wx.VERTICAL)


        # Manejar el evento de cierre de la ventana
        self.Bind(wx.EVT_CLOSE, self.on_close)

        # Cambiar el icono de la ventana
        icon = wx.Icon("img/iconoinstitucional.ico", wx.BITMAP_TYPE_ICO)  # Cambia la ruta al icono
        self.SetIcon(icon)

        # ComboBox para Nro. Expediente
        self.nro_expediente_combo = wx.ComboBox(panel, choices=self.controlador.obtener_casos_abiertos(self.usuario))
        vbox.Add(wx.StaticText(panel, label="Nro. Expediente:"), flag=wx.ALIGN_LEFT | wx.TOP, border=10)
        vbox.Add(self.nro_expediente_combo, flag=wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, border=10)

        # Bind para llenar los campos al seleccionar un expediente
        self.nro_expediente_combo.Bind(wx.EVT_COMBOBOX, self.on_expediente_select)

        # Campos de texto que pueden ser modificados
        campos_modificables = [
            "Descripción Modus Operandi", "Diagnostico / Detalle de Comprobación para Determinar Fraude",
            "Actuaciones/Acciones Realizadas", "Conclusiones / Recomendaciones", "Observaciones", "Soporte"
        ]
        for campo in campos_modificables:
            label = wx.StaticText(panel, label=f"{campo}:")
            vbox.Add(label, flag=wx.ALIGN_LEFT | wx.TOP, border=10)
            textbox = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
            vbox.Add(textbox, flag=wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, border=10)
            self.text_ctrls[campo] = textbox
            textbox.Bind(wx.EVT_TEXT, self.verificar_cambios)

        # ComboBox para cambiar el estatus del caso
        estatus_label = wx.StaticText(panel, label="Estatus del Caso:")
        vbox.Add(estatus_label, flag=wx.ALIGN_LEFT | wx.TOP, border=10)
        self.estatus_combo = wx.ComboBox(panel, choices=["Asignado", "Cerrado"])
        vbox.Add(self.estatus_combo, flag=wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, border=10)
        self.estatus_combo.Bind(wx.EVT_COMBOBOX, self.verificar_cambios)

        # Botones
        hbox_botones = wx.BoxSizer(wx.HORIZONTAL)
        self.boton_aceptar = wx.Button(panel, label="Aceptar")
        self.boton_aceptar.Enable(False)  # Deshabilitar inicialmente
        boton_cancelar = wx.Button(panel, label="Cancelar")
        hbox_botones.Add(self.boton_aceptar, flag=wx.RIGHT | wx.LEFT, border=10)
        hbox_botones.Add(boton_cancelar, flag=wx.LEFT, border=10)
        vbox.Add(hbox_botones, flag=wx.ALIGN_CENTER | wx.ALL, border=20)

        # Eventos
        self.boton_aceptar.Bind(wx.EVT_BUTTON, self.on_aceptar)
        boton_cancelar.Bind(wx.EVT_BUTTON, lambda event: self.on_cancel(event))
        panel.SetSizer(vbox)

    def on_expediente_select(self, event):
        """Llena los campos de texto con los datos del expediente seleccionado."""
        expediente_seleccionado = self.nro_expediente_combo.GetValue()
        datos_expediente = self.controlador.obtener_datos_expediente(expediente_seleccionado)

        if datos_expediente:
            # Asumiendo que datos_expediente es un diccionario con los datos del caso
            self.original_values.clear()
            for campo, valor in datos_expediente.items():
                if campo in self.text_ctrls:
                    self.text_ctrls[campo].SetValue(str(valor))
                    self.original_values[campo] = str(valor)
            # Establecer el valor del estatus
            self.estatus_combo.SetValue("Asignado")
            self.original_values["Estatus"] = "Asignado"

        self.verificar_cambios()

    def verificar_cambios(self, event=None):
        """Verifica si se ha seleccionado un expediente y se han hecho cambios en los campos."""
        expediente_seleccionado = self.nro_expediente_combo.GetValue() != ""
        cambios_realizados = any(
            self.text_ctrls[campo].GetValue() != self.original_values.get(campo, "")
            for campo in self.text_ctrls
        ) or self.estatus_combo.GetValue() != self.original_values.get("Estatus", "")

        self.boton_aceptar.Enable(expediente_seleccionado and cambios_realizados)

    def on_aceptar(self, event):
        from controllers.caso_controller import CasoController
        from patterns.decorator import CasoDecorator

        mensaje = '¿Está seguro de que desea realizar los cambios?'
        dialogo = wx.MessageDialog(None, mensaje, 'Confirmación', wx.YES_NO | wx.ICON_QUESTION)
        respuesta = dialogo.ShowModal()

        if respuesta == wx.ID_YES:
            nro_expediente = self.nro_expediente_combo.GetValue()
            datos_actualizados = {campo: self.text_ctrls[campo].GetValue() for campo in self.text_ctrls}
            nuevo_estatus = self.estatus_combo.GetValue()

            self.controle = CasoController(self.usuario, self.rol, self.menu_view)
            decorated_controller = CasoDecorator(self.controle)

            # Obtener el id del caso a partir del número de expediente
            caso_id = self.controle.obtener_id_caso_por_expediente(nro_expediente)
            if not caso_id:
                wx.MessageBox("No se pudo encontrar el ID del caso.", "Error", wx.OK | wx.ICON_ERROR)
                return

            # Modificar el caso
            resultado = decorated_controller.modificar_caso(nro_expediente, datos_actualizados, nuevo_estatus)
            if not resultado[0]:  # Si hubo un error al modificar el caso
                wx.MessageBox(resultado[1], "Error", wx.OK | wx.ICON_ERROR)
                return

            # Obtener la fecha actual
            fecha_actual = datetime.now().strftime('%Y-%m-%d')

            # Insertar en la tabla Avances
            descripcion_avances = datos_actualizados.get("Actuaciones/Acciones Realizadas", "")
            if descripcion_avances:
                self.controle.insertar_avance(caso_id, descripcion_avances, fecha_actual)

            # Insertar en la tabla Alarmas si el caso se cierra o si se detectan frases clave
            motivo_alarma = None
            if nuevo_estatus == "Cerrado":
                motivo_alarma = "Caso cerrado, requiere validación"
            else:
                frases_clave = [
                    "Pruebas no concluyentes, revisar",
                    "Denuncias crecientes, alta prioridad",
                    "Posible interferencia en el caso",
                    "Pruebas clave encontradas"
                ]
                for frase in frases_clave:
                    if frase in descripcion_avances:
                        motivo_alarma = frase
                        break

            if motivo_alarma:
                self.controle.insertar_alarma(caso_id, motivo_alarma, fecha_actual)

            # Insertar en la tabla Auditorias
            accion_auditoria = datos_actualizados.get("Actuaciones/Acciones Realizadas", "")  # Usar el contenido del campo
            self.controle.insertar_auditoria(caso_id, accion_auditoria, fecha_actual, self.usuario)

            # Mostrar mensaje de confirmación
            wx.MessageBox("Registro modificado exitosamente.", "Éxito", wx.OK | wx.ICON_INFORMATION)

            # Limpiar los campos de la vista
            self.limpiar_campos()

    def limpiar_campos(self):
        """Limpia todos los campos de la vista."""
        self.nro_expediente_combo.SetValue("")  # Limpiar el ComboBox de expediente
        for campo in self.text_ctrls:
            self.text_ctrls[campo].SetValue("")  # Limpiar todos los campos de texto
        self.estatus_combo.SetValue("Asignado")  # Restablecer el estatus a "Asignado"
        self.boton_aceptar.Enable(False)  # Deshabilitar el botón de aceptar

    def on_cancel(self, event):
        self.Hide()  # Cierra la ventana de modificación
        self.controlador.menu_view.reopen()

    def on_close(self, event):
        """Maneja el cierre de la ventana."""
        dialogo = wx.MessageDialog(self, "¿Estás seguro de que quieres salir?", "Cerrar aplicación", wx.YES_NO | wx.ICON_QUESTION)
        respuesta = dialogo.ShowModal()
        if respuesta == wx.ID_YES:
            self.Destroy()  # Cierra la ventana
            wx.Exit()  # Cierra la aplicación completamente
        else:
            event.Veto()  # Cancela el cierre de la ventana