'''
@Author: Xinsheng Guo
@Time: 2021年1月29日17:27:39
@File: priority_queue.py
'''
from utils.heap import MaxHeap, MinHeap

from collections import defaultdict
#%%
class PriorityQueue():
    '''
    PriorityQueue by myself.\n
    param:\n
    sense: \'max\' or \'min\'
    '''
    def __init__(self, sense: str):
        '''
        param:\n
        sense: \'max\' or \'min\'
        '''
        self.map_dict = defaultdict(list)
        if sense == 'max':
            self.heap = MaxHeap()
        elif sense == 'min':
            self.heap = MinHeap()
        else:
            raise Exception('Parameter sense should be \'min\' or \'max\'!')

    def push(self, element, priority):
        '''
        param:\n
        element: the element needed to insert.\n
        priority: the priority to the element.
        '''
        self.map_dict[priority].append(element)
        self.heap.insert(priority)

    def pop(self):
        '''
        Return the top priority.

        return:\n
        element:\n
        priority:
        '''
        priority = self.heap.peek()
        self.heap.poll()
        return self.map_dict[priority].pop(), priority

    def empty(self):
        '''
        Assert the queue is empty or not.
        '''
        return self.heap.empty()
