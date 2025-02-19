class Mediator:
    def __init__(self):
        self._components = []

    def add_component(self, component):
        self._components.append(component)

    def notify(self, sender, event):
        for component in self._components:
            if component != sender:
                component.receive(event)