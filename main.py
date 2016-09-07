#La aplicacion se corre desde aca
from vistas import Menu

from controladores import motorDeRutas

en_ejecucion = True
motor = motorDeRutas.MotorDeRutas()
menu = Menu.Menu(motor)

while en_ejecucion:
    menu.elejir_operacion()
