from util import *
import sys

name = sys.argv[1]
path = Path(name)
read_all_inputs()

parent = path.parent
name = path.name[:-5]
in_name = '-'.join(name.split('-')[:2])
out_data = read_sol(path, as_path=True)

sol_val = int(eval_sol(IN_DATA[in_name], out_data))
name = 'final-' + in_name + str(sol_val)

print('==== Value : ', sol_val)
output_sol_force_overwrite(name, out_data, as_path=True)