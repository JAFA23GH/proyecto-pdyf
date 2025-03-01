import wx
from wx.grid import Grid
from datetime import datetime  # Para manejar la fecha actual

class VentanaGestionardisciplinario(wx.Frame):
    def __init__(self, parent, controller, menu_view=None, *args, **kw):
        super(VentanaGestionardisciplinario, self).__init__(parent, *args, **kw)
        self.controller = controller
        self.menu_view = menu_view
        self.SetTitle("Gestión de Disciplinario")
        self.SetSize((800, 500))

        self.InitUI()
        self.Centre()
        self.Bind(wx.EVT_CLOSE, self.on_close)

    def InitUI(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Grid para mostrar los registros de disciplinario
        self.grid = Grid(panel)
        self.grid.CreateGrid(0, 6)  # 6 columnas según la estructura de la tabla
        self.grid.SetColLabelValue(0, "ID")
        self.grid.SetColLabelValue(1, "Usuario")
        self.grid.SetColLabelValue(2, "Equipo")
        self.grid.SetColLabelValue(3, "Estatus")
        self.grid.SetColLabelValue(4, "Estado del Equipo")
        self.grid.SetColLabelValue(5, "Fecha del Incidente")
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
        self.cargar_disciplinario()

    def cargar_disciplinario(self):
        """Carga los registros de disciplinario en la grid."""
        registros = self.controller.obtener_disciplinario()
        self.grid.ClearGrid()

        if self.grid.GetNumberRows() > 0:
            self.grid.DeleteRows(0, self.grid.GetNumberRows())

        for i, registro in enumerate(registros):
            self.grid.AppendRows(1)
            self.grid.SetCellValue(i, 0, str(registro['id']))
            self.grid.SetCellValue(i, 1, registro['nombre_usuario'])
            self.grid.SetCellValue(i, 2, registro['nombre_equipo'])
            self.grid.SetCellValue(i, 3, registro['estatus'])
            self.grid.SetCellValue(i, 4, registro['Estado_Equip'])
            self.grid.SetCellValue(i, 5, registro['fecha_incidente'])

    def on_agregar(self, event):
        """Abre un diálogo para agregar un nuevo registro de disciplinario."""
        dialog = wx.Dialog(self, title="Agregar Disciplinario", size=(400, 350))

        # Crear un ScrolledWindow
        scrolled_window = wx.ScrolledWindow(dialog)
        scrolled_window.SetScrollRate(10, 10)  # Velocidad del scroll

        # Crear un panel dentro del ScrolledWindow
        panel = wx.Panel(scrolled_window)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Obtener listas de usuarios y equipos
        usuarios = self.controller.obtener_usuarios()
        equipos = self.controller.obtener_equipos()

        # Campo para seleccionar usuario
        vbox.Add(wx.StaticText(panel, label="Usuario:"), flag=wx.TOP | wx.LEFT, border=5)
        self.combo_usuario = wx.ComboBox(panel, choices=[u[1] for u in usuarios], style=wx.CB_READONLY)
        vbox.Add(self.combo_usuario, flag=wx.EXPAND | wx.ALL, border=5)

        # Campo para seleccionar equipo
        vbox.Add(wx.StaticText(panel, label="Equipo:"), flag=wx.TOP | wx.LEFT, border=5)
        self.combo_equipo = wx.ComboBox(panel, choices=[f"{e[1]} (Serial: {e[2]})" for e in equipos], style=wx.CB_READONLY)
        vbox.Add(self.combo_equipo, flag=wx.EXPAND | wx.ALL, border=5)

        # Campo para seleccionar estatus (solo "Amonestado" o "Suspendido")
        vbox.Add(wx.StaticText(panel, label="Estatus:"), flag=wx.TOP | wx.LEFT, border=5)
        self.combo_estatus = wx.ComboBox(panel, choices=["Amonestado", "Suspendido"], style=wx.CB_READONLY)
        vbox.Add(self.combo_estatus, flag=wx.EXPAND | wx.ALL, border=5)

        # Campo para seleccionar estado del equipo (solo "N/A", "Robado", "Extraviado", "Dañado")
        vbox.Add(wx.StaticText(panel, label="Estado del Equipo:"), flag=wx.TOP | wx.LEFT, border=5)
        self.combo_estado_equipo = wx.ComboBox(panel, choices=["N/A", "Robado", "Extraviado", "Dañado"], style=wx.CB_READONLY)
        vbox.Add(self.combo_estado_equipo, flag=wx.EXPAND | wx.ALL, border=5)

        # Campo para la fecha del incidente (fecha actual por defecto)
        vbox.Add(wx.StaticText(panel, label="Fecha del Incidente:"), flag=wx.TOP | wx.LEFT, border=5)
        self.fecha_incidente = wx.TextCtrl(panel, value=datetime.now().strftime("%Y-%m-%d"), style=wx.TE_READONLY)
        vbox.Add(self.fecha_incidente, flag=wx.EXPAND | wx.ALL, border=5)

        # Campo para la descripción
        vbox.Add(wx.StaticText(panel, label="Descripción:"), flag=wx.TOP | wx.LEFT, border=5)
        self.descripcion = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        vbox.Add(self.descripcion, flag=wx.EXPAND | wx.ALL, border=5)

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
            # Obtener el id del usuario seleccionado
            usuario_index = self.combo_usuario.GetSelection()
            usuario_id = usuarios[usuario_index][0] if usuario_index != wx.NOT_FOUND else None

            # Obtener el id del equipo seleccionado
            equipo_index = self.combo_equipo.GetSelection()
            equipo_id = equipos[equipo_index][0] if equipo_index != wx.NOT_FOUND else None

            # Obtener los demás campos
            estatus = self.combo_estatus.GetValue()
            estado_equip = self.combo_estado_equipo.GetValue()
            fecha_incidente = self.fecha_incidente.GetValue()
            descripcion = self.descripcion.GetValue()

            if usuario_id and equipo_id:
                self.controller.agregar_disciplinario(usuario_id, equipo_id, estatus, estado_equip, fecha_incidente, descripcion)
                self.cargar_disciplinario()
            else:
                wx.MessageBox("Debe seleccionar un usuario y un equipo.", "Error", wx.OK | wx.ICON_ERROR)
        dialog.Destroy()

    def on_editar(self, event):
        """Abre un diálogo para editar un registro de disciplinario."""
        selected_row = self.grid.GetGridCursorRow()
        if selected_row >= 0:
            disciplina_id = int(self.grid.GetCellValue(selected_row, 0))

            dialog = wx.Dialog(self, title="Editar Disciplinario", size=(400, 350))

            # Crear un ScrolledWindow
            scrolled_window = wx.ScrolledWindow(dialog)
            scrolled_window.SetScrollRate(10, 10)  # Velocidad del scroll

            # Crear un panel dentro del ScrolledWindow
            panel = wx.Panel(scrolled_window)
            vbox = wx.BoxSizer(wx.VERTICAL)

            # Obtener listas de usuarios y equipos
            usuarios = self.controller.obtener_usuarios()
            equipos = self.controller.obtener_equipos()

            # Campo para seleccionar usuario
            vbox.Add(wx.StaticText(panel, label="Usuario:"), flag=wx.TOP | wx.LEFT, border=5)
            self.combo_usuario = wx.ComboBox(panel, choices=[u[1] for u in usuarios], style=wx.CB_READONLY)
            vbox.Add(self.combo_usuario, flag=wx.EXPAND | wx.ALL, border=5)

            # Campo para seleccionar equipo
            vbox.Add(wx.StaticText(panel, label="Equipo:"), flag=wx.TOP | wx.LEFT, border=5)
            self.combo_equipo = wx.ComboBox(panel, choices=[f"{e[1]} (Serial: {e[2]})" for e in equipos], style=wx.CB_READONLY)
            vbox.Add(self.combo_equipo, flag=wx.EXPAND | wx.ALL, border=5)

            # Campo para seleccionar estatus (solo "Amonestado" o "Suspendido")
            vbox.Add(wx.StaticText(panel, label="Estatus:"), flag=wx.TOP | wx.LEFT, border=5)
            self.combo_estatus = wx.ComboBox(panel, choices=["Amonestado", "Suspendido"], style=wx.CB_READONLY)
            self.combo_estatus.SetValue(self.grid.GetCellValue(selected_row, 3))  # Cargar valor actual
            vbox.Add(self.combo_estatus, flag=wx.EXPAND | wx.ALL, border=5)

            # Campo para seleccionar estado del equipo (solo "N/A", "Robado", "Extraviado", "Dañado")
            vbox.Add(wx.StaticText(panel, label="Estado del Equipo:"), flag=wx.TOP | wx.LEFT, border=5)
            self.combo_estado_equipo = wx.ComboBox(panel, choices=["N/A", "Robado", "Extraviado", "Dañado"], style=wx.CB_READONLY)
            self.combo_estado_equipo.SetValue(self.grid.GetCellValue(selected_row, 4))  # Cargar valor actual
            vbox.Add(self.combo_estado_equipo, flag=wx.EXPAND | wx.ALL, border=5)

            # Campo para la fecha del incidente (fecha actual por defecto)
            vbox.Add(wx.StaticText(panel, label="Fecha del Incidente:"), flag=wx.TOP | wx.LEFT, border=5)
            self.fecha_incidente = wx.TextCtrl(panel, value=self.grid.GetCellValue(selected_row, 5), style=wx.TE_READONLY)
            vbox.Add(self.fecha_incidente, flag=wx.EXPAND | wx.ALL, border=5)

            # Campo para la descripción
            vbox.Add(wx.StaticText(panel, label="Descripción:"), flag=wx.TOP | wx.LEFT, border=5)
            self.descripcion = wx.TextCtrl(panel, value="", style=wx.TE_MULTILINE)  # Aquí puedes cargar la descripción si la tienes
            vbox.Add(self.descripcion, flag=wx.EXPAND | wx.ALL, border=5)

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
                # Obtener el id del usuario seleccionado
                usuario_index = self.combo_usuario.GetSelection()
                usuario_id = usuarios[usuario_index][0] if usuario_index != wx.NOT_FOUND else None

                # Obtener el id del equipo seleccionado
                equipo_index = self.combo_equipo.GetSelection()
                equipo_id = equipos[equipo_index][0] if equipo_index != wx.NOT_FOUND else None

                # Obtener los demás campos
                estatus = self.combo_estatus.GetValue()
                estado_equip = self.combo_estado_equipo.GetValue()
                fecha_incidente = self.fecha_incidente.GetValue()
                descripcion = self.descripcion.GetValue()

                if usuario_id and equipo_id:
                    self.controller.editar_disciplinario(disciplina_id, usuario_id, equipo_id, estatus, estado_equip, fecha_incidente, descripcion)
                    self.cargar_disciplinario()
                else:
                    wx.MessageBox("Debe seleccionar un usuario y un equipo.", "Error", wx.OK | wx.ICON_ERROR)
            dialog.Destroy()

    def on_eliminar(self, event):
        """Elimina el registro de disciplinario seleccionado."""
        selected_row = self.grid.GetGridCursorRow()
        if selected_row >= 0:
            disciplina_id = int(self.grid.GetCellValue(selected_row, 0))
            confirm = wx.MessageBox("¿Estás seguro de que quieres eliminar este registro?", "Confirmar", wx.YES_NO | wx.ICON_WARNING)
            if confirm == wx.YES:
                self.controller.eliminar_disciplinario(disciplina_id)
                self.cargar_disciplinario()

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