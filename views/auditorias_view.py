import wx
import wx.adv
import sqlite3
import datetime

class VentanaConsultarAuditorias(wx.Frame):
    def __init__(self, parent, usuario, rol, *args, **kw):
        super(VentanaConsultarAuditorias, self).__init__(parent, title="Consultar Auditorías", size=(800, 600), *args, **kw)
        
        self.usuario = usuario
        self.rol = rol

        self.InitUI()
        self.Centre()
        self.Show()

    def InitUI(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Sección de Filtros
        hbox_filters = wx.BoxSizer(wx.HORIZONTAL)
        
        lbl_user = wx.StaticText(panel, label="Usuario:")
        hbox_filters.Add(lbl_user, flag=wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, border=5)
        self.txt_user = wx.TextCtrl(panel, size=(100, -1))
        hbox_filters.Add(self.txt_user, flag=wx.RIGHT, border=15)

        lbl_action = wx.StaticText(panel, label="Acción:")
        hbox_filters.Add(lbl_action, flag=wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, border=5)
        self.txt_action = wx.TextCtrl(panel, size=(150, -1))
        hbox_filters.Add(self.txt_action, flag=wx.RIGHT, border=15)

        lbl_date_from = wx.StaticText(panel, label="Fecha desde:")
        hbox_filters.Add(lbl_date_from, flag=wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, border=5)
        self.date_from = wx.adv.DatePickerCtrl(panel)
        hbox_filters.Add(self.date_from, flag=wx.RIGHT, border=15)

        lbl_date_to = wx.StaticText(panel, label="Fecha hasta:")
        hbox_filters.Add(lbl_date_to, flag=wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, border=5)
        self.date_to = wx.adv.DatePickerCtrl(panel)
        hbox_filters.Add(self.date_to, flag=wx.RIGHT, border=15)

        vbox.Add(hbox_filters, flag=wx.EXPAND | wx.ALL, border=10)

        # Sección de Botones
        hbox_buttons = wx.BoxSizer(wx.HORIZONTAL)

        btn_filter = wx.Button(panel, label="Filtrar")
        btn_filter.Bind(wx.EVT_BUTTON, self.OnFilter)
        hbox_buttons.Add(btn_filter, flag=wx.RIGHT, border=10)

        btn_export = wx.Button(panel, label="Exportar CSV")
        btn_export.Bind(wx.EVT_BUTTON, self.OnExport)
        hbox_buttons.Add(btn_export, flag=wx.RIGHT, border=10)

        btn_back = wx.Button(panel, label="Regresar")
        btn_back.Bind(wx.EVT_BUTTON, self.OnBack)
        hbox_buttons.Add(btn_back, flag=wx.RIGHT, border=10)

        vbox.Add(hbox_buttons, flag=wx.ALIGN_CENTER | wx.ALL, border=10)

        # Lista de Auditorías
        self.audit_list = wx.ListCtrl(panel, style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        self.audit_list.InsertColumn(0, 'ID', width=50)
        self.audit_list.InsertColumn(1, 'Fecha', width=150)
        self.audit_list.InsertColumn(2, 'Usuario', width=100)
        self.audit_list.InsertColumn(3, 'Acción', width=200)
        self.audit_list.InsertColumn(4, 'Caso', width=270)
        
        vbox.Add(self.audit_list, proportion=1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=10)

        panel.SetSizer(vbox)
        self.LoadAuditLogs()

    def GetDatabaseConnection(self):
        conn = sqlite3.connect('investigacion.db')  # Asegúrate de que este es el mismo archivo
        return conn

    def LoadAuditLogs(self, filters=None):
        conn = self.GetDatabaseConnection()
        cursor = conn.cursor()

        query = '''
            SELECT 
                Auditorias.id,
                Auditorias.fecha,
                Usuarios.nombre AS usuario,
                Auditorias.accion,
                Casos.nro_expediente AS caso
            FROM 
                Auditorias
            JOIN 
                Usuarios ON Auditorias.usuario_id = Usuarios.id
            JOIN
                Casos ON Auditorias.caso_id = Casos.id
        '''
        params = []
        if filters:
            query += " WHERE " + " AND ".join(filters['conditions'])
            params = filters['params']
        query += " ORDER BY Auditorias.fecha DESC"

        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()

        self.audit_list.DeleteAllItems()
        for idx, (aud_id, fecha, usuario, accion, caso) in enumerate(rows):
            self.audit_list.InsertItem(idx, str(aud_id))
            self.audit_list.SetItem(idx, 1, fecha)
            self.audit_list.SetItem(idx, 2, usuario)
            self.audit_list.SetItem(idx, 3, accion)
            self.audit_list.SetItem(idx, 4, caso)

    def OnFilter(self, event):
        conditions = []
        params = []

        user_filter = self.txt_user.GetValue().strip()
        if user_filter:
            conditions.append("Usuarios.nombre LIKE ?")
            params.append(f"%{user_filter}%")

        action_filter = self.txt_action.GetValue().strip()
        if action_filter:
            conditions.append("Auditorias.accion LIKE ?")
            params.append(f"%{action_filter}%")

        date_from = self.date_from.GetValue()
        date_to = self.date_to.GetValue()

        # Convertir wx.DateTime a datetime.datetime
        if date_from.IsValid():
            py_date_from = datetime.datetime(date_from.Year, date_from.Month + 1, date_from.Day)
            conditions.append("Auditorias.fecha >= ?")
            params.append(py_date_from.strftime("%Y-%m-%d"))

        if date_to.IsValid():
            py_date_to = datetime.datetime(date_to.Year, date_to.Month + 1, date_to.Day)
            conditions.append("Auditorias.fecha <= ?")
            params.append(py_date_to.strftime("%Y-%m-%d"))

        filters = {'conditions': conditions, 'params': params}
        self.last_filters = filters  # Guardamos los filtros para usarlos en exportación
        self.LoadAuditLogs(filters)

    def OnExport(self, event):
        import csv
        with wx.FileDialog(self, "Guardar archivo CSV", wildcard="CSV files (*.csv)|*.csv",
                           style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # El usuario canceló

            pathname = fileDialog.GetPath()
            try:
                with open(pathname, 'w', newline='', encoding='utf-8') as csvfile:
                    csvwriter = csv.writer(csvfile)
                    # Escribir encabezados
                    csvwriter.writerow(['ID', 'Fecha', 'Usuario', 'Acción', 'Caso'])
                    # Obtener datos actuales
                    conn = self.GetDatabaseConnection()
                    cursor = conn.cursor()

                    query = '''
                        SELECT 
                            Auditorias.id,
                            Auditorias.fecha,
                            Usuarios.nombre AS usuario,
                            Auditorias.accion,
                            Casos.nro_expediente AS caso
                        FROM 
                            Auditorias
                        JOIN 
                            Usuarios ON Auditorias.usuario_id = Usuarios.id
                        JOIN
                            Casos ON Auditorias.caso_id = Casos.id
                    '''
                    params = []
                    if hasattr(self, 'last_filters'):
                        filters = self.last_filters
                        query += " WHERE " + " AND ".join(filters['conditions'])
                        params = filters['params']
                    query += " ORDER BY Auditorias.fecha DESC"

                    cursor.execute(query, params)
                    rows = cursor.fetchall()
                    conn.close()

                    for row in rows:
                        csvwriter.writerow(row)
                wx.MessageBox('Datos exportados correctamente.', 'Información', wx.OK | wx.ICON_INFORMATION)
            except IOError:
                wx.MessageBox('Error al guardar el archivo.', 'Error', wx.OK | wx.ICON_ERROR)

    def OnBack(self, event):
        # Acción para el botón "Regresar"
        self.Close()
