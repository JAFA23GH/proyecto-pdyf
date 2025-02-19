import wx
import sqlite3

class VentanaRegistro(wx.Frame):
    def __init__(self, parent, usuario, rol, *args, **kw):
        super(VentanaRegistro, self).__init__(parent, *args, **kw)
        self.SetTitle("Registro de Caso")
        self.SetSize((600, 800))
        self.usuario = usuario
        self.rol = rol

        panel = wx.ScrolledWindow(self)
        panel.SetScrollRate(5, 5)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Radio Button para Tipo de Caso
        tipo_caso_label = wx.StaticText(panel, label="Tipo de Caso:")
        vbox.Add(tipo_caso_label, flag=wx.ALIGN_LEFT | wx.TOP, border=5)
        self.tipo_caso_radiobox = wx.RadioBox(panel, label="", choices=["Gestión", "Reclamo", "Caso"], style=wx.RA_SPECIFY_COLS)
        vbox.Add(self.tipo_caso_radiobox, flag=wx.ALIGN_LEFT | wx.TOP, border=5)

        # Campos de texto
        campos = [
            "Nro. Expediente", "Fecha de inicio", "Móvil afectado", "Tipo de irregularidad", "Subtipo irregularidad",
            "Objetivo / Agraviado", "Incidencia", "Duración (Días)", "Descripción Modus Operandi",
            "Área Apoyo a Resolver", "Detección / Procedencia del Caso",
            "Diagnostico / Detalle de Comprobación para Determinar Fraude",
            "Actuaciones/Acciones Realizadas", "Conclusiones / Recomendaciones", "Observaciones", "Soporte"
        ]

        self.text_ctrls = {}  # Diccionario para almacenar los textboxes

        for campo in campos:
            label = wx.StaticText(panel, label=campo + ":")
            vbox.Add(label, flag=wx.ALIGN_LEFT | wx.TOP, border=5)
            textbox = wx.TextCtrl(panel)
            vbox.Add(textbox, flag=wx.EXPAND | wx.TOP, border=5)
            self.text_ctrls[campo] = textbox  # Guardar el campo

        # Campo Investigador
        investigador_label = wx.StaticText(panel, label="Investigador:")
        vbox.Add(investigador_label, flag=wx.ALIGN_LEFT | wx.TOP, border=5)

        if self.rol == "Administrador":
            self.investigador_combo = wx.ComboBox(panel, choices=self.obtener_investigadores())
            vbox.Add(self.investigador_combo, flag=wx.EXPAND | wx.TOP, border=5)
        else:
            self.investigador_text = wx.TextCtrl(panel, value=self.usuario, style=wx.TE_READONLY)
            vbox.Add(self.investigador_text, flag=wx.EXPAND | wx.TOP, border=5)

        # Espaciado antes de los botones
        vbox.AddStretchSpacer()

        # Botones Aceptar y Cancelar
        hbox_botones = wx.BoxSizer(wx.HORIZONTAL)
        boton_aceptar = wx.Button(panel, label="Aceptar")
        boton_cancelar = wx.Button(panel, label="Cancelar")
        hbox_botones.Add(boton_aceptar, flag=wx.RIGHT, border=5)
        hbox_botones.Add(boton_cancelar)
        vbox.Add(hbox_botones, flag=wx.ALIGN_CENTER | wx.ALL, border=10)

        # Enlazar eventos de los botones
        boton_aceptar.Bind(wx.EVT_BUTTON, self.on_aceptar)
        boton_cancelar.Bind(wx.EVT_BUTTON, self.on_cancelar)

        panel.SetSizer(vbox)
        panel.SetVirtualSize((580, 1200))  # Tamaño virtual para permitir desplazamiento

    def obtener_investigadores(self):
        """Obtiene la lista de investigadores de la base de datos."""
        conn = sqlite3.connect("investigacion.db")
        cursor = conn.cursor()
        cursor.execute("SELECT nombre FROM Usuarios WHERE rol = 'Investigador'")
        investigadores = [row[0] for row in cursor.fetchall()]
        conn.close()
        return investigadores

    def on_aceptar(self, event):
        # Lista de campos requeridos
        campos_requeridos = [
            "Nro. Expediente",
            "Fecha de inicio",
            "Móvil afectado",
            "Tipo de irregularidad",
            "Objetivo / Agraviado",
            "Descripción Modus Operandi",
            "Conclusiones / Recomendaciones"
        ]

        # Verificar si los campos requeridos están llenos
        for campo in campos_requeridos:
            if not self.text_ctrls[campo].GetValue().strip():
                wx.MessageBox(f"El campo '{campo}' es requerido.", "Error", wx.OK | wx.ICON_ERROR)
                return  # Salir si hay un campo requerido vacío

        # Verificar el campo "Investigador"
        if self.rol == "Administrador":
            if not self.investigador_combo.GetValue().strip():
                wx.MessageBox("El campo 'Investigador' es requerido.", "Error", wx.OK | wx.ICON_ERROR)
                return  # Salir si el campo está vacío
        else:
            if not self.investigador_text.GetValue().strip():
                wx.MessageBox("El campo 'Investigador' es requerido.", "Error", wx.OK | wx.ICON_ERROR)
                return  # Salir si el campo está vacío

        # Si todos los campos requeridos están completos
        wx.MessageBox("Datos guardados (simulado)", "Información", wx.OK | wx.ICON_INFORMATION)
        self.Close()

    def on_cancelar(self, event):
        self.Close()



if __name__ == '__main__':
    app = wx.App()
    frame = VentanaRegistro(None, usuario="Juan Pérez", rol="Administrador")  # Cambia según el usuario logueado
    frame.Show()
    app.MainLoop()
