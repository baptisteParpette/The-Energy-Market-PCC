import array
from threading import Thread, Lock, Semaphore, current_thread

class BoundedBuffer:
    def __init__(self, size):
        self.buffer = array.array('l', range(size))
        self.size = size
        self.p = self.q = 0
        self.mutex = Lock()
        self.full = Semaphore(0)
        self.empty = Semaphore(size)

    def put(self, item):
        self.empty.acquire()
        with self.mutex:
            self.buffer[self.p] = item
            print(current_thread().name, "produces:", item, "in:", self.p, flush=True)            
            self.p = (self.p + 1) % self.size
        self.full.release()

    def get(self):
        self.full.acquire()
        with self.mutex:
            item = self.buffer[self.q]
            print(current_thread().name, "consumes:", item, "from:", self.q, flush=True)
            self.q = (self.q + 1) % self.size 
        self.empty.release()
        return item
        
class ProducerThread(Thread):
    def __init__(self, buffer, n):
        super().__init__()
        self.buffer = buffer
        self.n = n

    def run(self):
        i = 0
        a, b = 0, 1
        while i < self.n:
            a, b = b, a+b
            self.buffer.put(a)
            i += 1

class ConsumerThread(Thread):
    def __init__(self, buffer):
        super().__init__()
        self.buffer = buffer

    def run(self):
        i = 0
        while True:
            item = self.buffer.get()

if __name__ == "__main__":
    buffer = BoundedBuffer(5)
    cons = [ConsumerThread(buffer) for i in range(2)]   
    prod = [ProducerThread(buffer, 3) for i in range(2)]   
 
    for t in cons:
        t.start()
        
    for t in prod:
        t.start()
        
    for t in cons:
        t.join()
        
    for t in prod:
        t.join()
