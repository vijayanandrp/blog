import threading
import time
import random

try:
    import Queue
except:
    import queue as Queue


class Producer:
    """ Producesor make the plate of foods """
    def __init__(self):
        self.food = ['ham', 'soup', 'salad']
        self.next_time = 0
    
    def run(self):
        global q
        while time.clock() < 10:
            if self.next_time < time.clock():
                f = self.food[random.randrange(len(self.food))]
                q.put(f)
                print('Adding ' + f)
                self.next_time += random.random()
                
                
class Consumer:
    """ Consumes or eats the plate of foods """
    def __init__(self):
        self.next_time = 0
        
    def run(self):
        global q
        while time.clock() < 10:
            if self.next_time < time.clock() and not q.empty():
                f = q.get()
                print('Removing '+ f)
                self.next_time += random.random() * 2

if __name__ == '__main__':
    q = Queue.Queue(10)
    
    p = Producer()
    c = Consumer()
    pt = threading.Thread(target=p.run(), args=())
    ct = threading.Thread(target=c.run(), args=())
    pt.start()
    ct.start()