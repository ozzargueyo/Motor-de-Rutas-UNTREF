from controladores import motorDeRutas
from terminaltables import DoubleTable
import os


class Menu(object):
    def __init__(self):
        # El menu se inicializa con el flag en terminar como False
        self.terminar = False
        self.motor = motorDeRutas.MotorDeRutas()
        self.operaciones = self.definirOperaciones()
        self.menus_disponibles = self.operacionesDisponibles()

    def definirOperaciones(self):

        return {
            1: "Crear trayecto",
            2: "Agregar ciudad a trayecto existente",
            3: "Listar trayectos",
            4: "Obtener informacion de trayecto",
            5: "Comparar trayectos",
            6: "Salir",
        }

    def operacionesDisponibles(self):
        return {
            1: self.crear_trayecto,
            2: self.agregar_ciudad,
            3: self.listar_trayectos,
            4: self.info_trayecto,
            5: self.comparar_trayectos,
            6: self.motor.salir_y_guardar_trayectos
        }

    def elegir_operacion(self):
        """PREGUNTA AL USUARIO QUE FUNCIONALIDAD REQUIERE"""
        try:
            op = int(self.seleccionMenu(self.operaciones, "operación"))
            print("--------------------------------------------------")
            print("\nOperacion seleccionada:", self.operaciones[op], "\n")
            self.menus_disponibles[op]()

            self.continuarOperacion(op)
        except IndentationError:
            print("Ocurrio un error")

    def crear_trayecto(self):
        """MENU PARA CREAR UN NUEVO TRAYECTO"""
        nombre_trayecto = ""
        while (nombre_trayecto in self.motor.trayectos.keys() or nombre_trayecto == ""):
            nombre_trayecto = input("Inserte nombre del nuevo trayecto: ").strip()
            if (nombre_trayecto in self.motor.trayectos.keys()):
                print("Ya existe un trayecto con ese nombre")
            elif (nombre_trayecto == ""):
                print("El nombre del trayecto no puede ser vacio")
        origen = self.obtener_nombre_de_ciudad("de origen")
        destino = self.obtener_nombre_de_ciudad("de destino")
        self.motor.crear_trayecto(nombre_trayecto, origen, destino)
        self.clear()

    def agregar_ciudad(self):
        """MENU PARA AÑADIR CIUDAD"""
        trayecto = self.motor.trayectos[self.seleccionar_trayecto()]
        posicion = -1
        table_data = [["Opcion", "Ciudad origen- Ciudad destino"]]
        table_data.append([1, "Primer Lugar"])
        for i in range(0, len(trayecto) - 1):
            table_data.append([i + 2, self.motor.unir_origen_destino(trayecto[i], trayecto[i + 1])])
        table_data.append([len(trayecto) + 1, "Ultimo Lugar"])
        table = DoubleTable(table_data, "Seleccion de posicion")
        table.justify_columns = {0: 'center', 1: 'left'}
        print(table.table, "\n")
        while posicion == -1:
            try:
                numero = int(input("Seleccione la posicion a insertar la nueva ciudad."))
                if numero >= 1 and len(trayecto) + 1 >= numero:
                    posicion = numero - 1
                else:
                    print("Debe ingresar un numero entre 1 y " + str(len(trayecto)))
            except:
                print("Debe ingresar un numero entre 1 y " + str(len(trayecto)))
        self.motor.agregar_ciudad_intermedia(trayecto, self.obtener_nombre_de_ciudad("a añadir"), posicion)

    def info_trayecto(self):
        """MENU PARA OBTENER INFORMACION DE UN TARYECTO SELECCIONADO"""
        op = self.seleccionar_trayecto()
        data_trayecto = self.motor.ver_trayecto(op)
        table_data = [["Nombre", "Ciudades del Trayecto", "Distancia en Kms", "Tiempo estimado de viaje"]]
        table_data.append(data_trayecto)
        table = DoubleTable(table_data, "Ver Informacion de Trayecto seleccionado ")
        table.justify_columns = {0: 'center'}
        print(table.table)

    def listar_trayectos(self):

        table_data = [["Nro", "Nombre del Trayecto"]]
        index = 1
        for valor in sorted(self.motor.trayectos.keys()):
            row = [index, valor]
            table_data.append(row)
            index += 1

        table = DoubleTable(table_data, "Trayectos almacenados ")
        table.justify_columns = {0: 'center', 1: 'left'}
        print(table.table)

    def comparar_trayectos(self):
        """MENU PARA COMPARAR DOS TRAYECTOS EXISTENTES"""
        pass

    def seleccionarCiudadesValidas(self, term, tipo_ciudad):

        ciudades_posibles = self.motor.obtener_ciudades_posibles(term)

        posicion = -1
        table_data = [["Opcion", "Ciudades"]]
        for id, ciudad in sorted(ciudades_posibles.items()):
            table_data.append([id, ciudad])

        table = DoubleTable(table_data, "Seleccion de ciudades disponibles")
        table.justify_columns = {0: 'center', 1: 'left'}
        print(table.table, "\n")
        while posicion == -1:
            try:
                print('Confirme la opción de la ciudad ingresada. Oprima 0 (Cero) para ingresarla nuevamente.')
                numero = int(input("Número de opción correcta: "))
                if numero == 0:
                    return self.obtener_nombre_de_ciudad(tipo_ciudad)
                elif numero >= 1 and len(ciudades_posibles) >= numero:
                    posicion = numero
                else:
                    print("Debe ingresar un numero entre 1 y " + str(len(ciudades_posibles)))
            except:
                print("Debe ingresar un numero entre 1 y " + str(len(ciudades_posibles)))

        return ciudades_posibles[posicion]

    def obtener_nombre_de_ciudad(self, tipo_ciudad):
        ciudad = input("Ingrese nombre de la ciudad " + tipo_ciudad + ": ")

        ciudadSeleccionada = self.seleccionarCiudadesValidas(ciudad, tipo_ciudad)

        return ciudadSeleccionada

    def seleccionar_trayecto(self):

        trayectos = []
        for t in self.motor.trayectos.keys():
            trayectos.append(t)

        op = self.seleccionDeTrayectos(trayectos, "  Seleccionar Trayectos  ")
        return trayectos[op]

    def seleccionMenu(self, opciones, texto):
        posicion = -1
        while posicion == -1:
            print("------------------------------------------------")
            print("Motor de Rutas", " - ", "Operaciones Disponibles")
            for clave, valor in sorted(opciones.items()):
                print("\t [" + str(clave) + "] - ", valor)
            print("------------------------------------------------")
            try:
                numero = int(input("\nInserte número de la " + texto + " que desea: "))
                if numero >= 1 and len(opciones) >= numero:
                    posicion = numero
                else:
                    self.clear()
                    print("Debe ingresar un numero entre 1 y " + str(len(opciones)))
            except:
                print("Debe ingresar un numero entre 1 y " + str(len(opciones)))
        return posicion

    def seleccionDeTrayectos(self, lista, title):
        posicion = -1
        table_data = [["Nro", "Nombre del Trayecto"]]
        index = 1
        for valor in lista:
            row = [index, valor]
            table_data.append(row)
            index += 1

        table = DoubleTable(table_data, title)
        table.justify_columns = {0: 'center', 1: 'left'}
        print(table.table, "\n")
        while posicion == -1:
            try:
                numero = int(input("Ingese la opción que desea:"))
                if numero >= 1 and len(lista) >= numero:
                    posicion = numero - 1
                else:
                    print("Debe ingresar un numero entre 1 y " + str(len(lista)))
            except:
                print("Debe ingresar un numero entre 1 y " + str(len(lista)))
        return posicion

    def mensajeDeSalida(self):
        print("Gracias por usar el Motor de Rutas UNTREF")
        exit()

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def continuarOperacion(self, op):
        if op != 6:
            print("¿Desea continuar operando con el Motor de Rutas?"
                  "\n Oprima [Enter] para continuar o [N] para salir:")
            continuarConMotor = str(input())
            if continuarConMotor.upper() == "N":
                self.menus_disponibles[6]()
            else:
                self.clear()


menu = Menu()
