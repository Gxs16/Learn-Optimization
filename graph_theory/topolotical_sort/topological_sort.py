'''
@Author: Xinsheng Guo
@Time: 2021年3月21日22:24:25
@File: topological_sort.py
'''
def depth_first_search(graph, node, visit_set, sort_result):
    if node in graph:
        for i in graph[node]:
            if not i in visit_set:
                visit_set.append(i)
                depth_first_search(graph, i, visit_set, sort_result)
    sort_result.append(node)

def topological_sort(graph, start_node):
    visited = []
    sort_result = []
    depth_first_search(graph, start_node, visited, sort_result)
    return sort_result[::-1]

if __name__ == '__main__':
    _graph = {'a': ['d'],
             'b': ['d'],
             'c': ['a', 'b'],
             'd': ['h', 'g'],
             'e': ['a', 'd', 'f'],
             'f': ['k', 'j'],
             'g': ['i'],
             'h': ['j', 'i'],
             'i': ['l'],
             'j': ['l', 'm'],
             'k': ['j']}

    print(topological_sort(_graph, 'e'))
