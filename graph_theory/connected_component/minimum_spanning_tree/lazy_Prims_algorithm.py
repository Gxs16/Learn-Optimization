'''
@Author: Xinsheng Guo
@Time: 2021年1月31日18:21:54
@File: lazy_Prims_algorithm.py
@Reference: <https://www.bilibili.com/video/BV11E411o7Fb?p=22>
@Description: Greedy; Choose the most promising target in the priority queue.
'''
import sys
sys.path.append('graph_theory')

import networkx as nx
from util.priority_queue import PriorityQueue

def add_edges(graph, node, queue, node_visited):
    '''
    param:\n
    graph:\n
    node: node we are visiting now.
    queue:\n
    node_visited: nodes which have been visited in this set.
    '''
    node_visited.add(node)
    for i in graph.neighbors(node):
        if not i in node_visited:
            queue.push((node, i), graph.edges[(node, i)]['cost'])

def lazy_prims(graph, start):
    '''
    param:
    start: start node in the graph.

    return:
    minimum_cost: the minimum cost of MST
    edge_mst: a list of edges in the MST
    '''
    # get the number of edges in MST
    m = len(graph.nodes) - 1
    node_visited = set()
    edge_mst = []
    minimum_cost = 0

    pq = PriorityQueue('min')

    add_edges(graph, start, pq, node_visited)

    while (not pq.empty()) and (len(edge_mst) != m):
        edge, cost = pq.pop()
        next_node = edge[1]

        if not next_node in node_visited:
            edge_mst.append(edge)
            minimum_cost += cost
            add_edges(graph, next_node, pq, node_visited)

    if len(edge_mst) != m:
        return (None, []) # There is no MST
    else:
        return minimum_cost, edge_mst

if __name__ == '__main__':

    #nodes = [str(i) for i in range(8)]
    edges = [(0, 1, 10), (0, 2, 1), (0, 3, 4),
             (1, 2, 3), (1, 4, 0), (2, 5, 8),
             (2, 3, 2), (3, 5, 2), (3, 6, 7),
             (4, 5, 1), (4, 7, 8), (5, 7, 9),
             (5, 6, 6), (6, 7, 12)]

    graph_mst = nx.Graph()
    #graph_mst.add_nodes_from(nodes)
    graph_mst.add_weighted_edges_from(edges, weight='cost')

    print(lazy_prims(graph_mst, 0))
    