import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import time

def update(frame):
    plt.cla()
    time.sleep(1)
    plt.plot(random.sample(range(100), 10))

fig = plt.figure()
#ani = animation.FuncAnimation(fig, update, frames=range(10), repeat=False)
ani = animation.FuncAnimation(fig, update, frames=range(10), interval=500, repeat=True, repeat_delay=1000)

plt.show()
