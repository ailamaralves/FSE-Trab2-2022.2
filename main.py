import signal
import time
from src.forno import Forno

interrupt = False

def sighandler(signum, frame):
    global interrupt
    interrupt = True

signal.signal(signal.SIGINT, sighandler)

matricula = [2, 6, 7, 3]

forno = Forno(matricula)

while True:
    user_cmd = forno.refreshCmd()
    if user_cmd != -1:
        forno.handleUserCmd(user_cmd)
    forno.playIt()
    if interrupt:
        break
    time.sleep(0.5)

forno.finishIt()