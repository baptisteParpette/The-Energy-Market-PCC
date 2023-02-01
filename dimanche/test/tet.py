import random
import time
import pylab as pl


prix = 170
lst_prix = []

for i in range(1000):
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

pl.plot(lst_prix)
pl.yscale("log")
pl.show()






