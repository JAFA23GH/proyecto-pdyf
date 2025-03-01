import wx

class VentanaCerrarCaso(wx.Frame):
    def __init__(self, parent, controlador, usuario, rol, *args, **kw):
        super(VentanaCerrarCaso, self).__init__(parent, *args, **kw)
        self.controlador = controlador  # Referencia al controlador
        self.usuario = usuario
        self.rol = rol

        # Cambiar el icono de la ventana
        icon = wx.Icon("img/iconoinstitucional.ico", wx.BITMAP_TYPE_ICO)  # Cambia la ruta al icono
        self.SetIcon(icon)

        self.InitUI()

        # Manejar el evento de cierre de la ventana
        self.Bind(wx.EVT_CLOSE, self.on_close)

    def InitUI(self):
        pnl = wx.Panel(self)

        vbox = wx.BoxSizer(wx.VERTICAL)

        st1 = wx.StaticText(pnl, label='Seleccione el caso:')
        vbox.Add(st1, flag=wx.LEFT | wx.TOP, border=10)

        # Obtener los casos asignados al investigador logueado
        self.casos_asignados = self.controlador.obtener_casos_asignados(self.usuario)
        self.case_choice = wx.Choice(pnl, choices=self.casos_asignados)
        self.case_choice.Bind(wx.EVT_CHOICE, self.OnSeleccionarCaso)  # Evento al seleccionar un caso
        vbox.Add(self.case_choice, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        st2 = wx.StaticText(pnl, label='Actuaciones / acciones:')
        vbox.Add(st2, flag=wx.LEFT | wx.TOP, border=10)

        self.obs_txt = wx.TextCtrl(pnl, style=wx.TE_MULTILINE)
        vbox.Add(self.obs_txt, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        st3 = wx.StaticText(pnl, label='Observaciones')
        vbox.Add(st3, flag=wx.LEFT | wx.TOP, border=10)

        self.concl_txt = wx.TextCtrl(pnl, style=wx.TE_MULTILINE)
        vbox.Add(self.concl_txt, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        st4 = wx.StaticText(pnl, label='Conclusiones / Recomendaciones:')
        vbox.Add(st4, flag=wx.LEFT | wx.TOP, border=10)

        self.rec_txt = wx.TextCtrl(pnl, style=wx.TE_MULTILINE)
        vbox.Add(self.rec_txt, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        hbox = wx.BoxSizer(wx.HORIZONTAL)

        close_btn = wx.Button(pnl, label='Cerrar Caso')
        close_btn.Bind(wx.EVT_BUTTON, self.OnCloseCase)
        hbox.Add(close_btn, flag=wx.RIGHT, border=10)

        cancel_btn = wx.Button(pnl, label='Cancelar')
        cancel_btn.Bind(wx.EVT_BUTTON, self.OnCancel)
        hbox.Add(cancel_btn, flag=wx.RIGHT, border=10)

        vbox.Add(hbox, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=10)

        pnl.SetSizer(vbox)

        self.SetSize((400, 600))
        self.SetTitle('Cerrar Caso de Investigación')
        self.Centre()

    def OnSeleccionarCaso(self, event):
        """Evento que se ejecuta cuando se selecciona un caso."""
        expediente = self.case_choice.GetStringSelection()
        if expediente:
            # Obtener los datos del expediente seleccionado
            datos_expediente = self.controlador.obtener_datos_expediente(expediente)
            if datos_expediente:
                # Llenar los campos con los datos del expediente
                self.obs_txt.SetValue(datos_expediente.get("Actuaciones/Acciones Realizadas", ""))
                self.concl_txt.SetValue(datos_expediente.get("Observaciones", ""))
                self.rec_txt.SetValue(datos_expediente.get("Conclusiones / Recomendaciones", ""))

    def OnCloseCase(self, event):
        # Obtener los valores de los campos
        case = self.case_choice.GetStringSelection()
        observations = self.obs_txt.GetValue()
        conclusions = self.concl_txt.GetValue()
        recommendations = self.rec_txt.GetValue()

        if not case:
            wx.MessageBox('Seleccione un caso.', 'Error', wx.OK | wx.ICON_ERROR)
            return

        if not observations or not conclusions or not recommendations:
            wx.MessageBox('Por favor, complete todos los campos.', 'Error', wx.OK | wx.ICON_ERROR)
            return

        # Llamar al controlador para cerrar el caso
        exito, mensaje = self.controlador.cerrar_caso(case, observations, conclusions, recommendations)
        wx.MessageBox(mensaje, 'Información', wx.OK | wx.ICON_INFORMATION)
        if exito:
            self.Close()

    def OnCancel(self, event):
        # Lógica para cancelar y cerrar la ventana
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