"""
@Author: Xinsheng Guo
@Time: 2022年10月23日
@File: subtour-elimination.py
@Reference: <https://mp.weixin.qq.com/s/iIT8Qu7IL1YXAjXQpQvhug>
@Dataset: <https://developers.google.cn/optimization/routing/tsp>
@Description: 整数规划cplex，消除子回路
"""
import math
from itertools import combinations
from docplex.mp.model import Model


def build_tsp_model(data):
    model = Model(name='tsp_model')
    setup_data(model, data)
    setup_variables(model)
    setup_constraints(model)
    setup_objects(model)
    return model


def setup_data(model: Model, data):
    model.data = data
    model.city_set = [i for i in range(len(data))]


def setup_variables(model: Model):
    model.x = model.binary_var_matrix(model.city_set, model.city_set, 'x')


def setup_constraints(model: Model):
    for i in model.city_set:
        model.add_constraint(model.sum(model.x[i, j] for j in model.city_set if i != j) == 1,
                             '约束1：每个点都被离开一次')

    for j in model.city_set:
        model.add_constraint(model.sum(model.x[i, j] for i in model.city_set if i != j) == 1,
                             '约束2：每个点都被到达一次')

    for k in range(2, len(model.city_set)):
        for sub_set in combinations(model.city_set, k):
            model.add_constraint(model.sum(model.x[i, j] for i in sub_set for j in sub_set) <= k - 1,
                                 '约束3：消除子回路')


def setup_objects(model: Model):
    model.minimize(model.sum(model.data[i][j] * model.x[i, j] for i in model.city_set for j in model.city_set))


def retrieve_route(model: Model):
    route = {}
    for i in model.city_set:
        for j in model.city_set:
            if model.x[i, j].solution_value > 0.5:
                route[i] = j
    start = 0
    end = route[start]
    route_str = str(start) + '->'
    while end != start:
        route_str += str(end) + '->'
        end = route[end]
    route_str += str(end)

    return route_str


def solve(model: Model):
    # Here, we set the number of threads for CPLEX to 2 and set the time limit to 2mins.
    sol = model.solve(log_output=True)

    if sol is not None:
        print("Objective: {} miles".format(model.objective_value))
        print("Route: {}".format(retrieve_route(model)))
    else:
        print("* model is infeasible")
        return None


def compute_euclidean_distance_matrix(locations):
    """Creates callback to return distance between points."""
    distances = [[0] * len(locations) for j in range(len(locations))]
    for from_counter, from_node in enumerate(locations):
        for to_counter, to_node in enumerate(locations):
            if from_counter == to_counter:
                distances[from_counter][to_counter] = 0
            else:
                # Euclidean distance
                distances[from_counter][to_counter] = (int(
                    math.hypot((from_node[0] - to_node[0]),
                               (from_node[1] - to_node[1]))))
    return distances


if __name__ == '__main__':
    tsp_usa_mini = [[0, 2451, 713, 1018, 1631, 1374, 2408, 213, 2571, 875, 1420, 2145, 1972],
                    [2451, 0, 1745, 1524, 831, 1240, 959, 2596, 403, 1589, 1374, 357, 579],
                    [713, 1745, 0, 355, 920, 803, 1737, 851, 1858, 262, 940, 1453, 1260],
                    [1018, 1524, 355, 0, 700, 862, 1395, 1123, 1584, 466, 1056, 1280, 987],
                    [1631, 831, 920, 700, 0, 663, 1021, 1769, 949, 796, 879, 586, 371],
                    [1374, 1240, 803, 862, 663, 0, 1681, 1551, 1765, 547, 225, 887, 999],
                    [2408, 959, 1737, 1395, 1021, 1681, 0, 2493, 678, 1724, 1891, 1114, 701],
                    [213, 2596, 851, 1123, 1769, 1551, 2493, 0, 2699, 1038, 1605, 2300, 2099],
                    [2571, 403, 1858, 1584, 949, 1765, 678, 2699, 0, 1744, 1645, 653, 600],
                    [875, 1589, 262, 466, 796, 547, 1724, 1038, 1744, 0, 679, 1272, 1162],
                    [1420, 1374, 940, 1056, 879, 225, 1891, 1605, 1645, 679, 0, 1017, 1200],
                    [2145, 357, 1453, 1280, 586, 887, 1114, 2300, 653, 1272, 1017, 0, 504],
                    [1972, 579, 1260, 987, 371, 999, 701, 2099, 600, 1162, 1200, 504, 0]]
    location = [
        (288, 149), (288, 129), (270, 133), (256, 141), (256, 157), (246, 157), (236, 169), (228, 169)
    ]
    tap_test = compute_euclidean_distance_matrix(location)
    model = build_tsp_model(tap_test)
    solve(model)
