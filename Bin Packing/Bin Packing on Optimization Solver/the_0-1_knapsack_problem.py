'''
@Author: Xinsheng Guo
@Time: 2021-1-11 17:17:20
@File: the_0-1_knapsack_problem.py
'''
#%%
import pyomo.kernel as pmo
from pyomo.opt import SolverStatus, TerminationCondition

# Create the data
values = [
        360, 83, 59, 130, 431, 67, 230, 52, 93, 125, 670, 892, 600, 38, 48, 147,
        78, 256, 63, 17, 120, 164, 432, 35, 92, 110, 22, 42, 50, 323, 514, 28,
        87, 73, 78, 15, 26, 78, 210, 36, 85, 189, 274, 43, 33, 10, 19, 389, 276,
        312]

weights = [
    7, 0, 30, 22, 80, 94, 11, 81, 70, 64, 59, 18, 0, 36, 3, 8, 15, 42, 9, 0,
    42, 47, 52, 32, 26, 48, 55, 6, 29, 84, 2, 4, 18, 56, 7, 29, 93, 44, 71,
    3, 86, 66, 31, 65, 0, 79, 20, 65, 52, 13]

capacities = 850

model = pmo.block()

# Create the sets
model.set_labels = range(len(values))

# Create the parameters
model.param_label_value = pmo.parameter_dict()
model.param_label_weight = pmo.parameter_dict()
for i in model.set_labels:
    model.param_label_value[i] = pmo.parameter(values[i])
    model.param_label_weight[i] = pmo.parameter(weights[i])

# Create the variables
model.var_pack = pmo.variable_dict()
for i in model.set_labels:
    model.var_pack[i] = pmo.variable(domain=pmo.Binary)

# Create the constraints
model.con_capacity = pmo.constraint(sum(model.var_pack[i] * weights[i] for i in model.set_labels) <= capacities)

# Create the objective
model.obj = pmo.objective(sum(model.var_pack[i] * values[i] for i in model.set_labels), sense=pmo.maximize)

# Solve
opt = pmo.SolverFactory('cplex')
result = opt.solve(model, tee=True)

# Print the solution
packed_items = []
packed_weights = []
if result.solver.termination_condition == TerminationCondition.optimal or result.solver.status == SolverStatus.ok:
    print('Total value = ', pmo.value(model.obj), '\n')
    for i in model.set_labels:
        if model.var_pack[i].value > 0.5:
            packed_items.append(i)
            packed_weights.append(weights[i])
print('Total weight:', sum(packed_weights))
print('Packed items:', packed_items)
print('Packed_weights:', packed_weights)

# %%
