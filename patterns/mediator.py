class Mediator:
    def __init__(self):
        self._components = []

    def add_component(self, component):
        print(f"Registrando componente: {component.__class__.__name__}")
        self._components.append(component)

    def notify(self, sender, event):
        print(f"Notificando evento: {event} desde {sender.__class__.__name__}")
        for component in self._components:
            if component != sender:
                component.receive(event)