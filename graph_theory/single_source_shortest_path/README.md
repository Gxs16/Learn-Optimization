# Single Source Shortest Path (SSSP)

## Dijkstra's Algorithm

No negative edge weights.

### [Simple Dijkstra's Algorithm](https://github.com/Gxs16/Learn-Optimization/tree/master/graph_theory/single_source_shortest_path/dijkstra/simple_Dijkstra_algorithm.py)

* Reference: <https://mp.weixin.qq.com/s/0scIC2fops4dKdejp6rRDA>
* Language: Python
* Description: Dijkstra's algorithm for digraph or graph, return the minimum distance. O(EV)

### [Lazy Dijkstra's Algorithm](https://github.com/Gxs16/Learn-Optimization/tree/master/graph_theory/single_source_shortest_path/dijkstra/lazy_Dijkstra_algorithm.py)

* Reference: <https://www.bilibili.com/video/BV11E411o7Fb?p=8>
* Language: Python
* Description: Greedy; Choose the most promising target in the priority queue. O((E+V)log(V))

### [Stop Early](https://github.com/Gxs16/Learn-Optimization/tree/master/graph_theory/single_source_shortest_path/dijkstra/stop_early.py)

* Reference: <https://www.bilibili.com/video/BV11E411o7Fb?p=8>
* Language: Python
* Description: Return the result after we have searched the destination.

### Eager Dijkstra's Algorithm (Uncompleted)

* Description: Indexed priority queue.

## Bellman Ford Algorithm

![Example](https://github.com/Gxs16/Learn-Optimization/blob/master/graph_theory/single_source_shortest_path/Bellman_Ford_algorithm/BF_algo.png)

### [BF Algorithm](https://github.com/Gxs16/Learn-Optimization/tree/master/graph_theory/single_source_shortest_path/Bellman_Ford_algorithm/BF_algorithm.py)

* Reference: <https://www.bilibili.com/video/BV11E411o7Fb?p=10>
* Language: Python
* Description: Detect the cycle with negative edge weights.

## SSSP on Directed Acycle Graph

### [Shortest and Longest Path](https://github.com/Gxs16/Learn-Optimization/tree/master/graph_theory/single_source_shortest_path/sssp_on_directed_acycle_graph/shortest_longest_path_on_DAG.py)

* Reference: <https://www.bilibili.com/video/BV11E411o7Fb?p=7>
* Language: Python