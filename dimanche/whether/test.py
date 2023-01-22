import numpy as np
import pylab as pl

import numpy as np

def simulate_temperature(mean:float, std:float, size:int):
    """
    Génère une série temporelle aléatoire suivant une distribution normale (loi de Gauss) pour simuler une température entre 0 et 30 degrés
    
    Parameters:
    mean (float) : la valeur moyenne de la température, elle doit être compris entre 0 et 30
    std (float) : l'écart-type de la température, il doit être suffisamment petit pour que la plupart des valeurs générées restent dans l'intervalle souhaité
    size (int) : nombre de valeurs à générer
    
    Returns:
    np.ndarray : Série temporelle générée
    """
    return np.random.normal(mean, std, size)


x = simulate_temperature(15,3,100)
print(x)
pl.plot(x)
pl.show()