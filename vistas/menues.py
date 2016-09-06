#from cursesmenu import *
#from cursesmenu.items import *
from controladores.motorDeRutas import *
class Menues(object):
    def __init__(self, motor):
        self.motor = motor

    def mainMenu(self):
        # Create the menu
        '''

        menu = SelectionMenu("Motor de Rutas", "- Operaciones Disponibles -", False)

        # Create some items

        # MenuItem is the base class for all items, it doesn't do anything when selected

        # A MenuItem runs a Python function when selected
        crear_trayecto = MenuItem("Crear nuevo trayecto", self.motor.crearTrayecto() , )
        agregar_ciudad_a_trayecto = MenuItem("Agregar ciudad a trayecto", self.motor.agregarCiudadATrayecto())
        concatenar_trayectos = MenuItem("Concatenar dos trayectos", self.motor.concatenarTrayectos())
        comparar_trayectos = MenuItem("Comparar trayectos", self.motor.compararTrayectos())
        ver_trayectos = MenuItem("Ver trayecto", self.motor.verTrayecto())
        listar_trayectos = MenuItem("Listar trayectos", self.motor.listarTrayectos())
        salir = ExitItem("Salir del motor de rutas",)

        menu.append_item(crear_trayecto)
        menu.append_item(agregar_ciudad_a_trayecto)
        menu.append_item(concatenar_trayectos)
        menu.append_item(comparar_trayectos)
        menu.append_item(ver_trayectos)
        menu.append_item(listar_trayectos)
        menu.append_item(salir)



        # Finally, we call show to show the menu and allow the user to interact
        menu.start()
        menu.join()
        :return:
        '''
        selection = 0
        a_list=["red", "blue", "salida"]

        while (selection != 2):


            menu = SelectionMenu(a_list,"Select an option" , "subtitulo" , False)
            menu.show()
            selection = menu.selected_option

        print(selection)
