from pathlib import Path
from collections import deque, namedtuple
from math import *
from random import randint, shuffle

import numpy as np

import json
import time

BEST_SOLS = {}
BEST_SOLS_DATA = {}
IN_DATA = {}
INPUT_NAMES = [e.name for e in Path('../inputs').iterdir() if e.name.endswith('.json')]

OUT_SUFFIX = '-out-1' # TODO : to have different solutions names

# ========== Input / Output ==========

def preprocess_input(data):
    # TODO si nécessaire ??
    return data

def read_input(name):
    p = Path('../inputs') / name
    with open(str(p), 'r') as f:
        data = json.load(f)
    return preprocess_input(data)

def read_all_inputs():
    for name in INPUT_NAMES:
        IN_DATA[name] = read_input(name)

def _out_with_suffix(name):
    return name[:-5] + OUT_SUFFIX + name[-5:]

def read_sol(name):
    p = Path('../sols') / _out_with_suffix(name)
    with open(str(p), 'r') as f:
        data = json.load(f)
    data['prods'] = set([s for s, typ in enumerate(data['sites']) if typ == T_AUTO or type == T_PROD])
    data['distribs'] = set([s for s, typ in enumerate(data['sites']) if typ == T_DISTRIB])
    return data

def outout_final_sol(name, data):
    p = Path('../sols') / ('final-' + _out_with_suffix(name))
    f_data = {
        "productionCenters" : [
            {"id" : s+1, "automaton" : 1 if typ == T_AUTO else 0 }
            for s, typ in enumerate(data['sites']) if typ == T_AUTO or type == T_PROD
        ],
        "distributionCenters" : [
            {"id" : s+1, "parent" : data['parent'][s]+1 }
            for s, typ in enumerate(data['sites']) if typ == T_DISTRIB
        ],
        "clients" : [{"id" : i+1, "parent" : p+1} for i, p in enumerate(data["clients"])]
    }
    

    with open(str(p), 'w') as f:
        json.dump(f_data, f)

def output_sol_force_overwrite(name, data):
    p = Path('../sols') / _out_with_suffix(name)
    data = {key : value for key, value in data.values()}
    del data['prods']
    del data['distribs']
    with open(str(p), 'w') as f:
        json.dump(data, f)

def output_sol_if_better(name, data):
    """ Returns True if the solution is better than the last found solution in this program run,
        even solution already written in the JSON file is even better.
        Updates BEST_SOLS_DATA and BEST_SOLS """
    sol_val = eval_sol(data)
    if name in BEST_SOLS and is_better_sol(sol_val, BEST_SOLS[name]):
        return False
    BEST_SOLS[name] = sol_val
    BEST_SOLS_DATA[name] = data

    cur_file_sol = None
    try:
        cur_file_sol = read_sol(name)
    except:
        pass
    if cur_file_sol is not None:
        old_val = eval_sol(cur_file_sol)
        if not is_better_sol(old_val, sol_val):
            return True
    print(f"----> Found solution for {name} of value {sol_val}")
    output_sol_force_overwrite(name, data)
    return True

# ========== Evaluation ==========

def eval_sol(data):
    return 0

def is_better_sol(old_sol_value, new_sol_value):
    return new_sol_value > old_sol_value # TODO : Replace by < if the best value is the lower one
            

# ========== Utilities ==========

def _print_color(color, *args, **kwargs):
    print(f"{color}{args[0]}", *args[1:], '\033[0m', **kwargs)

def print_err(*args, **kwargs):
    _print_color("\033[91m", "[ERROR]", *args, **kwargs)

def print_info(*args, **kwargs):
    _print_color("\033[94;1m", "[INFO]", *args, **kwargs)

def print_warning(*args, **kwargs):
    _print_color("\033[93m", "[WARNING]", *args, **kwargs)

def print_ok(*args, **kwargs):
    _print_color("\033[92m", "[WARNING]", *args, **kwargs)

class Heap(): # Smaller number on top
    def __init__(self, l=[]):
        self.l = copy(l)
        if self.l: heapq.heapify(self.l)
    def push(self, el): return heapq.heappush(self.l, el)
    def top(self): return self.l[0]
    def pop(self): return heapq.heappop(self.l)
    def size(self): return len(self.l)
    def empty(): return self.l == []