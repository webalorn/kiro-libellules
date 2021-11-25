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
    parent = in_data['parent']
    sites = in_data['sites']

    for i_client, c in enumerate(in_data['clients']):
        dist_client2site.append([])
        for s, typ in enumerate(sol['sites']):
            cost = 0
            if typ != t_vide:
                cost += c[0] * cost_route_secondary * siteClientDistances[s][i_client]
                if typ != t_distrib:
                    cost += c[0] * cost_route_primary * siteSiteDistances[s][parent[s]])
                dists.append((cost, i_client, s))
                dist_client2site[-1].append((cost, s))
        dist_client2site[-1].sort()
    
    dists.sort()
    return dists, dist_client2site

def assign_linear(clients, dist_client2site, capacities, demands, parent, sites):
    total_cost = 0
    for i_client in range(len(clients)):
        if clients[i_client] == -1:
            all_costs = []
            for cost, s in dist_client2site[i_client]:
                s_parent = parent[s] if sites[s] == t_distrib else s
                cost += max(0, demands[i_client] - max(0, capacities[s_parent])) * cost_capacity_exceed
                all_costs.append((cost, s, s_parent))
            
            all_costs.sort()
            cost, s, s_parent = all_costs[0]
            clients[i_client] = s
            capacities[s_parent] -= demands[i_client]
            total_cost += cost

    return total_cost
            

def reasign_clients_from_low(in_data, sol):
    parent = in_data['parent']
    sites = in_data['sites']
    demands = [c[0] for c in in_data['clients']]

    dists, dist_client2site = get_clients_dists(in_data, sol)

    total_cost = 0
    clients = [-1 for c in sol['clients']]
    capacities = get_capacities(sol)

    for assign in dists:
        cost, i_client, s = assign
        s_parent = parent[s] if sites[s] == t_distrib else s
        if clients[i_client] != -1 or demands[i_client] > capacities[s_parent]:
            continue
        capacities[s_parent] -= demands[i_client]
        total_cost += cost
        clients[i_client] = s

    total_cost += assign_linear(clients, dist_client2site, capacities, demands, parent, sites)

    sol = copy(sol)
    sol['clients'] = clients
    return sol, total_cost