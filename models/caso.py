import sqlite3
from patterns.observer import Subject

class CasoInvestigacionModel(Subject):
    def __init__(self, db_path="investigacion.db"):
        super().__init__() # Inicializamos Subject
        self.db_path = db_path



    def obtener_investigadores(self):
        """Obtiene la lista de investigadores de la base de datos."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT nombre FROM Usuarios WHERE rol = 'Investigador'")
        investigadores = [row[0] for row in cursor.fetchall()]
        conn.close()
        return investigadores

    def obtener_id_investigador(self, nombre):
        """Obtiene el ID de un investigador por su nombre."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM Usuarios WHERE nombre=?", (nombre,))
        resultado = cursor.fetchone()
        conn.close()
        return resultado[0] if resultado else None

    def guardar_caso(self, datos):
        """Guarda un caso de investigación en la base de datos."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO Casos (
                    tipo, nro_expediente, investigador, fecha_inicio, movil_afectado, 
                    tipo_irregularidad, subtipo_irregularidad, objetivo_agraviado, 
                    incidencia, duracion_dias, descripcion_modus_operandi, area_apoyo_resolver, 
                    deteccion_procedencia, diagnostico_detalle, actuaciones_acciones, 
                    conclusiones_recomendaciones, observaciones, soporte, estatus, investigador_id
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, datos)

            conn.commit()
            conn.close()
            return True, "Datos guardados correctamente."
        except sqlite3.Error as e:
            return False, f"Error al guardar los datos: {e}"


    def asignar_investigador(self, nro_expediente, nombre_investigador, investigador_id):
        """Asigna un investigador a un caso específico, notifica a los observadores."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Casos
            SET investigador_id = ?, estatus = 'Asignado', investigador = ?
            WHERE nro_expediente = ?
        """, (investigador_id, nombre_investigador, nro_expediente))
        conn.commit()
        conn.close()
        self.notify(f"Caso {nro_expediente} asignado a {nombre_investigador}") # Notificamos el cambio
        return True, "Investigador asignado correctamente."

    def modificar_caso(self, nro_expediente, datos_actualizados, nuevo_estatus):
        """Modifica los datos de un caso y notifica a los observadores."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Construir la consulta UPDATE dinámicamente
        set_clausulas = ", ".join([f"{campo} = ?" for campo in datos_actualizados.keys()])
        valores = list(datos_actualizados.values())
        valores.append(nuevo_estatus)
        valores.append(nro_expediente)

        cursor.execute(f"""
            UPDATE Casos
            SET {set_clausulas}, estatus = ?
            WHERE nro_expediente = ?
        """, valores)

        conn.commit()
        conn.close()
        self.notify(f"Caso {nro_expediente} modificado") # Notificamos el cambio
        return True, "Caso modificado correctamente."

    def obtener_casos_cerrados(self, investigador_id=None, rol=None):
        """
        Obtiene los casos de investigación según el rol del usuario.
        Si el rol es 'Administrador', obtiene todos los casos con estatus 'Cerrado'.
        Si el rol es 'Investigador', obtiene los casos con estatus 'Cerrado' asignados al investigador.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        if rol == 'Administrador':
            cursor.execute("SELECT nro_expediente, estatus FROM Casos WHERE estatus = 'Cerrado'")
        elif rol == 'Investigador' and investigador_id:
            cursor.execute("SELECT nro_expediente, estatus FROM Casos WHERE estatus = 'Cerrado' AND investigador_id = ?", (investigador_id,))
        else:
            conn.close()
            return []  # Si no hay rol o investigador_id, devuelve una lista vacía
        expedientes = [row[0] for row in cursor.fetchall()]
        conn.close()
        return expedientes

    def obtener_casos_abiertos(self, investigador_id=None):
        """Obtiene todos los casos de investigación de la base de datos."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        if investigador_id:
            cursor.execute("SELECT * FROM Casos WHERE estatus = 'Abierto' AND investigador_id")
        """Obtiene todos los casos de investigación de la base de datos."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT nro_expediente, estatus FROM Casos WHERE estatus = 'Abierto'")
        expedientes = [row[0] for row in cursor.fetchall()]
        conn.close()
        return expedientes

    import sqlite3

    def asignar_investigador(self, nro_expediente, nombre_investigador, investigador_id):
        """Asigna un investigador a un caso específico, cambia el estatus a 'Asignado' y guarda el nombre del investigador."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Casos
            SET investigador_id = ?, estatus = 'Asignado', investigador = ?
            WHERE nro_expediente = ?
        """, (investigador_id, nombre_investigador, nro_expediente))
        conn.commit()
        conn.close()
        return True, "Investigador asignado correctamente."


    def obtener_casos_asignados(self, investigador_id):
        """Obtiene los casos asignados a un investigador con estatus 'Asignado'."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT nro_expediente FROM Casos WHERE investigador_id = ? AND estatus = 'Asignado'", (investigador_id,))
        expedientes = [row[0] for row in cursor.fetchall()]
        conn.close()
        return expedientes


    def obtener_datos_expediente(self, expediente):
        """Devuelve los datos del expediente especificado."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Casos WHERE nro_expediente = ?", (expediente,))
        resultado=cursor.fetchall()
        conn.close()
        if resultado:
            # Asumiendo que el resultado es una fila con los datos del caso
            return {
                "Tipo de Caso": resultado[0][1],
                "Fecha de inicio": resultado[0][4],
                "Móvil afectado": resultado[0][5],
                "Tipo de irregularidad": resultado[0][6],
                "Subtipo irregularidad": resultado[0][7],
                "Objetivo / Agraviado": resultado[0][8],
                "Incidencia": resultado[0][9],
                "Duración (Días)": resultado[0][10],
                "Descripción Modus Operandi": resultado[0][11],
                "Área Apoyo a Resolver": resultado[0][12],
                "Detección / Procedencia del Caso": resultado[0][13],
                "Diagnostico / Detalle de Comprobación para Determinar Fraude": resultado[0][14],
                "Actuaciones/Acciones Realizadas": resultado[0][15],
                "Conclusiones / Recomendaciones": resultado[0][16],
                "Observaciones": resultado[0][17],
                "Soporte": resultado[0][18],
            }
        return None