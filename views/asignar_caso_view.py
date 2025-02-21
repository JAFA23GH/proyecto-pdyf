import wx
from datetime import date

class VentanaAsignar(wx.Frame):
    def __init__(self, parent, controlador, usuario, rol, menu_view=None):
        super(VentanaAsignar, self).__init__(parent)
        self.SetTitle("Asignar Caso")
        self.SetSize((600, 800))
        self.controlador = controlador  # Referencia al controlador
        self.usuario = usuario
        self.rol = rol
        self.menu_view = menu_view
        self.text_ctrls = {}
        panel = wx.ScrolledWindow(self)
        panel.SetScrollRate(5, 5)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # ComboBox para Nro. Expediente
        self.nro_expediente_combo = wx.ComboBox(panel, choices=self.controlador.obtener_casos_abiertos())
        vbox.Add(wx.StaticText(panel, label="Nro. Expediente:"), flag=wx.ALIGN_LEFT | wx.TOP, border=5)
        vbox.Add(self.nro_expediente_combo, flag=wx.EXPAND | wx.TOP, border=5)

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
            vbox.Add(label, flag=wx.ALIGN_LEFT | wx.TOP, border=5)
            textbox = wx.TextCtrl(panel)
            vbox.Add(textbox, flag=wx.EXPAND | wx.TOP, border=5)
            self.text_ctrls[campo] = textbox

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

    def on_expediente_select(self, event):
        """Llena los campos de texto con los datos del expediente seleccionado."""
        expediente_seleccionado = self.nro_expediente_combo.GetValue()
        datos_expediente = self.controlador.obtener_datos_expediente(expediente_seleccionado)

        if datos_expediente:
            # Asumiendo que datos_expediente es un diccionario con los datos del caso
            for campo, valor in datos_expediente.items():
                if campo in self.text_ctrls:
                    self.text_ctrls[campo].SetValue(str(valor))

    def on_aceptar(self, event):
        from controllers.caso_controller import CasoController
        self.controle = CasoController(self, rol=self.rol, menu_view=None)
        self.controle.asignar_investigador(self)  # Método que debes implementar para asignar el investigador

    def on_cancel(self, event):
        self.Close()  # Cierra la ventana de asignación
        self.controlador.menu_view.reopen()