from patterns.factory import ModelFactory

class AbstractFactory:
    def __init__(self, factory):
        self.factory = factory

    def create_model(self, model_type, *args, **kwargs):
        return self.factory.create_model(model_type, *args, **kwargs)