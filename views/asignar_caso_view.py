import wx

class VentanaAsignar(wx.Frame):
    def __init__(self, parent, controlador, usuario, rol, menu_view=None):
        super(VentanaAsignar, self).__init__(parent)
        self.SetTitle("Asignar Caso")
        self.SetSize((800, 600))  # Aumentar el tamaño de la ventana
        self.controlador = controlador  # Referencia al controlador
        self.usuario = usuario
        self.rol = rol
        self.menu_view = menu_view
        self.text_ctrls = {}
        panel = wx.ScrolledWindow(self)
        panel.SetScrollRate(5, 5)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Manejar el evento de cierre de la ventana
        self.Bind(wx.EVT_CLOSE, self.on_close)

        # Cambiar el icono de la ventana
        icon = wx.Icon("img/iconoinstitucional.ico", wx.BITMAP_TYPE_ICO)  # Cambia la ruta al icono
        self.SetIcon(icon)

        # ComboBox para Nro. Expediente
        self.nro_expediente_combo = wx.ComboBox(panel, choices=self.controlador.obtener_casos_abiertos(None))
        vbox.Add(wx.StaticText(panel, label="Nro. Expediente:"), flag=wx.ALIGN_LEFT | wx.TOP, border=10)
        vbox.Add(self.nro_expediente_combo, flag=wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, border=10)

        # Bind para llenar los campos al seleccionar un expediente
        self.nro_expediente_combo.Bind(wx.EVT_COMBOBOX, self.on_expediente_select)

        # Campos de texto
        campos = [
            "Tipo de Caso", "Fecha de inicio", "Móvil afectado", "Tipo de irregularidad", "Subtipo irregularidad",
            "Objetivo / Agraviado", "Incidencia", "Duración (Días)", "Descripción Modus Operandi",
            "Área Apoyo a Resolver", "Detección / Procedencia del Caso",
            "Diagnostico / Detalle de Comprobación para Determinar Fraude",
            "Actuaciones/Acciones Realizadas", "Conclusiones / Recomendaciones", "Observaciones", "Soporte"
        ]
        for campo in campos:
            label = wx.StaticText(panel, label=f"{campo}:")
            vbox.Add(label, flag=wx.ALIGN_LEFT | wx.TOP, border=10)
            textbox = wx.TextCtrl(panel)
            vbox.Add(textbox, flag=wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, border=10)
            self.text_ctrls[campo] = textbox

        # Campo Investigador
        investigador_label = wx.StaticText(panel, label="Investigador:")
        vbox.Add(investigador_label, flag=wx.ALIGN_LEFT | wx.TOP, border=10)
        if self.rol == "Administrador":
            self.investigador_combo = wx.ComboBox(panel, choices=self.controlador.obtener_investigadores())
            vbox.Add(self.investigador_combo, flag=wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, border=10)
            self.investigador_combo.Bind(wx.EVT_COMBOBOX, self.verificar_seleccion)
        else:
            self.investigador_text = wx.TextCtrl(panel, value=self.usuario, style=wx.TE_READONLY)
            vbox.Add(self.investigador_text, flag=wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, border=10)

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
            # Vaciar el campo Investigador
            if self.rol == "Administrador":
                self.investigador_combo.SetValue("")
            else:
                self.investigador_text.SetValue("")

            # Asumiendo que datos_expediente es un diccionario con los datos del caso
            for campo, valor in datos_expediente.items():
                if campo in self.text_ctrls:
                    self.text_ctrls[campo].SetValue(str(valor))
                    # Hacer los campos no modificables
                    self.text_ctrls[campo].SetEditable(False)

        self.verificar_seleccion()  # Verificar selección después de llenar los campos

    def verificar_seleccion(self, event=None):
        """Verifica si se ha seleccionado un expediente y un investigador."""
        expediente_seleccionado = self.nro_expediente_combo.GetValue() != ""
        investigador_seleccionado = (self.rol == "Administrador" and self.investigador_combo.GetValue() != "") or \
                                    (self.rol != "Administrador" and self.investigador_text.GetValue() != "")
        self.boton_aceptar.Enable(expediente_seleccionado and investigador_seleccionado)

    def on_aceptar(self, event):
        from controllers.caso_controller import CasoController
        self.controle = CasoController(self, rol=self.rol, menu_view=None)
        # Obtener el nro_expediente y el investigador_id
        nro_expediente = self.nro_expediente_combo.GetValue()
        nombre_investigador = self.investigador_combo.GetValue()
        investigador_id = self.controle.obtener_id_investigador(nombre_investigador)


        # Crear el controlador de Caso con los datos del expediente y el investigador
        # Llenar el campo Investigador con el nombre del investigador seleccionado
        if self.rol == "Administrador":
            self.investigador_combo.SetValue(nombre_investigador)
        else:
            self.investigador_text.SetValue(nombre_investigador)

        respuesta = self.controle.asignar_investigador(nro_expediente, investigador_id, nombre_investigador)

        if respuesta:
            mensaje = 'Investigador asignado correctamente. ¿Desea asignar más investigadores?'
            dialogo = wx.MessageDialog(None, mensaje, 'Información', wx.YES_NO | wx.ICON_INFORMATION)
            respuesta_dialogo = dialogo.ShowModal()

            if respuesta_dialogo == wx.ID_YES:
                self.limpiar_campos()
                self.actualizar_expedientes()
            else:
                self.Close()  # Cierra la ventana de asignación
                self.controlador.menu_view.reopen()
        else:
            wx.MessageBox('Error al asignar el investigador', 'Error', wx.OK | wx.ICON_ERROR)

    def limpiar_campos(self):
        """Limpia todos los campos del formulario."""
        for campo in self.text_ctrls.values():
            campo.SetValue("")
            campo.SetEditable(True)
        if self.rol == "Administrador":
            self.investigador_combo.SetValue("")
        else:
            self.investigador_text.SetValue("")

    def actualizar_expedientes(self):
        """Actualiza la lista de expedientes disponibles."""
        self.nro_expediente_combo.SetItems(self.controlador.obtener_casos_abiertos())
        self.nro_expediente_combo.SetValue("")

    def on_cancel(self, event):
        self.Hide()  # Cierra la ventana de asignación
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
