# La aplicacion se corre desde aca
# importamos una clase Menu que es un Singleton llamado menu
from vistas.Menu import menu

while not menu.terminar:
    menu.elegir_operacion()

if menu.terminar:
    menu.mensajeDeSalida()
