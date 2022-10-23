"""
@Author: Xinsheng Guo
@Time: 2022年10月23日
@File: subtour-elimination.py
@Reference: <https://mp.weixin.qq.com/s/iIT8Qu7IL1YXAjXQpQvhug>
@Dataset: <https://developers.google.cn/optimization/routing/tsp>
@Description: 整数规划cplex，消除子回路
"""
import math

from docplex.mp.model import Model


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

    model.mu = model.continuous_var_list(model.city_set, 0, None, 'mu')


def setup_constraints(model: Model):
    N = len(model.city_set)-1
    for i in model.city_set[1:]:
        model.add_constraint(model.sum(model.x[i, j] for j in model.city_set if i != j) == 1,
                             '约束1：每个点都被离开一次')

    for j in model.city_set[: -1]:
        model.add_constraint(model.sum(model.x[i, j] for i in model.city_set if i != j) == 1,
                             '约束2：每个点都被到达一次')

    for i in model.city_set[: -1]:
        for j in model.city_set[1:]:
            if i != j:
                model.add_constraint(model.mu[i] - model.mu[j] + N * model.x[i, j] <= N - 1)


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
        # print("Route: {}".format(retrieve_route(model)))
    else:
        print("* model is infeasible")
        return None


if __name__ == '__main__':
    location = [
        (288, 149), (288, 129), (270, 133), (256, 141), (256, 157), (246, 157), (236, 169), (228, 169), (228, 161),
        (220, 169), (212, 169), (204, 169), (196, 169), (188, 169), (196, 161), (188, 145), (172, 145), (164, 145),
        (156, 145), (148, 145), (140, 145), (148, 169), (164, 169), (172, 169), (156, 169), (140, 169), (132, 169),
        (228, 145), (236, 145), (246, 141), (252, 125), (260, 129), (280, 133), (288, 149)
    ]
    tap_test = compute_euclidean_distance_matrix(location)
    model = build_tsp_model(tap_test)
    solve(model)
