from util import *
from solution_tiny import *
<<<<<<< HEAD
from affichage_sites import *
=======
from reassign import *
>>>>>>> cc2281f4bddca404f89c37157e15d63f35432fb2
import time
from stupid import stupid
from pertubations import *

# TODO : should import functions from modules

def generate_base_solution(in_data):
    # return {'empty' : True} # TODO : use functions from modules
    return stupid(in_data)

def improve_sol(in_data, sol):
    # return data # TODO : use functions from modules
    return try_improve_sol(in_data, sol)

# ========== Main loop ==========

def main():
    t1 = time.time()
    inputs_names = ['KIRO-large.json'] # If we want to tune only some solutions
    # inputs_names = INPUT_NAMES
    read_all_inputs()

    #print(IN_DATA['KIRO-tiny.json'])
    #print(generate_empty_solution(IN_DATA['KIRO-tiny.json']))
    #print(all_possible_soluce(IN_DATA['KIRO-tiny.json']))
    affichage(IN_DATA['KIRO-large.json'])
    # in_data = IN_DATA['KIRO-tiny.json']
    # for sol in all_possible_soluce(in_data):
    #     print(1 in sol['sites'] or 2 in sol['sites'])
    #     sol = reasign_best(in_data, sol)
    #     output_sol_if_better(in_data['name'], sol)
    # exit(0)
    

    for name in inputs_names:
        print(f"========== GENERATE {name} ==========")
        in_data = IN_DATA[name]
        for _ in range(1): # TODO : number of iterations
            sol_data = generate_base_solution(in_data)
            output_sol_if_better(name, sol_data)
        
    
    for name in inputs_names:
        print(f"========== IMPROVE {name} ==========")
        in_data = IN_DATA[name]
        for _ in range(10): # TODO : number of iterations
            sol_data = improve_sol(in_data, BEST_SOLS_DATA[name])
            output_sol_if_better(name, sol_data)
    
    

    print(f"\n\nFinished for now, took {int(time.time()-t1)}s")
        





if __name__ == "__main__":
    main()