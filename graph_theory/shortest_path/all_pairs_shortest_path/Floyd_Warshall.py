'''
@Author: Xinsheng Guo
@Time: 2021年3月28日21:09:14
@File: Floyd_Warshall.py
'''
import numpy as np
from collections import defaultdict
import networkx as nx

def setup(graph):
    dp = defaultdict(dict)
    next_dict = defaultdict(dict)
    for i in graph.nodes():
        for j in graph.nodes():
            try:
                dp[i][j] = graph[i][j]['distance']
                next_dict[i][j] = j
            except:
                if i == j:
                    dp[i][j] = 0
                    next_dict[i][j] = j
                else:
                    dp[i][j] = np.inf
            
    return dp, next_dict

def detect_negative_cycle(graph, dp, next_dict):
    for k in graph.nodes():
        for i in graph.nodes():
            for j in graph.nodes():
                if dp[i][k] + dp[k][j] < dp[i][j]:
                    dp[i][j] = -np.inf
                    next_dict[i][j] = -1

def floyd_warshall_algo(graph):
    dp, next_dict = setup(graph)
    for k in graph.nodes():
        for i in graph.nodes():
            for j in graph.nodes():
                if dp[i][k]+dp[k][j] < dp[i][j]:
                    dp[i][j] = dp[i][k]+dp[k][j]
                    next_dict[i][j] = next_dict[i][k]
    detect_negative_cycle(graph, dp, next_dict)
    return dp, next_dict

def reconstruct_path(start, end, next_dict, dp):
    path = []
    if dp[start][end] == np.inf:
        return None
    current = start
    while current != end:
        if current == -1:
            return None
        path.append(current)
        current = next_dict[current][end]
    if next_dict[current][end] == -1:
        return None
    path.append(end)
    return path

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
    distance_dict, next_node_dict = floyd_warshall_algo(digraph)
    print(reconstruct_path(0, 8, next_node_dict, distance_dict))
