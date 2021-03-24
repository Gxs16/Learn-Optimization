'''
@Author: Xinsheng Guo
@Time: 2020-12-3 14:22:14
@File: assignment_with_teams.py
'''
#%%
import pyomo.kernel as pmo
from pyomo.opt import SolverStatus, TerminationCondition

# Create the data
costs = [[90, 76, 75, 70],
         [35, 85, 55, 65],
         [125, 95, 90, 105],
         [45, 110, 95, 115],
         [60, 105, 80, 75],
         [45, 65, 110, 95]]
team1 = [0, 2, 4]
team2 = [1, 3, 5]
TEAM_MAX = 2
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
## Each worker is assigned to at most 1 task
model.con_worker = pmo.constraint_list()
for _worker in model.set_workers:
    model.con_worker.append(pmo.constraint(
        sum(model.var_x[(_worker, _task)] for _task in model.set_tasks) <= 1))
## Each task is assigned to exactly 1 worker
model.con_task = pmo.constraint_list()
for _task in model.set_tasks:
    model.con_task.append(pmo.constraint(
        sum(model.var_x[(_worker, _task)] for _worker in model.set_workers) == 1))
## Each teams takes on two tasks
model.con_team = pmo.constraint_list()
model.con_team.append(pmo.constraint(
    sum(model.var_x[(_worker, _task)] for _worker in team1 for _task in model.set_tasks)
    <= TEAM_MAX))
model.con_team.append(pmo.constraint(
    sum(model.var_x[(_worker, _task)] for _worker in team2 for _task in model.set_tasks)
    <= TEAM_MAX))

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
# %%
