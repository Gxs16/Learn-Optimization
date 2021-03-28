'''
@Author: Xinsheng Guo
@Time: 2021年3月27日23:46:35
@File: BF_algorithm.py
'''
import numpy as np
import networkx as nx

def bellman_ford(graph, start):
    min_distance = {start: 0}
    for _i in range(graph.number_of_nodes()):
        for edge in graph.edges:
            min_distance[edge[1]] = min(min_distance.get(edge[0], np.inf)+graph.edges[edge]['distance'],
                                        min_distance.get(edge[1], np.inf))

    for _i in range(graph.number_of_nodes()):
        for edge in graph.edges:
            if graph.edges[edge]['distance'] + min_distance[edge[0]] < min_distance[edge[1]]:
                min_distance[edge[1]] = -np.inf

    return min_distance

if __name__ == '__main__':
    edges = [(0, 1, 5),
             (1, 2, 20), (1, 5, 30), (1, 6, 60),
             (2, 3, 10), (2, 4, 75),
             (3, 2, -15),
             (4, 9, 100),
             (5, 4, 9), (5, 6, 5), (5, 8, 50),
             (6, 7, -50),
             (7, 8, -10)]
    digraph = nx.DiGraph()
    digraph.add_weighted_edges_from(edges, weight='distance')
    print(bellman_ford(digraph, 0))
