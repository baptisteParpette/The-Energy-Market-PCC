import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

prix = 170
lst_prix = []

fig, (ax1, ax2) = plt.subplots(2, 1)

def update(i):
    global prix, lst_prix
    rapport = random.uniform(0,2)

    if rapport >= 1:
        prix = prix *1.02
    if rapport < 1 :
        prix = prix * 1/1.02

    formated ="{:.3f}".format(prix)
    lst_prix.append(prix)
    
    ax2.clear()
    ax2.plot(lst_prix)

    ax1.text(3, 5, "le prix de l'électricité: "+formated+" KWh", style='italic',
        bbox={'facecolor': 'red', 'alpha': 1, 'pad': 10})

ani = animation.FuncAnimation(fig, update, frames=range(1000), interval=0.1)
plt.show()
