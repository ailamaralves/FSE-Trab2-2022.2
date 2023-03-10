from utils.bme280 import *
from utils.csv_reader import *
from utils.pid import PID
from src.uart import UART
from src.gpio import PWM

class Forno:
    COMANDOS_USUARIO = [0xA1, 0xA2, 0xA3, 0xA4, 0xA5]

    def __init__(self, matricula):
        self.uart = UART(matricula)
        self.pwm = PWM()
        self.pid = PID()
        self.temp_ambiente = calcula_temp_ambiente()
        
        self.ligado = 0x00
        self.modo = 0x00
        self.iniciar = 0x00
        self.curva = read_record()

        self.temp_interna = self.uart.envia(0, None)
        self.temp_referencia = self.uart.envia(1, None)
        self.uart.envia(5, self.ligado)
        self.uart.envia(6, self.modo)
        self.uart.envia(7, self.iniciar)
        self.uart.envia(8, self.temp_ambiente)
        print("Temperatura interna: {}".format(self.temp_interna))
        print("Temperatura de referencia: {}".format(self.temp_referencia))
        print("Temperatura ambiente: {}".format(self.temp_ambiente))

    def handleUserCmd(self, user_cmd):
        print(user_cmd)
        if user_cmd == self.COMANDOS_USUARIO[0]:
            self.ligado = 0x01
            self.uart.envia(5, self.ligado)  # On/Off
        elif user_cmd == self.COMANDOS_USUARIO[1]:
            self.ligado = 0x00
            self.uart.envia(5, self.ligado)  # On/Off
        elif user_cmd == self.COMANDOS_USUARIO[2]:
            if self.ligado == 0x00:
                return
            self.iniciar = 0x01
            self.uart.envia(7, self.iniciar)   # Start/Stop
        elif user_cmd == self.COMANDOS_USUARIO[3]:
            self.iniciar = 0x00
            self.uart.envia(7, self.iniciar)   # Start/Stop
            self.stopIt()
        elif user_cmd == self.COMANDOS_USUARIO[4]:
            self.modo = not self.modo
            self.uart.envia(6, self.modo)   # Dashboard
            self.tempo_curva = 0
        else:
            pass
        return

    def refreshCmd(self):
        return self.uart.envia(2, None)

    def isPlaying(self):
        return self.iniciar

    def playIt(self):
        if not self.isPlaying():
            return
        if self.modo:
            if self.tempo_curva % 120 == 0:
                idx = 1 + (self.tempo_curva / 120)
                idx = 9 if idx > 9 else idx
                print("curva: ", idx)
                self.temp_referencia = self.curva.temp[idx]
                print("curva: ", self.temp_referencia)
                self.uart.envia(4, self.temp_referencia)
            self.tempo_curva += 1
        else:
            ref_ = self.uart.envia(1, None)
            ref2_ = self.temp_referencia
            if ref_ != ref2_:
                self.temp_referencia = ref_
        self.temp_interna = self.uart.envia(0, None)
        print("temp_interna: ", self.temp_interna)
        controle = self.pid.pid_controle(self.temp_referencia, self.temp_interna)
        print("pid: ", controle)
        intensity = int(controle)
        sinal_controle = self.pwm <= intensity
        self.uart.envia(3, sinal_controle)
        return
        
    def stopIt(self):
        sinal_controle = self.pwm <= 0
        self.uart.envia(3, sinal_controle)
        self.uart.envia(6, sinal_controle)
        self.uart.envia(8, sinal_controle)

    def finishIt(self):
        self.stopIt()
        del self.uart