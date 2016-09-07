#La aplicacion se corre desde aca
from vistas import Menu

from controladores import motorDeRutas

motor = motorDeRutas.MotorDeRutas()
menu = Menu.Menu(motor)

while True:
    menu.elejir_operacion()
