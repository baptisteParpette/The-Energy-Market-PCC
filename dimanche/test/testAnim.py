import random
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation





NB_ANNEE = 10
CHANGEMENT_PAR_JOUR = 10


GUERRE = 0 


t_avant = time.time()

for j in range(1):
    lst_prix = []
    prix = 170
    taux_max_journalier = 1.01
    taux_max_mensuel = 1.05
    taux_max_annuel = 1.1
    DIFF_ENTRE_PRIX = 1.01
    COLOR = "blue"

    prix_max_annuel = round(prix*taux_max_annuel,3)
    prix_min_annuel = round(prix*1/taux_max_annuel,3)
    prix_max_mensuel = round(prix*taux_max_mensuel,3)
    prix_min_mensuel = round(prix*1/taux_max_mensuel,3)
    prix_max_journalier = round(prix*taux_max_journalier,3)
    prix_min_journalier = round(prix*1/taux_max_journalier,3)

    if random.randint(0,4*360 * CHANGEMENT_PAR_JOUR * NB_ANNEE) == GUERRE:
        DIFF_ENTRE_PRIX = 1.03
        COLOR = 'green'
        taux_max_journalier = 1.03
        taux_max_mensuel = 1.2
        taux_max_annuel = 1.5
    
    def update(i):
        print(i)
        global prix, lst_prix
        #demande = random.randint(1,10)
        #offre = random.randint(1,10)
        #rapport = round(demande / offre, 3)
        rapport = random.uniform(0,2)
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
            #print(prix_min_annuel, prix_max_annuel)

        #time.sleep(2)
        #print(rapport)
        if rapport >= 1 and prix < prix_max_journalier and prix < prix_max_mensuel and prix < prix_max_annuel:
            prix = prix * DIFF_ENTRE_PRIX
        
        if rapport < 1 and prix > prix_min_journalier and prix > prix_min_mensuel and prix > prix_min_annuel:
            prix = prix * 1/DIFF_ENTRE_PRIX

        prix = round(prix,3)
        lst_prix.append(prix)
        plt.cla()
        plt.plot(lst_prix)

    fr = range(360 * CHANGEMENT_PAR_JOUR * NB_ANNEE)
    fig = plt.figure()
    ani = animation.FuncAnimation(fig, update, frames=range(100), interval=0.000001, repeat=False)
    plt.show()
    
    #max_val = max(lst_prix)
    #indice_max_val = lst_prix.index(max_val)
    #min_val = min(lst_prix)
    #indice_min_val = lst_prix.index(min_val)
    #plt.subplot(2,4,j+1)
    #plt.title("Simulation"+str(j+1))
    #plt.ylim(50,500) 
    #plt.plot(lst_prix, COLOR)
    #plt.plot(indice_max_val, max_val, 'or')
    #plt.plot(indice_min_val, min_val, 'ok')
    


t_apres = time.time()
t_exec = t_apres - t_avant
print("Le temps d'execution de la boucle est de : ",round(t_exec,3)," ms")
#print("Le maximum des {} années est : {} €/MWh atteint en {}".format(NB_ANNEE, max(lst_prix), lst_prix.index(max(lst_prix))//(360*CHANGEMENT_PAR_JOUR)+2023))
#print("Le minimum des {} années est : {} €/MWh atteint en {}".format(NB_ANNEE, min(lst_prix), lst_prix.index(min(lst_prix))//(360*CHANGEMENT_PAR_JOUR)+2023))



#plt.plot(lst_prix)
#plt.yscale("log")
#plt.show()


#inclure l'inflation
