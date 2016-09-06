from modelos import Model

def CREAR_RUTA(duracion, distancia):
    """METODO TEMPORAL
                    no podia crear una instancia de la clase desde motor de Rutas.
                         eliminar
    """
    return Ruta(duracion, distancia)

class Ruta():
    def __init__(self, duracion, distancia):
        self.distancia = distancia
        self.duracion = duracion
