import wx

class VentanaReabrir(wx.Frame):
    def __init__(self, parent, controlador, usuario, rol, menu_view=None):
        super(VentanaReabrir, self).__init__(parent)
        self.SetTitle("Reabrir Caso")
        self.SetSize((600, 800))
        self.controlador = controlador
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

        icon = wx.Icon("img/iconoinstitucional.ico", wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)

        self.nro_expediente_combo = wx.ComboBox(panel, choices=self.controlador.obtener_casos_cerrados(self.usuario))
        vbox.Add(wx.StaticText(panel, label="Nro. Expediente:"), flag=wx.ALIGN_LEFT | wx.TOP, border=10)
        vbox.Add(self.nro_expediente_combo, flag=wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, border=10)

        self.nro_expediente_combo.Bind(wx.EVT_COMBOBOX, self.on_expediente_select)

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

        estatus_label = wx.StaticText(panel, label="Estatus del Caso:")
        vbox.Add(estatus_label, flag=wx.ALIGN_LEFT | wx.TOP, border=10)
        self.estatus_combo = wx.ComboBox(panel, choices=["Cerrado", "Re-abierto"])
        vbox.Add(self.estatus_combo, flag=wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, border=10)
        self.estatus_combo.Bind(wx.EVT_COMBOBOX, self.verificar_cambios)

        hbox_botones = wx.BoxSizer(wx.HORIZONTAL)
        self.boton_aceptar = wx.Button(panel, label="Aceptar")
        self.boton_aceptar.Enable(False)
        boton_cancelar = wx.Button(panel, label="Cancelar")
        hbox_botones.Add(self.boton_aceptar, flag=wx.RIGHT | wx.LEFT, border=10)
        hbox_botones.Add(boton_cancelar, flag=wx.LEFT, border=10)
        vbox.Add(hbox_botones, flag=wx.ALIGN_CENTER | wx.ALL, border=20)

        self.boton_aceptar.Bind(wx.EVT_BUTTON, self.on_aceptar)
        boton_cancelar.Bind(wx.EVT_BUTTON, lambda event: self.on_cancel(event))
        panel.SetSizer(vbox)

    def on_expediente_select(self, event):
        expediente_seleccionado = self.nro_expediente_combo.GetValue()
        datos_expediente = self.controlador.obtener_datos_expediente(expediente_seleccionado)

        if datos_expediente:
            self.original_values.clear()
            for campo, valor in datos_expediente.items():
                if campo in self.text_ctrls:
                    self.text_ctrls[campo].SetValue(str(valor))
                    self.original_values[campo] = str(valor)

            # Obtener el estado del caso desde los datos del expediente
            estado_caso = datos_expediente.get("Estatus", "Cerrado")
            # Establecer el valor del estatus
            self.estatus_combo.SetValue(estado_caso)
            self.original_values["Estatus"] = estado_caso

        self.verificar_cambios()

    def verificar_cambios(self, event=None):
        expediente_seleccionado = self.nro_expediente_combo.GetValue() != ""
        cambios_realizados = any(
            self.text_ctrls[campo].GetValue() != self.original_values.get(campo, "")
            for campo in self.text_ctrls
        ) or self.estatus_combo.GetValue() != self.original_values.get("Estatus", "Cerrado")

        # Habilitar el botón "Aceptar" solo si el estatus es "Re-abierto"
        estatus_actual = self.estatus_combo.GetValue()
        self.boton_aceptar.Enable(expediente_seleccionado and cambios_realizados and estatus_actual == "Re-abierto")

    def on_aceptar(self, event):
        from controllers.caso_controller import CasoController
        from patterns.decorator import CasoDecorator

        mensaje = '¿Está seguro de que desea realizar los cambios?'
        dialogo = wx.MessageDialog(None, mensaje, 'Confirmación', wx.YES_NO | wx.ICON_QUESTION)
        respuesta = dialogo.ShowModal()

        if respuesta == wx.ID_YES:
            nro_expediente = self.nro_expediente_combo.GetValue()
            datos_actualizados = {campo: self.text_ctrls[campo].GetValue() for campo in self.text_ctrls}
            nuevo_estatus = "Re-abierto"

            self.controle = CasoController(self.usuario, self.rol, self.menu_view)
            decorated_controller = CasoDecorator(self.controle)

            decorated_controller.modificar_caso(nro_expediente, datos_actualizados, nuevo_estatus)

    def on_cancel(self, event):
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