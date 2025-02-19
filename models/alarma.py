from database.db import Database

class Alarma:
    def __init__(self, id, caso_id, motivo, fecha):
        self.id = id
        self.caso_id = caso_id
        self.motivo = motivo
        self.fecha = fecha

    def save(self):
        db = Database()
        db.execute("INSERT INTO Alarmas (caso_id, motivo, fecha) VALUES (?, ?, ?)",
                   (self.caso_id, self.motivo, self.fecha))