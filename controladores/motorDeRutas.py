from controladores.controladorBase import ControladorBase
from librerias import gmaps
from modelos.Trayecto import Trayecto
from modelos.Ruta import Ruta


class MotorDeRutas(ControladorBase):
    trayectosModel = Trayecto()
    rutasModel = Ruta()
    trayectos = {}
    rutas = {}

    def __init__(self):
        super().__init__()
        # try:

        self.trayectos = self.trayectosModel.get()
        self.rutas = self.rutasModel.get()
        #self.rutas = json.load(open(os.getcwd() + "\storage\Rutas.json", "r"))

        # except:
        #  print(
        #        "Error al recuperar los trayectos almacenados, la aplicacion seguira funcionando con trayectos nuevos")

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
            if ciudad == trayecto[int(indice) - 1]:
                print("no se puede crear un trayecto desde y hacia la misma ciudad")
                return
            self.crear_ruta(trayecto[indice - 1], ciudad)
        if int(indice) < len(trayecto):
            if ciudad == trayecto[int(indice)]:
                print("no se puede crear un trayecto desde y hacia la misma ciudad")
                return
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

        dataTrayecto = [
                        nombre_trayecto,
                        "->".join(trayecto),
                        self.formatear_distancia(self.obtener_distancia_total(nombre_trayecto)),
                        self.formatear_tiempo(self.obtener_tiempo_total(nombre_trayecto))
        ]

        return dataTrayecto

        print(nombre_trayecto + ": " + str(trayecto))
        print("Distancia: " + self.formatear_distancia(self.obtener_distancia_total(nombre_trayecto)))
        print("Tiempo estimado de viaje: " + self.formatear_tiempo(self.obtener_tiempo_total(nombre_trayecto)))

    def listar_trayectos(self):
        for trayecto in self.trayectos.keys():
            info = trayecto + ": " + (30 - len(trayecto)) * " "
            for ciudad in self.trayectos[trayecto]:
                info += ciudad + " - "
            info = info[:-3] + "."
            print(info)

    def listar_rutas(self, nombre_trayecto):
        trayecto = self.trayectos[nombre_trayecto]
        for i in range(0, len(trayecto) - 1):
            ruta = self.unir_origen_destino(trayecto[i], trayecto[i + 1])
            print(ruta)
            print(self.formatear_distancia(self.rutas[ruta][1]))
            print(self.formatear_tiempo(self.rutas[ruta][0]))

    def salir_y_guardar_trayectos(self):
        """Todavia no probe el exit"""
        # try:
        self.trayectosModel.toJson(self.trayectos)
        self.rutasModel.toJson(self.rutas)

        #open(os.getcwd() + r"\storage\Trayectos.json", "w").write(json.dumps(self.trayectos))
        #open(os.getcwd() + r"\storage\Rutas.json", "w").write(json.dumps(self.rutas))

        from vistas.Menu import menu
        menu.terminar = True
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
                matriz = gmaps.distance_matrix(origen, destino)
                ruta = (matriz['rows'][0]['elements'][0]['duration']['value'],
                        matriz['rows'][0]['elements'][0]['distance']['value'])
                self.rutas[self.unir_origen_destino(origen, destino)] = ruta
            except Exception as e:
                # no se ha podido crear la ruta
                print(e)

    def unir_origen_destino(self, origen, destino):
        return origen + "-" + destino

    def separar_origen_destino(self, ruta):
        return ruta.split("-")

    def obtener_tiempo_total(self, nombre):
        trayecto = self.trayectos[nombre]
        total = 0
        for i in range(0, len(trayecto) - 1):
            total += self.rutas[self.unir_origen_destino(trayecto[i], trayecto[i + 1])][1]
        return total

    def obtener_distancia_total(self, nombre):
        trayecto = self.trayectos[nombre]
        total = 0
        for i in range(0, len(trayecto) - 1):
            total += self.rutas[self.unir_origen_destino(trayecto[i], trayecto[i + 1])][0]
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
        d = distancia / 1000
        return "{0:8.2f} km".format(d)

    def obtener_nombre_correcto(self, ciudad):
        return (gmaps.distance_matrix(ciudad, ciudad)['origin_addresses'][0].split(",")[0])


# CON LOS CAMBIOS ESTE TEST YA NO SE PUEDE EJECUTAR DESDE ACA
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
