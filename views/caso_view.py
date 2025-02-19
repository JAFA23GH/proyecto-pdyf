import wx
import sqlite3
from datetime import date, datetime

class VentanaRegistro(wx.Frame):
    def __init__(self, parent, usuario, rol, *args, **kw):
        super(VentanaRegistro, self).__init__(parent, *args, **kw)
        self.SetTitle("Registro de Caso")
        self.SetSize((600, 800))
        self.usuario = usuario
        self.rol = rol

        self.text_ctrls = {}  # Diccionario para almacenar los textboxes


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
            "Nro. Expediente", "Móvil afectado", "Tipo de irregularidad", "Subtipo irregularidad",
            "Objetivo / Agraviado", "Incidencia", "Duración (Días)", "Descripción Modus Operandi",
            "Área Apoyo a Resolver", "Detección / Procedencia del Caso",
            "Diagnostico / Detalle de Comprobación para Determinar Fraude",
            "Actuaciones/Acciones Realizadas", "Conclusiones / Recomendaciones", "Observaciones", "Soporte"
        ]

        for campo in campos:
            label = wx.StaticText(panel, label=campo + ":")
            vbox.Add(label, flag=wx.ALIGN_LEFT | wx.TOP, border=5)
            textbox = wx.TextCtrl(panel)
            vbox.Add(textbox, flag=wx.EXPAND | wx.TOP, border=5)
            self.text_ctrls[campo] = textbox  # Guardar el campo

        label_fecha_inicio = wx.StaticText(panel, label="Fecha de inicio:")  # Etiqueta
        vbox.Add(label_fecha_inicio, flag=wx.ALIGN_LEFT | wx.TOP, border=5)  # Añade etiqueta al sizer
        self.text_ctrls["Fecha de inicio"] = wx.TextCtrl(panel)  # Crea el control y lo agrega al diccionario
        vbox.Add(self.text_ctrls["Fecha de inicio"], flag=wx.EXPAND | wx.TOP, border=5)  # Añade control al sizer

        # Obtener y formatear la fecha actual (opcional)
        fecha_actual = date.today()
        fecha_actual_str = fecha_actual.strftime('%d/%m/%Y')  # Formato DD/MM/AAAA

        # Establecer la fecha actual en el campo de texto (DESPUÉS de agregar la clave)
        self.text_ctrls["Fecha de inicio"].SetValue(fecha_actual_str)  # Ahora funciona

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

    def on_cancelar(self, event):
        self.Close()  # Cierra la ventana

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

        try:
            conn = sqlite3.connect("investigacion.db")
            cursor = conn.cursor()

            # Obtener los valores de los campos
            tipo_caso = self.tipo_caso_radiobox.GetStringSelection()
            nro_expediente = self.text_ctrls["Nro. Expediente"].GetValue()
            fecha_inicio_str = self.text_ctrls["Fecha de inicio"].GetValue()
            movil_afectado = self.text_ctrls["Móvil afectado"].GetValue()
            tipo_irregularidad = self.text_ctrls["Tipo de irregularidad"].GetValue()
            subtipo_irregularidad = self.text_ctrls["Subtipo irregularidad"].GetValue()
            objetivo_agraviado = self.text_ctrls["Objetivo / Agraviado"].GetValue()
            incidencia = self.text_ctrls["Incidencia"].GetValue()
            duracion_dias = self.text_ctrls["Duración (Días)"].GetValue()
            descripcion_modus_operandi = self.text_ctrls["Descripción Modus Operandi"].GetValue()
            area_apoyo_resolver = self.text_ctrls["Área Apoyo a Resolver"].GetValue()
            deteccion_procedencia = self.text_ctrls["Detección / Procedencia del Caso"].GetValue()
            diagnostico_detalle = self.text_ctrls["Diagnostico / Detalle de Comprobación para Determinar Fraude"].GetValue()
            actuaciones_acciones = self.text_ctrls["Actuaciones/Acciones Realizadas"].GetValue()
            conclusiones_recomendaciones = self.text_ctrls["Conclusiones / Recomendaciones"].GetValue()
            observaciones = self.text_ctrls["Observaciones"].GetValue()
            soporte = self.text_ctrls["Soporte"].GetValue()

            # Obtener el investigador y su ID
            if self.rol == "Administrador":
                investigador_nombre = self.investigador_combo.GetValue()
            else:
                investigador_nombre = self.investigador_text.GetValue()

            cursor.execute("SELECT id FROM Usuarios WHERE nombre=?", (investigador_nombre,))
            resultado = cursor.fetchone()  # Guarda el resultado en una variable

            if resultado:  # Verifica si se encontró un resultado
                investigador_id = resultado[0]
            else:
                wx.MessageBox(f"No se encontró un investigador con el nombre '{investigador_nombre}'.", "Error", wx.OK | wx.ICON_ERROR)
                conn.close() # Cerrar la conexión en caso de error
                return  # Salir de la función on_aceptar

            # Lógica para asignar el estatus
            if self.rol == "Investigador":
                estatus = "Abierto"
            else:  # Rol es Administrador
                estatus = "Asignado"

            # Convertir la fecha a formato ISO 8601 (YYYY-MM-DD)
            fecha_inicio_str = self.text_ctrls["Fecha de inicio"].GetValue()
            try:
                fecha_inicio = date.fromisoformat(fecha_inicio_str)
            except ValueError:
                try:
                    fecha_inicio = datetime.strptime(fecha_inicio_str, '%d/%m/%Y').date()  # Usa datetime.strptime y .date()
                    fecha_inicio = fecha_inicio.strftime('%Y-%m-%d') # Convierte a string YYYY-MM-DD
                except ValueError:
                    wx.MessageBox("Formato de fecha incorrecto. Debe ser YYYY-MM-DD o DD/MM/AAAA.", "Error", wx.OK | wx.ICON_ERROR)
                    return  # Salir de la función si la fecha es inválida

            # Insertar los datos en la base de datos (sin cambios)
            cursor.execute("""
                INSERT INTO Casos (
                    tipo, nro_expediente, investigador, fecha_inicio, movil_afectado, 
                    tipo_irregularidad, subtipo_irregularidad, objetivo_agraviado, 
                    incidencia, duracion_dias, descripcion_modus_operandi, area_apoyo_resolver, 
                    deteccion_procedencia, diagnostico_detalle, actuaciones_acciones, 
                    conclusiones_recomendaciones, observaciones, soporte, estatus, investigador_id
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                tipo_caso, nro_expediente, investigador_nombre, fecha_inicio, movil_afectado,
                tipo_irregularidad, subtipo_irregularidad, objetivo_agraviado, incidencia,
                duracion_dias, descripcion_modus_operandi, area_apoyo_resolver,
                deteccion_procedencia, diagnostico_detalle, actuaciones_acciones,
                conclusiones_recomendaciones, observaciones, soporte, estatus, investigador_id
            ))

            conn.commit()
            conn.close()

            wx.MessageBox("Datos guardados correctamente.", "Éxito", wx.OK | wx.ICON_INFORMATION)
            self.Close()

        except sqlite3.Error as e:
            wx.MessageBox(f"Error al guardar los datos: {e}", "Error", wx.OK | wx.ICON_ERROR)
            conn.close()  # Cerrar la conexión en caso de error