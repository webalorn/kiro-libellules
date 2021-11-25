from util import *
from reassign import *

def get_best_sol(in_data, sol, val_sol=None, new_sol=None):
    new_sol = reasign_best(in_data, new_sol if new_sol else sol)
    if val_sol is None:
        val_sol = eval_sol(in_data, sol)
    new_val = eval_sol(in_data, new_sol)

    if new_val < val_sol:
        val_sol, sol = new_val, new_sol
        output_sol_if_better(in_data['name'], sol, sol_val=val_sol)
    return sol, val_sol

def try_assign_distrib(in_data, sol, to_assign):
    sol['clients'] = reasign_best(in_data, sol)['clients']
    val_sol = None
    shuffle(to_assign)
    sites = sol['sites']
    for s in to_assign:
        for s_parent in range(len(sites)):
            if sites[s_parent] != t_auto and sites[s_parent] != t_prod:
                continue
            new_sol = deepcopy(sol)
            new_sol['sites'][s] = t_distrib
            new_sol['parent'][s] = s_parent
            sol, val_sol = get_best_sol(in_data, sol, val_sol=val_sol, new_sol=new_sol)
    return sol
        

def try_change_typ(in_data, sol, s, s_new_typ):
    typ = sol['sites'][s]
    sites = sol['sites']
    parent = sol['parent']
    sites[s] = s_new_typ

    if s_new_typ == typ and typ != t_distrib:
        return False
    
    if s_new_typ == t_vide:
        if typ == t_prod or typ == t_auto:
            to_reassign = []
            for s2 in range(len(sites)):
                if sites[s2] == t_distrib and parent[s2] == s:
                    to_reassign.append(s2)
                    sites[s2] = t_vide
                    parent[s2] = -1
                
            sol = try_assign_distrib(in_data, sol, to_reassign)
    elif s_new_typ == t_distrib:
        to_reassign = [s]
        sites[s] = t_vide

        if typ == t_prod or typ == t_auto:
            for s2 in range(len(sites)):
                to_reassign = []
                if sites[s2] == t_distrib and parent[s2] == s:
                    to_reassign.append(s2)
                    sites[s2] = t_vide
    
        sol = try_assign_distrib(in_data, sol, to_reassign)
    return sol

def try_move(in_data, sol, s, d):
    typ = sol['sites'][s]
    sites = sol['sites']
    parent = sol['parent']
    clients = sol['clients']
    sites[d] = sites[s]
    sites[s] = t_vide

    if typ != t_distrib:
        for i in range(len(parent)):
            if parent[i] == s:
                parent[i] = d
    for i in range(len(clients)):
        if clients[i] == s:
            clients[i] = d
    
    sol, _ = get_best_sol(in_data, sol)
    return sol
            


def try_improve_sol(in_data, sol):
    siteSiteDistances = in_data['siteSiteDistances']
    siteClientDistances = in_data['siteClientDistances']
    parent = sol['parent']
    out_sites = sol['sites']

    val_sol = eval_sol(in_data, sol)
    sol, val_sol = get_best_sol(in_data, sol, val_sol=val_sol)

    out_sites_states = []
    for s in range(len(out_sites)):
        for state in range(4):
            out_sites_states.append((s, state))
    shuffle(out_sites_states)

    print("Try change states")
    for s, s_new_typ in out_sites_states:
        new_sol = deepcopy(sol)
        new_sol = try_change_typ(in_data, new_sol, s, s_new_typ)
        if new_sol:
            sol, val_sol = get_best_sol(in_data, sol, val_sol=val_sol, new_sol=new_sol)
    
    print("Try moves")
    # Try moves
    move_dests = []
    for s in range(len(out_sites)):
        for d in range(len(out_sites)):
            move_dests.append((s, d))
    for s, d in move_dests:
        if sol['sites'][s] != t_vide and sol['sites'][d] == t_vide:
            new_sol = deepcopy(sol)
            new_sol = try_move(in_data, new_sol, s, d)
            sol, val_sol = get_best_sol(in_data, sol, val_sol=val_sol, new_sol=new_sol)
    
    return sol
    