from pathlib import Path
from collections import deque, namedtuple
from math import *
from random import randint, shuffle, choice
from copy import copy, deepcopy

import numpy as np

import json
import time

BEST_SOLS = {}
BEST_SOLS_DATA = {}
IN_DATA = {}
INPUT_NAMES = [e.name for e in Path('../inputs').iterdir() if e.name.endswith('.json')]

OUT_SUFFIX = '-brutal-1' # TODO : to have different solutions names

# ========== Constants ==========

cost_build_prod = 800000.0
cost_automation = 1200000.0
cost_build_distrib = 60000.0

cost_prod_prod = 18.0
cost_prod_auto_bonus = 3.4
cost_prod_distrib = 2.0

cost_route_primary = 0.0075
cost_route_secondary = 0.11

cost_capacity_exceed = 1000.0
capacity_base = 1250000
capacity_auto_bonus = 1250000

t_vide = 0
t_prod = 1
t_auto = 2
t_distrib = 3

# ========== Compute vals on sols ==========

def generate_empty_solution(in_data): #Initialise une solution vide
    nb_sites = len(in_data['sites'])
    nb_clients = len(in_data['clients'])
    out = {}
    out['sites'] = [0 for _ in range(nb_sites)]
    out['parent'] = [-1 for _ in range(nb_sites)]
    out['prods'] = set()
    out['distribs'] = set()
    out['clients'] = [-1 for _ in range(nb_clients)]
    return out

def get_capacities(sol):
    return [capacity_base+capacity_auto_bonus if s == t_auto else
    (capacity_base) if s == t_prod else 0 for s in sol['sites']]

# ========== Input / Output ==========

def preprocess_input(data, name):
    clients = data["clients"]
    for i in range(len(clients)):
        d = clients[i]["demand"]
        x,y = clients[i]["coordinates"]
        clients[i] = (d,(x,y))

    sites = data["sites"]
    for i in range(len(sites)):
        x,y = sites[i]["coordinates"]
        sites[i] = (x,y)

    data = {
        'siteSiteDistances' : data['siteSiteDistances'],
        'siteClientDistances' : data['siteClientDistances'],
    }
    data["clients"] = clients
    data["sites"] = sites
    data['name'] = name

    return data

def read_input(name):
    p = Path('../inputs') / name
    with open(str(p), 'r') as f:
        data = json.load(f)
    return preprocess_input(data, name)

def read_all_inputs():
    for name in INPUT_NAMES:
        IN_DATA[name] = read_input(name)

def _out_with_suffix(name):
    return name[:-5] + OUT_SUFFIX + name[-5:]

def read_sol(name):
    p = Path('../sols') / _out_with_suffix(name)
    with open(str(p), 'r') as f:
        data = json.load(f)
    return data

def output_sol_force_overwrite(name, data):
    p = Path('../sols') / _out_with_suffix(name)
    with open(str(p), 'w') as f:
        json.dump(data, f)

def output_sol_if_better(name, data):
    """ Returns True if the solution is better than the last found solution in this program run,
        even solution already written in the JSON file is even better.
        Updates BEST_SOLS_DATA and BEST_SOLS """
    sol_val = eval_sol(IN_DATA[name], data)
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
        old_val = eval_sol(IN_DATA[name], cur_file_sol)
        if not is_better_sol(old_val, sol_val):
            return True
    print(f"----> Found solution for {name} of value {sol_val}")
    output_sol_force_overwrite(name, data)
    return True

# ========== Evaluation ==========

def eval_sol(in_data, out_data):
    ret = 0
    # Building cost
    for t in out_data["sites"]:
        if t == t_prod:
            ret += cost_build_prod
        elif t == t_auto:
            ret += cost_build_prod + cost_automation
        elif t == t_distrib:
            ret += cost_build_distrib

    # Capacity cost
    capacities = [capacity_base+capacity_auto_bonus if t == t_auto else capacity_base for t in out_data["sites"]]
    for k, center in enumerate(out_data["clients"]):
        demand = in_data["clients"][k][0]
        source = center

        if out_data["sites"][center] == t_distrib:
            source = out_data["parent"][center]
            if out_data["sites"][source] not in [t_prod,t_auto]: # check prod
                return None

            # Production cost
            ret += cost_prod_distrib * demand # relay

            # Routing cost
            ret += demand * cost_route_primary * in_data["siteSiteDistances"][source][center]
            ret += demand * cost_route_secondary * in_data["siteClientDistances"][center][k]
        elif out_data["sites"][center] != t_vide:
            # Routing cost
            ret += demand * cost_route_secondary * in_data["siteClientDistances"][source][k]
        else:
            return None


        capacities[source] -= demand # capacity cost ?

        # Production cost
        ret += cost_prod_prod * demand
        if out_data["sites"][source] == t_auto:
            ret -= cost_prod_auto_bonus * demand

    # Capacity cost
    for c in capacities:
        if c<0:
            ret += -c * cost_capacity_exceed

    return ret

def is_better_sol(old_sol_value, new_sol_value):
    return new_sol_value < old_sol_value # TODO : Replace by < if the best value is the lower one
            

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
