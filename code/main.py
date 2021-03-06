from util import *
from solution_tiny import *
from affichage_sites import *
from reassign import *
import time
from stupid import stupid, stupid2
from pertubations import *
from sous_probleme import *
from echange_prod_distrib import *

def tres_stupide(in_data):
    sol = generate_empty_solution(in_data)
    sites = in_data['sites']
    sol['sites'] = [randint(0, 3) for _ in range(len(sites))]
    places = [s for s, sv in enumerate(sol['sites']) if sv == t_auto or sv == t_prod]
    sol['parent'] = [choice(places) for _ in range(len(sites))]
    reasign_best(in_data, sol, 30)
    return sol

# TODO : should import functions from modules

def generate_base_solution(in_data):
    # return {'empty' : True} # TODO : use functions from modules
    print("--- start stupid2")
    # data = stupid2(in_data)
    data = read_sol(in_data['name'])
    print("--- end stupid2")
    return data
    # return tres_stupide(in_data)

def improve_sol(in_data, sol):
    # return data # TODO : use functions from modules
    return try_improve_sol(in_data, sol)
    # return improve_sol_2(in_data,sol)

def improve_sol_2(in_data, sol):
    sol = sous_probleme(in_data, 42, 55, -5, 15, sol)
    return sol

def improve_sol_3(in_data,sol):
    return echange_try(in_data,sol)
# ========== Main loop ==========

def main():
    t1 = time.time()
    inputs_names = ['KIRO-large.json']
    # inputs_names = ['KIRO-medium.json']
    # inputs_names = INPUT_NAMES
    read_all_inputs()

    #print(IN_DATA['KIRO-tiny.json'])
    #print(generate_empty_solution(IN_DATA['KIRO-tiny.json']))
    #print(all_possible_soluce(IN_DATA['KIRO-tiny.json']))
    # affichage(IN_DATA['KIRO-large.json'])
    # in_data = IN_DATA['KIRO-small.json']
    # for sol in all_possible_soluce(in_data):
    #     print(1 in sol['sites'] or 2 in sol['sites'])
    #     sol = reasign_best(in_data, sol)
    #     output_sol_if_better(in_data['name'], sol)
    # exit(0)
    

    for name in inputs_names:
        print(f"========== GENERATE {name} ==========")
        in_data = IN_DATA[name]
        for _ in range(15): # TODO : number of iterations
            sol_data = generate_base_solution(in_data)
            print(eval_sol(in_data, sol_data))
            output_sol_if_better(name, sol_data)

            sol_data = reasign_best(in_data, sol_data, 50)
            print("-> reasign_best", eval_sol(in_data, sol_data))
            output_sol_if_better(name, sol_data)
        
    
    for name in inputs_names:
        print(f"========== IMPROVE {name} ==========")
        in_data = IN_DATA[name]
        for _ in range(100): # TODO : number of iterations
            sol_data = improve_sol_3(in_data, BEST_SOLS_DATA[name])
            output_sol_if_better(name, sol_data)
    
    

    print(f"\n\nFinished for now, took {int(time.time()-t1)}s")
        





if __name__ == "__main__":
    main()