import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import threading

prix = 170
lst_prix = []

def update(frame):
    global prix, lst_prix

    rapport = random.uniform(0,2)

    if rapport >= 1:
        prix = prix *1.02
    if rapport < 1 :
        prix = prix * 1/1.02

    prix = round(prix,3)
    lst_prix.append(prix)
    
    plt.cla()
    plt.plot(lst_prix)
    plt.yscale("log")

def run_graphique():
    fig = plt.figure()
    ani = animation.FuncAnimation(fig, update, frames=range(100), interval=0.000000000001, repeat=False)
    plt.show()

thread = threading.Thread(target=run_graphique)
thread.start()
