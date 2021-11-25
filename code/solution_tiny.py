from util import *

def perm(longueur,l_all,previous,valable):
    if len(previous) == longueur:
        if valable:
            l_all.append(previous)
        return l_all

    for i in range(4):
        prod = False
        if i == 1 or i == 2:
            prod = True
        act = previous + [i]
        l_all = perm(longueur,l_all,act,(valable or prod))


    return l_all
    
def generate_all_plants(sites):
    nb_sites = len(sites)
    return perm(nb_sites,[],[],False)

def processing_plants(sites):
    prods = set()
    distrib = set()
    for i in range(len(sites)):
        if sites[i] == 1 or sites[i] == 2:
            prods.add(i)
        elif sites[i] == 3:
            distrib.add(i)
    
    return prods,distrib


def assign_parents(prods,distrib,parents,indice,possible):
    if indice >= len(parents):
        possible.append(parents)
        return possible
    
    if indice in distrib:
        for x in prods:
            p = parents[::]
            p[indice] = x
            possible = assign_parents(prods,distrib,p,indice+1,possible)

    else:
        possible = assign_parents(prods,distrib,parents,indice+1,possible)
    
    return possible

def assign_all_perm_parents(sites):
    l_all_perm = generate_all_plants(sites)
    all_parents = []
    for perm in l_all_perm:
        prods,distrib = processing_plants(perm)
        l = assign_parents(prods,distrib,[-1]*len(sites),0,[])
        all_parents.append(l)

    return prods,distrib,l_all_perm,all_parents

def all_possible_soluce(in_data):
    all_soluce = []
    p,d,l1,l2 = assign_all_perm_parents(in_data['sites'])
    for i in range(len(l1)):
        for x in l2[i]:
            out = generate_empty_solution(in_data)
            out['sites'] = l1[i]
            out['parent'] = x
            out['prods'] = p
            out['distribs'] = d
            all_soluce.append(out)
    return all_soluce






