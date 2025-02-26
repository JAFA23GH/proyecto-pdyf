from controllers.caso_controller import CasoController
import wx

class MenuView(wx.Frame):
    def __init__(self, controller, user_id, nombre, rol, *args, **kw):
        super(MenuView, self).__init__(*args, **kw)
        self.controller = controller
        self.user_id = user_id
        self.nombre = nombre
        self.rol = rol

        # Cambiar el icono de la ventana
        icon = wx.Icon("img/iconoinstitucional.ico", wx.BITMAP_TYPE_ICO)  # Cambia la ruta al icono
        self.SetIcon(icon)

        self.InitUI()

    def InitUI(self):
        self.SetTitle(f"Menú Principal {self.nombre} ({self.rol})")
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
        self.controlador = CasoController(user_id=self.user_id, rol=self.rol, menu_view=self)
        if opcion == "Registrar caso de investigación":
            self.Hide()  # Oculta la ventana del menú principal
            self.controlador.mostrar_ventana(vista="registro")
        elif opcion == "Asignar casos":
            self.Hide()  # Oculta la ventana del menú principal
            self.controlador.mostrar_ventana(vista="asignar")
        elif opcion == "Modificar caso de investigación":
            self.Hide()  # Oculta la ventana del menú principal
            self.controlador.mostrar_ventana(vista="modificar")
        elif opcion == "Generar reportes":
            self.Hide()  # Oculta la ventana del menú principal
            self.controlador.mostrar_ventana(vista="Gen-reporte")
        elif opcion == "Visualizar alarmas":
            self.Hide()  # Oculta la ventana del menú principal
            self.controlador.mostrar_ventana(vista="Vis-alarma")
        elif opcion == "Reabrir caso de investigación":
            self.Hide()  # Oculta la ventana del menú principal
            self.controlador.mostrar_ventana(vista="Reabrir-caso")
        else:
            wx.MessageBox(f"Seleccionaste: {opcion}", "Información", wx.OK | wx.ICON_INFORMATION)



    def reopen(self):
        self.Show()  # Muestra la ventana del menú principal