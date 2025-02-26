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
                estatus TEXT NOT NULL CHECK(estatus IN ('Abierto', 'Asignado', 'Cerrado', 'Re-abierto')),
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
                ("Juan Pérez", "jperez", bcrypt.hashpw("123".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Ana Gómez", "agomez", bcrypt.hashpw("investigador2".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
                ("Carlos Ruiz", "cruz", bcrypt.hashpw("123".encode('utf-8'), bcrypt.gensalt()), "Investigador"),
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
                ('Gestión', 'EXP-2024-001', '', '2024-01-15', 'Teléfono', 'Fraude', 'Corrupción', 'Empresa X', 'Alta', 15, 'Engaño financiero', 'Denuncia anónima', 'Análisis financiero', 'Investigación interna', 'Acciones legales', 'Se recomienda seguimiento', 'Ninguna', 'Adjunto PDF', 'Abierto', 0),
                ('Reclamo', 'EXP-2024-002', 'Ana Gómez', '2024-02-01', 'Computadora', 'Estafa', 'Phishing', 'Cliente', 'Media', 7, 'Suplantación de identidad', 'Reporte interno', 'Análisis de correos', 'Bloqueo de cuentas', 'Recomendación de seguridad', 'Caso resuelto', 'Se realizó informe', 'Adjunto DOC', 'Cerrado', 3),
                ('Caso', 'EXP-2024-003', 'Carlos Ruiz', '2024-03-10', 'Tarjeta de crédito', 'Fraude financiero', 'Cargos no autorizados', 'Cliente VIP', 'Alta', 10, 'Departamento de fraudes', 'Reporte bancario', 'Monitoreo de transacciones', 'Reversión de cargos', 'Educación al cliente', 'Seguimiento en curso', 'Pendiente de validación', 'Adjunto XLS', 'Asignado', 4),
                ('Caso','EXP-2784-933','','2023-09-15','precious gemstone','hurto','lesiones graves','Diego Torres','Media',3,'Poisoning by other synthetic narcotics, intentional self-harm, initial encounter','Denuncia anónima','Monitoreo de transacciones','Reversión de cargos','Recomendación de seguridad','Caso resuelto','Pendiente de validación','Adjunto DOC','Abierto',0),
                ('Caso','EXP-8755-706','','2023-08-17','luxury car','estafa','amenazas','Pedro Martinez','Alta',3,'Injury of lumbar and sacral spinal cord and nerves at abdomen, lower back and pelvis level','Denuncia anónima','Monitoreo de transacciones','Reversión de cargos','Educación al cliente','Se recomienda seguimiento','Pendiente de validación','Adjunto XLS','Abierto',0),
                ('Caso','EXP-3328-477','','2022-09-03','vintage watch','fraude','estafa','Fernando Reyes','Alta',0,'Nondisplaced comminuted fracture of shaft of unspecified tibia, subsequent encounter for open fracture type IIIA, IIIB, or IIIC with routine healing','Reporte bancario','Monitoreo de transacciones','Investigación interna','Recomendación de seguridad','Se recomienda seguimiento','Ninguna','Adjunto XLS','Abierto',0),
                ('Caso','EXP-6655-263','','2024-01-14','luxury car','lesiones','robo con violencia','Patricia Soto','Alta',9,'Accidental discharge of machine gun, sequela','Denuncia anónima','Análisis financiero','Investigación interna','Acciones legales','Seguimiento en curso','Pendiente de validación','Adjunto XLS','Abierto',0),
                ('Caso','EXP-5030-376','','2022-08-14','luxury car','violación','hurto agravado','Roberto Vargas','Baja',7,'Strain of flexor muscle, fascia and tendon of right index finger at forearm level, initial encounter','Denuncia anónima','Monitoreo de transacciones','Bloqueo de cuentas','Educación al cliente','Se recomienda seguimiento','Ninguna','Adjunto PDF','Abierto',0),
                ('Caso','EXP-5074-341','','2023-01-24','collectible figurine','daño a la propiedad','hurto agravado','Elena Jimenez','Alta',10,'Puncture wound with foreign body of left cheek and temporomandibular area, subsequent encounter','Denuncia anónima','Análisis de correos','Reversión de cargos','Recomendación de seguridad','Se recomienda seguimiento','Se realizó informe','Adjunto DOC','Abierto',0),
                ('Caso','EXP-4009-436','','2022-04-16','antique vase','lesiones','robo con violencia','Carmen Navarro','Baja',15,'Pruritus scroti','Denuncia anónima','Monitoreo de transacciones','Bloqueo de cuentas','Acciones legales','Caso resuelto','Se realizó informe','Adjunto PDF','Abierto',0),
                ('Caso','EXP-4176-618','','2023-08-26','valuable stamp collection','daño a la propiedad','estafa','Patricia Soto','Media',11,'Maternal care for disproportion due to deformity of maternal pelvic bones','Reporte bancario','Análisis de correos','Investigación interna','Acciones legales','Se recomienda seguimiento','Ninguna','Adjunto PDF','Abierto',0),
                ('Caso','EXP-8289-498','Torey Sheering','2022-02-25','designer handbag','estafa','robo con violencia','Diego Torres','Media',9,'Unspecified superficial injury of unspecified knee','Denuncia anónima','Monitoreo de transacciones','Reversión de cargos','Recomendación de seguridad','Seguimiento en curso','Se realizó informe','Adjunto PDF','Asignado',18),
                ('Caso','EXP-5370-052','Harp Le Huquet','2022-12-13','rare painting','amenazas','amenazas','Juan Perez','Baja',14,'Other specified injury of unspecified renal vein, initial encounter','Denuncia anónima','Análisis financiero','Investigación interna','Acciones legales','Se recomienda seguimiento','Ninguna','Adjunto DOC','Asignado',94),
                ('Caso','EXP-0403-659','Glennis Haggleton','2023-05-05','limited edition sneakers','violación','amenazas','Ana Lopez','Alta',15,'Alcoholic fatty liver','Denuncia anónima','Monitoreo de transacciones','Investigación interna','Acciones legales','Seguimiento en curso','Pendiente de validación','Adjunto DOC','Asignado',64),
                ('Caso','EXP-7458-378','Derek Gergolet','2022-06-21','valuable sports memorabilia','daño a la propiedad','hurto agravado','Fernando Reyes','Baja',3,'Poisoning by drugs affecting uric acid metabolism, accidental (unintentional), initial encounter','Denuncia anónima','Monitoreo de transacciones','Investigación interna','Educación al cliente','Se recomienda seguimiento','Pendiente de validación','Adjunto XLS','Cerrado',30),
                ('Caso','EXP-3206-700','','2022-07-09','collectible figurine','lesiones','robo con violencia','Jorge Ramirez','Media',7,'Juvenile myoclonic epilepsy, intractable','Reporte interno','Análisis financiero','Bloqueo de cuentas','Acciones legales','Seguimiento en curso','Se realizó informe','Adjunto DOC','Cerrado',0),
                ('Caso','EXP-1932-880','Glennis Haggleton','2023-10-11','collectible figurine','violación','hurto agravado','Miguel Castro','Baja',9,'Unspecified superficial injury of unspecified eyelid and periocular area, initial encounter','Reporte bancario','Análisis financiero','Bloqueo de cuentas','Acciones legales','Caso resuelto','Ninguna','Adjunto XLS','Cerrado',64),
                ('Caso','EXP-4890-129','Tremaine Curthoys','2022-12-16','collectible figurine','violencia de género','robo con violencia','Patricia Soto','Media',5,'Maternal care for unstable lie, fetus 4','Denuncia anónima','Análisis de correos','Reversión de cargos','Educación al cliente','Caso resuelto','Se realizó informe','Adjunto XLS','Re-abierto',61),
                ('Caso','EXP-4287-088','Lilah Brand-Hardy','2023-07-10','diamond ring','violación','hurto agravado','Luisa Rodriguez','Baja',9,'Supervision of high risk pregnancy due to social problems, first trimester','Denuncia anónima','Análisis de correos','Reversión de cargos','Recomendación de seguridad','Seguimiento en curso','Se realizó informe','Adjunto DOC','Re-abierto',80),
                ('Caso','EXP-8629-639','Leola McSparran','2023-10-04','antique vase','daño a la propiedad','hurto agravado','Monica Diaz','Alta',11,'Nondisplaced fracture of left ulna styloid process, subsequent encounter for closed fracture with nonunion','Reporte interno','Análisis de correos','Investigación interna','Educación al cliente','Caso resuelto','Ninguna','Adjunto DOC','Re-abierto',46),
                ('Caso','EXP-9641-516','Fons Vuitte','2023-07-20','platinum bracelet','daño a la propiedad','robo con violencia','Jorge Ramirez','Alta',15,'Dislocation of distal interphalangeal joint of unspecified finger, sequela','Denuncia anónima','Monitoreo de transacciones','Reversión de cargos','Recomendación de seguridad','Se recomienda seguimiento','Ninguna','Adjunto XLS','Re-abierto',23),
                ('Caso','EXP-0054-175','Aura Crasswell','2022-05-24','antique vase','fraude','estafa','Juan Perez','Media',14,'Acquired clawhand, left hand','Reporte bancario','Análisis de correos','Bloqueo de cuentas','Educación al cliente','Caso resuelto','Ninguna','Adjunto XLS','Re-abierto',17),
                ('Caso','EXP-0647-183','Vanni Langabeer','2022-02-05','luxury car','lesiones','lesiones graves','Monica Diaz','Alta',3,'Non-in- line roller-skate accident','Reporte interno','Monitoreo de transacciones','Reversión de cargos','Recomendación de seguridad','Caso resuelto','Pendiente de validación','Adjunto PDF','Re-abierto',25),
                ('Caso','EXP-2588-780','Miner Petherick','2023-06-04','collectible figurine','tráfico de drogas','estafa','Juan Perez','Baja',3,'Poisoning by other nonsteroidal anti-inflammatory drugs [NSAID], undetermined, subsequent encounter','Reporte bancario','Monitoreo de transacciones','Bloqueo de cuentas','Educación al cliente','Se recomienda seguimiento','Pendiente de validación','Adjunto XLS','Re-abierto',65),
                ('Gestión','EXP-0208-416','','2024-02-26','vintage watch','violencia de género','lesiones graves','Laura Fernandez','Baja',8,'Toxic effect of herbicides and fungicides, undetermined, sequela','Denuncia anónima','Análisis de correos','Investigación interna','Educación al cliente','Caso resuelto','Se realizó informe','Adjunto PDF','Abierto',0),
                ('Gestión','EXP-6392-893','Zed Bordes','2022-01-14','valuable antique pottery','hurto','hurto agravado','Isabel Morales','Baja',4,'Other displaced fracture of base of first metacarpal bone, left hand, subsequent encounter for fracture with nonunion','Reporte interno','Análisis financiero','Bloqueo de cuentas','Acciones legales','Se recomienda seguimiento','Ninguna','Adjunto PDF','Asignado',69),
                ('Gestión','EXP-5610-253','Abbye Hrihorovich','2023-01-16','rare painting','violación','amenazas','Juan Perez','Baja',7,'Strain of muscle and tendon of long flexor muscle of toe at ankle and foot level, left foot, initial encounter','Reporte bancario','Análisis de correos','Bloqueo de cuentas','Educación al cliente','Caso resuelto','Ninguna','Adjunto PDF','Asignado',99),
                ('Gestión','EXP-3934-076','Gaspar Carss','2023-08-18','precious gemstone','daño a la propiedad','lesiones graves','Isabel Morales','Alta',1,'Unspecified physeal fracture of upper end of right tibia, subsequent encounter for fracture with delayed healing','Denuncia anónima','Análisis de correos','Investigación interna','Acciones legales','Se recomienda seguimiento','Pendiente de validación','Adjunto DOC','Asignado',78),
                ('Gestión','EXP-5993-572','Derek Gergolet','2022-02-28','valuable antique furniture','violación','amenazas','Raul Ortega','Media',7,'Car driver injured in collision with heavy transport vehicle or bus in traffic accident, subsequent encounter','Reporte interno','Análisis de correos','Reversión de cargos','Educación al cliente','Se recomienda seguimiento','Se realizó informe','Adjunto XLS','Asignado',30),
                ('Gestión','EXP-7380-595','Aundrea Cancutt','2023-09-11','platinum bracelet','lesiones','amenazas','Roberto Vargas','Alta',0,'Lens-induced iridocyclitis, left eye','Reporte interno','Monitoreo de transacciones','Reversión de cargos','Educación al cliente','Seguimiento en curso','Pendiente de validación','Adjunto XLS','Asignado',73),
                ('Gestión','EXP-5458-106','Masha Reihill','2022-10-14','crystal chandelier','daño a la propiedad','estafa','Raul Ortega','Media',8,'Pervasive developmental disorder, unspecified','Reporte bancario','Análisis de correos','Investigación interna','Recomendación de seguridad','Caso resuelto','Se realizó informe','Adjunto DOC','Asignado',39),
                ('Gestión','EXP-3686-343','Allin Sinderland','2022-01-31','fine wine collection','robo a mano armada','lesiones graves','Elena Jimenez','Alta',0,'Unspecified injury of posterior tibial artery, left leg','Reporte bancario','Monitoreo de transacciones','Reversión de cargos','Acciones legales','Se recomienda seguimiento','Se realizó informe','Adjunto PDF','Cerrado',22),
                ('Gestión','EXP-3892-874','Gannie Bracknall','2022-08-20','valuable antique pottery','lesiones','estafa','Luisa Rodriguez','Alta',0,'Personal history of malignant neoplasm of breast','Denuncia anónima','Monitoreo de transacciones','Bloqueo de cuentas','Acciones legales','Caso resuelto','Se realizó informe','Adjunto XLS','Cerrado',36),
                ('Gestión','EXP-0233-772','Othilia Tremblett','2024-02-24','valuable antique furniture','fraude','robo con violencia','Ana Lopez','Media',4,'Nondisplaced other fracture of tuberosity of left calcaneus, subsequent encounter for fracture with routine healing','Reporte interno','Análisis de correos','Reversión de cargos','Acciones legales','Seguimiento en curso','Ninguna','Adjunto PDF','Cerrado',84),
                ('Gestión','EXP-4492-457','Kial Monument','2022-01-27','limited edition sneakers','violencia de género','estafa','Elena Jimenez','Baja',15,'Nondisplaced fracture (avulsion) of lateral epicondyle of right humerus, subsequent encounter for fracture with nonunion','Denuncia anónima','Monitoreo de transacciones','Bloqueo de cuentas','Recomendación de seguridad','Caso resuelto','Se realizó informe','Adjunto XLS','Re-abierto',54),
                ('Gestión','EXP-9604-720','Vanni Langabeer','2022-12-01','limited edition sneakers','amenazas','estafa','Carlos Sanchez','Alta',1,'Type III traumatic spondylolisthesis of sixth cervical vertebra, initial encounter for open fracture','Reporte interno','Monitoreo de transacciones','Reversión de cargos','Acciones legales','Caso resuelto','Pendiente de validación','Adjunto PDF','Re-abierto',25),
                ('Gestión','EXP-9667-394','Devora Killock','2023-09-07','valuable musical instrument','robo a mano armada','amenazas','Fernando Reyes','Media',14,'Drowning and submersion due to other accident to passenger ship','Denuncia anónima','Monitoreo de transacciones','Bloqueo de cuentas','Educación al cliente','Se recomienda seguimiento','Se realizó informe','Adjunto XLS','Re-abierto',75),
                ('Gestión','EXP-4067-331','Everard Halstead','2024-02-17','diamond ring','amenazas','robo con violencia','Carlos Sanchez','Baja',7,'Unspecified open wound of unspecified part of neck, subsequent encounter','Reporte interno','Análisis de correos','Bloqueo de cuentas','Acciones legales','Se recomienda seguimiento','Pendiente de validación','Adjunto PDF','Re-abierto',85),
                ('Reclamo','EXP-8166-698','','2022-03-12','vintage watch','robo a mano armada','amenazas','Ana Lopez','Baja',11,'Other infective bursitis, shoulder','Reporte bancario','Análisis de correos','Bloqueo de cuentas','Acciones legales','Seguimiento en curso','Pendiente de validación','Adjunto PDF','Abierto',0),
                ('Reclamo','EXP-5983-994','','2023-05-16','valuable antique pottery','amenazas','amenazas','Diego Torres','Baja',0,'Acute embolism and thrombosis of deep veins of unspecified upper extremity','Reporte bancario','Monitoreo de transacciones','Investigación interna','Educación al cliente','Seguimiento en curso','Pendiente de validación','Adjunto XLS','Abierto',0),
                ('Reclamo','EXP-6898-572','','2023-01-06','platinum bracelet','amenazas','robo con violencia','Juan Perez','Media',11,'Minor laceration of femoral artery','Denuncia anónima','Análisis financiero','Bloqueo de cuentas','Acciones legales','Se recomienda seguimiento','Se realizó informe','Adjunto XLS','Abierto',0),
                ('Reclamo','EXP-8487-299','','2022-07-26','collectible figurine','daño a la propiedad','robo con violencia','Miguel Castro','Alta',8,'Unspecified fracture of lower end of unspecified tibia, initial encounter for closed fracture','Reporte bancario','Análisis financiero','Reversión de cargos','Recomendación de seguridad','Seguimiento en curso','Pendiente de validación','Adjunto XLS','Abierto',0),
                ('Reclamo','EXP-1589-184','','2024-01-12','valuable musical instrument','fraude','estafa','Diego Torres','Alta',3,'Acquired absence of hand','Reporte interno','Análisis financiero','Investigación interna','Educación al cliente','Caso resuelto','Pendiente de validación','Adjunto PDF','Abierto',0),
                ('Reclamo','EXP-8502-049','Lilah Brand-Hardy','2023-05-05','platinum bracelet','violencia de género','hurto agravado','Raul Ortega','Baja',1,'Unspecified injury of unspecified muscle, fascia and tendon at shoulder and upper arm level, left arm, initial encounter','Reporte interno','Monitoreo de transacciones','Reversión de cargos','Educación al cliente','Se recomienda seguimiento','Pendiente de validación','Adjunto PDF','Cerrado',80),
                ('Reclamo','EXP-9474-550','Brynn Wapples','2024-01-08','valuable stamp collection','robo a mano armada','lesiones graves','Laura Fernandez','Baja',14,'Malignant neoplasm of ill-defined sites within the digestive system','Denuncia anónima','Análisis de correos','Reversión de cargos','Acciones legales','Caso resuelto','Ninguna','Adjunto PDF','Cerrado',90),
                ('Reclamo','EXP-7729-815','Sherry Wilfling','2023-12-30','valuable sports memorabilia','fraude','estafa','Elena Jimenez','Media',9,'Driver of heavy transport vehicle injured in collision with railway train or railway vehicle in nontraffic accident, initial encounter','Reporte interno','Análisis de correos','Investigación interna','Recomendación de seguridad','Se recomienda seguimiento','Ninguna','Adjunto PDF','Cerrado',7),
                ('Reclamo','EXP-1261-117','Nerti Groome','2022-07-20','vintage watch','lesiones','estafa','Ana Lopez','Alta',4,'Unspecified physeal fracture of lower end of left tibia, subsequent encounter for fracture with delayed healing','Reporte bancario','Análisis financiero','Reversión de cargos','Acciones legales','Se recomienda seguimiento','Ninguna','Adjunto DOC','Cerrado',63),
                ('Reclamo','EXP-2181-036','Jareb Verey','2023-06-09','crystal chandelier','estafa','amenazas','Laura Fernandez','Alta',13,'Unilateral post-traumatic osteoarthritis, unspecified knee','Reporte bancario','Análisis financiero','Bloqueo de cuentas','Educación al cliente','Se recomienda seguimiento','Pendiente de validación','Adjunto DOC','Cerrado',58),
                ('Reclamo','EXP-9623-554','Allin Sinderland','2022-06-22','valuable antique pottery','amenazas','estafa','Ana Lopez','Alta',1,'Displaced oblique fracture of shaft of right fibula, subsequent encounter for open fracture type IIIA, IIIB, or IIIC with delayed healing','Reporte interno','Análisis de correos','Reversión de cargos','Recomendación de seguridad','Se recomienda seguimiento','Se realizó informe','Adjunto DOC','Re-abierto',22),
                ('Reclamo','EXP-4455-533','Baxie Macoun','2023-11-14','luxury car','violencia de género','estafa','Fernando Reyes','Media',4,'Maternal care for hydrops fetalis, unspecified trimester, fetus 3','Reporte interno','Monitoreo de transacciones','Investigación interna','Recomendación de seguridad','Caso resuelto','Pendiente de validación','Adjunto DOC','Re-abierto',49),
                ('Reclamo','EXP-8645-620','Horst Enrietto','2022-09-25','valuable musical instrument','daño a la propiedad','lesiones graves','Fernando Reyes','Baja',6,'Laceration with foreign body of unspecified hand, initial encounter','Reporte bancario','Análisis de correos','Reversión de cargos','Acciones legales','Se recomienda seguimiento','Ninguna','Adjunto XLS','Re-abierto',86),
                ('Reclamo','EXP-1962-054','Ted Benoy','2022-10-03','rare painting','amenazas','estafa','Juan Perez','Alta',14,'Puncture wound with foreign body of unspecified external genital organs, male, sequela','Reporte bancario','Monitoreo de transacciones','Bloqueo de cuentas','Educación al cliente','Caso resuelto','Pendiente de validación','Adjunto XLS','Re-abierto',97),
                ('Reclamo','EXP-0069-144','Lilah Brand-Hardy','2023-09-19','luxury car','amenazas','hurto agravado','Carlos Sanchez','Baja',14,'Maternal care for breech presentation, fetus 4','Reporte interno','Monitoreo de transacciones','Bloqueo de cuentas','Educación al cliente','Seguimiento en curso','Se realizó informe','Adjunto DOC','Re-abierto',80)
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