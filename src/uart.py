import serial
import time

from utils.crc16 import calcula_CRC

class UART:
    conectado = False
    endereco = 1
    comando = [0x23, 0x16]
    #              0      1     2     3     4     5     6    7     8
    subComando = [0xC1, 0xC2, 0xC3, 0xD1, 0xD2, 0xD3, 0xD4, 0xD5, 0xD6]
    matricula:list
    def __init__(self, matricula):
        self.matricula = matricula
        self.conecta()

    def conecta(self):
        filestream = "/dev/serial0"
        baudrate = 9600
        timeout = 1
        self.serial = serial.Serial(filestream, baudrate, timeout=timeout)

        if (self.serial.isOpen()):
            self.conectado = True
            print('Porta aberta, conexao realizada')
        else:
            self.conectado = False
            print('Porta fechada, conexao nao realizada')
    
    def desconecta(self):
        self.serial.close()
        self.conectado = False
        print('Porta desconectada')

    def envia(self, subcomando, dado):
        if dado == None:
            dado = []
        print(dado)
        mensagem = [self.endereco , self.comando[int(subcomando >= 4)] , self.subComando[subcomando]] + self.matricula 
        bmensagem = bytearray(mensagem) + bytearray(dado)
        
        crc = calcula_CRC(bmensagem, len(bmensagem)).to_bytes(2, 'little')
        print(crc)
        msg = bmensagem + crc
        self.serial.write(msg)
        time.sleep(0.1)
        res = self.recebe()
        return res
        # print('Mensagem enviada: {}'.format(msg))

    def recebe(self):
        time.sleep(0.2)
        buffer = self.serial.read(9)
        buffer_tam = len(buffer)

        if buffer_tam == 9:
            data = buffer[3:7]
            crc16_recebido = buffer[7:9]
            crc16_calculado = calcula_CRC(buffer[0:7], 7).to_bytes(2, 'little')

            if crc16_recebido == crc16_calculado:
                # print('Mensagem recebida: {}'.format(buffer))
                return data
            else:
                print('Mensagem recebida: {}'.format(buffer))
                print('CRC16 invalido')
                return None
        elif buffer_tam == 5:
            crc16_recebido = buffer[3:5]
            crc16_calculado = calcula_CRC(buffer[0:3], 3).to_bytes(2, 'little')

            if crc16_recebido == crc16_calculado:
                # print('Mensagem recebida: {}'.format(buffer))
                return data
            else:
                print('Mensagem recebida: {}'.format(buffer))
                print('CRC16 invalido')
                return None
        else:
            print('Mensagem recebida: {}'.format(buffer))
            print('Mensagem no formato incorreto, tamanho: {}'.format(buffer_tam))
            return None

