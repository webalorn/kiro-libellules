from pathlib import Path
import json

# ========== Evaluation ==========

def preprocess_input(data):
    # TODO si nécessaire ??
    return data

def read_input(name):
    p = Path('../inputs') / name
    with open(str(p), 'r') as f:
        data = json.load(f)
    return preprocess_input(data)

def read_sol(name):
    p = Path('../sols') / name
    with open(str(p), 'r') as f:
        data = json.load(f)
    return data

def output_sol(name, data):
    p = Path('../sols') / name
    with open(str(p), 'w') as f:
        json.dump(data, f)

# ========== Utilities ==========

# ========== Evaluation ==========

def eval_sol(data):
    return 0
