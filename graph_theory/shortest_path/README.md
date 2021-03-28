# Shortest Path

## [Single Source Shortest Path (SSSP)](./single_source_shortest_path)

![Compare](https://github.com/Gxs16/Learn-Optimization/blob/master/graph_theory/shortest_path/compare.png)

### [Dijkstra's Algorithm](./single_source_shortest_path/dijkstra)

#### [Simple Dijkstra's Algorithm](./single_source_shortest_path/dijkstra/simple_Dijkstra_algorithm.py)

* Reference: <https://mp.weixin.qq.com/s/0scIC2fops4dKdejp6rRDA>
* Language: Python
* Description: Dijkstra's algorithm for digraph or graph, return the minimum distance. O(EV)

#### [Lazy Dijkstra's Algorithm](./single_source_shortest_path/dijkstra/lazy_Dijkstra_algorithm.py)

* Reference: <https://www.bilibili.com/video/BV11E411o7Fb?p=8>
* Language: Python
* Description: Greedy; Choose the most promising target in the priority queue. O((E+V)log(V))

#### [Stop Early](./single_source_shortest_path/dijkstra/stop_early.py)

* Reference: <https://www.bilibili.com/video/BV11E411o7Fb?p=8>
* Language: Python
* Description: Return the result after we have searched the destination.

#### Eager Dijkstra's Algorithm (Uncompleted)

* Description: Indexed priority queue.

### [Bellman Ford Algorithm](./single_source_shortest_path/Bellman_Ford_algorithm/BF_algorithm.py)

![Example](https://github.com/Gxs16/Learn-Optimization/blob/master/graph_theory/shortest_path/single_source_shortest_path/Bellman_Ford_algorithm/BF_algo.png)

* Reference: <https://www.bilibili.com/video/BV11E411o7Fb?p=10>
* Language: Python
* Description: Detect the cycle with negative edge weights.

### [SSSP on Directed Acycle Graph](./single_source_shortest_path/sssp_on_directed_acycle_graph)

#### [Shortest and Longest Path](./single_source_shortest_path/sssp_on_directed_acycle_graph/shortest_longest_path_on_DAG.py)

* Reference: <https://www.bilibili.com/video/BV11E411o7Fb?p=7>
* Language: Python

## [All Pairs Shortest Path (ASAP)](./all_pairs_shortest_path)

![Example](https://github.com/Gxs16/Learn-Optimization/blob/master/graph_theory/shortest_path/single_source_shortest_path/Bellman_Ford_algorithm/BF_algo.png)

### [Floyd-Warshall Algorithm](./all_pairs_shortest_path/Floyd_Warshall.py)

* Reference: <https://www.bilibili.com/video/BV11E411o7Fb?p=11>
* Language: Python
