from util import *
from solution_tiny import *
import time

# TODO : should import functions from modules

def generate_base_solution(in_data):
    return {'empty' : True} # TODO : use functions from modules

def improve_sol(data):
    return data # TODO : use functions from modules

# ========== Main loop ==========

def main():
    t1 = time.time()
    # inputs_names = [] # If we want to tune only some solutions
    inputs_names = INPUT_NAMES
    read_all_inputs()

    #print(IN_DATA['KIRO-tiny.json'])
    #print(generate_empty_solution(IN_DATA['KIRO-tiny.json']))
    #print(all_possible_soluce(IN_DATA['KIRO-tiny.json']))

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
            sol_data = improve_sol(BEST_SOLS_DATA[name])
            output_sol_if_better(name, sol_data)
    
    

    print(f"\n\nFinished for now, took {int(time.time()-t1)}s")
        





if __name__ == "__main__":
    main()