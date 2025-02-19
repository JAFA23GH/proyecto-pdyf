from models.caso import Caso
from models.avance import Avance
from models.alarma import Alarma

class ModelFactory:
    @staticmethod
    def create_model(model_type, *args, **kwargs):
        if model_type == 'Caso':
            return Caso(*args, **kwargs)
        elif model_type == 'Avance':
            return Avance(*args, **kwargs)
        elif model_type == 'Alarma':
            return Alarma(*args, **kwargs)
        else:
            raise ValueError(f"Model type {model_type} not recognized")