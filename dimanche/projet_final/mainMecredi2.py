import random
import multiprocessing
import time
import math
from numpy import random
import os, signal
import sysv_ipc


class Weather(multiprocessing.Process):
    def __init__(self,shared):
        super().__init__()
        self.shared=shared

    def run(self):
        t=0.0
        dt=1/6
        while True:
            rdm=(random.normal()*dt)
            temperature = round((-7.5*math.sin((math.pi*t/12)+math.pi/6)+10.5)+(rdm),2)
            t=t+dt
            self.shared[0] = temperature
            self.shared[1] = t
            time.sleep(1)

class Market(multiprocessing.Process):
    def __init__(self,shared):
        super().__init__()
        self.shared=shared
        self.child_process = None
        signal.signal(signal.SIGUSR1, self.war)
        signal.signal(signal.SIGUSR2, self.natural)
        signal.signal(signal.SIGALRM, self.fuel)

    def run(self):
        a=1
        
    
    def create_child(self):
        self.child_process = multiprocessing.Process(target=self.child_function)
        self.child_process.start()
        print("Child process started with PID", self.child_process.pid)

    def child_function(self):
        temp=shared_memory[1]
        while True:
            while temp!=shared_memory[1]:
                temp=shared_memory[1]
                my_proba=random.randint(0,100)
                print(shared_memory[0],my_proba)
                if my_proba==1:
                    os.kill(os.getppid(), signal.SIGUSR1)
                if my_proba==2:
                    os.kill(os.getppid(), signal.SIGUSR2)
                if my_proba==3:
                    os.kill(os.getppid(), signal.SIGALRM)
        time.sleep(2)
        os.kill(os.getppid(), signal.SIGALRM)
        time.sleep(2)
        os.kill(os.getppid(), signal.SIGUSR2)


    def war(self, sig, frame):
        print("Received signal 1", sig, "in process with PID", os.getpid())
        #os.kill(self.child_process.pid, signal.SIGKILL)
    
    def natural(self, sig, frame):
        print("Received signal 2", sig, "in process with PID", os.getpid())
        #os.kill(self.child_process.pid, signal.SIGKILL)

    def fuel(self, sig, frame):
        print("Received signal 3", sig, "in process with PID", os.getpid())
        #os.kill(self.child_process.pid, signal.SIGKILL)

class Home(multiprocessing.Processround(time.time()*1000)):
    def __init__(self, id):
        super().__init__()
        self.id = id
        self.production_rate = 0
        self.consumption_rate =0
        self.nsPannSol = random.randint(0,10)
        self.tailleMaison = random.randint(1,4)
        self.trade_policy = random.choice(['always_give', 'always_sell', 'sell_if_no_takers'])
        self.surplus = 0
        self.shortage = 0

    def run(self):
        temp=shared_memory[1]
        while True:
            while temp!=shared_memory[1]:
                temp=shared_memory[1]
                self.production_rate=self.nsPannSol*random.randint(0,5)
                self.consumption_rate=self.tailleMaison*random.randint(0,5)
                self.surplus = self.production_rate - self.consumption_rate
                self.shortage = self.consumption_rate - self.production_rate
                print("tem ",round(time.time()*1000),"maison: ",self.id," surplus: ",self.surplus)

                if(self.surplus>0):
                    match self.trade_policy:    
                        case "always_give":
                            print("tem ",round(time.time()*1000),"maison: ",self.id,"don")
                            msg=str(self.id)+";"+str(self.surplus)
                            mq_don.send(msg.encode())
                            self.surplus=0
                        case "always_sell":
                            print("tem ",round(time.time()*1000),"maison: ",self.id,"vendu")
                            self.surplus=0

                        case "sell_if_no_takers":
                            if mq_need.current_messages == 0:
                                print("tem ",round(time.time()*1000),"maison: ",self.id,"vendu car personne")
                            else:
                                (msg,_)=mq_need.receive()
                                print("tem ",round(time.time()*1000),"maison: ",self.id," message: ",msg.decode())

                            self.surplus=0
                    
                        case _:
                            print("no match")
                        
                if(self.surplus<0):
                    if mq_don.current_messages == 0:
                        print("tem ",round(time.time()*1000),"maison: ",self.id,"Achat marché")
                        self.surplus=0

                        #ACHETE AU MARCHE
                    else:
                        (msg,_)=mq_don.receive()
                        print("tem ",round(time.time()*1000),"maison: ",self.id," message: ",msg.decode()," NEED")
                        self.surplus=0



    def trade_energy(self, market_price):
        if self.trade_policy == 'always_give':
            return self.surplus
        elif self.trade_policy == 'always_sell':
            return -self.shortage
        else:  # self.trade_policy == 'sell_if_no_takers':
            if self.surplus > 0:
                return self.surplus
            elif self.shortage > 0 and market_price < threshold:
                return -self.shortage
            else:
                return 0

def generate_homes(num_homes):
    homes = []
    for i in range(num_homes):
        h=Home(i)
        h.start()
        homes.append(h)

    return homes

if __name__ == '__main__':
    shared_memory = multiprocessing.Array('d', range(2))

    mq_don=sysv_ipc.MessageQueue(666,sysv_ipc.IPC_CREAT)
    mq_need=sysv_ipc.MessageQueue(777,sysv_ipc.IPC_CREAT)
    print(mq_don.current_messages)
    print(mq_need.current_messages)

    mq_don.remove()
    mq_need.remove()
    
    mq_don=sysv_ipc.MessageQueue(666,sysv_ipc.IPC_CREAT)
    mq_need=sysv_ipc.MessageQueue(777,sysv_ipc.IPC_CREAT)
    print(mq_don.current_messages)
    print(mq_need.current_messages)

    Process_weather = Weather(shared_memory)
    Process_weather.start()

    Process_Market = Market(shared_memory)
    Process_Market.start()

    #External process creation
    Process_Market.create_child()


    market_price = 0.15
    threshold = 0.2
    homes = generate_homes(3)


    for home in homes:
        #home.update_surplus_shortage()
        market_price += home.trade_energy(market_price)
        print("Home {} has surplus: {} and shortage: {} pid: {}      {}        {}      {}".format(home.id, home.surplus, home.shortage, home.pid, home.nsPannSol, home.tailleMaison, home.trade_policy))
    print("Market price is: {}".format(market_price))





    Process_weather.join()
    Process_Market.join()

