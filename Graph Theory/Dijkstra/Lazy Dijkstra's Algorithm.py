'''
@Author: Xinsheng Guo
@Time: 2021年1月29日16:08:31
@File: Lazy Dijkstra's Algorithm.py
'''
#%%
import networkx as nx
import numpy as np
from util import PriorityQueue

def Dijkstra(Graph, start, end):
    '''
    param:
    Graph: nx.Digraph()
    start: node which the path starts from
    end: node which the path ends in

    return:
    min_distance
    '''

    # 获得点的列表
    node_list = list(Graph.nodes())

    # 初始情况：起始点到其他所有点的距离未知，设为无穷大
    for node in node_list:
        if node != start:
            Graph.nodes[node]['min_dis'] = np.inf

    node_queue = PriorityQueue('min')
    node_queue.push(start, 0) # 构造接下来要遍历的优先级队列

    while not node_queue.empty():
        current_node, _min_distance = node_queue.pop() # 队列中弹出下一个遍历的点
        # 当我们已经找到一个到达当前节点的更优路径时，就不需要再在这个点搜索了
        if _min_distance > Graph.nodes[current_node]['min_dis']:
            continue

        for successor in Graph.neighbors(current_node):
            arc = (current_node, successor)
            _distance = Graph.nodes[current_node]['min_dis'] \
                        + Graph.edges[arc]['length'] # 计算起始点通过当前点到达后继节点的距离

            # 更新起始点到达后继节点的距离
            if _distance < Graph.nodes[successor]['min_dis']:
                Graph.nodes[successor]['min_dis'] = _distance
                node_queue.push(successor, _distance) # 在队列中加入需要后继节点
                Graph.nodes[successor]['prev'] = current_node
                
    min_distance = Graph.nodes[end]['min_dis']
    path = []
    prev_node = end
    while prev_node:
        path.insert(0, prev_node)
        prev_node = Graph.nodes[prev_node]['prev']

    return min_distance, path
#%%
if __name__ == '__main__':
    Nodes = ['s', 'a', 'b', 'c', 't']

    arcs = {('s', 'a'):1, ('s', 'c'):100, ('a', 'c'):100, ('b','a'):1, ('c','b'):1, ('a','t'):100, ('c','t'):1}
    Graph = nx.Graph()

    for node in Nodes:
        Graph.add_node(node, min_dis=0, prev=None)

    for key in arcs.keys():
        Graph.add_edge(key[0], key[1], length = arcs[key])

    print(Dijkstra(Graph, 's', 't'))
# %%
