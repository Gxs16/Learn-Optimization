'''
@Author: Xinsheng Guo
@Time: 2021年1月28日17:06:33
@File: Simple Dijkstra's Algorithm.py
'''
#%%
import networkx as nx

Nodes = ['s', 'a', 'b', 'c', 't']

Arecs = {('s', 'a'):5, ('s', 'b'):8, ('a', 'c'):2, ('b','a'):10, ('c','b'):3, ('b','t'):4, ('c','t'):3}

Graph = nx.DiGraph()

for node in Nodes:
    Graph.add_node(node, min_dis = 0, previous_node = None)

for key in Arecs.keys():
    Graph.add_edge(key[0],key[1],length = Arecs[key])
#%%
Graph.degree['a']
#%%
def Dijkstra(Graph, start, end):
    '''
    Graph: nx.Digraph()
    start: node which the path starts from
    end: node which the path ends in
    '''
    