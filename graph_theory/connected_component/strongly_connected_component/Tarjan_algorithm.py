'''
@Author: Xinsheng Guo
@Time: 2021年4月1日22:47:14
@File: Tarjan_algorithm.py
@Reference: <https://www.bilibili.com/video/BV11E411o7Fb?p=15>
@Description: 总体思想就是通过标注low link值的方法来判断有向环是否存在，如果存在有向环，就把这个环标记为一个强连通分量。
              同时用一个栈来维护尚未被标记上连通分量但是已经被遍历过的点，并且区分判别下一个要遍历的点是否已经属于另一个连通分量。
'''
from collections import defaultdict
import networkx as nx

def depth_first_search(graph, current, identity, stack):
    graph.nodes[current]['visited'] = True
    graph.nodes[current]['low'] = graph.nodes[current]['id'] = identity[-1]
    identity.append(identity[-1]+1)
    stack.append(current)

    for node_to in graph[current]:
        if not graph.nodes[node_to]['visited']:
            depth_first_search(graph, node_to, identity, stack)
        if node_to in stack:
            # 如果即将遍历的节点node_to不在栈中，那么说明node_to已经属于其他的连通分量
            graph.nodes[current]['low'] = min(graph.nodes[current]['low'],
                                              graph.nodes[node_to]['low'])

    if graph.nodes[current]['id'] == graph.nodes[current]['low']:
        # 当id值等于low值的时候说明已经回调到环的开始状态，需要将栈中此节点及之后入栈的节点全部弹出
        node = stack.pop()
        graph.nodes[node]['low'] = graph.nodes[current]['id']
        while node != current:
            node = stack.pop()
            # 给弹出的节点的low值打上相同的lowlink值
            graph.nodes[node]['low'] = graph.nodes[current]['id']

def find_scc(graph):
    identity = [0]
    stack = []
    for node in graph.nodes():
        if not graph.nodes[node]['visited']:
            depth_first_search(graph, node, identity, stack)

if __name__ == '__main__':
    edges = [(0, 1), (1, 2), (2, 0), 
             (3, 4), (4, 5), (5, 6), 
             (6, 4), (3, 7), (7, 3)]
    digraph = nx.DiGraph()
    digraph.add_edges_from(edges)
    nx.set_node_attributes(digraph, 0, 'id')
    nx.set_node_attributes(digraph, False, 'visited')
    nx.set_node_attributes(digraph, 0, 'low')
    find_scc(digraph)

    component = defaultdict(list)
    for _node in digraph.nodes():
        component[digraph.nodes[_node]['low']].append(_node)
    print(component)
