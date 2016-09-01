from controladores.controladorBase import ControladorBase
from vistas.menues import *


class MotorDeRutas(ControladorBase):

    def __init__(self):
        super().__init__()
        self.menus = Menues(self)

    def run(self):
        self.menus.mainMenu()

    def crearTrayecto(self):
        print("Aca estamos con la creacion de trayectos")

    def agregarCiudadATrayecto(self):
        pass

    def concatenarTrayectos(self):
        pass

    def compararTrayectos(self):
        pass

    def verTrayecto(self):
        pass

    def listarTrayectos(self):
        pass

    def salirYGuardarTrayectos(self):
        pass
