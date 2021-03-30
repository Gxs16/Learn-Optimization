'''
@Author: Xinsheng Guo
@Time: 2021年3月21日21:23:07
@File: Dinic_algorithm.py
@Reference: <https://www.bilibili.com/video/BV11E411o7Fb?p=34>
@Description: Construct a level-graph which can guide the BFS to the sink approximately.
'''

import networkx as nx

def construct_level_graph(graph):
    visited = ['s']
    successor = ['s']
    while successor:
        start = successor.pop(0)
        visited.append(start)
        for node in graph.successors(start):
            if not node in visited and graph[start][node]['capacity']-graph[start][node]['cur_flow'] > 0:
                graph.nodes[node]['level'] = graph.nodes[start]['level']+1
                successor.append(node)
                visited.append(node)
    if 't' in visited:
        return True
    else:
        return False


def find_augment_path(graph):
    '''
    BFS
    param:\n
    graph:\n
    return:\n
    prev_dict\n
    '''
    queue = ['s']
    visited = []
    prev_dict = {}
    while queue:
        start = queue.pop(0)
        for node in graph[start]:
            if not node in visited and graph[start][node]['capacity']-graph[start][node]['cur_flow'] > 0 and graph.nodes[node]['level'] > graph.nodes[start]['level']:
                prev_dict[node] = start
                visited.append(node)
                if node == 't':
                    return prev_dict
                queue.append(node)
    return {}

def get_max_flow(graph):
    '''
    param:\n
    graph:\n
    return:\n
    graph:\n
    '''
    
    bottleneck_list = []
    while construct_level_graph(graph):
        prev_dict = find_augment_path(graph)
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
    return graph, bottleneck_list

if __name__ == '__main__':
    digraph = nx.DiGraph()

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

    digraph.add_weighted_edges_from(edges, weight='capacity', cur_flow=0)
    digraph.nodes['s']['level'] = 0
    digraph, max_flow = get_max_flow(digraph)
    print(max_flow)