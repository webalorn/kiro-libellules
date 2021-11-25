from util import *
# def reassign_clients(in_data, sol):
    


# def reassign(in_data, sol):
#     reassign_clients(in_data, sol)
#     reassign_distrib_centers(in_data, sol)

def get_clients_dists(in_data, sol):
    dists = []
    dist_client2site = []
    siteSiteDistances = in_data['siteSiteDistances']
    siteClientDistances = in_data['siteClientDistances']
    parent = sol['parent']
    out_sites = sol['sites']

    for i_client, c in enumerate(in_data['clients']):
        dist_client2site.append([])
        for s, typ in enumerate(out_sites):
            cost = 0
            if typ != t_vide:
                s_prod = s
                cost += c[0] * cost_route_secondary * siteClientDistances[s][i_client]
                if typ == t_distrib:
                    s_prod = parent[s]
                    cost += c[0] * cost_route_primary * siteSiteDistances[s][s_prod]
                if out_sites[s_prod] == t_prod:
                    cost += c[0] * 3.4
                dists.append((cost, i_client, s))
                dist_client2site[-1].append((cost, s))
        dist_client2site[-1].sort()
    
    dists.sort()
    return dists, dist_client2site

def assign_linear(clients, dist_client2site, capacities, demands, parent, out_sites, clients_order=None):
    total_cost = 0
    if clients_order is None:
        clients_order = list(range(len(clients)))
        shuffle(clients_order)
    for i_client in clients_order:
        if clients[i_client] == -1:
            all_costs = []
            for cost, s in dist_client2site[i_client]:
                s_parent = parent[s] if out_sites[s] == t_distrib else s
                cost += max(0, demands[i_client] - max(0, capacities[s_parent])) * cost_capacity_exceed
                all_costs.append((cost, s, s_parent))
            
            all_costs.sort()
            cost, s, s_parent = all_costs[0]
            clients[i_client] = s
            capacities[s_parent] -= demands[i_client]
            total_cost += cost

    return total_cost
            

def reasign_clients_from_low(in_data, sol):
    sol = deepcopy(sol)
    parent = sol['parent']
    out_sites = sol['sites']
    demands = [c[0] for c in in_data['clients']]

    dists, dist_client2site = get_clients_dists(in_data, sol)

    total_cost = 0
    clients = [-1 for c in sol['clients']]
    capacities = get_capacities(sol)

    for assign in dists:
        cost, i_client, s = assign
        s_parent = parent[s] if out_sites[s] == t_distrib else s
        if clients[i_client] != -1 or demands[i_client] > capacities[s_parent]:
            continue
        capacities[s_parent] -= demands[i_client]
        total_cost += cost
        clients[i_client] = s

    total_cost += assign_linear(clients, dist_client2site, capacities, demands, parent, out_sites)

    sol['clients'] = clients
    return sol, total_cost


def reasign_clients_random(in_data, sol):
    sol = deepcopy(sol)
    parent = sol['parent']
    out_sites = sol['sites']
    demands = [c[0] for c in in_data['clients']]

    dists, dist_client2site = get_clients_dists(in_data, sol)

    clients = [-1 for c in sol['clients']]
    capacities = get_capacities(sol)
    clients_order = list(range(len(clients)))
    shuffle(clients_order)

    total_cost = assign_linear(clients, dist_client2site, capacities, demands, parent, out_sites, clients_order=clients_order)

    sol['clients'] = clients
    return sol, total_cost

def reasign_best(in_data, sol, max_random=10):
    sol_min, cost_min = reasign_clients_from_low(in_data, sol)
    cost_min = eval_sol(in_data, sol_min)

    for _ in range(max_random):
        sol, cost = reasign_clients_random(in_data, sol)
        cost = eval_sol(in_data, sol)
        if cost < cost_min:
            # print("Better sol random")
            sol_min, cost_min = sol, cost
    return sol_min