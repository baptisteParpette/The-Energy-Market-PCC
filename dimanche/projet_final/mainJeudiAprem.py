import random
import multiprocessing
import time
import math
from numpy import random
import os, signal
import sysv_ipc
import socket
import select
import concurrent.futures


class Weather(multiprocessing.Process):
    def __init__(self,shared):
        super().__init__()
        self.shared=shared

    def run(self):
        t=0.0
        dt=1/6 #heure
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
        signal.signal(signal.SIGUSR1, self.war)
        signal.signal(signal.SIGUSR2, self.natural)
        signal.signal(signal.SIGALRM, self.fuel)

    def socket_handler(self, s, a):
        global serve
        with s:
            print("Connected to client: ", a)
            data = s.recv(1024)
            while len(data):
                #print("Le market à reçu ",data.decode())
                with lock:
                    self.data.append(data.decode())
                #TRAITER LA DATA
                data = s.recv(1024)
            print("Disconnecting from client: ", a)

    def run(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers = NB_HOME) as executor:
            while self.serve:
                readable, writable, error = select.select([self.server_socket], [], [], 1)
                if self.server_socket in readable:
                    client_socket, address = self.server_socket.accept()
                    executor.submit(self.socket_handler, client_socket, address)
                with lock:
                    print("debut: ",self.data)                            
                    if(self.data!=[]):
                        firstElem=self.data[0].split(';')
                        tempo = firstElem[2]
                        #print(tempo)
                        lst = []
                        #print("HEYYYYYY on va faire la boucle")
                        #print(len(self.data))
                        for a in range(len(self.data)):
                            #print("Ca y est on y est pourquoi tu me copies")
                            #print("self;data = ",self.data)
                            element = self.data[a]
                            #print(element.split(';')[2])
                            #print("l'élément est ", element)
                            if element.split(';')[2]==tempo:
                                #print("ccccccccccc")
                                #print(element.split(';')[1])

                                lst.append(element)
                                #lst.append("JEsuisdanslalisteetjaimepaslesespaces(vectoriel)")
                        """taille=len(self.data)
                        for a in range(taille):
                            element = self.data[a]
                            if element.split(';')[2]==tempo:
                                del self.data[a]
                                taille = len(self.data)"""

                        for elem in lst:
                            self.data.remove(elem)
                            a=1

                        print("La liste lst est: ",lst)                            
                        print("fin: ",self.data)                            

            #print("coucoucoucouc")
            #with lock:
             #   print("DANS MARKET",transaction)
              #  if transaction!=[]:
               #     for trans in transaction:
                #        print("DANS MARKET TRANS",trans)
                 #       transaction.remove(trans)

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
        temp=shared_memory[1]
        while True:
            while temp!=shared_memory[1]:
                temp=shared_memory[1]
                my_proba=random.randint(9,100)
                #print(shared_memory[0],my_proba)
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

class Home(multiprocessing.Process):
    def __init__(self, id):
        super().__init__()
        self.id = id
        self.production_rate = 0
        self.consumption_rate =0
        self.nsPannSol = random.randint(0,10)
        self.tailleMaison = random.randint(1,4)
        #self.trade_policy = random.choice(['always_give', 'always_sell', 'sell_if_no_takers'])
        self.trade_policy = 'always_sell'
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

                #VIDER LE QUEUE DON

                self.production_rate=self.nsPannSol*random.randint(0,5)
                self.consumption_rate=self.tailleMaison*random.randint(0,5)
                self.surplus = self.production_rate - self.consumption_rate
                self.shortage = self.consumption_rate - self.production_rate
                #print("tem ",round(time.time()*1000),"maison: ",self.id," surplus: ",self.surplus)

                if(self.surplus>0):
                    match self.trade_policy:    
                        case "always_give":
                            #print("tem ",round(time.time()*1000),"maison: ",self.id,"don")
                            msg=str(self.id)+";"+str(self.surplus)#1;30 (La maison 1 à un surplus de 30 à donner)
                            mq_don.send(msg.encode())
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
                                #print("tem ",round(time.time()*1000),"maison: ",self.id," message: ",msg.decode())

                            self.surplus=0
                    
                        case _:
                            a=1
                            #print("no match")
                        
                if(self.surplus<0):
                    if mq_don.current_messages == 0:
                        #
                        #print("tem ",round(time.time()*1000),"maison: ",self.id,"Achat marché")
                        msg=str(self.id)+";"+str(self.surplus)+";"+str(temp)
                        self.send_message(msg)
                        self.surplus=0
                    else:
                        while self.surplus !=0:
                            if mq_don.current_messages == 0:
                                #print("tem ",round(time.time()*1000),"maison: ",self.id,"Achat marché COUCOU")
                                msg=str(self.id)+";"+str(self.surplus)+";"+str(temp)
                                self.send_message(msg)
                                self.surplus=0
                                
                            else:
                                (msg,_)=mq_don.receive()
                                string = msg.decode()
                                quantite=int(string.split(";")[1])
                                donneur=string.split(";")[0]
                                if(abs(self.surplus)<quantite):
                                    quantite=quantite-abs(self.surplus)
                                    self.surplus=0
                                    msg=donneur+";"+str(quantite)
                                    mq_don.send(msg.encode())
                                    print("COUCOU")
                                else:
                                    self.surplus=self.surplus+quantite
                                    print("ELSE COUCOU")

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
    NB_HOME = 4

    lock = multiprocessing.Lock()

    shared_memory = multiprocessing.Array('d', range(2))
    


    mq_don=sysv_ipc.MessageQueue(666,sysv_ipc.IPC_CREAT)
    mq_need=sysv_ipc.MessageQueue(777,sysv_ipc.IPC_CREAT)

    mq_don.remove()
    mq_need.remove()
    
    mq_don=sysv_ipc.MessageQueue(666,sysv_ipc.IPC_CREAT)
    mq_need=sysv_ipc.MessageQueue(777,sysv_ipc.IPC_CREAT)

    Process_weather = Weather(shared_memory)
    Process_weather.start()

    Process_Market = Market(shared_memory)
    Process_Market.start()

    #External process creation
    Process_Market.create_child()


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

