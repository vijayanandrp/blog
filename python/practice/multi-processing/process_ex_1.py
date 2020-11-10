from os import getpid
from multiprocessing import Process


def prove_existence():
    print(getpid())
    

if __name__ == '__main__':
    p = Process(target=prove_existence, args=())
    p.start()
    p.join()

    p1 = Process(target=prove_existence, args=())
    p1.start()
    p1.join()


