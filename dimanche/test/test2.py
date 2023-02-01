import random
import time
import pylab as pl
import matplotlib.pyplot as plt
import matplotlib.animation as animation


prix = 170
lst_prix = []

for i in range(3000000):
    demande = random.randint(1,10)
    offre = random.randint(1,10)
    #rapport = round(demande / offre, 3)
    rapport = random.uniform(0,2)
    #print(rapport)

    #time.sleep(2)
    #print(rapport)
    if rapport >= 1:
        prix = prix *1.02
    
    if rapport < 1 :
        prix = prix * 1/1.02

    prix = round(prix,3)
    lst_prix.append(prix)
    #print(prix,'\n')

#pl.plot(lst_prix)
#pl.yscale("log")
#pl.show()


def update(frame):
    plt.cla()
    time.sleep(1)
    plt.plot(random.sample(range(100), 10))

fig = plt.figure()
#ani = animation.FuncAnimation(fig, update, frames=range(10), repeat=False)
ani = animation.FuncAnimation(fig, update, frames=range(1000), interval=500, repeat=True, repeat_delay=1000)

plt.show()





