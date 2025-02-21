from datetime import date
import wx


class VentanaRegistro(wx.Frame):
    def __init__(self, parent, controlador, usuario, rol, menu_view=None):
        super(VentanaRegistro, self).__init__(parent)
        self.SetTitle("Registro de Caso")
        self.SetSize((600, 800))
        self.controlador = controlador  # Referencia al controlador
        self.usuario = usuario
        self.rol = rol
        self.menu_view = menu_view

        self.text_ctrls = {}
        panel = wx.ScrolledWindow(self)
        panel.SetScrollRate(5, 5)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Radio Button Tipo de Caso
        tipo_caso_label = wx.StaticText(panel, label="Tipo de Caso:")
        vbox.Add(tipo_caso_label, flag=wx.ALIGN_LEFT | wx.TOP, border=5)
        self.tipo_caso_radiobox = wx.RadioBox(panel, choices=["Gestión", "Reclamo", "Caso"])
        vbox.Add(self.tipo_caso_radiobox, flag=wx.ALIGN_LEFT | wx.TOP, border=5)

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
            vbox.Add(label, flag=wx.ALIGN_LEFT | wx.TOP, border=5)
            textbox = wx.TextCtrl(panel)
            vbox.Add(textbox, flag=wx.EXPAND | wx.TOP, border=5)
            self.text_ctrls[campo] = textbox

        # Campo Fecha de Inicio
        label_fecha_inicio = wx.StaticText(panel, label="Fecha de inicio:")
        vbox.Add(label_fecha_inicio, flag=wx.ALIGN_LEFT | wx.TOP, border=5)
        self.text_ctrls["Fecha de inicio"] = wx.TextCtrl(panel)
        vbox.Add(self.text_ctrls["Fecha de inicio"], flag=wx.EXPAND | wx.TOP, border=5)
        self.text_ctrls["Fecha de inicio"].SetValue(date.today().strftime('%d/%m/%Y'))

        # Campo Investigador
        investigador_label = wx.StaticText(panel, label="Investigador:")
        vbox.Add(investigador_label, flag=wx.ALIGN_LEFT | wx.TOP, border=5)

        if self.rol == "Administrador":
            self.investigador_combo = wx.ComboBox(panel, choices=self.controlador.obtener_investigadores())
            vbox.Add(self.investigador_combo, flag=wx.EXPAND | wx.TOP, border=5)
        else:
            self.investigador_text = wx.TextCtrl(panel, value=self.usuario, style=wx.TE_READONLY)
            vbox.Add(self.investigador_text, flag=wx.EXPAND | wx.TOP, border=5)

        # Botones
        hbox_botones = wx.BoxSizer(wx.HORIZONTAL)
        boton_aceptar = wx.Button(panel, label="Aceptar")
        boton_cancelar = wx.Button(panel, label="Cancelar")
        hbox_botones.Add(boton_aceptar, flag=wx.RIGHT, border=5)
        hbox_botones.Add(boton_cancelar)
        vbox.Add(hbox_botones, flag=wx.ALIGN_CENTER | wx.ALL, border=10)

        # Eventos
        boton_aceptar.Bind(wx.EVT_BUTTON, self.on_aceptar)
        boton_cancelar.Bind(wx.EVT_BUTTON, lambda event: self.on_cancel(event))

        panel.SetSizer(vbox)

    def on_aceptar(self, event):
        from controllers.caso_controller import CasoController
        self.controle = CasoController(self, rol=self.rol, menu_view=None)
        self.controle.registrar_caso(self)


    def on_cancel(self, event):
        self.Close()  # Cierra la ventana de registro
        self.controlador.menu_view.reopen()