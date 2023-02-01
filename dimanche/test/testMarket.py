import random
import time
import pylab as pl

prix = 170


taux_max_journalier = 1.01
taux_max_mensuel = 1.1
taux_max_annuel = 1.3

NB_ANNEE = 10
CHANGEMENT_PAR_JOUR = 5
DIFF_ENTRE_PRIX = 1.008


lst_prix = []

t_avant = time.time()
 
lst_demande = []
lst_offre = []
lst_rapport = []



for i in range(360 * CHANGEMENT_PAR_JOUR * NB_ANNEE):
    demande = random.randint(1,10)
    offre = random.randint(1,10)
    lst_demande.append(demande)
    lst_offre.append(offre)
    rapport = round(demande / offre, 3)
    #rapport = round(demande - offre, 3)
    #rapport = random.uniform(0,2)
    #print(rapport)
    lst_rapport.append(rapport)
    if i% CHANGEMENT_PAR_JOUR == 0:
        prix_max_journalier = round(prix*taux_max_journalier,3)
        prix_min_journalier = round(prix*1/taux_max_journalier,3)

    if i%30*CHANGEMENT_PAR_JOUR == 0:
        prix_max_mensuel = round(prix*taux_max_mensuel,3)
        prix_min_mensuel = round(prix*1/taux_max_mensuel,3)

    if i%360*CHANGEMENT_PAR_JOUR == 0:
        prix_max_annuel = round(prix*taux_max_annuel,3)
        prix_min_annuel = round(prix*1/taux_max_annuel,3)
        print(prix_min_annuel, prix_max_annuel)

    #time.sleep(2)
    #print(rapport)
    if rapport > 1 and prix < prix_max_journalier and prix < prix_max_mensuel and prix < prix_max_annuel:
        prix = prix * DIFF_ENTRE_PRIX
    
    elif rapport < 1 and prix > prix_min_journalier and prix > prix_min_mensuel and prix > prix_min_annuel:
        prix = prix * 1/DIFF_ENTRE_PRIX
    else:
        continue

    prix = round(prix,3)
    lst_prix.append(prix)
    #print(prix,'\n')


t_apres = time.time()
t_exec = t_apres - t_avant
print("Le temps d'execution de la boucle est de : ",round(t_exec,3)," ms")
print("Le maximum des {} années est : {} €/MWh atteint en {}".format(NB_ANNEE, max(lst_prix), lst_prix.index(max(lst_prix))//(360*CHANGEMENT_PAR_JOUR)+2023))
print("Le minimum des {} années est : {} €/MWh atteint en {}".format(NB_ANNEE, min(lst_prix), lst_prix.index(min(lst_prix))//(360*CHANGEMENT_PAR_JOUR)+2023))

print("\nLe nbr d'éléments dans la liste demande: ",len(lst_demande), "la moyenne est de ", sum(lst_demande)/len(lst_demande))
print("\nLe nbr d'éléments dans la liste offre: ",len(lst_offre), "la moyenne est de ", sum(lst_offre)/len(lst_offre))
print("\nLe nbr d'éléments dans la liste rapport: ",len(lst_rapport), "la moyenne est de ", sum(lst_rapport)/len(lst_rapport))

pl.plot(lst_prix)
#pl.yscale("log")
pl.show()


#inclure l'inflation
