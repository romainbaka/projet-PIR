import math
from math import *
import numpy as np
import matplotlib.pyplot as plt
def S(r,rayon_noyau):
    if(r<=rayon_noyau):
        return 2E-12
    else:
        return 0

def calc_masse(masse,r,rayon_noyau,pas):
    return(masse+pas*4*pi*np.power(r,2)*densite(r,rayon_noyau))

def lambda_(R,rayon_noyau):
    conduc_ther_glace = 2.1
    conduc_ther_silicate = 0.22
    if (R<=rayon_noyau):
        return conduc_ther_silicate
    else:
        return conduc_ther_glace

def densite(R,rayon_noyau):
    masse_vol_glace = 1000
    masse_vol_silicate = 3700
    if (R<=rayon_noyau):
        return masse_vol_silicate
    else:
        return masse_vol_glace

def calc_P(p,g,pas):
    return (p+pas*g*densite(rayon,rayon_noyau))

def calc_Q(q,r,rayon_noyau,pas):
    if (r>rayon_noyau):
        return (q-pas*(-1*np.power(rayon_noyau/r,3))*densite(rayon_noyau,rayon_noyau)*S(rayon_noyau,rayon_noyau))
    else:
        return (q-densite(r,rayon_noyau)*S(r,rayon_noyau)/3)

def calc_T(T,r,Q,rayon_noyau):
    T+=pas*(Q/lambda_(r,rayon_noyau))
    return (T)

def calc_I(rayon,rayon_noyau):
    densite_lune = (densite(rayon_noyau,rayon_noyau)-densite(rayon,rayon_noyau))*np.power(rayon_noyau/rayon,3)+densite(rayon,rayon_noyau)
    I = (2/5)*(((densite(0,rayon_noyau)-densite(rayon,rayon_noyau))*np.power(rayon_noyau/rayon,5)/densite_lune)+densite(rayon,rayon_noyau)/densite_lune)
    return I

def calc_g(rayon,rayon_noyau,G,pas):
    r=0
    masse=0
    while (r<=rayon):
        masse += pas*4*pi*np.power(r,2)*densite(r,rayon_noyau)
        r += pas
    return (G*masse/np.power(rayon,2))

def affichage(tour,g,pression,chaleur,T,rayon):
    x = np.linspace(rayon,0,tour+1) 
    plt.plot (x,g)
    plt.xlabel("rayon")
    plt.ylabel("g")
    plt.show()
    plt.plot(x,pression)
    plt.xlabel("Rayon")
    plt.ylabel("pression")
    plt.show()
    plt.plot(x,chaleur)
    plt.xlabel("Rayon")
    plt.ylabel("chaleur")
    plt.show()
    plt.plot(x,T)
    plt.xlabel("Rayon")
    plt.ylabel("température")
    plt.show()

def calc_forme (masse,masse_lune,rayon_noyau):
    masse_vol_glace = 1000
    masse_vol_silicate = 3700
    delta_masse = masse-masse_lune
    delta_volume = (masse_vol_silicate-masse_vol_glace)*delta_masse
    nv_rayon = math.cbrt( np.power(rayon_noyau,3)+3/(4*pi)*delta_volume)
    return nv_rayon

def calc_forme_init(masse,rayon): 
    densite_glace = 0.917 #glace pure
    densite_silicate = 3.5#valeur a peut etre redeterminée suivant le noyau que l'on cherche a avoir 
    volume =4/3*pi*np.power(rayon,3)
    densite_lune = masse/(1000*volume)
    print("la densité de la lune est " + str(densite_lune))
    volume_noyau = volume*(densite_lune-densite_glace)/(densite_silicate-densite_glace)
    rayon_noyau = math.cbrt(volume_noyau*3/(4*pi))#!! si noyau metallique present on peut avoir un rayon de silicate > rayon de la lune ex io
    print("le rayon du noyau de la lune est " + str(rayon_noyau))
    return rayon_noyau,densite_lune

masse_lune = 1.4819E23
rayon_lune = 2631.2E3
moment_inertie = 0.3115
pression_surface = 0 
temperature_surface = 110
chaleur_surface = 0.002
pas = 1000.
G = 6.6743E-11
g_lune = masse_lune*G/np.power(rayon_lune,2)
tour_global = 0
masse = 0
I = 0
rayon_noyau,densite_lune = calc_forme_init(masse_lune,rayon_lune)
nb_iteration_max = 1
while ((tour_global==0 or abs(masse_lune-masse)>1E6)and(tour_global<nb_iteration_max)):
    tour_global += 1
    g = [G*masse_lune/np.power(rayon_lune,2)]
    pression = [pression_surface]
    T = [temperature_surface]
    chaleur = [chaleur_surface]
    masse = 0
    rayon = rayon_lune
    tour = 0
    while (rayon>2*pas):
        tour +=1
        rayon-=pas
        g.append(calc_g(rayon,rayon_noyau,G,pas))
        pression.append(calc_P(pression[-1],g[-1],pas))
        chaleur.append(calc_Q(chaleur[-1],rayon,rayon_noyau,pas))
        T.append(calc_T(T[-1],rayon,chaleur[-1],rayon_noyau))
        masse += calc_masse(masse,rayon,rayon_noyau,pas)
    print("I = {}".format(calc_I(rayon_lune,rayon_noyau)))
    #rayon_noyau = calc_forme(masse,masse_lune,rayon_noyau) marche pas encore

affichage(tour,g,pression,chaleur,T,rayon_lune)

# while (rayon>rayon_noyau):#1ere couche
#     tour +=1
#     rayon-=pas
#     g.append(g[-1]-pas*(4*pi*G*masse_vol_glace-2*g[-1]/rayon))
    
#     pression.append(pression[-1]+pas*g[-1]*masse_vol_glace)
#     if (tour%10==0):
#         fichier.write("{}\t{}\t{}\n".format(rayon,pression[-1],g[-1]))
# while (rayon>=pas):#2eme couche
#     tour +=1
#     rayon=rayon-pas
#     g.append(g[-1]-pas*(4*pi*G*masse_vol_silicate-2*g[-1]/rayon))
#     pression.append(pression[-1]+pas*g[-1]*masse_vol_silicate)
#     if (tour%10==0):
#         fichier.write("{}\t{}\t{}\n".format(rayon,pression[-1],g[-1]))