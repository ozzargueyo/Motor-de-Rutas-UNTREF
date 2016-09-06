from Tools.scripts.treesync import raw_input


class Menu():
    def __init__(self, motor):
        self.motor = motor

    def elejir_operacion(self):
        """PREGUNTA AL USUARIO QUE FUNCIONALIDAD REQUIERE"""
        operacion_elejida = ""
        operaciones_permitidas = ["Crear trayecto", "Agregar ciudad a trayecto existente", "Listar trayectos",
                                  "Obtener informacion de trayecto", "Comparar trayectos", "Salir"]
        while operacion_elejida not in operaciones_permitidas:
            print()
            for i in range(0, len(operaciones_permitidas)):
                print(str(i + 1) + len(str(i + 1)) * " " + operaciones_permitidas[i])
            numero = raw_input("Inserte número de la operacion que desea : \n")
            try:
                if int(numero) > 0:
                    operacion_elejida = operaciones_permitidas[int(numero) - 1]
            except:
                print("Debe ingresar un numero entre 1 y " + str(len(operaciones_permitidas)))
        self.abrir_menu(operacion_elejida)

    def abrir_menu(self, operacion_elejida):
        """ABRE EL MENU SELECCIONADO"""
        print(operacion_elejida)
        menus_disponibles = {"Crear trayecto": self.crear_trayecto,
                             "Agregar ciudad a trayecto existente": self.agregar_ciudad,
                             "Listar trayectos": self.motor.listar_trayectos,
                             "Obtener informacion de trayecto": self.info_trayecto,
                             "Comparar trayectos": self.comparar_trayectos,
                             "Salir": self.motor.salir_y_guardar_trayectos}
        menus_disponibles[operacion_elejida]()

    def crear_trayecto(self):
        """MENU PARA CREAR UN NUEVO TRAYECTO"""
        nombre = raw_input("Inserte nombre del nuevo trayecto \n")
        origen = self.obtener_nombre_de_ciudad("de origen")
        destino = self.obtener_nombre_de_ciudad("de destino")
        self.motor.crear_trayecto(nombre, origen, destino)

    def agregar_ciudad(self):
        """MENU PARA AGREGAR UNA CIUDAD A UN TRAYECTO EXISTENTE"""
        pass

    def info_trayecto(self):
        """MENU PARA OBTENER INFORMACION DE UN TARYECTO SELECCIONADO"""
        pass

    def comparar_trayectos(self):
        """MENU PARA COMPARAR DOS TRAYECTOS EXISTENTES"""
        pass

    def obtener_nombre_de_ciudad(self, objetivo):
        """METODO PROVISIONAL PARA VALIDAR EL NOMBRE DE LA CIUDAD"""
        ciudad_incorrecta = True
        nombre = ""
        while ciudad_incorrecta:
            ciudad = raw_input("Inserte nombre de la ciudad " + objetivo + " \n")
            nombre = self.motor.obtener_nombre_correcto(ciudad)
            seleccion = ""
            while ("si" not in seleccion and "no" not in seleccion):
                seleccion = raw_input(
                    'Escriba "si" si la ciudad que usted eligio es: ' + nombre + ' o esciba "no" para reescribir el nombre \n').casefold()
                print(seleccion)
                ciudad_incorrecta = "si" not in seleccion
        print(nombre)
        return nombre
