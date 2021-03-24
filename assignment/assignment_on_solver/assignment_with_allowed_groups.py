'''
@Author: Xinsheng Guo
@Time: 2020-12-3 16:27:11
@File: assignment_with_allowed_groups.py
'''
#%%
import time
import pyomo.kernel as pmo
from pyomo.opt import SolverStatus, TerminationCondition

start = time.time()
costs = [[90, 76, 75, 70, 50, 74],
          [35, 85, 55, 65, 48, 101],
          [125, 95, 90, 105, 59, 120],
          [45, 110, 95, 115, 104, 83],
          [60, 105, 80, 75, 59, 62],
          [45, 65, 110, 95, 47, 31],
          [38, 51, 107, 41, 69, 99],
          [47, 85, 57, 71, 92, 77],
          [39, 63, 97, 49, 118, 56],
          [47, 101, 71, 60, 88, 109],
          [17, 39, 103, 64, 61, 92],
          [101, 45, 83, 59, 92, 27]]
NUM_WORKERS = len(costs)
NUM_TASKS = len(costs[1])
group1 = [[2, 3],       # Subgroups of workers 0 - 3
          [1, 3],
          [1, 2],
          [0, 1],
          [0, 2]]

group2 = [[6, 7],       # Subgroups of workers 4 - 7
          [5, 7],
          [5, 6],
          [4, 5],
          [4, 7]]

group3 = [[10, 11],     # Subgroups of workers 8 - 11
          [9, 11],
          [9, 10],
          [8, 10],
          [8, 11]]
# group1 = [[0, 0, 1, 1],      # Workers 2, 3
#           [0, 1, 0, 1],      # Workers 1, 3
#           [0, 1, 1, 0],      # Workers 1, 2
#           [1, 1, 0, 0],      # Workers 0, 1
#           [1, 0, 1, 0]]      # Workers 0, 2

# group2 = [[0, 0, 1, 1],      # Workers 6, 7
#           [0, 1, 0, 1],      # Workers 5, 7
#           [0, 1, 1, 0],      # Workers 5, 6
#           [1, 1, 0, 0],      # Workers 4, 5
#           [1, 0, 0, 1]]      # Workers 4, 7

# group3 = [[0, 0, 1, 1],      # Workers 10, 11
#           [0, 1, 0, 1],      # Workers 9, 11
#           [0, 1, 1, 0],      # Workers 9, 10
#           [1, 0, 1, 0],      # Workers 8, 10
#           [1, 0, 0, 1]]      # Workers 8, 11

# Define the model
model = pmo.block()

# Create the sets
model.set_workers = range(NUM_WORKERS)
model.set_tasks = range(NUM_TASKS)

# Create the parameters
model.param_cost = pmo.parameter_dict()
for _worker in model.set_workers:
    for _task in model.set_tasks:
        model.param_cost[(_worker, _task)] = pmo.parameter(costs[_worker][_task])

# Create the variables
model.var_group1 = pmo.variable_dict()
for _pair in range(5):
    model.var_group1[_pair] = pmo.variable(domain=pmo.Binary)

model.var_group2 = pmo.variable_dict()
for _pair in range(5):
    model.var_group2[_pair] = pmo.variable(domain=pmo.Binary)

model.var_group3 = pmo.variable_dict()
for _pair in range(5):
    model.var_group3[_pair] = pmo.variable(domain=pmo.Binary)

model.var_x = pmo.variable_dict()
for _worker in model.set_workers:
    for _task in model.set_tasks:
        model.var_x[(_worker, _task)] = pmo.variable(domain=pmo.Binary)

# Create the constraints
## Each pair in groups can only be chosen once
model.con_group = pmo.constraint_list()
model.con_group.append(pmo.constraint(
    sum(model.var_group1[_pair] for _pair in range(5)) == 1))
model.con_group.append(pmo.constraint(
    sum(model.var_group2[_pair] for _pair in range(5)) == 1))
model.con_group.append(pmo.constraint(
    sum(model.var_group3[_pair] for _pair in range(5)) == 1))


## Each task is assigned to exactly 1 worker
model.con_task = pmo.constraint_list()
for _task in model.set_tasks:
    model.con_task.append(pmo.constraint(
        sum(model.var_x[(_worker, _task)] for _worker in model.set_workers) == 1))
## Each worker is assigned to at most 1 task
model.con_worker = pmo.constraint_list()
for _worker in model.set_workers:
    model.con_worker.append(pmo.constraint(
        sum(model.var_x[(_worker, _task)] for _task in model.set_tasks) <= 1))

model.con_pair = pmo.constraint_list()
for _pair in range(5):
    model.con_pair.append(pmo.constraint(
        sum(model.var_x[(group1[_pair][0], _task)] for _task in model.set_tasks)
        >= model.var_group1[_pair]))
    model.con_pair.append(pmo.constraint(
        sum(model.var_x[(group1[_pair][0], _task)] for _task in model.set_tasks)
        >= model.var_group1[_pair]))
for _pair in range(5):
    model.con_pair.append(pmo.constraint(
        sum(model.var_x[(group2[_pair][0], _task)] for _task in model.set_tasks)
        >= model.var_group2[_pair]))
    model.con_pair.append(pmo.constraint(
        sum(model.var_x[(group2[_pair][0], _task)] for _task in model.set_tasks)
        >= model.var_group2[_pair]))
for _pair in range(5):
    model.con_pair.append(pmo.constraint(
        sum(model.var_x[(group3[_pair][0], _task)] for _task in model.set_tasks)
        >= model.var_group3[_pair]))
    model.con_pair.append(pmo.constraint(
        sum(model.var_x[(group3[_pair][0], _task)] for _task in model.set_tasks)
        >= model.var_group3[_pair]))

# Create the objective
expr = pmo.expression_list()
for _worker in model.set_workers:
    for _task in model.set_tasks:
        expr.append(pmo.expression(
            model.param_cost[(_worker, _task)]*model.var_x[(_worker, _task)]))
model.obj = pmo.objective(sum(expr), sense=pmo.minimize)

# Solve
opt = pmo.SolverFactory('cplex')
result = opt.solve(model, tee=True)

# Print the solution
if result.solver.termination_condition == TerminationCondition.optimal:
    print('Total cost = ', pmo.value(model.obj), '\n')
    for i in range(NUM_WORKERS):
        for j in range(NUM_TASKS):
            # Test if x[i,j] is 1 (with tolerance for floating point arithmetic).
            if model.var_x[(i, j)].value > 0.5:
                print('Worker %d assigned to task %d.  Cost = %d' %
                      (i, j, costs[i][j]))
end = time.time()
print("Time = ", round(end - start, 4), "seconds")

# %%