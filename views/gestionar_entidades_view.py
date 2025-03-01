import wx
from wx.grid import Grid

class VentanaGestionarEntidades(wx.Frame):
    def __init__(self, parent, controller, menu_view=None, *args, **kw):
        super(VentanaGestionarEntidades, self).__init__(parent, *args, **kw)
        self.controller = controller
        self.menu_view = menu_view
        self.SetTitle("Gestión de Entidades")
        self.SetSize((800, 500))

        self.InitUI()
        self.Centre()
        self.Bind(wx.EVT_CLOSE, self.on_close)

    def InitUI(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Grid para mostrar las entidades
        self.grid = Grid(panel)
        self.grid.CreateGrid(0, 9)  # 9 columnas según la estructura de la tabla
        self.grid.SetColLabelValue(0, "ID")
        self.grid.SetColLabelValue(1, "Tipo Brecha")
        self.grid.SetColLabelValue(2, "Tipo Proyecto")
        self.grid.SetColLabelValue(3, "Proceso Corregido")
        self.grid.SetColLabelValue(4, "Proceso Realizado")
        self.grid.SetColLabelValue(5, "Investigador ID")
        self.grid.SetColLabelValue(6, "Empresa")
        self.grid.SetColLabelValue(7, "Subtipo Ficha")
        self.grid.SetColLabelValue(8, "Tipo Irregularidad")
        vbox.Add(self.grid, 1, wx.EXPAND | wx.ALL, 10)

        # Botones para CRUD
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        btn_agregar = wx.Button(panel, label="Agregar")
        btn_editar = wx.Button(panel, label="Editar")
        btn_eliminar = wx.Button(panel, label="Eliminar")
        btn_cancelar = wx.Button(panel, label="Cancelar")
        hbox.Add(btn_agregar)
        hbox.Add(btn_editar, flag=wx.LEFT, border=5)
        hbox.Add(btn_eliminar, flag=wx.LEFT, border=5)
        hbox.Add(btn_cancelar, flag=wx.LEFT, border=5)
        vbox.Add(hbox, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=10)

        # Eventos de los botones
        btn_agregar.Bind(wx.EVT_BUTTON, self.on_agregar)
        btn_editar.Bind(wx.EVT_BUTTON, self.on_editar)
        btn_eliminar.Bind(wx.EVT_BUTTON, self.on_eliminar)
        btn_cancelar.Bind(wx.EVT_BUTTON, self.on_cancelar)

        panel.SetSizer(vbox)
        self.cargar_entidades()

    def cargar_entidades(self):
        entidades = self.controller.obtener_entidades()  # Suponiendo que devuelve una lista de listas o tuplas

        # Asegúrate de que el grid tiene suficientes filas y columnas
        self.grid.ClearGrid()

        if self.grid.GetNumberRows() < len(entidades):
            self.grid.AppendRows(len(entidades) - self.grid.GetNumberRows())

        if self.grid.GetNumberCols() < len(entidades[0]):
            self.grid.AppendCols(len(entidades[0]) - self.grid.GetNumberCols())

        # Rellena el grid con los datos
        for i, entidad in enumerate(entidades):
            for j, dato in enumerate(entidad):
                self.grid.SetCellValue(i, j, str(dato))

    def on_agregar(self, event):
        """Abre un diálogo para agregar una nueva entidad."""
        dialog = wx.Dialog(self, title="Agregar Entidad", size=(400, 300))

        # Crear un ScrolledWindow
        scrolled_window = wx.ScrolledWindow(dialog)
        scrolled_window.SetScrollRate(10, 10)  # Velocidad del scroll

        # Crear un panel dentro del ScrolledWindow
        panel = wx.Panel(scrolled_window)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Campos del formulario
        campos = [
            ("Tipo Brecha", wx.TextCtrl(panel)),
            ("Tipo Proyecto", wx.TextCtrl(panel)),
            ("Proceso Corregido", wx.TextCtrl(panel)),
            ("Proceso Realizado", wx.TextCtrl(panel)),
            ("Investigador ID", wx.TextCtrl(panel)),
            ("Empresa", wx.TextCtrl(panel)),
            ("Subtipo Ficha", wx.TextCtrl(panel)),
            ("Tipo Irregularidad", wx.TextCtrl(panel))
        ]

        for label, control in campos:
            vbox.Add(wx.StaticText(panel, label=label), flag=wx.TOP | wx.LEFT, border=5)
            vbox.Add(control, flag=wx.EXPAND | wx.ALL, border=5)

        # Botones de acción
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        btn_aceptar = wx.Button(panel, label="Aceptar", id=wx.ID_OK)
        btn_cancelar = wx.Button(panel, label="Cancelar", id=wx.ID_CANCEL)
        hbox.Add(btn_aceptar)
        hbox.Add(btn_cancelar, flag=wx.LEFT, border=5)

        vbox.Add(hbox, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=10)

        # Asignar el sizer al panel
        panel.SetSizer(vbox)

        # Ajustar el tamaño del ScrolledWindow para que se active el scroll si es necesario
        scrolled_window.SetSizer(wx.BoxSizer())
        scrolled_window.GetSizer().Add(panel, 1, wx.EXPAND)
        scrolled_window.FitInside()  # Ajustar el contenido dentro del ScrolledWindow

        # Mostrar el diálogo y manejar la respuesta
        resultado = dialog.ShowModal()
        if resultado == wx.ID_OK:
            datos = [control.GetValue() for _, control in campos]
            self.controller.agregar_entidad(*datos)
            self.cargar_entidades()
        dialog.Destroy()

    def on_editar(self, event):
        """Abre un diálogo para editar una entidad."""
        selected_row = self.grid.GetGridCursorRow()
        if selected_row >= 0:
            entidad_id = self.grid.GetCellValue(selected_row, 0)
            datos_actuales = [self.grid.GetCellValue(selected_row, col) for col in range(1, 9)]

            dialog = wx.Dialog(self, title="Editar Entidad", size=(400, 300))

            # Crear un ScrolledWindow
            scrolled_window = wx.ScrolledWindow(dialog)
            scrolled_window.SetScrollRate(10, 10)  # Velocidad del scroll

            # Crear un panel dentro del ScrolledWindow
            panel = wx.Panel(scrolled_window)
            vbox = wx.BoxSizer(wx.VERTICAL)

            # Campos del formulario
            campos = [
                ("Tipo Brecha", wx.TextCtrl(panel, value=datos_actuales[0])),
                ("Tipo Proyecto", wx.TextCtrl(panel, value=datos_actuales[1])),
                ("Proceso Corregido", wx.TextCtrl(panel, value=datos_actuales[2])),
                ("Proceso Realizado", wx.TextCtrl(panel, value=datos_actuales[3])),
                ("Investigador ID", wx.TextCtrl(panel, value=datos_actuales[4])),
                ("Empresa", wx.TextCtrl(panel, value=datos_actuales[5])),
                ("Subtipo Ficha", wx.TextCtrl(panel, value=datos_actuales[6])),
                ("Tipo Irregularidad", wx.TextCtrl(panel, value=datos_actuales[7]))
            ]

            for label, control in campos:
                vbox.Add(wx.StaticText(panel, label=label), flag=wx.TOP | wx.LEFT, border=5)
                vbox.Add(control, flag=wx.EXPAND | wx.ALL, border=5)

            # Botones de acción
            hbox = wx.BoxSizer(wx.HORIZONTAL)
            btn_aceptar = wx.Button(panel, label="Aceptar", id=wx.ID_OK)
            btn_cancelar = wx.Button(panel, label="Cancelar", id=wx.ID_CANCEL)
            hbox.Add(btn_aceptar)
            hbox.Add(btn_cancelar, flag=wx.LEFT, border=5)

            vbox.Add(hbox, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=10)

            # Asignar el sizer al panel
            panel.SetSizer(vbox)

            # Ajustar el tamaño del ScrolledWindow para que se active el scroll si es necesario
            scrolled_window.SetSizer(wx.BoxSizer())
            scrolled_window.GetSizer().Add(panel, 1, wx.EXPAND)
            scrolled_window.FitInside()  # Ajustar el contenido dentro del ScrolledWindow

            # Mostrar el diálogo y manejar la respuesta
            resultado = dialog.ShowModal()
            if resultado == wx.ID_OK:
                nuevos_datos = [control.GetValue() for _, control in campos]
                self.controller.editar_entidad(entidad_id, *nuevos_datos)
                self.cargar_entidades()
            dialog.Destroy()

    def on_eliminar(self, event):
        """Elimina la entidad seleccionada."""
        selected_row = self.grid.GetGridCursorRow()
        if selected_row >= 0:
            entidad_id = self.grid.GetCellValue(selected_row, 0)
            confirm = wx.MessageBox("¿Estás seguro de que quieres eliminar esta entidad?", "Confirmar", wx.YES_NO | wx.ICON_WARNING)
            if confirm == wx.YES:
                self.controller.eliminar_entidad(entidad_id)
                self.cargar_entidades()

    def on_cancelar(self, event):
        """Regresa al menú anterior."""
        self.Hide()
        self.menu_view.Show()

    def on_close(self, event):
        """Maneja el cierre de la ventana."""
        dialogo = wx.MessageDialog(self, "¿Estás seguro de que quieres regresar al menú anterior?", "Cerrar ventana", wx.YES_NO | wx.ICON_QUESTION)
        respuesta = dialogo.ShowModal()
        if respuesta == wx.ID_YES:
            self.Hide()
            self.menu_view.Show()
        else:
            event.Veto()