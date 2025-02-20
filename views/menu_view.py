from views.caso_view import VentanaRegistro
import wx

class MenuView(wx.Frame):
    def __init__(self, controller, user_id, nombre, rol, *args, **kw):
        super(MenuView, self).__init__(*args, **kw)
        self.controller = controller
        self.user_id = user_id
        self.nombre = nombre
        self.rol = rol
        self.InitUI()

    def InitUI(self):
        self.SetTitle(f"Menú Principal - {self.nombre} ({self.rol})")
        self.SetSize((400, 500))
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Mostrar mensaje de bienvenida
        bienvenida = wx.StaticText(panel, label=f"Bienvenido, {self.nombre}")
        vbox.Add(bienvenida, flag=wx.ALIGN_CENTER | wx.TOP, border=10)

        # Opciones comunes a ambos roles
        opciones = [
            "Registrar caso de investigación",
            "Reabrir caso de investigación",
            "Consultar auditorías"
        ]

        # Opciones según el rol
        if self.rol == "Investigador":
            opciones += [
                "Modificar caso de investigación",
                "Cerrar caso de investigación"
            ]
        elif self.rol == "Administrador":
            opciones += [
                "Asignar casos",
                "Generar reportes",
                "Visualizar alarmas",
                "Gestionar entidades",
                "Registrar archivos negados",
                "Configurar criterios de alarmas",
                "Consultar cartelera de casos"
            ]

        # Crear botones dinámicamente
        for opcion in opciones:
            btn = wx.Button(panel, label=opcion, size=(250, 30))
            vbox.Add(btn, flag=wx.ALIGN_CENTER | wx.TOP, border=5)
            btn.Bind(wx.EVT_BUTTON, self.on_option_selected)

        panel.SetSizer(vbox)

    def on_option_selected(self, event):
        """Maneja el clic en las opciones del menú."""
        button = event.GetEventObject()
        opcion = button.GetLabel()
        if opcion == "Registrar caso de investigación":
            ventana = VentanaRegistro(self, usuario=self.nombre, rol=self.rol)  # Pasa el usuario y rol
            ventana.Show()  # Muestra la ventana
        wx.MessageBox(f"Seleccionaste: {opcion}", "Información", wx.OK | wx.ICON_INFORMATION)

