class Decorator:
    def __init__(self, component):
        self._component = component

    def operation(self):
        return self._component.operation()