import random
import multiprocessing
import time
import math
from numpy import random
import os, signal
import sysv_ipc
import socket
import sys
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
        dt= DT
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
        self.time_values = []
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

        self.times_nothing = []
        self.prices_nothing = []
        self.times_1 = []
        self.prices_1 = []
        self.times_2 = []
        self.prices_2 = []
        self.times_3 = []
        self.prices_3 = []

        self.index=0
        self.state_war=0
        self.state_natural=0
        self.state_fuel=0
        self.last_temp=0
        self.volat=0.0000005
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


            t=len(self.lst_prix)/24*DT + 1
            if rapport == 2**31-1 and self.state_war==0:#WAR
                self.volat=self.volat*5
                self.state_war=1
                self.last_temp = rapport
                #print("DEBUT GUERRE")
                self.prix = self.prix + 1 * self.volat
                self.prix = round(self.prix, 10)
                self.lst_prix.append(self.prix)
                self.last_temp = rapport
            if rapport == 2**31-2 and self.state_natural==0:#NATURAL
                self.volat=self.volat*3
                self.state_natural=1
                self.last_temp = rapport
                #print("DEBUT NATURAL")
                self.prix = self.prix + 1 * self.volat
                self.prix = round(self.prix, 10)
                self.lst_prix.append(self.prix)
                self.last_temp = rapport

            if rapport == 2**31-3 and self.state_fuel==0:#FUEL
                self.volat=self.volat*2
                self.state_fuel=1
                self.last_temp = rapport
                #print("DEBUT FUEL")
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
                        #print("FIN GUERRE")

                if self.state_natural==1:
                    if(random.randint(0,500)==1):
                        self.volat=self.volat/3

                        self.last_temp = rapport
                        self.state_natural=0
                        #print("FIN NATURAL")

                if self.state_fuel==1:
                    if(random.randint(0,500)==1):
                        self.volat=self.volat/2
                        
                        self.last_temp = rapport
                        self.state_fuel=0
                         #print("FIN FUEL")

                self.prix = self.prix + rapport * self.volat
                if self.prix<=0.1:
                    self.prix = self.prix + abs(rapport) * self.volat
                sum =self.state_war+self.state_natural+self.state_fuel
                if sum==0 and self.prix>=0.2:
                    self.prix = self.prix - abs(rapport) * self.volat*random.randint(5,10)


                self.prix = round(self.prix, 10)
                self.lst_prix.append(self.prix)
                self.last_temp = rapport


            sum =self.state_war+self.state_natural+self.state_fuel 
            print("Il y a actuellement : ")
            if self.state_war==1:
                print("une guerre - ",end =" ")
            if self.state_natural==1:
                print("une catastrophe naturel - ",end =" ")
            if self.state_fuel==1:
                print("une penurie de gaz  - ",end =" ")
            if sum==0:
                print("rien de grave",end =" ")
            print(" ")
            print(" ")
            """
            if sum ==1:
                self.times_1.append(t)
                self.prices_1.append(self.prix)
            if sum ==2:

                self.times_2.append(t)
                self.prices_2.append(self.prix)
            if sum ==3:

                self.times_3.append(t)
                self.prices_3.append(self.prix)
            if sum==0 :

                self.times_nothing.append(t)
                self.prices_nothing.append(self.prix)
            """
            plt.cla()
            self.time_values.append(t)
            plt.title("Prix de l'electricté sur le marché (en € TTC par kWh) au court du temps (en jours)")
            
            diff=len(self.time_values)-len(self.lst_prix)
            if diff!=0:
                if len(self.time_values)>len(self.lst_prix):
                    for i in range(diff):
                        self.time_values.pop()
                else:
                    for i in range(diff):
                        self.lst_prix.pop()
            plt.plot(self.time_values, self.lst_prix)
            

            """"plt.plot(self.times_nothing, self.prices_nothing,linewidth="0.4",marker='.',antialiased=True,linestyle='-',markersize="4",markeredgecolor="black",markerfacecolor="black",color='k')
            plt.plot(self.times_1, self.prices_1, linewidth="0.4",marker='.',antialiased=True,linestyle='-',markersize="4",markeredgecolor="yellow",markerfacecolor="yellow",color='k')
            plt.plot(self.times_2, self.prices_2, linewidth="0.4",marker='.',antialiased=True,linestyle='-',markersize="4",markeredgecolor="orange",markerfacecolor="orange",color='k')
            plt.plot(self.times_3, self.prices_3, linewidth="0.4",marker='.',antialiased=True,linestyle='-',markersize="4",markeredgecolor="red",markerfacecolor="red",color='k')
            """
            


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
        fig, ax = plt.subplots()
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
                        #print(len(self.temp))
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
                my_proba=random.randint(0,600)
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
    def __init__(self, id,choice):
        super().__init__()
        self.id = id
        self.production_rate = 0
        self.consumption_rate =0
        #self.nsPannSol = random.randint(1,10)
        self.nsPannSol = 5
        #self.tailleMaison = random.randint(1,10)
        self.tailleMaison = 5
        self.trade_policy = choice
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

                    self.production_rate=random.randint(0,300)
                    self.consumption_rate=random.randint(0,300)
                    self.surplus = self.production_rate - self.consumption_rate
                    #self.surplus = 1
                    self.shortage = self.consumption_rate - self.production_rate
                    #print("tem ",round(time.time()*1000),"maison: ",self.id," surplus: ",self.surplus)
                    if(self.surplus>=0):
                        match self.trade_policy:    
                            case "always_give":
                                msg=str(self.id)+";"+str(self.surplus)+";"+str(temp)
                                with lock2:
                                    mq_don.send(msg.encode())
                                self.send_message(str(self.id)+";"+"0"+";"+str(temp))
                                self.surplus=0
                            case "always_sell":
                                msg=str(self.id)+";"+str(self.surplus)+";"+str(temp)
                                self.send_message(msg)
                                self.surplus=0

                            case "sell_if_no_takers":
                                tt=""
                                with lock2:
                                    tt=mq_don.current_messages
                                if tt != 0:
                                    msg=str(self.id)+";"+str(self.surplus)+";"+str(temp)
                                    self.send_message(msg)
                                else:
                                    msg=str(self.id)+";"+str(self.surplus)+";"+str(temp)
                                    with lock2:
                                        mq_don.send(msg.encode())

                                self.surplus=0
                        
                            case _:
                                print("no match")
                    
                            
                    if(self.surplus<0):
                        tt=""
                        with lock2:
                            tt=mq_don.current_messages
                        
                        
                        if tt == 0:
                            msg=str(self.id)+";"+str(self.surplus)+";"+str(temp)
                            self.send_message(msg)
                            self.surplus=0                            
                        else:    
                            while self.surplus !=0:
                                print("cc")
                                with lock2:
                                    tt=mq_don.current_messages
                                print(tt)
                                if tt != 0:
                                    with lock2:
                                        (msg,_)=mq_don.receive()   
                                    print(self.id," NB_MSG ", tt)
                                    print(self.id," J'AI PRISSSSSSSS") 
                                    with lock2:
                                        tt=mq_don.current_messages
                                    print(self.id," NB_MSG ", tt)
                                    print(" ")
                                    string = msg.decode()
                                    quantite=eval(string.split(";")[1])
                                    donneur=string.split(";")[0]
                                    
                                    if(abs(self.surplus)<quantite):
                                        quantite=quantite-abs(self.surplus)
                                        self.surplus=0
                                        msg=donneur+";"+str(self.surplus)+";"+str(temp)
                                        with lock2:
                                            mq_don.send(msg.encode())
                                    else:
                                        self.surplus=self.surplus+quantite
                                else:
                                    break 
                            msg=str(self.id)+";"+str(self.surplus)+";"+str(temp)
                            self.send_message(msg)
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
    choice=['always_give', 'always_sell', 'sell_if_no_takers']
    choice=['always_sell', 'always_sell', 'always_sell']
    for i in range(num_homes):
        h=Home(i,choice[i%3])
        h.start()
        homes.append(h)

    return homes


def signal_handler(signal,frame):
    #print("EXIT")
    sys.exit(0)

if __name__ == '__main__':
    DT=1  #le plus petit interval de temps (ex : 1/2 = 30min, 1/6 = 10 min)
    signal.signal(signal.SIGINT,signal_handler)
    PORT=random.randint(10000,50000)
    ADDR_LOCAL="localhost"
    NB_HOME = 6
    prixStart=0.17

    consFlag = True
    producerCount = 2
    pcMutex = Lock()

    lock = threading.Lock()
    lock2 = multiprocessing.Lock()
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
        #print("Home {} has surplus: {} and shortage: {} pid: {}      {}        {}      {}".format(home.id, home.surplus, home.shortage, home.pid, home.nsPannSol, home.tailleMaison, home.trade_policy))
    #print("Market price is: {}".format(market_price

    Process_weather.join()
    Process_Market.join()

    

