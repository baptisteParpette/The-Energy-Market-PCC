import random
import pylab as pl

def lst_price(t):
    lst =[]
    alpha = 0.001
    beta = 0.01
    gama = 0.99
    prix_elec = 0.1740
    for i in range(t):
        temp = random.randint(0,35)
        prix_elec = gama*prix_elec + alpha*(1/temp)
        lst += [prix_elec]
    return lst

absx = lst_price(10^6)

pl.plot(absx)
pl.show()