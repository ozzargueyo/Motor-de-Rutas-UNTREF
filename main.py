#La aplicacion se corre desde aca


from controladores import motorDeRutas

if __name__ == "__main__":
    motor = motorDeRutas.MotorDeRutas()

    motor.run()
