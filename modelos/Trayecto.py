from modelos import Model

class Trayecto(Model):

    def __init__(self):
        super(Trayecto, self).__init__("trayectos")
        self.nombre = ""
        self.rutaInicial = None
        self.distanciaTotal = None
        self.tiempoTotal = None

    def __tojson__(self):
