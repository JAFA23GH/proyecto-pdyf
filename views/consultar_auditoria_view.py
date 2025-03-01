import wx
from wx.grid import Grid

class ConsultarAuditoriaView(wx.Frame):
    def __init__(self, parent, controller, menu_view, *args, **kw):
        super(ConsultarAuditoriaView, self).__init__(parent, *args, **kw)
        self.controller = controller  # Asignar el controlador correctamente
        self.menu_view = menu_view  # Guardar referencia al menú anterior
        self.SetTitle("Consultar Auditorías")
        self.SetSize((800, 400))

        self.InitUI()
        self.Centre()

        # Manejar el evento de cierre de la ventana
        self.Bind(wx.EVT_CLOSE, self.on_close)

    def InitUI(self):
        # Crear un panel principal con scroll
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Crear una ventana desplazable
        scrolled_window = wx.ScrolledWindow(panel)
        scrolled_window.SetScrollRate(10, 10)  # Establecer la tasa de desplazamiento
        scrolled_vbox = wx.BoxSizer(wx.VERTICAL)

        # Grid para mostrar las auditorías
        self.grid = Grid(scrolled_window)
        self.grid.CreateGrid(0, 5)  # Crear una tabla vacía con 5 columnas
        self.grid.SetColLabelValue(0, "ID")
        self.grid.SetColLabelValue(1, "Caso ID")
        self.grid.SetColLabelValue(2, "Acción")
        self.grid.SetColLabelValue(3, "Fecha")
        self.grid.SetColLabelValue(4, "Usuario ID")
        scrolled_vbox.Add(self.grid, 1, wx.EXPAND | wx.ALL, 10)

        # Botón para regresar al menú anterior
        btn_cancelar = wx.Button(scrolled_window, label="Regresar")
        scrolled_vbox.Add(btn_cancelar, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=10)

        # Evento del botón
        btn_cancelar.Bind(wx.EVT_BUTTON, self.on_cancelar)

        # Asignar el sizer a la ventana desplazable
        scrolled_window.SetSizer(scrolled_vbox)

        # Añadir la ventana desplazable al panel principal
        vbox.Add(scrolled_window, 1, wx.EXPAND)
        panel.SetSizer(vbox)

        # Cargar datos iniciales
        self.cargar_auditorias()

    def cargar_auditorias(self):
        """Carga las auditorías en la grid."""
        auditorias = self.controller.obtener_auditorias()
        self.grid.ClearGrid()
        if self.grid.GetNumberRows() > 0:
            self.grid.DeleteRows(0, self.grid.GetNumberRows())

        for i, auditoria in enumerate(auditorias):
            self.grid.AppendRows(1)
            self.grid.SetCellValue(i, 0, str(auditoria[0]))  # ID
            self.grid.SetCellValue(i, 1, str(auditoria[1]))  # Caso ID
            self.grid.SetCellValue(i, 2, auditoria[2])  # Acción
            self.grid.SetCellValue(i, 3, str(auditoria[3]))  # Fecha
            self.grid.SetCellValue(i, 4, str(auditoria[4]))  # Usuario ID

    def on_cancelar(self, event):
        """Regresa al menú anterior."""
        self.Hide()  # Cierra la ventana de consulta
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