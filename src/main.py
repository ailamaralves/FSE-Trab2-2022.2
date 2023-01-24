from uart import UART
from utils.pid import PID

matricula = [2, 6, 7, 3]
pid = PID()
uart = UART(matricula)
temp_ref = uart.envia(0xC1, [])
print(temp_ref)