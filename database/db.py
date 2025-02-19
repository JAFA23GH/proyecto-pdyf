import sqlite3
import bcrypt

class Database:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.connection = sqlite3.connect('investigacion.db')
            cls._instance.cursor = cls._instance.connection.cursor()
            cls._instance.create_tables()  # Crear tablas al iniciar
        return cls._instance

    def execute(self, query, params=()):
        """Ejecuta una consulta SQL y hace commit."""
        self.cursor.execute(query, params)
        self.connection.commit()

    def fetch_all(self, query, params=()):
        """Ejecuta una consulta y devuelve todos los resultados."""
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def close(self):
        """Cierra la conexión a la base de datos."""
        self.connection.close()

    def create_tables(self):
        """Crea las tablas si no existen."""
        tables = [
            """CREATE TABLE IF NOT EXISTS Usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                usuario TEXT NOT NULL UNIQUE,
                contraseña TEXT NOT NULL,
                rol TEXT NOT NULL CHECK(rol IN ('Investigador', 'Administrador'))
            );""",
            """CREATE TABLE IF NOT EXISTS Casos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo TEXT NOT NULL CHECK(tipo IN ('Gestión', 'Reclamo', 'Caso')),
                nro_expediente TEXT,
                investigador TEXT,
                fecha_inicio DATE NOT NULL,
                movil_afectado TEXT,
                tipo_irregularidad TEXT,
                subtipo_irregularidad TEXT,
                objetivo_agraviado TEXT,
                incidencia TEXT,
                duracion_dias INTEGER,
                descripcion_modus_operandi TEXT,
                area_apoyo_resolver TEXT,
                deteccion_procedencia TEXT,
                diagnostico_detalle TEXT,
                actuaciones_acciones TEXT,
                conclusiones_recomendaciones TEXT,
                observaciones TEXT,
                soporte TEXT,
                estatus TEXT NOT NULL CHECK(estatus IN ('Abierto', 'Asignado', 'Cerrado', 'Reabierto')),
                investigador_id INTEGER,
                FOREIGN KEY (investigador_id) REFERENCES Usuarios(id)
            );""",
            """CREATE TABLE IF NOT EXISTS Avances (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                caso_id INTEGER NOT NULL,
                descripcion TEXT NOT NULL,
                fecha DATE NOT NULL,
                FOREIGN KEY (caso_id) REFERENCES Casos(id)
            );""",
            """CREATE TABLE IF NOT EXISTS Alarmas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                caso_id INTEGER NOT NULL,
                motivo TEXT NOT NULL,
                fecha DATE NOT NULL,
                FOREIGN KEY (caso_id) REFERENCES Casos(id)
            );""",
            """CREATE TABLE IF NOT EXISTS Auditorias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                caso_id INTEGER NOT NULL,
                accion TEXT NOT NULL,
                fecha DATE NOT NULL,
                usuario_id INTEGER NOT NULL,
                FOREIGN KEY (caso_id) REFERENCES Casos(id),
                FOREIGN KEY (usuario_id) REFERENCES Usuarios(id)
            );"""
        ]
        for table in tables:
            self.execute(table)

        self.insert_default_data()  # Insertar datos ficticios si la BD está vacía

    def insert_default_data(self):
        """Inserta datos ficticios si la base de datos está vacía."""
        # Verificar si hay usuarios registrados
        if not self.fetch_all("SELECT id FROM Usuarios LIMIT 1"):
            usuarios = [
                ("Admin", "admin", bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt()), "Administrador"),
                ("Juan Pérez", "jperez", bcrypt.hashpw("investigador1".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Ana Gómez", "agomez", bcrypt.hashpw("investigador2".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Carlos Ruiz", "cruiz", bcrypt.hashpw("investigador3".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Sofía López", "slopez", bcrypt.hashpw("investigador4".encode('utf-8'), bcrypt.gensalt()), "Investigador")
            ]
            for u in usuarios:
                self.execute("INSERT INTO Usuarios (nombre, usuario, contraseña, rol) VALUES (?, ?, ?, ?)", u)

        # Insertar Casos si no hay registros
        if not self.fetch_all("SELECT id FROM Casos LIMIT 1"):
            casos = [
                ('Gestión', 'EXP-2024-001', 'Juan Pérez', '2024-01-15', 'Teléfono', 'Fraude', 'Corrupción', 'Empresa X', 'Alta', 15, 'Engaño financiero', 'Legal', 'Denuncia anónima', 'Análisis financiero', 'Investigación interna', 'Acciones legales', 'Se recomienda seguimiento', 'Ninguna', 'Adjunto PDF', 'Abierto', 2),

                ('Reclamo', 'EXP-2024-002', 'Ana Gómez', '2024-02-01', 'Computadora', 'Estafa', 'Phishing', 'Cliente', 'Media', 7, 'Suplantación de identidad', 'TI', 'Reporte interno', 'Análisis de correos', 'Bloqueo de cuentas', 'Recomendación de seguridad', 'Caso resuelto', 'Se realizó informe', 'Adjunto DOC', 'Cerrado', 3),

                ('Caso', 'EXP-2024-003', 'Carlos Ruiz', '2024-03-10', 'Tarjeta de crédito', 'Fraude financiero', 'Cargos no autorizados', 'Cliente VIP', 'Alta', 10, 'Uso de credenciales robadas', 'Departamento de fraudes', 'Reporte bancario', 'Monitoreo de transacciones', 'Reversión de cargos', 'Educación al cliente', 'Seguimiento en curso', 'Pendiente de validación', 'Adjunto XLS', 'Asignado', 4)
            ]
            for c in casos:
                self.execute("INSERT INTO Casos (tipo, nro_expediente, investigador, fecha_inicio, movil_afectado, tipo_irregularidad, subtipo_irregularidad, objetivo_agraviado, incidencia, duracion_dias, descripcion_modus_operandi, area_apoyo_resolver, deteccion_procedencia, diagnostico_detalle, actuaciones_acciones, conclusiones_recomendaciones, observaciones, soporte, estatus, investigador_id) "
                             "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", c)

        # Insertar Avances
        if not self.fetch_all("SELECT id FROM Avances LIMIT 1"):
            avances = [
                (1, "Entrevista con testigos realizada", "2024-01-16"),
                (2, "Revisión de documentos completada", "2024-01-20"),
                (3, "Persona encontrada en buen estado", "2024-02-02"),
                (4, "Denuncias anónimas recibidas", "2024-02-07"),
                (5, "Presentación de pruebas en fiscalía", "2024-02-12")
            ]
            for a in avances:
                self.execute("INSERT INTO Avances (caso_id, descripcion, fecha) VALUES (?, ?, ?)", a)

        # Insertar Alarmas
        if not self.fetch_all("SELECT id FROM Alarmas LIMIT 1"):
            alarmas = [
                (1, "Pruebas clave encontradas", "2024-01-17"),
                (2, "Posible interferencia en el caso", "2024-01-21"),
                (3, "Caso cerrado, requiere validación", "2024-02-03"),
                (4, "Denuncias crecientes, alta prioridad", "2024-02-08"),
                (5, "Pruebas no concluyentes, revisar", "2024-02-13")
            ]
            for al in alarmas:
                self.execute("INSERT INTO Alarmas (caso_id, motivo, fecha) VALUES (?, ?, ?)", al)

        # Insertar Auditorías
        if not self.fetch_all("SELECT id FROM Auditorias LIMIT 1"):
            auditorias = [
                (1, "Modificación en la descripción del caso", "2024-01-16", 2),
                (2, "Cambio de estatus a 'Asignado'", "2024-01-20", 3),
                (3, "Cierre del caso por resolución", "2024-02-02", 4),
                (4, "Reapertura del caso", "2024-02-07", 5),
                (5, "Registro de nueva prueba", "2024-02-12", 2)
            ]
            for aud in auditorias:
                self.execute("INSERT INTO Auditorias (caso_id, accion, fecha, usuario_id) VALUES (?, ?, ?, ?)", aud)
