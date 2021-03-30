'''
@Author: Xinsheng Guo
@Time: 2021年3月29日22:50:17
@File: low_link.py
@Reference: <https://www.bilibili.com/video/BV11E411o7Fb?p=13>
@Description: Depth First Search.
'''
import networkx as nx

def depth_first_search(graph, parent, current, identity):
    graph.nodes[current]['visited'] = True
    graph.nodes[current]['low'] = graph.nodes[current]['id'] = identity[-1]
    identity.append(identity[-1]+1)

    for node_to in graph[current]:
        if node_to != parent:
            if not graph.nodes[node_to]['visited']:
                depth_first_search(graph, current, node_to, identity)
                graph.nodes[current]['low'] = min(graph.nodes[current]['low'],
                                                  graph.nodes[node_to]['low'])
                if graph.nodes[current]['id'] < graph.nodes[node_to]['low']:
                    graph.edges[(current, node_to)]['is_bridge'] = True
            else:
                graph.nodes[current]['low'] = min(graph.nodes[current]['low'],
                                                  graph.nodes[node_to]['id'])

def find_bridges(graph):
    identity = [0]
    for node in graph.nodes():
        if not graph.nodes[node]['visited']:
            depth_first_search(graph, -1, node, identity)

if __name__ == '__main__':
    edges = [(0, 1), (1, 2), (2, 0), (2, 5), (5, 6), (6, 7), (7, 8), (2, 3), (3, 4), (8, 5)]
    digraph = nx.Graph()
    digraph.add_edges_from(edges)
    nx.set_node_attributes(digraph, 0, 'id')
    nx.set_node_attributes(digraph, False, 'visited')
    nx.set_node_attributes(digraph, 0, 'low')
    nx.set_edge_attributes(digraph, False, 'is_bridge')
    find_bridges(digraph)
    for _edge in digraph.edges():
        if digraph.edges[_edge]['is_bridge']:
            print(_edge)
