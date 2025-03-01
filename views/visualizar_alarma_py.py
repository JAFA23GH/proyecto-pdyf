import wx

class VentanaVisAlarma(wx.Frame):
    def __init__(self, parent, controlador, usuario, rol, menu_view=None):
        super(VentanaVisAlarma, self).__init__(parent)
        self.SetTitle("Visualizar Alarma")  # Cambiado el título a "Visualizar Alarma"
        self.SetSize((800, 600))
        self.controlador = controlador
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
        icon = wx.Icon("img/iconoinstitucional.ico", wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)

        # ComboBox para Nro. Expediente
        self.nro_expediente_combo = wx.ComboBox(panel, choices=self.controlador.obtener_casos_abiertos1(None))
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
            textbox = wx.TextCtrl(panel, style=wx.TE_READONLY)  # Hacer los campos no modificables
            vbox.Add(textbox, flag=wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, border=10)
            self.text_ctrls[campo] = textbox

        # Campo Investigador (solo mostrar, no solicitar)
        investigador_label = wx.StaticText(panel, label="Investigador:")
        vbox.Add(investigador_label, flag=wx.ALIGN_LEFT | wx.TOP, border=10)
        investigador_text = wx.TextCtrl(panel, style=wx.TE_READONLY)  # Campo no modificable
        vbox.Add(investigador_text, flag=wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, border=10)
        self.text_ctrls["Investigador"] = investigador_text  # Agregar al diccionario para llenarlo

        # Botones
        hbox_botones = wx.BoxSizer(wx.HORIZONTAL)
        boton_aceptar = wx.Button(panel, label="Aceptar")
        boton_cancelar = wx.Button(panel, label="Cancelar")
        hbox_botones.Add(boton_aceptar, flag=wx.RIGHT | wx.LEFT, border=10)
        hbox_botones.Add(boton_cancelar, flag=wx.LEFT, border=10)
        vbox.Add(hbox_botones, flag=wx.ALIGN_CENTER | wx.ALL, border=20)

        # Eventos
        boton_aceptar.Bind(wx.EVT_BUTTON, self.on_cerrar)  # Ambos botones cierran la ventana
        boton_cancelar.Bind(wx.EVT_BUTTON, self.on_cerrar)
        panel.SetSizer(vbox)

    def on_expediente_select(self, event):
        """Llena los campos de texto con los datos del expediente seleccionado."""
        expediente_seleccionado = self.nro_expediente_combo.GetValue()

        # Limpiar el expediente (eliminar etiquetas entre paréntesis)
        expediente_limpio = expediente_seleccionado.split(" ")[0]  # Toma solo el número

        datos_expediente = self.controlador.obtener_datos_expediente(expediente_limpio)

        if datos_expediente:
            for campo, valor in datos_expediente.items():
                if campo in self.text_ctrls:
                    self.text_ctrls[campo].SetValue(str(valor))


    def on_cerrar(self, event):
        self.Hide()
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