import multiprocessing

class Data:
    def __init__(self):
        self.value = multiprocessing.Value("i", 0)

class Process1(multiprocessing.Process):
    def __init__(self, data):
        super().__init__()
        self.data = data

    def run(self):
        with self.data.value.get_lock():
            self.data.value.value += 1
        print("Process 1: data.value =", self.data.value.value)

class Process2(multiprocessing.Process):
    def __init__(self, data):
        super().__init__()
        self.data = data

    def run(self):
        with self.data.value.get_lock():
            self.data.value.value -= 1
        print("Process 2: data.value =", self.data.value.value)

if __name__ == '__main__':
    data = Data()

    p1 = Process1(data)
    p2 = Process2(data)

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    print("Data value after process execution:", data.value.value)
