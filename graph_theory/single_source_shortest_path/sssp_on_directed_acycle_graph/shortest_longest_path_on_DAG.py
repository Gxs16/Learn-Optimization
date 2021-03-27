'''
@Author: Xinsheng Guo
@Time: 2021年3月27日22:45:20
@File: shortest_longest_path_on_DAG.py
@Desc: While finding longest path, multiply all 'distance' by -1
'''
import numpy as np
import networkx as nx

def depth_first_search(graph, node, shortest_path_dict):
    for successor in graph[node]:
        shortest_path_dict[successor] = min(shortest_path_dict.get(successor, np.inf),
                                       shortest_path_dict[node]+graph[node][successor]['distance'])
        depth_first_search(graph, successor, shortest_path_dict)

def shortest_path(graph, start, end):
    shortest_path_dict = {start: 0}
    depth_first_search(graph, start, shortest_path_dict)
    return shortest_path_dict[end]

if __name__ == '__main__':
    digraph = nx.DiGraph()

    edges = [('a', 'b', -1), ('b', 'c', -2), ('a', 'c', -4)]
    digraph.add_weighted_edges_from(edges, weight='distance')
    least_distance = shortest_path(digraph, 'a', 'c')
    print(least_distance)
