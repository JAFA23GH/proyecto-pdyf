class Decorator:
    def __init__(self, component):
        self._component = component

    def modificar_caso(self, nro_expediente, datos_actualizados, nuevo_estatus):
        return self._component.modificar_caso(nro_expediente, datos_actualizados, nuevo_estatus)


class CasoDecorator(Decorator):
    def __init__(self, component):
        super().__init__(component)

    def modificar_caso(self, nro_expediente, datos_actualizados, nuevo_estatus):
        # Llamar a la operación original
        resultado = self._component.modificar_caso(nro_expediente, datos_actualizados, nuevo_estatus)

        # Operación adicional: Log de la modificación
        if resultado:
            self.log_modificacion(nro_expediente, datos_actualizados, nuevo_estatus)

        return resultado

    def log_modificacion(self, nro_expediente, datos_actualizados, nuevo_estatus):
        print(f"Modificación registrada para expediente {nro_expediente}:")
        print(f"Datos actualizados: {datos_actualizados}")
        print(f"Nuevo estatus: {nuevo_estatus}")