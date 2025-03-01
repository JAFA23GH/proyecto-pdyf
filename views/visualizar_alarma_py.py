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

        # Filtro de días abierto
        self.dias_abierto_label = wx.StaticText(panel, label="Días abierto mínimo:")
        vbox.Add(self.dias_abierto_label, flag=wx.ALIGN_LEFT | wx.TOP, border=10)
        self.dias_abierto_ctrl = wx.TextCtrl(panel)
        vbox.Add(self.dias_abierto_ctrl, flag=wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, border=10)

        # Filtro de tipo de irregularidad
        self.tipo_irregularidad_label = wx.StaticText(panel, label="Tipo de irregularidad:")
        vbox.Add(self.tipo_irregularidad_label, flag=wx.ALIGN_LEFT | wx.TOP, border=10)
        self.tipo_irregularidad_combo = wx.ComboBox(panel, choices=self.controlador.obtener_tipos_irregularidades())
        vbox.Add(self.tipo_irregularidad_combo, flag=wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, border=10)

        # Botón de aplicar filtros
        self.boton_aplicar_filtros = wx.Button(panel, label="Aplicar Filtros")
        self.boton_aplicar_filtros.Disable()  # Deshabilitar el botón inicialmente
        vbox.Add(self.boton_aplicar_filtros, flag=wx.ALIGN_CENTER | wx.ALL, border=20)
        self.boton_aplicar_filtros.Bind(wx.EVT_BUTTON, self.on_aplicar_filtros)

        # Eventos para habilitar/deshabilitar el botón de filtrar
        self.dias_abierto_ctrl.Bind(wx.EVT_TEXT, self.on_cambio_filtro)
        self.tipo_irregularidad_combo.Bind(wx.EVT_COMBOBOX, self.on_cambio_filtro)

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

    def on_cambio_filtro(self, event):
        """Habilita o deshabilita el botón de filtrar según si hay filtros seleccionados."""
        dias_abierto = self.dias_abierto_ctrl.GetValue().strip()
        tipo_irregularidad = self.tipo_irregularidad_combo.GetValue().strip()

        # Habilitar el botón si al menos un filtro está seleccionado
        if dias_abierto or tipo_irregularidad:
            self.boton_aplicar_filtros.Enable()
        else:
            self.boton_aplicar_filtros.Disable()

    def on_aplicar_filtros(self, event):
        """Aplica los filtros y actualiza la vista."""
        dias_abierto = self.dias_abierto_ctrl.GetValue().strip()
        tipo_irregularidad = self.tipo_irregularidad_combo.GetValue().strip()

        # Validar que al menos un filtro esté seleccionado
        if not dias_abierto and not tipo_irregularidad:
            wx.MessageBox("Debe seleccionar al menos un filtro (días abierto o tipo de irregularidad).", "Error", wx.OK | wx.ICON_ERROR)
            return

        # Convertir días abierto a entero (si está presente)
        dias_abierto_int = None
        if dias_abierto:
            try:
                dias_abierto_int = int(dias_abierto)
            except ValueError:
                wx.MessageBox("El valor de días abierto debe ser un número entero.", "Error", wx.OK | wx.ICON_ERROR)
                return

        # Obtener los casos filtrados
        casos_filtrados = self.controlador.obtener_casos_filtrados(dias_abierto_int, tipo_irregularidad)

        # Mostrar mensaje con la cantidad de expedientes filtrados
        wx.MessageBox(f"Se encontraron {len(casos_filtrados)} expedientes que cumplen con los filtros.", "Resultados", wx.OK | wx.ICON_INFORMATION)

        # Actualizar la vista con los casos filtrados
        self.actualizar_vista(casos_filtrados)


    def actualizar_vista(self, casos):
        """Actualiza la vista con los casos filtrados."""
        # Limpiar la lista de expedientes en el ComboBox
        self.nro_expediente_combo.Clear()

        # Agregar los casos filtrados al ComboBox
        for caso in casos:
            self.nro_expediente_combo.Append(caso['nro_expediente'])

        # Limpiar todos los campos de texto
        for campo in self.text_ctrls:
            self.text_ctrls[campo].SetValue("")

        # Dejar la lista vacía, esperando que el usuario seleccione un expediente
        if casos:
            self.nro_expediente_combo.SetSelection(wx.NOT_FOUND)  # No seleccionar nada automáticamente


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