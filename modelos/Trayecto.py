from modelos import Model


def CREAR_TRAYECTO(ciudades):
    """METODO TEMPORAL
                    no podia crear una instancia de la clase desde motor de Rutas.
                         eliminar
    """
    return Trayecto(ciudades)


class Trayecto():
    def __init__(self, ciudades):
        self.ciudades = ciudades
