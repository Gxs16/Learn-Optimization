'''
@Author: Xinsheng Guo
@Time: 2021年2月8日23:25:02
@File: Ford-Fulkerson Method.py
'''

import networkx as nx



def find_augment_path(graph, start, path, visited):
    '''
    param:\n
    start: start node (source node)\n
    path: the edges from source to sink.\n
    visited: the nodes which have been visited.\n
    return:\n
    path: the edges from source to sink.\n
    visited: the nodes which have been visited.\n
    '''
    for node in graph[start]:
        if not node in visited and graph[start][node]['capacity']-graph[start][node]['cur_flow'] > 0:
            visited.append(node)
            path.append((start, node))
            if node == 't':
                return visited, path
            else:
                _visited, _path = find_augment_path(graph, node, path, visited)
                if 't' in _visited:
                    return _visited, _path
                else:
                    path.pop()
    else:
        return visited, path

def get_max_flow(graph):
    '''
    param:\n
    graph:\n
    return:\n
    graph:\n
    '''
    visited = ['s']
    path = []
    visited, path = find_augment_path(graph, 's', path, visited)
    while 't' in visited:
        augment_value = []
        for edge in path:
            augment_value.append(graph.edges[edge]['capacity']-graph.edges[edge]['cur_flow'])
        bottleneck = min(augment_value)
        for edge in path:
            graph[edge[0]][edge[1]]['cur_flow'] += bottleneck
            graph[edge[1]][edge[0]]['cur_flow'] -= bottleneck
        visited = ['s']
        path = []
        visited, path = find_augment_path(graph, 's', path, visited)
    return graph

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
    graph = get_max_flow(graph)
    max_flow = 0
    for node in graph['t']:
        max_flow -= graph['t'][node]['cur_flow']
    print(max_flow)
