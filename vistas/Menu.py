from controladores import motorDeRutas
from terminaltables import DoubleTable
import os


class Menu(object):
    def __init__(self):
        # El menu se inicializa con el flag en terminar como False
        self.terminar = False
        self.motor = motorDeRutas.MotorDeRutas()
        self.operaciones = self.definir_operaciones()
        self.menus_disponibles = self.operaciones_disponibles()

    def definir_operaciones(self):

        return {
            1: "Crear trayecto",
            2: "Agregar ciudad a trayecto existente",
            3: "Concatenar trayectos",
            4: "Listar trayectos",
            5: "Obtener informacion de trayecto",
            6: "Obtener rutas de trayecto",
            7: "Comparar trayectos",
            8: "Salir",
        }

    def operaciones_disponibles(self):
        return {
            1: self.crear_trayecto,
            2: self.agregar_ciudad,
            3: self.concatenar_trayectos,
            4: self.listar_trayectos,
            5: self.info_trayecto,
            6: self.rutas_trayecto,
            7: self.comparar_trayectos,
            8: self.motor.salir_y_guardar_trayectos
        }

    def elegir_operacion(self):
        """PREGUNTA AL USUARIO QUE FUNCIONALIDAD REQUIERE"""
        try:
            op = int(self.seleccion_menu(self.operaciones, "operación"))
            print("-" * 70)
            print("\nOperacion seleccionada:", self.operaciones[op], "\n")
            self.menus_disponibles[op]()
            self.continuar_operacion(op)
        except IndentationError:
            print("Ocurrio un error")

    def crear_trayecto(self):
        """MENU PARA CREAR UN NUEVO TRAYECTO"""
        try:
            nombre_trayecto = self.validar_nombre_trayecto()
            origen = self.obtener_nombre_de_ciudad("de origen")
            destino = self.obtener_nombre_de_ciudad("de destino")
            self.motor.crear_trayecto(nombre_trayecto, origen, destino)
        except:
            print("Error en la coneccion con el servidor de google, reintente nuevamente en un momento")

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
                if len(trayecto) + 1 >= numero >= 1:
                    posicion = numero - 1
                else:
                    print("Debe ingresar un numero entre 1 y " + str(len(trayecto)))
            except ValueError:
                print("Debe ingresar un numero entre 1 y " + str(len(trayecto)))
        try:
            nombre_ciudad = self.obtener_nombre_de_ciudad("a añadir")
            self.motor.agregar_ciudad_intermedia(trayecto, nombre_ciudad, posicion)
        except:
            print("Error en la coneccion con el servidor de google, reintente nuevamente en un momento")

    def concatenar_trayectos(self):
        nombre = self.validar_nombre_trayecto()
        op1 = self.seleccionar_trayecto()
        op2 = self.seleccionar_trayecto()
        self.motor.concatenar_trayectos(nombre, op1, op2)

    def info_trayecto(self):
        """MENU PARA OBTENER INFORMACION DE UN TARYECTO SELECCIONADO"""
        op = self.seleccionar_trayecto()
        self.motor.ver_trayecto(op)

    def rutas_trayecto(self):
        """MENU PARA OBTENER INFORMACION DE LAS RUTAS DE UN TRAYECTO"""
        op = self.seleccionar_trayecto()
        self.motor.listar_rutas(op)

    def listar_trayectos(self):
        """Lista los nombres de los trayectos"""
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
        trayecto_1 = self.seleccionar_trayecto()
        trayecto_2 = self.seleccionar_trayecto()
        tipo = ""
        while tipo != "d" and tipo != "t":
            tipo = str(input("Ingrese D para comparar distancia o T para comparar por tiempo").casefold())
        self.motor.comparar_trayectos(trayecto_1, trayecto_2, tipo)

    def seleccionar_ciudades_validas(self, term, tipo_ciudad):
        """En base a un ingreso valida el nombre de la ciudad"""
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
                elif len(ciudades_posibles) >= numero >= 1:
                    posicion = numero
                else:
                    print("Debe ingresar un numero entre 1 y " + str(len(ciudades_posibles)))
            except ValueError:
                print("Debe ingresar un numero entre 1 y " + str(len(ciudades_posibles)))

        return ciudades_posibles[posicion]

    def obtener_nombre_de_ciudad(self, tipo_ciudad):
        ciudad = input("Ingrese nombre de la ciudad " + tipo_ciudad + ": ")

        ciudad_seleccionada = self.seleccionar_ciudades_validas(ciudad, tipo_ciudad)

        return ciudad_seleccionada

    def seleccionar_trayecto(self):

        trayectos = []
        for t in self.motor.trayectos.keys():
            trayectos.append(t)

        op = self.seleccion_de_trayectos(trayectos, "  Seleccionar Trayectos  ")
        return trayectos[op]

    def seleccion_menu(self, opciones, texto):
        posicion = -1
        while posicion == -1:
            print("-" * 70)
            print("Motor de Rutas", " - ", "Operaciones Disponibles")
            for clave, valor in sorted(opciones.items()):
                print("\t [" + str(clave) + "] - ", valor)
            print("-" * 70)
            try:
                numero = int(input("\nInserte número de la " + texto + " que desea: "))
                if len(opciones) >= numero >= 1:
                    posicion = numero
                else:
                    self.clear()
                    print("Debe ingresar un numero entre 1 y " + str(len(opciones)))
            except ValueError:
                print("Debe ingresar un numero entre 1 y " + str(len(opciones)))
        return posicion

    def seleccion_de_trayectos(self, lista, title):
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
                if len(lista) >= numero >= 1:
                    posicion = numero - 1
                else:
                    print("Debe ingresar un numero entre 1 y " + str(len(lista)))
            except ValueError:
                print("Debe ingresar un numero entre 1 y " + str(len(lista)))
        return posicion

    def validar_nombre_trayecto(self):
        nombre_trayecto = ""
        while nombre_trayecto in self.motor.trayectos.keys() or nombre_trayecto == "":
            nombre_trayecto = input("Inserte nombre del nuevo trayecto: ").strip()
            if nombre_trayecto in self.motor.trayectos.keys():
                print("Ya existe un trayecto con ese nombre")
            elif nombre_trayecto == "":
                print("El nombre del trayecto no puede ser vacio")
        return nombre_trayecto

    def mensaje_de_salida(self):
        print("Gracias por usar el Motor de Rutas UNTREF")
        exit()

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def continuar_operacion(self, op):
        if op != len(self.operaciones):
            print("¿Desea continuar operando con el Motor de Rutas?"
                  "\n Oprima [Enter] para continuar o [N] para salir:")
            continuar_con_motor = str(input())
            if continuar_con_motor.strip().upper() == "N":
                self.menus_disponibles[len(self.operaciones)]()
            else:
                self.clear()


menu = Menu()
