'''
@Author: Xinsheng Guo
@Time: 2021年4月4日17:42:23
@File: Eulerian_path_digraph.py
@Reference: <https://www.bilibili.com/video/BV11E411o7Fb?p=20>
@Description: DFS, Back Tracing
'''
from collections import defaultdict

def count_in_out(graph):
    in_out_dict = defaultdict(dict)
    for node in graph:
        in_out_dict[node].setdefault('in', 0)
        in_out_dict[node]['out'] = in_out_dict[node].setdefault('out', 0)+len(graph[node])
        for next_node in graph[node]:
            in_out_dict[next_node]['in'] = in_out_dict[next_node].setdefault('in', 0)+1
    return in_out_dict

def has_Eulerian_path(in_out_dict) -> bool:
    start_nodes = 0
    end_nodes = 0
    for node in in_out_dict:
        if abs(in_out_dict[node]['in']-in_out_dict[node]['out']) > 1:
            return False
        if in_out_dict[node]['out']-in_out_dict[node]['in'] == 1:
            start_nodes += 1
        elif in_out_dict[node]['in']-in_out_dict[node]['out'] == 1:
            end_nodes += 1
    return (end_nodes == 0 and start_nodes == 0) or (end_nodes == 1 and start_nodes == 1)

def find_start_node(in_out_dict):
    start = None
    for node in in_out_dict:
        if in_out_dict[node]['out']-in_out_dict[node]['in'] == 1:
            return node
        if in_out_dict[node]['out'] > 0:
            start = node
    return start

def depth_first_search(graph, in_out_dict, node, path):
    while in_out_dict[node]['out'] > 0:
        in_out_dict[node]['out'] -= 1
        next_node = graph[node][in_out_dict[node]['out']]
        depth_first_search(graph, in_out_dict, next_node, path)
    path.append(node)
    return path

def find_Eulerian_path(graph):
    num_edges = 0
    for node in graph:
        num_edges += len(graph[node])

    in_out_dict = count_in_out(graph)

    if not has_Eulerian_path(in_out_dict):
        raise Exception('No Eulerian path exists!')

    start_node = find_start_node(in_out_dict)
    path = []
    path = depth_first_search(graph, in_out_dict, start_node, path)

    if len(path) == num_edges+1:
        return path[::-1]
    else:
        raise Exception('The graph might be disconnected!')
if __name__ == '__main__':
    digraph = {0: [],
               1: [2, 3],
               2: [2, 4, 4],
               3: [1, 2, 5],
               4: [3, 6],
               5: [6],
               6: [3]}
    print(find_Eulerian_path(digraph))
