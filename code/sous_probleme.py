from stupid import * 
from util import *

capacity_base = 1250000
capacity_auto_bonus = 1250000

def quantite_sites(in_data,sol):
    parents = sol['parent']
    clients_pere = sol['clients']
    clients = in_data['clients']

    quantite = [0]*(len(parents))

    for i in range(len(clients)):
        pere = clients_pere[i]
        prod_init = parents[pere]
        quantite[prod_init] += client[i][0]

    return quantite


def sous_probleme(in_data,x_debut,x_fin,y_debut,y_fin,sol):
    quantite = quantite_sites(in_data,sol)

    pere = sol['parents']
    sites_typ = sol['sites']

    site_zone = []
    sites = in_data['sites']
    distance_site = []

    milieu_x = abs(x_fin-x_debut)/2 + x_debut 
    milieu_y = abs(y_fin-y_debut)/2 + y_debut


    for i in range(len(sites)):
        x = sites[i][0]
        y = sites[i][1]
        if x >= x_debut and x <= x_fin and y >= y_debut and y <= y_fin:
            d = (x-milieu_x)**2 + (y-milieu_y)**2
            distance_site.append((d,i,quantite[i]))

    distance_site.sort()

    site_prod = 0
    assignation = [0]*(len(distance_site))

    for i in range(len(distance_site)):
        d,indice,q = distance_site[i]
        q_init = distance_site[site_prod][2] 
        if q+q_init > capacity_base:
            assignation[site_prod] -= 1
            site_prod += 1
            q_init = distance_site[site_prod][2]
        else:
            q_init += q

        assignation[site_prod] += 1
    
    nb_assign = 0
    site_prod = 0
    for i in range(len(distance_site)):
        indice_prod = distance_site[site_prod][1]
        indice = distance_site[i][1]
        if i <= site_prod:
            sites_typ[indice] = 1
        elif sites_typ[indice] != 0:
            sites_typ[indice] = 3
            if nb_assign > assignation[site_prod]:
                site_prod += 1
                nb_assign = 0
            pere[indice] = indice_prod
            nb_assign += 1
    
    sol['parents'] = pere
    sol['site'] = sites_typ
    return sol


