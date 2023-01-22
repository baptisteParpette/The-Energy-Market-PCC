import multiprocessing
import numpy as np

# Définir la température moyenne et l'écart-type pour simuler une température entre -10 et 35 degrés
mean = 15
std = 5

# Définir la taille de la série temporelle
size = 1000

# Créer une mémoire partagée pour stocker la température
temperature_shared_memory = multiprocessing.Array('f', size)

def weather_process(shared_memory):
    """
    Processus pour simuler la température
    """
    while True:
        # Générer une nouvelle série temporelle
        temperature = np.random.normal(mean, std, size)

        # Mettre à jour la mémoire partagée avec la nouvelle série temporelle
        for i in range(size):
            shared_memory[i] = temperature[i]

# Créer le processus pour simuler la température
weather_process = multiprocessing.Process(target=weather_process, args=(temperature_shared_memory,))

# Lancer le processus
weather_process.start()

# Utiliser la mémoire partagée pour accéder à la température
# par exemple pour afficher la température actuelle
while True:
    current_temperature = temperature_shared_memory[-1]
    print(f'Current temperature: {current_temperature}')
