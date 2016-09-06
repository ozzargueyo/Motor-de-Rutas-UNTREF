from controladores.controladorBase import ControladorBase
# from vistas.menues import *
import json
import os
import googlemaps


class MotorDeRutas(ControladorBase):
    trayectos = {}
    rutas = {}
    controlador_google = googlemaps.Client(key="AIzaSyDjhMhoPyvD7P4elZoBoVmVu3bGMT4be1Y")

    def __init__(self):
        super().__init__()
        # self.menus = Menues(self)
        try:
            self.trayectos = json.load(open(os.getcwd()[:-13] + "storage\Trayectos.json", "r"))
            self.rutas = json.load(open(os.getcwd()[:-13] + "storage\Rutas.json", "r"))
        except:
            print(
                "Error al recuperar los trayectos almacenados, la aplicacion seguira funcionando con trayectos nuevos")

    def run(self):
        # self.menus.mainMenu()
        pass

    def crear_trayecto(self, nombre_trayecto, origen, destino):
        """Crea un nuevo trayecto con un nombre determinado a partir de dos ciudades

        DEBE RECIBIR EL NOMBRE DE LAS CIUDADES COMO ESTAN ESCRITAS EN GOOGLEMAPS MATRIX ADDRESSES

        en caso de que ya exista un trayecto con ese nombre levanta una exepcion
        """
        if nombre_trayecto in self.trayectos.keys():
            print("ya existe un trayecto con ese nombre")
            return
        self.crear_ruta(origen, destino)
        ciudades = [origen, destino]
        self.trayectos[nombre_trayecto] = ciudades

    def agregar_ciudad_intermedia(self, nombre_trayecto, ciudad, indice):
        """Agrega una ruta entre las ciudades indice - 1 indice y indice + 1 si es posible"""
        trayecto = self.trayectos[nombre_trayecto]
        if int(indice) > 0:
            self.crear_ruta(trayecto[indice - 1], ciudad)
        if int(indice) < len(trayecto):
            self.crear_ruta(ciudad, trayecto[indice])
        trayecto.insert(indice, ciudad)

    def agregar_ciudad_final(self, nombre_trayecto, ciudad):
        self.agregar_ciudad_intermedia(nombre_trayecto, ciudad, len(self.trayectos[nombre_trayecto]))

    def concatenar_trayectos(self, nuevo_trayecto, primer_trayecto, segundo_trayecto):
        if nuevo_trayecto in self.trayectos.keys():
            print("ya existe un trayecto con ese nombre")
            return
        self.crear_ruta(self.trayectos[primer_trayecto][-1], self.trayectos[segundo_trayecto][0])
        self.trayectos[nuevo_trayecto] = self.trayectos[primer_trayecto] + self.trayectos[segundo_trayecto]

    def comparar_trayectos_por_distancia(self, primer_trayecto, segundo_trayecto):
        total_primero = self.obtener_distancia_total(primer_trayecto)
        total_segundo = self.obtener_distancia_total(segundo_trayecto)
        print(primer_trayecto + ": " + self.formatear_distancia(total_primero))
        print(segundo_trayecto + ": " + self.formatear_distancia(total_segundo))
        if total_primero < total_segundo:
            print("Diferencia: " + self.formatear_distancia(total_segundo - total_primero))
        else:
            print("Diferencia: " + self.formatear_distancia(total_primero - total_segundo))

    def comparar_trayectos_por_tiempo(self, primer_trayecto, segundo_trayecto):
        total_primero = self.obtener_tiempo_total(primer_trayecto)
        total_segundo = self.obtener_tiempo_total(segundo_trayecto)
        print(primer_trayecto + ": " + self.formatear_tiempo(total_primero))
        print(segundo_trayecto + ": " + self.formatear_tiempo(total_segundo))
        if total_primero < total_segundo:
            print("Diferencia: " + self.formatear_tiempo(total_segundo - total_primero))
        else:
            print("Diferencia: " + self.formatear_tiempo(total_primero - total_segundo))

    def ver_trayecto(self, nombre_trayecto):
        trayecto = self.trayectos[nombre_trayecto]
        print(nombre_trayecto + ": " + str(trayecto))
        print("Distancia: " + self.formatear_distancia(self.obtener_distancia_total(nombre_trayecto)))
        print("Tiempo estimado de viaje: " + self.formatear_tiempo(self.obtener_tiempo_total(nombre_trayecto)))

    def listar_trayectos(self):
        print(self.trayectos.keys())

    def listar_rutas(self, nombre_trayecto):
        trayecto = self.trayectos[nombre_trayecto]
        for i in range(0, len(trayecto) - 1):
            ruta = self.unir_origen_destino(trayecto[i], trayecto[i + 1])
            print(ruta)
            print(self.formatear_distancia(self.rutas[ruta][0]))
            print(self.formatear_tiempo(self.rutas[ruta][1]))

    def salir_y_guardar_trayectos(self):
        """Todavia no probe el exit"""
        # try:
        open(os.getcwd()[:-13] + r"storage\Trayectos.json", "w").write(json.dumps(self.trayectos))
        open(os.getcwd()[:-13] + r"storage\Rutas.json", "w").write(json.dumps(self.rutas))

        exit()
        # except:

    def crear_ruta(self, origen, destino):
        """Crea una nueva ruta si no esta presente en el diccionario

        si no puede crear la ruta tira una excepcion
        """
        if origen == destino:
            print("las ciudades deben ser distintas")
            return
        nombre_de_ruta = self.unir_origen_destino(origen, destino)
        if nombre_de_ruta not in self.rutas.keys():
            try:
                matriz = self.controlador_google.distance_matrix(origen, destino)
                ruta = (matriz['rows'][0]['elements'][0]['duration']['value'],
                        matriz['rows'][0]['elements'][0]['distance']['value'])
                self.rutas[self.unir_origen_destino(origen, destino)] = ruta
            except:
                # no se ha podido crear la ruta
                raise

    def unir_origen_destino(self, origen, destino):
        return origen + "-" + destino

    def separar_origen_destino(self, ruta):
        return ruta.split("-")

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
        t = tiempo
        dias = int(t / 24 / 60 / 60)
        t -= dias * 24 * 60 * 60
        horas = int(t / 60 / 60)
        t -= horas * 60 * 60
        minutos = int(t / 60)
        return "{0:2d} dias, {1:2d} horas, {2:2d} min".format(dias, horas, minutos)

    def formatear_distancia(self, distancia):
        d = distancia / 1000000
        return "{0:8.4f} km".format(d)


if __name__ == '__main__':
    motor = MotorDeRutas()
    motor.crear_trayecto("Mi Trayecto", "Buenos Aires", "La Plata")
    motor.agregar_ciudad_final("Mi Trayecto", "Santiago Del Estero")
    motor.crear_trayecto("Mi Trayecto 2", "Rosario", "La Pampa")
    motor.concatenar_trayectos("Mi Trayecto Concatenado", "Mi Trayecto", "Mi Trayecto 2")
    motor.comparar_trayectos_por_distancia("Mi Trayecto", "Mi Trayecto 2")
    motor.comparar_trayectos_por_tiempo("Mi Trayecto", "Mi Trayecto 2")
    motor.agregar_ciudad_intermedia("Mi Trayecto Concatenado", "Chubut", 1)
    motor.ver_trayecto("Mi Trayecto")
    motor.listar_trayectos()
    motor.listar_rutas("Mi Trayecto")
    motor.salir_y_guardar_trayectos()
