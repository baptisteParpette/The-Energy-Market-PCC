import random
import time
import pylab as pl
import matplotlib.pyplot as plt






NB_ANNEE = 10
CHANGEMENT_PAR_JOUR = 10


GUERRE = 0 


t_avant = time.time()

for j in range(8):
    lst_prix = []
    prix = 170
    taux_max_journalier = 1.01
    taux_max_mensuel = 1.02
    taux_max_annuel = 1.1
    AUGMENTATION = 1.001
    DIMINUTION = 1.001
    COLOR = "blue"
    liste_guerre = []
    for i in range(360 * CHANGEMENT_PAR_JOUR * NB_ANNEE):
        if random.randint(0,3*360 * CHANGEMENT_PAR_JOUR * NB_ANNEE) == GUERRE:
            AUGMENTATION = 1.005
            DIMINUTION = 1.005
            COLOR = 'green'
            liste_guerre.append(i)
            taux_max_journalier = 1.03
            taux_max_mensuel = 1.2
            taux_max_annuel = 1.5
        demande = random.randint(1,10)
        offre = random.randint(1,10)
        rapport = round(demande / offre, 3)
        #rapport = random.uniform(0,2)
        #print(rapport)
        if i% CHANGEMENT_PAR_JOUR == 0:
            prix_max_journalier = round(prix*taux_max_journalier,3)
            prix_min_journalier = round(prix*1/taux_max_journalier,3)

        if i%30*CHANGEMENT_PAR_JOUR == 0:
            prix_max_mensuel = round(prix*taux_max_mensuel,3)
            prix_min_mensuel = round(prix*1/taux_max_mensuel,3)

        if i%360*CHANGEMENT_PAR_JOUR == 0:
            prix_max_annuel = round(prix*taux_max_annuel,3)
            prix_min_annuel = round(prix*1/taux_max_annuel,3)
            AUGMENTATION += 0.0000005

        #time.sleep(2)
        #print(rapport)
        if rapport > 1 and prix < prix_max_journalier and prix < prix_max_mensuel and prix < prix_max_annuel:
            prix = prix * AUGMENTATION
        elif rapport < 1 and prix > prix_min_journalier and prix > prix_min_mensuel and prix > prix_min_annuel:
            prix = prix * 1/DIMINUTION
        else:
            continue


        prix = round(prix,3)
        lst_prix.append(prix)
        #print(prix,'\n')
    
    max_val = max(lst_prix)
    indice_max_val = lst_prix.index(max_val)
    min_val = min(lst_prix)
    indice_min_val = lst_prix.index(min_val)
    pl.subplot(2,4,j+1)
    pl.title("Simulation"+str(j+1))
    pl.ylim(50,600) 
    pl.plot(lst_prix, COLOR)
    pl.plot(indice_max_val, max_val, 'or')
    pl.plot(indice_min_val, min_val, 'ok')

    for pt in liste_guerre:
        plt.axvline(x=pt, color='purple', linestyle='--')

    


t_apres = time.time()
t_exec = t_apres - t_avant
print("Le temps d'execution de la boucle est de : ",round(t_exec,3)," ms")
#print("Le maximum des {} années est : {} €/MWh atteint en {}".format(NB_ANNEE, max(lst_prix), lst_prix.index(max(lst_prix))//(360*CHANGEMENT_PAR_JOUR)+2023))
#print("Le minimum des {} années est : {} €/MWh atteint en {}".format(NB_ANNEE, min(lst_prix), lst_prix.index(min(lst_prix))//(360*CHANGEMENT_PAR_JOUR)+2023))



#pl.plot(lst_prix)
#pl.yscale("log")
pl.show()


#inclure l'inflation
