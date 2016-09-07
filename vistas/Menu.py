from Tools.scripts.treesync import raw_input


class Menu():
    def __init__(self, motor):
        self.motor = motor
        self.operaciones = ["Crear trayecto", "Agregar ciudad a trayecto existente", "Listar trayectos",
                            "Obtener informacion de trayecto", "Comparar trayectos", "Salir"]
        self.menus_disponibles = [self.crear_trayecto, self.agregar_ciudad, self.motor.listar_trayectos,
                                  self.info_trayecto, self.comparar_trayectos, self.motor.salir_y_guardar_trayectos]

    def elejir_operacion(self):
        """PREGUNTA AL USUARIO QUE FUNCIONALIDAD REQUIERE"""
        self.menus_disponibles[self.seleccion_por_numero(self.operaciones, "operacion")]()

    def crear_trayecto(self):
        """MENU PARA CREAR UN NUEVO TRAYECTO"""
        nombre = raw_input("Inserte nombre del nuevo trayecto \n")
        origen = self.obtener_nombre_de_ciudad("de origen")
        destino = self.obtener_nombre_de_ciudad("de destino")
        self.motor.crear_trayecto(nombre, origen, destino)

    def agregar_ciudad(self):
        """MENU PARA AÑADIR CIUDAD"""
        trayecto = self.seleccionar_trayecto()
        self.motor.ver_trayecto(trayecto)
        posicion = -1
        ciudad = self.obtener_nombre_de_ciudad("a añadir")
        # while posicion == -1:
        #    respuesta = raw_input("Elija la posicion de la nueva cuidad \n")
        #
        pass

    def info_trayecto(self):
        """MENU PARA OBTENER INFORMACION DE UN TARYECTO SELECCIONADO"""
        self.motor.ver_trayecto(self.seleccionar_trayecto())

    def comparar_trayectos(self):
        """MENU PARA COMPARAR DOS TRAYECTOS EXISTENTES"""
        pass

    def obtener_nombre_de_ciudad(self, texto):
        """METODO PROVISIONAL PARA VALIDAR EL NOMBRE DE LA CIUDAD"""
        ciudad_incorrecta = True
        nombre = ""
        while ciudad_incorrecta:
            ciudad = raw_input("Inserte nombre de la ciudad " + texto + " \n")
            # nombre = self.motor.obtener_nombre_correcto(ciudad)
            nombre = ciudad
            seleccion = ""
            while ("si" not in seleccion and "no" not in seleccion):
                seleccion = raw_input(
                    'Escriba "si" si la ciudad que usted eligio es: ' + nombre + ' o esciba "no" para reescribir el nombre \n').casefold()
                print(seleccion)
                ciudad_incorrecta = "si" not in seleccion
        print(nombre)
        return nombre

    def seleccionar_trayecto(self):
        trayectos = []
        for t in self.motor.trayectos.keys():
            trayectos.append(t)
        return trayectos[self.seleccion_por_numero(trayectos, "trayecto")]

    def seleccion_por_numero(self, lista, texto):
        posicion = -1
        while posicion == -1:
            for i in range(0, len(lista)):
                print(str(i + 1) + len(str(i + 1)) * " " + lista[i])
            try:
                numero = int(raw_input("Inserte número del " + texto + " que desea \n"))
                if numero >= 1 and len(lista) >= numero:
                    posicion = numero - 1
                else:
                    print("Debe ingresar un numero entre 1 y " + str(len(lista)))
            except:
                print("Debe ingresar un numero entre 1 y " + str(len(lista)))
        return posicion