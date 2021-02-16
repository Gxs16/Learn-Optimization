'''
@Author: Xinsheng Guo
@Time: 2021年2月8日23:25:02
@File: Ford-Fulkerson Method.py
'''

import networkx as nx

def find_augment_path(graph):
    '''
    DFS\n
    param:\n
    graph:\n
    return:\n
    prev_dict\n
    '''
    stack = ['s']
    visited = []
    prev_dict = {}
    while stack:
        start = stack.pop()
        for node in graph[start]:
            if not node in visited and graph[start][node]['capacity']-graph[start][node]['cur_flow'] > 0:
                prev_dict[node] = start
                visited.append(node)
                if node == 't':
                    return prev_dict
                stack.append(node)
    else:
        return {}

def get_max_flow(graph):
    '''
    param:\n
    graph:\n
    return:\n
    graph:\n
    '''
    prev_dict = find_augment_path(graph)
    bottleneck_list = []
    while prev_dict:
        augment_value = []
        node = 't'
        while node != 's':
            augment_value.append(graph[prev_dict[node]][node]['capacity']-graph[prev_dict[node]][node]['cur_flow'])
            node = prev_dict[node]
        bottleneck = min(augment_value)
        bottleneck_list.append(bottleneck)
        node = 't'
        while node != 's':
            graph[prev_dict[node]][node]['cur_flow'] += bottleneck
            graph[node][prev_dict[node]]['cur_flow'] -= bottleneck
            node = prev_dict[node]
        prev_dict = find_augment_path(graph)
    return graph, bottleneck_list

if __name__ == '__main__':
    graph = nx.DiGraph()

    edges = [('s', '0', 10), ('s', '1', 5), ('s', '2', 10),
            ('0', 's', 0), ('1', 's', 0), ('2', 's', 0),
            ('0', '3', 10),
            ('3', '0', 0),
            ('1', '2', 10),
            ('2', '1', 0),
            ('2', '5', 15),
            ('5', '2', 0),
            ('3', '1', 20), ('3', '6', 15),
            ('1', '3', 0), ('6', '3', 0),
            ('5', '4', 4), ('5', '8', 10),
            ('4', '5', 0), ('8', '5', 0),
            ('4', '1', 15), ('4', '3', 3),
            ('1', '4', 0), ('3', '4', 0),
            ('8', 't', 10),
            ('t', '8', 0),
            ('6', '7', 10), ('6', 't', 15),
            ('7', '6', 0), ('t', '6', 0),
            ('7', '4', 10), ('7', '5', 7),
            ('4', '7', 0), ('5', '7', 0),
            ]

    graph.add_weighted_edges_from(edges, weight='capacity', cur_flow=0)
    graph, max_flow = get_max_flow(graph)
    print(max_flow)
