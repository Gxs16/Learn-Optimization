'''
@Author: Xinsheng Guo
@Time: 2020-12-3 15:27:07
@File: assignment_with_task_sizes.py
'''
#%%
import time
import pyomo.kernel as pmo
from pyomo.opt import SolverStatus, TerminationCondition

start = time.time()
# Create the data
costs = [[90, 76, 75, 70, 50, 74, 12, 68],
         [35, 85, 55, 65, 48, 101, 70, 83],
         [125, 95, 90, 105, 59, 120, 36, 73],
         [45, 110, 95, 115, 104, 83, 37, 71],
         [60, 105, 80, 75, 59, 62, 93, 88],
         [45, 65, 110, 95, 47, 31, 81, 34],
         [38, 51, 107, 41, 69, 99, 115, 48],
         [47, 85, 57, 71, 92, 77, 109, 36],
         [39, 63, 97, 49, 118, 56, 92, 61],
         [47, 101, 71, 60, 88, 109, 52, 90]]
sizes = [10, 7, 3, 12, 15, 4, 11, 5]
TOTAL_SIZE_MAX = 15
NUM_WORKERS = len(costs)
NUM_TASKS = len(costs[0])

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
model.var_x = pmo.variable_dict()
for _worker in model.set_workers:
    for _task in model.set_tasks:
        model.var_x[(_worker, _task)] = pmo.variable(domain=pmo.Binary)

# Create the constraints
## Each task is assigned to at least 1 worker
model.con_task = pmo.constraint_list()
for _task in model.set_tasks:
    model.con_task.append(pmo.constraint(
        sum(model.var_x[(_worker, _task)] for _worker in model.set_workers) >= 1))
## Total size of tasks for each worker is at most total_size_max
model.con_size = pmo.constraint_list()
for _worker in model.set_workers:
    model.con_task.append(pmo.constraint(
        sum(sizes[_task]*model.var_x[(_worker, _task)] for _task in model.set_tasks) <= TOTAL_SIZE_MAX
    ))

# Create the objective
expr = pmo.expression_list()
for _worker in model.set_workers:
    for _task in model.set_tasks:
        expr.append(pmo.expression(
            model.param_cost[(_worker, _task)]*model.var_x[(_worker, _task)]))
model.obj = pmo.objective(sum(expr), sense=pmo.minimize)

# Solve
opt = pmo.SolverFactory('cplex')
result = opt.solve(model)

# Print the solution
if result.solver.termination_condition == TerminationCondition.optimal or\
    result.solver.status == SolverStatus.ok:
    print('Total cost = ', pmo.value(model.obj), '\n')
    for i in range(NUM_WORKERS):
        for j in range(NUM_TASKS):
            # Test if x[i,j] is 1 (with tolerance for floating point arithmetic).
            if model.var_x[(i, j)].value > 0.5:
                print('Worker %d assigned to task %d.  Cost = %d' %
                      (i, j, costs[i][j]))
end = time.time()
print("Time = ", round(end - start, 4), "seconds")