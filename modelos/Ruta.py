from modelos import Model

class Ruta(Model):

    def __init__(self):
        self.id = None
        self.origen = ""
        self.destino = None
        self.distancia = None
        self.tiempo = None
        self.idRutaSiguiente = None
