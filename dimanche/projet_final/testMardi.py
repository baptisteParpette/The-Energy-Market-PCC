import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import time

# initialisation des données pour les deux graphiques
x = np.arange(100)
y1 = np.sin(x)
y2 = np.cos(x)

# création des figures pour les deux graphiques
fig, ax = plt.subplots(1, 2, figsize=(10,5))

# initialisation des graphiques
line1, = ax[0].plot(x, y1, color='blue', lw=2)
line2, = ax[1].plot(x, y2, color='red', lw=2)

# définition de la fonction d'animation
def animate(i):
    line1.set_ydata(np.sin(x + i/10.0))
    line2.set_ydata(np.cos(x + i/10.0))
    return line1, line2

# démarrage de l'animation
ani = animation.FuncAnimation(fig, animate, frames=100, interval=0.50, blit=True)

# affichage des graphiques
plt.show()
