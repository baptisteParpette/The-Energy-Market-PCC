import random
import multiprocessing
import time
import math
from numpy import random
import os, signal
import sysv_ipc
import socket
import select
import threading
import concurrent.futures
import array
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from threading import Thread, Lock, Semaphore, current_thread        

class Weather(multiprocessing.Process):
    def __init__(self,shared):
        super().__init__()
        self.shared=shared

    def run(self):
        t=0.0
        dt= 1
        while True:
            rdm=(random.normal()*dt)
            temperature = round((-7.5*math.sin((math.pi*t/12)+math.pi/6)+10.5)+(rdm),2)
            t=t+dt
            self.shared[0] = temperature
            self.shared[1] = t
            time.sleep(0.01)

class Market(multiprocessing.Process):
    def __init__(self,shared, prixStart,shared_Value):
        super().__init__()
        self.serve = True
        self.host = ADDR_LOCAL
        self.port = PORT
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setblocking(False)
        self.server_socket.bind((ADDR_LOCAL, PORT))
        self.server_socket.listen()
        self.shared=shared
        self.child_process = None
        self.data=[]
        self.testtt=0
        self.temp=[]
        self.res=[]
        self.lst_prix=[]
        self.index=0
        self.state_war=0
        self.state_natural=0
        self.state_fuel=0
        self.last_temp=0
        self.volat=0.0000001
        self.prix=prixStart
        self.shared_Value=shared_Value
        #self.shared_Value=shared_Value

        signal.signal(signal.SIGUSR1, self.war)
        signal.signal(signal.SIGUSR2, self.natural)
        signal.signal(signal.SIGALRM, self.fuel)
        

    def update(self,frame):
        temp = self.shared_Value.value
        rapport = temp        
        
        if rapport != self.last_temp:
            if rapport == 2**31-1 and self.state_war==0:#WAR
                self.volat=self.volat*5
                self.state_war=1
                self.last_temp = rapport
                print("DEBUT GUERRE")
                self.prix = self.prix + 1 * self.volat
                self.prix = round(self.prix, 10)
                self.lst_prix.append(self.prix)
                self.last_temp = rapport
            if rapport == 2**31-2 and self.state_natural==0:#NATURAL
                self.volat=self.volat*5
                self.state_natural=1
                self.last_temp = rapport
                print("DEBUT NATURAL")
                self.prix = self.prix + 1 * self.volat
                self.prix = round(self.prix, 10)
                self.lst_prix.append(self.prix)
                self.last_temp = rapport

            if rapport == 2**31-3 and self.state_fuel==0:#FUEL
                self.volat=self.volat*5
                self.state_fuel=1
                self.last_temp = rapport
                print("DEBUT FUEL")
                self.prix = self.prix + 1 * self.volat
                self.prix = round(self.prix, 10)
                self.lst_prix.append(self.prix)
                self.last_temp = rapport

            if rapport < 2**31-3:

                if self.state_war==1:
                    if(random.randint(0,500)==1):
                        self.volat=self.volat/5

                        self.last_temp = rapport
                        self.state_war=0
                        print("FIN GUERRE")

                if self.state_natural==1:
                    if(random.randint(0,500)==1):
                        self.volat=self.volat/5

                        self.last_temp = rapport
                        self.state_natural=0
                        print("FIN NATURAL")

                if self.state_fuel==1:
                    if(random.randint(0,500)==1):
                        self.volat=self.volat/5
                        
                        self.last_temp = rapport
                        self.state_fuel=0
                        print("FIN FUEL")
                self.prix = self.prix + rapport * self.volat
                self.prix = round(self.prix, 10)
                self.lst_prix.append(self.prix)
                self.last_temp = rapport

            plt.cla()
            plt.plot(self.lst_prix)

    def socket_handler(self, s, a):

        with s:
            print("Connected to client: ", a)
            data = s.recv(4096)
            while len(data):
                self.testtt+=1
                t=data.decode().split(";")[2]
                self.data.append(data.decode())
                if sem.get_value()==0 and self.testtt==NB_HOME:
                    if self.data!=[]:
                        with lock:
                            self.temp=self.data
                    self.data=[]
                    self.testtt=0
                    for i in range(NB_HOME):
                        sem.release()
                data = s.recv(4096)

            print("Disconnecting from client: ", a)

    def plotPrice(self):
        time.sleep(1)
        fig = plt.figure()
        ani = animation.FuncAnimation(fig, self.update,interval=0.0000000001, repeat=False)
        plt.show()

    def run(self):
        self.create_child()
        chartPriceThread = multiprocessing.Process(target=self.plotPrice)
        chartPriceThread.start()
        temp=shared_memory[1]
        nbthread=0
        with concurrent.futures.ThreadPoolExecutor(max_workers = NB_HOME) as executor:
            while self.serve:
                readable, writable, error = select.select([self.server_socket], [], [], 1)
                if self.server_socket in readable:
                    client_socket, address = self.server_socket.accept()
                    executor.submit(self.socket_handler, client_socket, address)
                    nbthread+=1
                    if nbthread==NB_HOME:
                        break
            while self.serve:  
                if self.temp!=[]:
                    with lock:
                        Todo=[]
                        resTemp=0
                        for elem in self.temp:
                            Todo.append(elem.split(";")[1])
                            resTemp+=eval(elem.split(";")[1])
                        self.res.append(resTemp)
                        self.shared_Value.value=resTemp
                        self.temp=[]
                        self.index+=1
                        if self.state_war==1:
                            self.shared_Value.value=2**31-1
                        self.state_war=0
                        if self.state_natural==1:
                            self.shared_Value.value=2**31-2
                        self.state_natural=0
                        if self.state_fuel==1:
                            self.shared_Value.value=2**31-3
                        self.state_fuel=0
                        

    def stop(self):
        self.serve = False
        self.server_socket.close()
        
    def __del__(self):
        self.stop() 
    
    def create_child(self):
        self.child_process = multiprocessing.Process(target=self.child_function)
        self.child_process.start()
        #print("Child process started with PID", self.child_process.pid)

    def child_function(self):
        print("Enfant",os.getpid(),os.getppid())
        
        while True:
            temp = self.shared_Value.value
            rapport = temp
            
            
            if rapport != self.last_temp:
                
                self.last_temp = rapport
                my_proba=random.randint(0,10000)
                if my_proba==1: #WAR
                    os.kill(os.getppid(), signal.SIGUSR1)
                if my_proba==2: #NNATURAL
                    os.kill(os.getppid(), signal.SIGUSR2)
                if my_proba==3: #FUEL
                    os.kill(os.getppid(), signal.SIGALRM)


    def war(self, sig, frame):
        self.state_war=1
    
    def natural(self, sig, frame):
        self.state_natural=1

    def fuel(self, sig, frame):
        self.state_fuel=1

class Home(multiprocessing.Process):
    def __init__(self, id ):
        super().__init__()
        self.id = id
        self.production_rate = 0
        self.consumption_rate =0
        self.nsPannSol = random.randint(1,10)
        self.tailleMaison = random.randint(1,10)
        self.trade_policy = random.choice(['always_give', 'always_sell', 'sell_if_no_takers'])
        #self.trade_policy = 'always_sell'
        self.surplus = 0
        self.shortage = 0
        self.host = ADDR_LOCAL
        self.port = PORT
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))

    def send_message(self,msg):
        m = msg
        self.client_socket.sendall(m.encode())

    def run(self):
        temp=shared_memory[1]
        while True:
            while temp!=shared_memory[1]:
                temp=shared_memory[1]
                if sem.acquire(block=False): 

                    rdm=random.normal()
                    product_temp=round((-300*math.sin((math.pi*temp/10)+math.pi/5))+(rdm/2),2)
                    if product_temp<=0:
                         self.production_rate=0
                    if product_temp>=0:
                         self.production_rate=abs(product_temp+300)
                    

                    temp_mod=round(temp%24,2)
                   #self.consumption_rate=self.tailleMaison*random.randint(0,5)
                    if(temp_mod>=0.0 and temp_mod<6.0):
                        self.consumption_rate=round(20*abs(1/2*(temp_mod-2)**2+5),2)
                    if(temp_mod>=6.0 and temp_mod<17.9):
                        self.consumption_rate=round(20*abs(-1/6*(temp_mod)+9+5),2)

                    if(temp_mod>=17.9 and temp_mod<19.0):
                        self.consumption_rate=round(20*abs(-5*(temp_mod-19)**2+12+5),2)

                    if(temp_mod>=19.0 and temp_mod<24.0):
                        self.consumption_rate=round(20*abs(-2*(temp_mod)+50+5),2)


                    self.surplus = self.production_rate - self.consumption_rate
                    #self.surplus = 1
                    self.shortage = self.consumption_rate - self.production_rate
                    #print("tem ",round(time.time()*1000),"maison: ",self.id," surplus: ",self.surplus)
                    if(self.surplus>=0):
                        match self.trade_policy:    
                            case "always_give":
                                #print("tem ",round(time.time()*1000),"maison: ",self.id,"don")
                                msg=str(self.id)+";"+str(self.surplus)#1;30 (La maison 1 à un surplus de 30 à donner)
                                #mq_don.send(msg.encode())
                                self.send_message(str(self.id)+";"+"0"+";"+str(temp))
                                self.surplus=0
                            case "always_sell":
                                #print("tem ",round(time.time()*1000),"maison: ",self.id,"vendu")
                                msg=str(self.id)+";"+str(self.surplus)+";"+str(temp)
                                self.send_message(msg)
                                self.surplus=0

                            case "sell_if_no_takers":
                                if mq_need.current_messages == 0:
                                    #print("tem ",round(time.time()*1000),"maison: ",self.id,"vendu car personne")
                                    msg=str(self.id)+";"+str(self.surplus)+";"+str(temp)
                                    self.send_message(msg)
                                    self.surplus=0
                                else:
                                    (msg,_)=mq_need.receive()
                                    msg=str(self.id)+";"+"0"+";"+str(temp)
                                    self.send_message(msg)
                                    self.surplus=0
                                    #print("tem ",round(time.time()*1000),"maison: ",self.id," message: ",msg.decode())

                                self.surplus=0
                        
                            case _:
                                a=1
                                #print("no match")
                    
                            
                    if(self.surplus<0):
                        if mq_don.current_messages == 0:
                            #
                            #print("tem ",round(time.time()*1000),"maison: ",self.id,"Achat marché")
                            #msg=str(self.id)+";"+str(self.surplus)+";"+str(temp)
                            msg=str(self.id)+";"+str(self.surplus)+";"+str(temp)
                            self.send_message(msg)
                            self.surplus=0
                        else:
                            if mq_don.current_messages == 0:
                                    #print("tem ",round(time.time()*1000),"maison: ",self.id,"Achat marché COUCOU")
                                    msg=str(self.id)+";"+str(self.surplus)+";"+str(temp)
                                    self.send_message(msg)
                                    self.surplus=0
                            
                            else:
                                self.send_message(str(self.id)+";"+"0"+";"+str(temp))
                                """while self.surplus !=0:
                                    (msg,_)=mq_don.receive()
                                    string = msg.decode()
                                    quantite=int(string.split(";")[1])
                          ..          donneur=string.split(";")[0]
                                    
                                    if(abs(self.surplus)<quantite):
                                        quantite=quantite-abs(self.surplus)
                                        self.surplus=0
                                        msg=donneur+";"+str(quantite)
                                        mq_don.send(msg.encode())
                                        #print("COUCOU")
                                    else:
                                        self.surplus=self.surplus+quantite
                                        #print("ELSE COUCOU")"""


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
    PORT=random.randint(10000,50000)
    ADDR_LOCAL="localhost"
    NB_HOME = 5
    prixStart=0.17

    consFlag = True
    producerCount = 2
    pcMutex = Lock()

    lock = threading.Lock()
    sem = multiprocessing.BoundedSemaphore(NB_HOME)
    sem2 = multiprocessing.Semaphore(1)

    shared_memory = multiprocessing.Array('d', range(2))
    shared_Value = multiprocessing.Value('d', 0)
    


    mq_don=sysv_ipc.MessageQueue(666,sysv_ipc.IPC_CREAT)
    mq_need=sysv_ipc.MessageQueue(777,sysv_ipc.IPC_CREAT)

    mq_don.remove()
    mq_need.remove()
    
    mq_don=sysv_ipc.MessageQueue(666,sysv_ipc.IPC_CREAT)
    mq_need=sysv_ipc.MessageQueue(777,sysv_ipc.IPC_CREAT)

    Process_weather = Weather(shared_memory)
    Process_weather.start()

    Process_Market = Market(shared_memory,prixStart,shared_Value)
    Process_Market.start()

    #External process creation
    


    market_price = 0.15
    threshold = 0.2
    homes = generate_homes(NB_HOME)


    for home in homes:
        #home.update_surplus_shortage()
        market_price += home.trade_energy(market_price)
        print("Home {} has surplus: {} and shortage: {} pid: {}      {}        {}      {}".format(home.id, home.surplus, home.shortage, home.pid, home.nsPannSol, home.tailleMaison, home.trade_policy))
    #print("Market price is: {}".format(market_price

    Process_weather.join()
    Process_Market.join()

    

