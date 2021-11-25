from util import *
import random

def recup_fils(parent,p):
    fils = []
    for i in range(len(parent)):
        if parent[i] == p:
            fils.append(i)
    return fils

def echange_prod_fils(f,p,parent):
    for i in range(parent):
        if parent[i] == p:
            parent[i] = f
    parent[p] = parent[f]

    return parent

def echange_try(in_data,sol):
    parent = sol['parent']
    sites = sol['sites']


    n = random.randint(0,len(parent)-1)
    while sites[n] != 1 or sites[n] != 2:
        n = random.randint(0,len(parent)-1)

    fils = recup_fils(parent,n)
    indice_f = random.randint(0,len(fils))

    f = fils[indice_f]
    parent = echange_prod_fils(f,n,parent)

    if sites[n] == 1:
        sites[f] = 1
    elif sites[n] ==2:
        sites[f] = 2
    
    sites[n] = 3

    sol['sites'] = sites
    sol['parent'] = parent

    return sol


