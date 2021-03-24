'''
@Author: Xinsheng Guo
@Time: 2021-1-11 18:05:46
@File: the_bin_packing_problem.py
'''

#%%
import pyomo.kernel as pmo
from pyomo.opt import SolverStatus, TerminationCondition

# Create the data
weights = [48, 30, 19, 36, 36, 27, 42, 42, 36, 24, 30]
capacity = 100

model = pmo.block()

# Create the sets
model.set_items = range(len(weights))
model.set_bins = range(len(weights))

# Create the variables
model.var_pack = pmo.variable_dict()
model.var_bin = pmo.variable_dict()
for j in model.set_bins:
    model.var_bin[j] = pmo.variable(domain=pmo.Binary)
    for i in model.set_items:
        model.var_pack[(i, j)] = pmo.variable(domain=pmo.Binary)

# Create the constraints
model.con_capacity = pmo.constraint_list()
for j in model.set_bins:
    model.con_capacity.append(pmo.constraint(sum(model.var_pack[(i, j)] * weights[i] for i in model.set_items) <= capacity))

model.con_ispack = pmo.constraint_list()
for i in model.set_items:
    model.con_ispack.append(pmo.constraint(sum(model.var_pack[(i, j)] for j in model.set_bins) == 1))

model.con_use = pmo.constraint_list()
K = 10
for j in model.set_bins:
    model.con_use.append(pmo.constraint(sum(model.var_pack[(i, j)] for i in model.set_items) - K*model.var_bin[j] <= 0))

# Create the objective
model.obj = pmo.objective(sum(model.var_bin[j] for j in model.set_bins))

# Solve
opt = pmo.SolverFactory('cplex')
result = opt.solve(model, tee=True)

print('Total value = ', pmo.value(model.obj), '\n')  
# %%
