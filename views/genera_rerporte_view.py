import wx
import wx.grid
import sqlite3

class VentanaReportes(wx.Frame):
    def __init__(self, parent,  controlador, usuario, rol, menu_view=None, db_path="investigacion.db",):
        super(VentanaReportes, self).__init__(parent, title="Menú de Reportes", size=(600, 400))
        self.db_path = db_path
        self.SetTitle("Generar Reporte")
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Cambiar el icono de la ventana
        icon = wx.Icon("img/iconoinstitucional.ico", wx.BITMAP_TYPE_ICO)  # Cambia la ruta al icono
        self.SetIcon(icon)

        # Título del menú
        titulo = wx.StaticText(panel, label="Seleccione el Reporte:")
        titulo.SetFont(wx.Font(18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        vbox.Add(titulo, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=20)

        # Botones para cada reporte
        botones = [
            ("Casos por Tipo", self.generar_reporte_casos_por_tipo),
            ("Casos por Investigador", self.generar_reporte_casos_por_investigador),
            ("Casos Abiertos por Investigador", self.generar_reporte_casos_abiertos_por_investigador),
            ("Avances por Caso", self.generar_reporte_avances_por_caso),
            ("Auditorías por Usuario", self.generar_reporte_auditorias_por_usuario),
            ("Alarmas por Caso", self.generar_reporte_alarmas_por_caso),  # Ejemplo adicional
            ("Casos por Estatus", self.generar_reporte_casos_por_estatus), # Ejemplo adicional
            ("Casos por Tipo Irregularidad", self.generar_reporte_casos_por_tipo_irregularidad) # Ejemplo adicional

        ]

        for texto_boton, funcion_reporte in botones:
            boton = wx.Button(panel, label=texto_boton)
            boton.Bind(wx.EVT_BUTTON, lambda event, func=funcion_reporte: self.mostrar_reporte(event, func))
            vbox.Add(boton, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        panel.SetSizer(vbox)

    def mostrar_reporte(self, event, funcion_reporte):
        """Genera y muestra el reporte en una nueva ventana."""
        resultados = funcion_reporte()
        if resultados:
            ventana_reporte = VentanaMostrarReporte(self, resultados, funcion_reporte.__name__)
            ventana_reporte.Show()
        else:
            wx.MessageBox("No se encontraron resultados para este reporte.", "Información", wx.OK | wx.ICON_INFORMATION)

    def generar_reporte_casos_por_tipo(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT tipo, COUNT(*) AS cantidad_casos
            FROM Casos
            GROUP BY tipo;
        """)
        resultados = cursor.fetchall()
        conn.close()
        return resultados

    def generar_reporte_casos_por_investigador(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT u.nombre, COUNT(c.id) AS cantidad_casos
            FROM Casos c
            LEFT JOIN Usuarios u ON c.investigador_id = u.id
            GROUP BY c.investigador_id;
        """)
        resultados = cursor.fetchall()
        conn.close()
        return resultados

    def generar_reporte_casos_abiertos_por_investigador(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT u.nombre, COUNT(c.id) AS cantidad_casos_abiertos
            FROM Casos c
            LEFT JOIN Usuarios u ON c.investigador_id = u.id
            WHERE c.estatus = 'Abierto'
            GROUP BY c.investigador_id;
        """)
        resultados = cursor.fetchall()
        conn.close()
        return resultados

    def generar_reporte_avances_por_caso(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.nro_expediente, a.descripcion, a.fecha
            FROM Avances a
            JOIN Casos c ON a.caso_id = c.id;
        """)
        resultados = cursor.fetchall()
        conn.close()
        return resultados

    def generar_reporte_auditorias_por_usuario(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT u.nombre, a.accion, a.fecha, c.nro_expediente
            FROM Auditorias a
            JOIN Usuarios u ON a.usuario_id = u.id
            JOIN Casos c ON a.caso_id = c.id;
        """)
        resultados = cursor.fetchall()
        conn.close()
        return resultados
    def generar_reporte_alarmas_por_caso(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.nro_expediente, a.motivo, a.fecha
            FROM Alarmas a
            JOIN Casos c ON a.caso_id = c.id;
        """)
        resultados = cursor.fetchall()
        conn.close()
        return resultados
    def generar_reporte_casos_por_estatus(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT estatus, COUNT(*) AS cantidad_casos
            FROM Casos
            GROUP BY estatus;
        """)
        resultados = cursor.fetchall()
        conn.close()
        return resultados

    def generar_reporte_casos_por_tipo_irregularidad(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT tipo_irregularidad, COUNT(*) AS cantidad_casos
            FROM Casos
            GROUP BY tipo_irregularidad;
        """)
        resultados = cursor.fetchall()
        conn.close()
        return resultados

class VentanaMostrarReporte(wx.Frame):
    def __init__(self, parent, resultados, nombre_reporte):
        super(VentanaMostrarReporte, self).__init__(parent, title=f"Reporte: {nombre_reporte}", size=(800, 600))
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        grid = wx.grid.Grid(panel)
        grid.CreateGrid(len(resultados), len(resultados[0]))

        # Establecer encabezados de columna
        for i, columna in enumerate(resultados[0]):
            grid.SetColLabelValue(i, str(columna))

        # Llenar la cuadrícula con los datos del reporte
        for fila, datos_fila in enumerate(resultados):
            for columna, valor in enumerate(datos_fila):
                grid.SetCellValue(fila, columna, str(valor))

        grid.AutoSizeColumns()
        vbox.Add(grid, flag=wx.EXPAND | wx.ALL, border=10)
        panel.SetSizer(vbox)