import sqlite3
import bcrypt
from patterns.singleton import SingletonMeta

class Database(metaclass=SingletonMeta):
    def __init__(self):
        self.connection = sqlite3.connect('investigacion.db')
        self.cursor = self.connection.cursor()
        self.create_tables()  # Crear tablas al iniciar

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
                nro_expediente TEXT NOT NULL,
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
                ("Sofía López", "slopez", bcrypt.hashpw("investigador4".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Ulrica Worrell", "uworrell0", bcrypt.hashpw("6PUhX".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Sherry Wilfling", "swilfling1", bcrypt.hashpw("ca9Ou".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Sherm Starbuck", "sstarbuck2", bcrypt.hashpw("MeBOA".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Jimmy Blonden", "jblonden3", bcrypt.hashpw("ox6uj".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Henry Tindley", "htindley4", bcrypt.hashpw("HhFIx".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Moritz Romanet", "mromanet5", bcrypt.hashpw("I9oVA".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Valentine Fountain", "vfountain6", bcrypt.hashpw("8FVF0".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Hannis Jedrzej", "hjedrzej7", bcrypt.hashpw("61LrL".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Ellswerth Shillitoe", "eshillitoe8", bcrypt.hashpw("xtDhf".encode('utf-8'), bcrypt.gensalt()), "Administrador"),
                ("Arleyne Furphy", "afurphy9", bcrypt.hashpw("Ngdm9".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Norry Lethlay", "nlethlaya", bcrypt.hashpw("dMsnS".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Aura Crasswell", "acrasswellb", bcrypt.hashpw("U5D5V".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Torey Sheering", "tsheeringc", bcrypt.hashpw("aeCeG".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Belinda Tingly", "btinglyd", bcrypt.hashpw("Khhf0".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Aile Pedracci", "apedraccie", bcrypt.hashpw("UMFVo".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Betsey Crepin", "bcrepinf", bcrypt.hashpw("JrIuA".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Allin Sinderland", "asinderlandg", bcrypt.hashpw("7MnHM".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Fons Vuitte", "fvuitteh", bcrypt.hashpw("poBLT".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Rosella Plumstead", "rplumsteadi", bcrypt.hashpw("hyJoo".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Vanni Langabeer", "vlangabeerj", bcrypt.hashpw("obN2k".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Jewell Zellick", "jzellickk", bcrypt.hashpw("QEFMV".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Tadeo Greenless", "tgreenlessl", bcrypt.hashpw("QHFgM".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Imelda Maffeo", "imaffeom", bcrypt.hashpw("PkRHF".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Averil Postlewhite", "apostlewhiten", bcrypt.hashpw("ShnwX".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Derek Gergolet", "dgergoleto", bcrypt.hashpw("ZRcv9".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("August Dovidaitis", "adovidaitisp", bcrypt.hashpw("TzPJ4".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Allina Reinert", "areinertq", bcrypt.hashpw("FyfXU".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Benoite Polini", "bpolinir", bcrypt.hashpw("QDQHi".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Darrick Moloney", "dmoloneys", bcrypt.hashpw("JQkn6".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Freda Delos", "fdelost", bcrypt.hashpw("98Ec9".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Gannie Bracknall", "gbracknallu", bcrypt.hashpw("VWj8w".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Perrine Novelli", "pnovelliv", bcrypt.hashpw("UkXtR".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Lorna Lightwing", "llightwingw", bcrypt.hashpw("9kAAB".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Masha Reihill", "mreihillx", bcrypt.hashpw("pcE5E".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Bord Noulton", "bnoultony", bcrypt.hashpw("ZrcpT".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Beverlee Kesper", "bkesperz", bcrypt.hashpw("fruvE".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Harbert Bowhey", "hbowhey10", bcrypt.hashpw("3EpY5".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Anthiathia Selley", "aselley11", bcrypt.hashpw("fngPX".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Orelee Saldler", "osaldler12", bcrypt.hashpw("4V32Y".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Rachele McCandless", "rmccandless13", bcrypt.hashpw("hNY3B".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Leola McSparran", "lmcsparran14", bcrypt.hashpw("doyS7".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Garrot Swindley", "gswindley15", bcrypt.hashpw("muoe6".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Kelwin Caldecutt", "kcaldecutt16", bcrypt.hashpw("GU1S6".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Baxie Macoun", "bmacoun17", bcrypt.hashpw("KXMtf".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Renee Bindin", "rbindin18", bcrypt.hashpw("WeCuv".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Pansy Bacop", "pbacop19", bcrypt.hashpw("TmDUz".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Field Kelwick", "fkelwick1a", bcrypt.hashpw("W4zMg".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Marena Lante", "mlante1b", bcrypt.hashpw("x0aAF".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Kial Monument", "kmonument1c", bcrypt.hashpw("T8o17".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Nil Skiplorne", "nskiplorne1d", bcrypt.hashpw("TAlou".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Katalin Hellikes", "khellikes1e", bcrypt.hashpw("d6PsO".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Darrick Boardman", "dboardman1f", bcrypt.hashpw("cKvMg".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Jareb Verey", "jverey1g", bcrypt.hashpw("9Pya1".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Ethel Mulchrone", "emulchrone1h", bcrypt.hashpw("wXD15".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Kirby Mulqueen", "kmulqueen1i", bcrypt.hashpw("DccPY".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Tremaine Curthoys", "tcurthoys1j", bcrypt.hashpw("MXxXn".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Alonso Ghioni", "aghioni1k", bcrypt.hashpw("cvFoq".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Nerti Groome", "ngroome1l", bcrypt.hashpw("JyTNl".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Glennis Haggleton", "ghaggleton1m", bcrypt.hashpw("g3SaI".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Miner Petherick", "mpetherick1n", bcrypt.hashpw("P7LCt".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Hi Youthed", "hyouthed1o", bcrypt.hashpw("nHTII".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Donielle O'Geneay", "dogeneay1p", bcrypt.hashpw("CqQ2E".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Abie Stiffkins", "astiffkins1q", bcrypt.hashpw("Y752S".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Zed Bordes", "zbordes1r", bcrypt.hashpw("8Cc3p".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Stephan Hulbert", "shulbert1s", bcrypt.hashpw("ATkSp".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Roda Gribble", "rgribble1t", bcrypt.hashpw("9Jri3".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Cheslie Caddell", "ccaddell1u", bcrypt.hashpw("PXeZd".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Aundrea Cancutt", "acancutt1v", bcrypt.hashpw("HQwmy".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Raddie Belsham", "rbelsham1w", bcrypt.hashpw("uF1lU".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Devora Killock", "dkillock1x", bcrypt.hashpw("84U2N".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Nani Le Blanc", "nle1y", bcrypt.hashpw("nnXZp".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Andrej Kenen", "akenen1z", bcrypt.hashpw("3d6MM".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Gaspar Carss", "gcarss20", bcrypt.hashpw("HObZ9".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Kelsey McCarlie", "kmccarlie21", bcrypt.hashpw("iuPkM".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Lilah Brand-Hardy", "lbrandhardy22", bcrypt.hashpw("FA5d4".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Conrad Kayne", "ckayne23", bcrypt.hashpw("M5OW5".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Nike Mumford", "nmumford24", bcrypt.hashpw("8ynYl".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Nicolette Elldred", "nelldred25", bcrypt.hashpw("Tk5S4".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Othilia Tremblett", "otremblett26", bcrypt.hashpw("jtV1t".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Everard Halstead", "ehalstead27", bcrypt.hashpw("Tp07v".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Horst Enrietto", "henrietto28", bcrypt.hashpw("JV66K".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Robb McNamee", "rmcnamee29", bcrypt.hashpw("9YkNR".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Shirline Himsworth", "shimsworth2a", bcrypt.hashpw("Dq2P1".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Laurel Cossey", "lcossey2b", bcrypt.hashpw("DoF9X".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Brynn Wapples", "bwapples2c", bcrypt.hashpw("9IC09".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Hernando Kondratovich", "hkondratovich2d", bcrypt.hashpw("R7vDi".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Nappy Jennery", "njennery2e", bcrypt.hashpw("DtZyI".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Babbette Gullis", "bgullis2f", bcrypt.hashpw("Onl9f".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Harp Le Huquet", "hle2g", bcrypt.hashpw("SHbXz".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Tisha Leitch", "tleitch2h", bcrypt.hashpw("tRpI9".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Jelene Borg", "jborg2i", bcrypt.hashpw("lVD1N".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Ted Benoy", "tbenoy2j", bcrypt.hashpw("lJei2".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Bertine Tropman", "btropman2k", bcrypt.hashpw("CAWan".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Abbye Hrihorovich", "ahrihorovich2l", bcrypt.hashpw("Yx88X".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Bella Caldera", "bcaldera2m", bcrypt.hashpw("Vd6Uc".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Becki Severns", "bseverns2n", bcrypt.hashpw("PjtmQ".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Tedi Pracy", "tpracy2o", bcrypt.hashpw("7iFCA".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Biddy Bover", "bbover2p", bcrypt.hashpw("srewu".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Alwin Zienkiewicz", "azienkiewicz2q", bcrypt.hashpw("C92iR".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Thane Huikerby", "thuikerby2r", bcrypt.hashpw("jqUmx".encode('utf-8'), bcrypt.gensalt()), "Investigador")
            ]
            for u in usuarios:
                self.execute("INSERT INTO Usuarios (nombre, usuario, contraseña, rol) VALUES (?, ?, ?, ?)", u)
        # Insertar Casos si no hay registros
        if not self.fetch_all("SELECT id FROM Casos LIMIT 1"):
            casos = [
                ('Gestión', 'EXP-2024-001', '', '2024-01-15', 'Teléfono', 'Fraude', 'Corrupción', 'Empresa X', 'Alta', 15, 'Engaño financiero', 'Denuncia anónima', 'Análisis financiero', 'Investigación interna', 'Acciones legales', 'Se recomienda seguimiento', 'Ninguna', 'Adjunto PDF', 'Abierto', 2),
                ('Reclamo', 'EXP-2024-002', 'Ana Gómez', '2024-02-01', 'Computadora', 'Estafa', 'Phishing', 'Cliente', 'Media', 7, 'Suplantación de identidad', 'Reporte interno', 'Análisis de correos', 'Bloqueo de cuentas', 'Recomendación de seguridad', 'Caso resuelto', 'Se realizó informe', 'Adjunto DOC', 'Cerrado', 3),
                ('Caso', 'EXP-2024-003', 'Carlos Ruiz', '2024-03-10', 'Tarjeta de crédito', 'Fraude financiero', 'Cargos no autorizados', 'Cliente VIP', 'Alta', 10, 'Departamento de fraudes', 'Reporte bancario', 'Monitoreo de transacciones', 'Reversión de cargos', 'Educación al cliente', 'Seguimiento en curso', 'Pendiente de validación', 'Adjunto XLS', 'Asignado', 4),

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