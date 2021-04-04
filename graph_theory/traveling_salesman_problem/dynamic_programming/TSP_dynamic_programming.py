'''
@Author: Xinsheng Guo
@Time: 2021年4月3日22:24:05
@File: TSP_dynamic_programming.py
@Reference: <https://www.bilibili.com/video/BV11E411o7Fb?p=17>
@Dataset: <https://developers.google.cn/optimization/routing/tsp>
@Description: min_dist(node_0, node_i, subset) = min(min_dist(node_0, node_k, subset-{node_i})+adj_mat[k][i], for k!=i, k!=0)
              在全图的某个子集合subset中，给定入点node_0，给定出点node_i，从node_0到node_i的最短距离，
              是子集合subset-{node_i}中，node_0到所有可能出点node_k加邻接矩阵adj_mat[k][i]的最小值
'''
from datetime import datetime
from collections import defaultdict
import numpy as np


def setup(adj_matrix, memo, start_node, num_nodes):
    '''
    设置子集中只有两个点的情况，最短距离是两点之间的边长
    param\n
    adj_matrix: 邻接矩阵，二维列表
    memo: 动态规划记忆字典
    start_node: 给定的起始点
    num_nodes: 节点的个数
    '''
    for _node in range(num_nodes):
        # 这里对相同节点不赋值为0而是None的原因是为了方便以后查bug，因为如果出现违法情况会报错
        memo[_node][(1 << start_node) | (1 << _node)] = adj_matrix[start_node][_node] if _node != start_node else None

def solve(adj_matrix, memo, start_node, num_nodes):
    '''
    求解动态规划方程
    param\n
    adj_matrix: 邻接矩阵，二维列表
    memo: 动态规划记忆字典
    start_node: 给定的起始点
    num_nodes: 节点的个数
    '''
    for num_subset in range(3, num_nodes+1):
        # 对元素个数为3个以上的集合进行搜索
        for subset in combinations(num_subset, num_nodes):
            # 对每种可能的组合进行搜索
            if not_in(start_node, subset):
                # 如果起始点都不在这个组合中，就跳过搜索
                continue
            for next_node in range(num_nodes):
                # 对给定集合subset中的所有可能出点进行搜索
                if (next_node == start_node) or not_in(next_node, subset):
                    # 如果这个出点和起始点相同或者出点不在这个集合中就跳过搜索
                    continue
                # 反推出subset去除该出点后的子集subset-next_node
                state = subset ^ (1<<next_node)
                min_dist = np.inf
                for _end in range(num_nodes):
                    # 对subset-next_node进行搜索，搜索出从start_node到next_node的最短路径
                    if _end == start_node or _end == next_node or not_in(_end, state):
                        continue
                    new_distance = memo[_end][state]+adj_matrix[_end][next_node]
                    min_dist = min(new_distance, min_dist)
                # 将搜索到的最短路径放入记忆字典中
                memo[next_node][subset] = min_dist

def not_in(i, subset):
    '''
    判断节点i是否在子集subset中
    '''
    return ((1 << i) & subset) == 0

def generate_combinations(at, r, n):
    '''
    生成器
    '''
    if r == 0:
        yield 0
    for i in range(at, n):
        for set_current in generate_combinations(i+1, r-1, n):
            yield set_current | (1 << i)
       
def combinations(r, n):
    '''
    生成器，生成c_r_n的全组合
    '''
    for comb in generate_combinations(0, r, n):
        yield comb
        
def find_min_cost(adj_matrix, memo, start_node, num_nodes):
    '''
    寻找最短的回路长度
    param\n
    adj_matrix: 邻接矩阵，二维列表
    memo: 动态规划记忆字典
    start_node: 给定的起始点
    num_nodes: 节点的个数
    '''
    # 最终状态就是指全集
    END_STATE = (1 << num_nodes)-1
    min_tour_cost = np.inf
    for _end in range(num_nodes):
        # 对每种可能的出点进行搜索
        if _end != start_node:
            # 最终最短路径是指start_node到end_node再到start_node
            min_tour_cost = min(min_tour_cost, memo[_end][END_STATE]+adj_matrix[_end][start_node])
    return min_tour_cost

def find_optimal_tour(adj_matrix, memo, start_node, num_nodes):
    '''
    寻找最短回路的路径
    param\n
    adj_matrix: 邻接矩阵，二维列表
    memo: 动态规划记忆字典
    start_node: 给定的起始点
    num_nodes: 节点的个数
    '''
    last_index = start_node
    state = (1 << num_nodes)-1
    tour = [start_node]+[None]*(num_nodes-1)+[start_node]

    for i in range(num_nodes-1, 0, -1):
        # 倒推
        index = -1
        for j in range(num_nodes):
            # 逐个比较j到上一个节点last_node的最小值是哪个
            if j == start_node or not_in(j, state):
                continue
            if index == -1:
                index = j
            prev_dist = memo[index][state] + adj_matrix[index][last_index]
            new_dist = memo[j][state] + adj_matrix[j][last_index]
            if new_dist < prev_dist:
                # 每找到一个新的最小距离，就把这个节点赋值给index
                index = j

        tour[i] = index
        state = state ^ (1 << index)
        last_index = index

    return tour

def tsp(data):
    '''
    tsp主函数\n
    param:\n
    data: 存有邻接矩阵与起始点的数据字典
    '''
    adj_matrix = data['adj_matrix']
    start_node = data['start_node']
    num_nodes = len(adj_matrix)
    memo = defaultdict(dict)

    setup(adj_matrix, memo, start_node, num_nodes)
    solve(adj_matrix, memo, start_node, num_nodes)
    min_cost = find_min_cost(adj_matrix, memo, start_node, num_nodes)
    tour = find_optimal_tour(adj_matrix, memo, start_node, num_nodes)

    return min_cost, tour

if __name__ == '__main__':
    start = datetime.now()
    data_usa_mini = {
        'adj_matrix': [[0, 2451, 713, 1018, 1631, 1374, 2408, 213, 2571, 875, 1420, 2145, 1972],
                        [2451, 0, 1745, 1524, 831, 1240, 959, 2596, 403, 1589, 1374, 357, 579],
                        [713, 1745, 0, 355, 920, 803, 1737, 851, 1858, 262, 940, 1453, 1260],
                        [1018, 1524, 355, 0, 700, 862, 1395, 1123, 1584, 466, 1056, 1280, 987],
                        [1631, 831, 920, 700, 0, 663, 1021, 1769, 949, 796, 879, 586, 371],
                        [1374, 1240, 803, 862, 663, 0, 1681, 1551, 1765, 547, 225, 887, 999],
                        [2408, 959, 1737, 1395, 1021, 1681, 0, 2493, 678, 1724, 1891, 1114, 701],
                        [213, 2596, 851, 1123, 1769, 1551, 2493, 0, 2699, 1038, 1605, 2300, 2099],
                        [2571, 403, 1858, 1584, 949, 1765, 678, 2699, 0, 1744, 1645, 653, 600],
                        [875, 1589, 262, 466, 796, 547, 1724, 1038, 1744, 0, 679, 1272, 1162],
                        [1420, 1374, 940, 1056, 879, 225, 1891, 1605, 1645, 679, 0, 1017, 1200],
                        [2145, 357, 1453, 1280, 586, 887, 1114, 2300, 653, 1272, 1017, 0, 504],
                        [1972, 579, 1260, 987, 371, 999, 701, 2099, 600, 1162, 1200, 504, 0]],
        'start_node': 0}
    data_test = {'adj_matrix':[[0, 1, 2, 3],
                               [1, 0, 5, 3],
                               [2, 5, 0, 4],
                               [3, 3, 4, 0]],
                 'start_node':0}

    cost, min_tour = tsp(data_usa_mini)
    print(min_tour)
    print(cost)
    end = datetime.now()
    print(end-start)
