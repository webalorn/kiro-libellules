from math import inf
import random

thresh = 300000

t_vide = 0
t_prod = 1
t_auto = 2
t_distrib = 3

max_cap = 2500000

def nearest(in_data, iC):
    nbSites = len(in_data["sites"])


def clients_setup(in_data):
    nbSites = len(in_data["sites"])
    nbClients = len(in_data["clients"])

    demand = [c[0] for c in in_data["clients"]]
    
    sites_capacity = [max_cap for _ in range(nbSites)]

    out_clients = [0 for _ in range(nbClients)]

    l = list(range(nbClients))
    random.shuffle(l)
    for iC in l:
        iBest = 0
        best = inf

        for iS in range(nbSites):
            if in_data["siteClientDistances"][iS][iC] < best and sites_capacity[iS] >= demand[iC]:
                iBest = iS

        out_clients[iC] = iBest
        sites_capacity[out_clients[iC]] -= demand[iC]

    return out_clients

def gen_prod(in_data, out_clients):
    nbSites = len(in_data["sites"])
    nbClients = len(in_data["clients"])

    demand = [c[0] for c in in_data["clients"]]
    
    sites_demand = [0 for _ in range(nbSites)]

    for iC in range(nbClients):
        sites_demand[out_clients[iC]] += demand[iC]

    out_sites = [0 if k == 0 else (1 if k < thresh else 2) for k in sites_demand]

    return out_sites

def gen_sol(out_clients, out_sites, out_parents):
    return {"sites": out_sites, "clients": out_clients, "parent": out_parents}

def stupid(in_data):
    nbSites = len(in_data["sites"])

    cli = clients_setup(in_data)
    sit = gen_prod(in_data, cli)
    par = [0 for _ in range(nbSites)]

    return gen_sol(cli, sit, par)



