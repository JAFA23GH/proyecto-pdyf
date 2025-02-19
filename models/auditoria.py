from database.db import Database

class Auditoria:
    def __init__(self, id, caso_id, accion, fecha, usuario_id):
        self.id = id
        self.caso_id = caso_id
        self.accion = accion
        self.fecha = fecha
        self.usuario_id = usuario_id

    def save(self):
        db = Database()
        db.execute("INSERT INTO Auditorias (caso_id, accion, fecha, usuario_id) VALUES (?, ?, ?, ?)",
                   (self.caso_id, self.accion, self.fecha, self.usuario_id))