import wx
from wx.grid import Grid
import bcrypt

class GestionarUsuariosView(wx.Frame):
    def __init__(self, parent, controller, menu_view, *args, **kw):
        super(GestionarUsuariosView, self).__init__(parent, *args, **kw)
        self.controller = controller  # Asignar el controlador correctamente
        self.menu_view = menu_view  # Guardar referencia al menú anterior
        self.SetTitle("Gestión de Investigadores")
        self.SetSize((600, 400))

        self.InitUI()
        self.Centre()

        # Manejar el evento de cierre de la ventana
        self.Bind(wx.EVT_CLOSE, self.on_close)

    def InitUI(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Grid para mostrar los usuarios
        self.grid = Grid(panel)
        self.grid.CreateGrid(0, 4)  # Crear una tabla vacía con 4 columnas
        self.grid.SetColLabelValue(0, "ID")
        self.grid.SetColLabelValue(1, "Nombre")
        self.grid.SetColLabelValue(2, "Usuario")
        self.grid.SetColLabelValue(3, "Rol")
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

        # Cargar datos iniciales
        self.cargar_usuarios()

    def cargar_usuarios(self):
        """Carga los usuarios en la grid."""
        usuarios = self.controller.obtener_usuarios()
        self.grid.ClearGrid()
        if self.grid.GetNumberRows() > 0:
            self.grid.DeleteRows(0, self.grid.GetNumberRows())

        for i, usuario in enumerate(usuarios):
            self.grid.AppendRows(1)
            self.grid.SetCellValue(i, 0, str(usuario[0]))  # ID
            self.grid.SetCellValue(i, 1, usuario[1])  # Nombre
            self.grid.SetCellValue(i, 2, usuario[2])  # Usuario
            self.grid.SetCellValue(i, 3, usuario[4])  # Rol

    def on_agregar(self, event):
        """Abre un diálogo para agregar un nuevo usuario."""
        dialog = wx.Dialog(self, title="Agregar Usuario", size=(300, 250))
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Campos del formulario
        nombre_label = wx.StaticText(dialog, label="Nombre:")
        self.nombre_text = wx.TextCtrl(dialog)
        vbox.Add(nombre_label)
        vbox.Add(self.nombre_text, flag=wx.EXPAND | wx.ALL, border=5)

        usuario_label = wx.StaticText(dialog, label="Alias (Usuario):")
        self.usuario_text = wx.TextCtrl(dialog)
        vbox.Add(usuario_label)
        vbox.Add(self.usuario_text, flag=wx.EXPAND | wx.ALL, border=5)

        contraseña_label = wx.StaticText(dialog, label="Contraseña:")
        self.contraseña_text = wx.TextCtrl(dialog, style=wx.TE_PASSWORD)
        vbox.Add(contraseña_label)
        vbox.Add(self.contraseña_text, flag=wx.EXPAND | wx.ALL, border=5)

        # Botones de acción
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        btn_aceptar = wx.Button(dialog, label="Aceptar", id=wx.ID_OK)
        btn_cancelar = wx.Button(dialog, label="Cancelar", id=wx.ID_CANCEL)
        hbox.Add(btn_aceptar)
        hbox.Add(btn_cancelar, flag=wx.LEFT, border=5)

        vbox.Add(hbox, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=10)

        # Asignar el sizer al diálogo
        dialog.SetSizer(vbox)

        # Mostrar el diálogo y manejar la respuesta
        resultado = dialog.ShowModal()
        if resultado == wx.ID_OK:
            self.on_guardar_agregar()
        dialog.Destroy()  # Cerrar el diálogo después de usarlo

    def on_guardar_agregar(self):
        """Guarda un nuevo usuario en la base de datos."""
        nombre = self.nombre_text.GetValue()
        usuario = self.usuario_text.GetValue()
        contraseña = self.contraseña_text.GetValue()

        if not nombre or not usuario or not contraseña:
            wx.MessageBox("Por favor, complete todos los campos.", "Error", wx.OK | wx.ICON_ERROR)
            return

        # Hashear la contraseña antes de guardarla
        hashed_password = bcrypt.hashpw(contraseña.encode('utf-8'), bcrypt.gensalt())

        # Guardar el usuario en la base de datos
        self.controller.agregar_usuario(nombre, usuario, hashed_password, "Investigador")
        self.cargar_usuarios()  # Recargar la lista de usuarios

    def on_editar(self, event):
        """Abre un diálogo para editar el usuario seleccionado."""
        selected_row = self.grid.GetGridCursorRow()
        if selected_row >= 0:
            usuario_id = self.grid.GetCellValue(selected_row, 0)
            nombre = self.grid.GetCellValue(selected_row, 1)
            usuario = self.grid.GetCellValue(selected_row, 2)

            dialog = wx.Dialog(self, title="Editar Usuario", size=(300, 250))
            vbox = wx.BoxSizer(wx.VERTICAL)

            # Campos del formulario
            nombre_label = wx.StaticText(dialog, label="Nombre:")
            self.nombre_text_edit = wx.TextCtrl(dialog, value=nombre)
            vbox.Add(nombre_label)
            vbox.Add(self.nombre_text_edit, flag=wx.EXPAND | wx.ALL, border=5)

            usuario_label = wx.StaticText(dialog, label="Alias (Usuario):")
            self.usuario_text_edit = wx.TextCtrl(dialog, value=usuario)
            vbox.Add(usuario_label)
            vbox.Add(self.usuario_text_edit, flag=wx.EXPAND | wx.ALL, border=5)

            contraseña_label = wx.StaticText(dialog, label="Nueva Contraseña (opcional):")
            self.contraseña_text_edit = wx.TextCtrl(dialog, style=wx.TE_PASSWORD)
            vbox.Add(contraseña_label)
            vbox.Add(self.contraseña_text_edit, flag=wx.EXPAND | wx.ALL, border=5)

            # Botones de acción
            hbox = wx.BoxSizer(wx.HORIZONTAL)
            btn_aceptar = wx.Button(dialog, label="Aceptar", id=wx.ID_OK)
            btn_cancelar = wx.Button(dialog, label="Cancelar", id=wx.ID_CANCEL)
            hbox.Add(btn_aceptar)
            hbox.Add(btn_cancelar, flag=wx.LEFT, border=5)

            vbox.Add(hbox, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=10)

            # Asignar el sizer al diálogo
            dialog.SetSizer(vbox)

            # Mostrar el diálogo y manejar la respuesta
            resultado = dialog.ShowModal()
            if resultado == wx.ID_OK:
                self.on_guardar_editar(usuario_id)
            dialog.Destroy()  # Cerrar el diálogo después de usarlo

    def on_guardar_editar(self, usuario_id):
        """Guarda los cambios de un usuario en la base de datos."""
        nombre = self.nombre_text_edit.GetValue()
        usuario = self.usuario_text_edit.GetValue()
        contraseña = self.contraseña_text_edit.GetValue()

        if not nombre or not usuario:
            wx.MessageBox("Por favor, complete los campos obligatorios.", "Error", wx.OK | wx.ICON_ERROR)
            return

        # Hashear la contraseña si se proporcionó una nueva
        hashed_password = None
        if contraseña:
            hashed_password = bcrypt.hashpw(contraseña.encode('utf-8'), bcrypt.gensalt())

        # Actualizar el usuario en la base de datos
        self.controller.editar_usuario(usuario_id, nombre, usuario, hashed_password)
        self.cargar_usuarios()  # Recargar la lista de usuarios

    def on_eliminar(self, event):
        """Elimina el usuario seleccionado."""
        selected_row = self.grid.GetGridCursorRow()
        if selected_row >= 0:
            usuario_id = self.grid.GetCellValue(selected_row, 0)
            confirm = wx.MessageBox("¿Estás seguro de que quieres eliminar este usuario?", "Confirmar", wx.YES_NO | wx.ICON_WARNING)
            if confirm == wx.YES:
                self.controller.eliminar_usuario(usuario_id)
                self.cargar_usuarios()  # Recargar la lista de usuarios

    def on_cancelar(self, event):
        """Regresa al menú anterior."""
        self.Hide()  # Cierra la ventana de registro
        self.controller.menu_view.reopen()

    def on_close(self, event):
        """Maneja el cierre de la ventana."""
        dialogo = wx.MessageDialog(self, "¿Estás seguro de que quieres regresar al menú anterior?", "Cerrar ventana", wx.YES_NO | wx.ICON_QUESTION)
        respuesta = dialogo.ShowModal()
        if respuesta == wx.ID_YES:
            self.Hide()  # Oculta la ventana actual
            if self.menu_view:  # Si hay una referencia al menú anterior
                self.menu_view.Show()  # Muestra la ventana del menú anterior
        else:
            event.Veto()  # Cancela el cierre de la ventana