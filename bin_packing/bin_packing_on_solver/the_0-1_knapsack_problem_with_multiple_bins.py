'''
@Author: Xinsheng Guo
@Time: 2021-1-11 17:44:58
@File: the_0-1_knapsack_problem_with_multiple_bins.py
'''
#%%
import pyomo.kernel as pmo
from pyomo.opt import SolverStatus, TerminationCondition

# Create the data
weights = [48, 30, 42, 36, 36, 48, 42, 42, 36, 24, 30, 30, 42, 36, 36]
values = [10, 30, 25, 50, 35, 30, 15, 40, 30, 35, 45, 10, 20, 30, 25]
capacities = [100] * 5

model = pmo.block()

# Create the sets
model.set_goods = range(len(values))
model.set_bins = range(len(capacities))

# Create the variables
model.var_pack = pmo.variable_dict()
for i in model.set_goods:
    for j in model.set_bins:
        model.var_pack[(i, j)] = pmo.variable(domain=pmo.Binary)

# Create the constraints
model.con_capacity = pmo.constraint_list()
for j in model.set_bins:
    model.con_capacity.append(pmo.constraint(sum(model.var_pack[(i, j)] * weights[i] for i in model.set_goods) <= capacities[j]))

model.con_ispack = pmo.constraint_list()
for i in model.set_goods:
    model.con_ispack.append(pmo.constraint(sum(model.var_pack[(i, j)] for j in model.set_bins)<= 1))

# Create the objective
model.obj = pmo.objective(sum(model.var_pack[(i, j)] * values[i] for i in model.set_goods for j in model.set_bins), sense=pmo.maximize)

# Solve
opt = pmo.SolverFactory('cplex')
result = opt.solve(model, tee=True)

# Print the solution
if result.solver.termination_condition == TerminationCondition.optimal or result.solver.status == SolverStatus.ok:
    print('Total value = ', pmo.value(model.obj), '\n')
    for j in model.set_bins:
        print('Bin', j,':')
        packed_weights = []
        packed_values = []
        for i in model.set_goods:
            if model.var_pack[(i, j)] == 1:
                print('Good', i, '- weight', weights[i], ' value', values[i])
                packed_weights.append(weights[i])
                packed_values.append(values[i])
        print('Packed_weight:', sum(packed_weights))
        print('Packed_value:', sum(packed_values), '\n')

# %%
