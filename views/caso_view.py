from datetime import date
import wx

class VentanaRegistro(wx.Frame):
    def __init__(self, parent, controlador, usuario, rol, menu_view=None):
        super(VentanaRegistro, self).__init__(parent)
        self.SetTitle("Registro de Caso")
        self.SetSize((800, 800))
        self.controlador = controlador  # Referencia al controlador
        self.usuario = usuario
        self.rol = rol
        self.menu_view = menu_view

        # Manejar el evento de cierre de la ventana
        self.Bind(wx.EVT_CLOSE, self.on_close)

        # Cambiar el icono de la ventana
        icon = wx.Icon("img/iconoinstitucional.ico", wx.BITMAP_TYPE_ICO)  # Cambia la ruta al icono
        self.SetIcon(icon)

        self.text_ctrls = {}
        panel = wx.ScrolledWindow(self)
        panel.SetScrollRate(5, 5)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Radio Button Tipo de Caso
        tipo_caso_label = wx.StaticText(panel, label="Tipo de Caso:")
        vbox.Add(tipo_caso_label, flag=wx.ALIGN_LEFT | wx.TOP, border=10)
        self.tipo_caso_radiobox = wx.RadioBox(panel, choices=["Gestión", "Reclamo", "Caso"])
        vbox.Add(self.tipo_caso_radiobox, flag=wx.ALIGN_LEFT | wx.TOP | wx.LEFT | wx.RIGHT, border=10)

        # Campos de texto
        campos = [
            "Nro. Expediente", "Móvil afectado", "Tipo de irregularidad", "Subtipo irregularidad",
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

        # Campo Fecha de Inicio
        label_fecha_inicio = wx.StaticText(panel, label="Fecha de inicio:")
        vbox.Add(label_fecha_inicio, flag=wx.ALIGN_LEFT | wx.TOP, border=10)
        self.text_ctrls["Fecha de inicio"] = wx.TextCtrl(panel)
        vbox.Add(self.text_ctrls["Fecha de inicio"], flag=wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, border=10)
        self.text_ctrls["Fecha de inicio"].SetValue(date.today().strftime('%d/%m/%Y'))

        # Campo Investigador
        investigador_label = wx.StaticText(panel, label="Investigador:")
        vbox.Add(investigador_label, flag=wx.ALIGN_LEFT | wx.TOP, border=10)

        if self.rol == "Administrador":
            self.investigador_combo = wx.ComboBox(panel, choices=self.controlador.obtener_investigadores())
            vbox.Add(self.investigador_combo, flag=wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, border=10)
        else:
            self.investigador_text = wx.TextCtrl(panel, value=self.usuario, style=wx.TE_READONLY)
            vbox.Add(self.investigador_text, flag=wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, border=10)

        # Botones
        hbox_botones = wx.BoxSizer(wx.HORIZONTAL)
        boton_aceptar = wx.Button(panel, label="Aceptar")
        boton_cancelar = wx.Button(panel, label="Cancelar")
        hbox_botones.Add(boton_aceptar, flag=wx.RIGHT | wx.LEFT, border=10)
        hbox_botones.Add(boton_cancelar, flag=wx.LEFT, border=10)
        vbox.Add(hbox_botones, flag=wx.ALIGN_CENTER | wx.ALL, border=20)

        # Eventos
        boton_aceptar.Bind(wx.EVT_BUTTON, self.on_aceptar)
        boton_cancelar.Bind(wx.EVT_BUTTON, lambda event: self.on_cancel(event))

        panel.SetSizer(vbox)

    def on_aceptar(self, event):
        from controllers.caso_controller import CasoController
        self.controle = CasoController(self, rol=self.rol, menu_view=None)
        self.controle.registrar_caso(self)

    def on_cancel(self, event):
        self.Hide()  # Cierra la ventana de registro
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
