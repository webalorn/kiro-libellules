tresh = 0

def nearest(in_data, iC):
    nbSites = len(in_data["sites"])

    iBest = 0
    best = in_data["siteClientDistances"][0][iC]

    for iS in range(nbSites):
        if in_data["siteClientDistances"][iS][iC] < best:
            iBest = iS

    return iBest

def clients_setup(in_data):
    nbSites = len(in_data["sites"])
    nbClients = len(in_data["clients"])

    out_clients = [0 for _ in range(nbClients)]

    for iC in range(nbClients):
        out_clients[iC] = nearest(in_data, iC)

    return out_clients

def gen_prod(out_clients):
    nbSites = len(in_data["sites"])
    nbClients = len(in_data["clients"])

    demand = [c[0] for c in in_data["clients"]]
    
    sites_demand = [0 for _ in range(nbSites)]

    for iC in range(nbClients):
        sites_demand[out_clients[iC]] += demand[iC]

    out_sites = [0 if k == 0 else (1 if k < thresh else 2) for k in sites_demand]

def gen_sol(out_clients, out_sites):
    nbSites = len(out_sites)
    out_prods = set()

    for iS in range(nbSites):
        if out_sites[iS] == 1 or out_sites[iS] == 2:
            out_prods.add(iS)
