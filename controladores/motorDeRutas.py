from librerias.gmaps import gmaps
from modelos.Trayecto import Trayecto
from modelos.Ruta import Ruta
from terminaltables import DoubleTable
import exepciones
from exepciones.MISMACIUDAD import MISMACIUDAD


class MotorDeRutas:
    trayectosModel = Trayecto()
    rutasModel = Ruta()
    trayectos = {}
    rutas = {}

    def __init__(self):
        try:
            self.trayectos = self.trayectosModel.get()
            self.rutas = self.rutasModel.get()
        except:
            print("Error al cargar datos guardados, la aplicacion seguira funcionando con trayectos nuevos")

    def crear_trayecto(self, nombre_trayecto, origen, destino):
        """Crea un nuevo trayecto con un nombre determinado a partir de dos ciudades"""
        try:
            self.crear_ruta(origen, destino)
            ciudades = [origen, destino]
            self.trayectos[nombre_trayecto] = ciudades
        except MISMACIUDAD as e:
            print(e.message)

    def agregar_ciudad_intermedia(self, trayecto, ciudad, indice):
        """Agrega una ruta entre las ciudades indice - 1 indice y indice + 1 si es posible"""
        try:
            if int(indice) > 0:
                self.crear_ruta(trayecto[indice - 1], ciudad)
            if int(indice) < len(trayecto):
                self.crear_ruta(ciudad, trayecto[indice])
            trayecto.insert(indice, ciudad)
        except MISMACIUDAD as e:
            print(e.message)

    def concatenar_trayectos(self, nuevo_trayecto, primer_trayecto, segundo_trayecto):
        try:
            self.crear_ruta(self.trayectos[primer_trayecto][-1], self.trayectos[segundo_trayecto][0])
            self.trayectos[nuevo_trayecto] = self.trayectos[primer_trayecto] + self.trayectos[segundo_trayecto]
        except MISMACIUDAD as e:
            print(e.message)

    def comparar_trayectos(self, primer_trayecto, segundo_trayecto, tipo):
        comparacion = self.obtener_distancia_total
        formato = self.formatear_distancia
        if tipo == "t":
            comparacion = self.obtener_tiempo_total
            formato = self.formatear_tiempo
        table_data = [["Nombre", "Distancia"]]
        total_primero = comparacion(primer_trayecto)
        total_segundo = comparacion(segundo_trayecto)
        table_data.append([primer_trayecto, formato(total_primero)])
        table_data.append([segundo_trayecto, formato(total_segundo)])
        table = DoubleTable(table_data, "")
        table.justify_columns = {0: 'center', 1: 'left'}
        print(table.table, "\n")
        if total_primero < total_segundo:
            print("El trayecto: " + primer_trayecto + ". Es" + formato(
                total_segundo - total_primero) + " mas largo \n")
        else:
            print("El trayecto: " + segundo_trayecto + ". Es" + formato(
                total_primero - total_segundo) + " mas largo \n")

    def ver_trayecto(self, nombre_trayecto):
        trayecto = self.trayectos[nombre_trayecto]

        data_trayecto = [
            nombre_trayecto,
            "->".join(trayecto),
            self.formatear_distancia(self.obtener_distancia_total(nombre_trayecto)),
            self.formatear_tiempo(self.obtener_tiempo_total(nombre_trayecto))
        ]

        return data_trayecto

    def listar_rutas(self, nombre_trayecto):
        trayecto = self.trayectos[nombre_trayecto]
        table_data = [["Origen -> Destino", "Distancia", "Duracion"]]
        for i in range(0, len(trayecto) - 1):
            ruta = self.unir_origen_destino(trayecto[i], trayecto[i + 1])
            table_data.append(
                [ruta, self.formatear_distancia(self.rutas[ruta][1]), self.formatear_tiempo(self.rutas[ruta][0])])
        table = DoubleTable(table_data, "")
        table.justify_columns = {0: 'center', 1: 'left', 2: 'left'}
        print(table.table, "\n")

    def salir_y_guardar_trayectos(self):
        """Guarda los datos en el Json y luego cierra el programa"""
        self.trayectosModel.toJson(self.trayectos)
        self.rutasModel.toJson(self.rutas)
        from vistas.Menu import menu
        menu.terminar = True

    def crear_ruta(self, origen, destino):
        """Crea una nueva ruta si no esta presente en el diccionario"""
        if origen == destino:
            raise MISMACIUDAD
        nombre_de_ruta = self.unir_origen_destino(origen, destino)
        if nombre_de_ruta not in self.rutas.keys():
            try:
                matriz = gmaps.distance_matrix(origen, destino)
                ruta = (matriz['rows'][0]['elements'][0]['duration']['value'],
                        matriz['rows'][0]['elements'][0]['distance']['value'])
                self.rutas[self.unir_origen_destino(origen, destino)] = ruta
            except Exception as e:
                # no se ha podido crear la ruta
                print(e)

    def unir_origen_destino(self, origen, destino):
        return origen + " -> " + destino

    def separar_origen_destino(self, ruta):
        return ruta.split(" -> ")

    def obtener_tiempo_total(self, nombre):
        trayecto = self.trayectos[nombre]
        total = 0
        for i in range(0, len(trayecto) - 1):
            total += self.rutas[self.unir_origen_destino(trayecto[i], trayecto[i + 1])][0]
        return total

    def obtener_distancia_total(self, nombre):
        trayecto = self.trayectos[nombre]
        total = 0
        for i in range(0, len(trayecto) - 1):
            total += self.rutas[self.unir_origen_destino(trayecto[i], trayecto[i + 1])][1]
        return total

    def formatear_tiempo(self, tiempo):
        respuesta = ""
        t = tiempo
        dias = int(t / 24 / 60 / 60)
        if dias != 0:
            respuesta += "{0:2d} dias,".format(dias)
        t -= dias * 24 * 60 * 60
        horas = int(t / 60 / 60)
        if dias != 0 or horas != 0:
            respuesta += "{0:2d} horas,".format(horas)
        t -= horas * 60 * 60
        minutos = int(t / 60)
        respuesta += "{0:2d} min".format(minutos)
        return respuesta

    def formatear_distancia(self, distancia):
        d = distancia / 1000
        return "{0:8.2f} km".format(d)

    def obtener_ciudades_posibles(self, ciudad):
        """Utilizando el autocomplete de gmaps devuelve las ciudades con nombre similar al ingresado"""
        data_ciudades = gmaps.places_autocomplete(ciudad, type="(cities)", language="es")
        ciudades_posibles = {}
        index = 1
        if len(data_ciudades) > 0:
            for ciudad in data_ciudades:
                ciudades_posibles[index] = ciudad["description"]
                index += 1

        return ciudades_posibles
