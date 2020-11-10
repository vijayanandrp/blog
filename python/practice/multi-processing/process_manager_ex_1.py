from time import sleep
from os import getpid
from multiprocessing import Process, Manager


def counter(d):
    d[getpid()] = 0
    for i in range(10):
        sleep(.1)
        d[getpid()] += 1
    return 0


# Not a thread safe
if __name__ == '__main__':
    with Manager() as m:
        d = m.dict()
        p1 = Process(target=counter, args=(d,))
        p2 = Process(target=counter, args=(d,))
        p1.start()
        p2.start()
        p1.join()
        p2.join()
        print('Finale value is ', d)