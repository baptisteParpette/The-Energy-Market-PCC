import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

prix = 170
lst_prix = []

fig = plt.figure()
ax = fig.add_subplot(2,1,1)
ax.axis([0, 10, 0, 10])
ax2 = fig.add_subplot(2,1,2)

def update():
    global prix, lst_prix
    #demande = random.randint(1,10)
    #offre = random.randint(1,10)
    rapport = random.uniform(0,2)

    if rapport >= 1:
        prix = prix *1.02
    if rapport < 1 :
        prix = prix * 1/1.02

    formated ="{:.3f}".format(prix)
    lst_prix.append(prix)
    
    #plt.cla()
    #plt.plot(lst_prix)
    ax2.plot(lst_prix)

    ax.text(3, 5, "le prix de l'√©lectricit√©: "+formated+" KWh", style='italic',
        bbox={'facecolor': 'red', 'alpha': 1, 'pad': 10})


#ani = animation.FuncAnimation(fig, update, frames=range(1000), interval=0.000001, repeat=True)
for i in range(1000):
    #time.sleep(0.00000001)
    update()
    plt.pause(0.0000001)
    plt.cla()

#plt.show()
