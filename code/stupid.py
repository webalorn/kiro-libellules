from math import inf
import random
import util

thresh = 300000

t_vide = 0
t_prod = 1
t_auto = 2
t_distrib = 3

max_cap = 2500000


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
                best = in_data["siteClientDistances"][iS][iC]

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

    out_sites = [t_vide if k == 0 else (t_prod if k < thresh else t_auto) for k in sites_demand]

    return out_sites

def gen_sol(out_clients, out_sites, out_parents):
    return {"sites": out_sites, "clients": out_clients, "parent": out_parents}

def merge(in_data, clients, sites, parents):
    nbSites = len(in_data["sites"])
    nbClients = len(in_data["clients"])

    sites_demand = [0 for _ in range(nbSites)]

    demand = [c[0] for c in in_data["clients"]]
    
    for iC in range(nbClients):
        src = clients[iC]
        if sites[src] == t_distrib:
            src = parents[src]
        sites_demand[src] += demand[iC]

    aBest = 0
    bBest = 1

    while aBest!=bBest:
        aBest = 0
        bBest = 0

        best = util.eval_sol(in_data, gen_sol(clients, sites, parents))
        best_clients = clients
        best_sites = sites
        best_parents = parents

        for a in range(nbSites):
            for b in range(nbSites):
                if a==b: continue
                if sites[a] not in [t_prod, t_auto] or sites[b] not in [t_prod, t_auto]: continue
                if sites_demand[a]+sites_demand[b] > max_cap: continue
                
                var_clients = clients.copy() #[a if k==b else k for k in clients]
                var_sites = sites.copy()
                var_sites[b] = t_distrib
                var_parents = [a if k==b else k for k in parents]
                var_parents[b] = a
                var_sites_demand = sites_demand.copy()
                var_sites_demand[a] += var_sites_demand[b]
                var_sites_demand[b] = 0

                if var_sites_demand[a] > thresh:
                    var_sites[a] = t_auto

                val = util.eval_sol(in_data, gen_sol(var_clients, var_sites, var_parents))

                if val < best:
                    aBest = a
                    bBest = b
                    best = val

                    best_clients = var_clients
                    best_sites = var_sites
                    best_parents = var_parents
                    best_sites_demand = var_sites_demand

        if aBest!=bBest:
            clients = best_clients
            sites = best_sites
            parents = best_parents
            sites_demand = best_sites_demand

    return gen_sol(clients, sites, parents)

def merge2(in_data, clients, sites, parents):
    nbSites = len(in_data["sites"])
    nbClients = len(in_data["clients"])

    sites_demand = [0 for _ in range(nbSites)]

    demand = [c[0] for c in in_data["clients"]]
    
    for iC in range(nbClients):
        src = clients[iC]
        if sites[src] == t_distrib:
            src = parents[src]
        sites_demand[src] += demand[iC]

    aBest = 0
    bBest = 1

    while aBest!=bBest:
        aBest = 0
        bBest = 0

        best = util.eval_sol(in_data, gen_sol(clients, sites, parents))
        best_clients = clients
        best_sites = sites
        best_parents = parents

        for a in range(nbSites):
            for b in range(nbSites):
                if a==b: continue
                if sites[a] not in [t_prod, t_auto] or sites[b] not in [t_prod, t_auto]: continue
                if sites_demand[a]+sites_demand[b] > max_cap: continue
                
                var_clients = clients
                var_sites = sites.copy()
                var_sites[b] = t_distrib
                var_parents = parents.copy()
                var_parents[b] = a
                var_sites_demand = sites_demand.copy()
                var_sites_demand[a] += var_sites_demand[b]
                var_sites_demand[b] = 0

                if var_sites_demand[a] > thresh:
                    var_sites[a] = t_auto

                val = util.eval_sol(in_data, gen_sol(var_clients, var_sites, var_parents))*(1+0.01*(0.5-random.random()))

                if val < best:
                    aBest = a
                    bBest = b
                    best = val

                    best_clients = var_clients
                    best_sites = var_sites
                    best_parents = var_parents
                    best_sites_demand = var_sites_demand

        if aBest!=bBest:
            clients = best_clients
            sites = best_sites
            parents = best_parents
            sites_demand = best_sites_demand

    return gen_sol(clients, sites, parents)



def stupid(in_data):
    nbSites = len(in_data["sites"])

    cli = clients_setup(in_data)
    sit = gen_prod(in_data, cli)
    par = [0 for _ in range(nbSites)]

    return gen_sol(cli, sit, par)

def stupid2(in_data):
    nbSites = len(in_data["sites"])

    cli = clients_setup(in_data)
    sit = gen_prod(in_data, cli)
    par = [0 for _ in range(nbSites)]

    return merge(in_data, cli, sit, par)

def stupid3(in_data):
    nbSites = len(in_data["sites"])

    cli = clients_setup(in_data)
    sit = gen_prod(in_data, cli)
    par = [0 for _ in range(nbSites)]

    return merge(in_data, cli, sit, par)
