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

def try_assign_distrib(in_data, sol, to_assign)

def try_change_typ(in_data, sol, s, s_new_typ):
    typ = sol['sites'][s]
    sites = sol['sites']
    parent = sol['parent']
    sites[s] = s_new_typ

    if s_new_typ == typ:
        return False
    
    if s_new_typ == t_vide:
        if s_new_typ == t_prod or s_new_typ == t_auto:
            for s2 in range(len(sites)):
                to_reassign = []
                if sites[s2] == t_distrib and parent[s2] == s:
                    to_reassign.append(s2)
                    sites[s2] = t_vide
                
                try_assign_distrib(in_data, sol, to_reassign)
    elif s_new_typ == t_distrib:
        return False
        try_assign_distrib(in_data, sol, [s])
        if s_new_typ != t_vide:
            return False

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
        if try_change_typ(in_data, new_sol, s, s_new_typ) is not False:
            sol, val_sol = get_best_sol(in_data, sol, val_sol=val_sol, new_sol=new_sol)
    
    return sol
    