import os
from multiprocessing import Process, Pipe
from time import sleep

def ponger(p, s):
    count = 0
    while count < 25:
        msg = p.recv()
        print("Process {} got message: {}".format(os.getpid(), msg))
        sleep(.5)
        p.send(s)
        count += 1
        

if __name__ == '__main__':
    parent, child = Pipe()
    
    proc = Process(target=ponger, args=(child, 'Ping'))
    proc.start()
    parent.send("Start Pong")
    ponger(parent, 'pong')
    proc.join()
