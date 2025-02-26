import wx

class LoginView(wx.Frame):
    def __init__(self, controller, *args, **kw):
        super(LoginView, self).__init__(*args, **kw)
        self.controller = controller  # Almacena la referencia al controlador
        self.SetTitle("Agencia de investigación gubernamental")  # Título de la ventana
        self.SetSize((400, 200))  # Establece un tamaño fijo para la ventana

        # Cambiar el icono de la ventana
        icon = wx.Icon("img/iconoinstitucional.ico", wx.BITMAP_TYPE_ICO)  # Cambia la ruta al icono
        self.SetIcon(icon)

        self.InitUI()

    def InitUI(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Campo de usuario
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        st1 = wx.StaticText(panel, label='Usuario:')
        hbox1.Add(st1, flag=wx.RIGHT, border=8)
        self.usuario = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER)  # Agregar la bandera aquí
        hbox1.Add(self.usuario, proportion=1)
        vbox.Add(hbox1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        # Campo de contraseña
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        st2 = wx.StaticText(panel, label='Contraseña:')
        hbox2.Add(st2, flag=wx.RIGHT, border=8)
        self.contraseña = wx.TextCtrl(panel, style=wx.TE_PASSWORD | wx.TE_PROCESS_ENTER)  # Agregar la bandera aquí
        hbox2.Add(self.contraseña, proportion=1)
        vbox.Add(hbox2, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        # Botón de login
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        btn_login = wx.Button(panel, label='Iniciar Sesión', size=(100, 30))
        hbox3.Add(btn_login)
        vbox.Add(hbox3, flag=wx.ALIGN_CENTER | wx.TOP, border=10)

        # Evento del botón
        btn_login.Bind(wx.EVT_BUTTON, self.on_login)

        # Asignar el evento de Enter a la función de login
        self.usuario.Bind(wx.EVT_TEXT_ENTER, self.on_login)
        self.contraseña.Bind(wx.EVT_TEXT_ENTER, self.on_login)

        panel.SetSizer(vbox)
        self.Centre()  # Centra la ventana en la pantalla

    def on_login(self, event):
        """Maneja el evento de clic en el botón de login."""
        usuario = self.usuario.GetValue()
        contraseña = self.contraseña.GetValue()
        # Validar que los campos no estén vacíos
        if not usuario or not contraseña:
            wx.MessageBox("Por favor, complete todos los campos", "Error", wx.OK | wx.ICON_ERROR)
            return
        # Llamar al controlador para validar el login
        self.controller.validar_login(usuario, contraseña)

    def on_enter(self, event):
        """Maneja el evento de enfoque al presionar Enter en el botón."""
        event.Skip()  # Permite que el evento continúe