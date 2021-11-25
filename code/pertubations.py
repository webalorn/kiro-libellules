from util import *
from reassign import *

def get_best_sol(in_data, sol, val_sol=None, new_sol=None):
    if new_sol:
        new_sol, _ = get_best_sol(in_data, new_sol)
    else:
        new_sol = reasign_best(in_data, new_sol if new_sol else sol)
    if val_sol is None:
        val_sol = eval_sol(in_data, sol)
    new_val = eval_sol(in_data, new_sol)

    if new_val < val_sol:
        val_sol, sol = new_val, new_sol
        output_sol_if_better(in_data['name'], sol, sol_val=val_sol)
    return sol, val_sol

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
            if out_sites[s] in [1,2] and state in [1,2]: # TODO : remove
                out_sites_states.append((s, state))
    shuffle(out_sites_states)

    print("Try change states")
    for s, s_new_typ in out_sites_states:
        new_sol = deepcopy(sol)
        new_sol['sites'][s] = s_new_typ
        sol, val_sol = get_best_sol(in_data, sol, val_sol=val_sol, new_sol=new_sol)
    
    return sol
    