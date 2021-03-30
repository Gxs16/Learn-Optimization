'''
@Author: Xinsheng Guo
@Time: 2021年3月30日22:24:23
@File: articulation_points.py
'''
import networkx as nx

def depth_first_search(graph, parent, current, root, identity, out_edge):
    if parent == root:
        out_edge.append(out_edge[-1]+1)
    graph.nodes[current]['visited'] = True
    graph.nodes[current]['low'] = graph.nodes[current]['id'] = identity[-1]
    identity.append(identity[-1]+1)

    for node_to in graph[current]:
        if node_to != parent:
            if not graph.nodes[node_to]['visited']:
                depth_first_search(graph, current, node_to, root, identity, out_edge)
                graph.nodes[current]['low'] = min(graph.nodes[current]['low'],
                                                  graph.nodes[node_to]['low'])
                if graph.nodes[current]['id'] <= graph.nodes[node_to]['low']:
                    # <: articulation point found via bridge; ==: articulation point found via cycle
                    graph.nodes[current]['is_art'] = True
            else:
                graph.nodes[current]['low'] = min(graph.nodes[current]['low'],
                                                  graph.nodes[node_to]['id'])

def find_bridges(graph):
    identity = [0]
    out_edge = [0]
    for node in graph.nodes():
        if not graph.nodes[node]['visited']:
            out_edge = [0]
            depth_first_search(graph, -1, node, node, identity, out_edge)
            graph.nodes[node]['is_art'] = (out_edge[-1] > 1)
    return graph

if __name__ == '__main__':
    # edges = [(0, 1), (1, 2), (2, 0), (2, 5), (5, 6), (6, 7), (7, 8), (2, 3), (3, 4), (8, 5)]
    edges = [(0, 1), (1, 2), (2, 3), (3, 1), (1, 4), (0, 4)]
    digraph = nx.Graph()
    digraph.add_edges_from(edges)
    nx.set_node_attributes(digraph, 0, 'id')
    nx.set_node_attributes(digraph, False, 'visited')
    nx.set_node_attributes(digraph, 0, 'low')
    nx.set_node_attributes(digraph, False, 'is_art')
    find_bridges(digraph)
    for _node in digraph.nodes():
        if digraph.nodes[_node]['is_art']:
            print(_node)
