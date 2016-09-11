from modelos.Model import Model


class Ruta(Model):
    def __init__(self, duracion = None, distancia = None):
        super().__init__("Rutas")
        self.distancia = distancia
        self.duracion = duracion
