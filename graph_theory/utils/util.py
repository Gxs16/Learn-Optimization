'''
@Author: Xinsheng Guo
@Time: 2021年1月29日17:27:39
@File: util.py
'''
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
        if not sense in ['min', 'max']:
            raise Exception('Parameter sense should be \'min\' or \'max\'!')
        else:
            self.data = []
            self.sense = sense

    def __contains__(self, key: int):
        if self.data:
            return self.data[key]
        else:
            raise Exception('Priority queue is empty!')

    def __str__(self):
        return str(self.data)

    def push(self, element, priority):
        '''
        param:\n
        element: the element needed to insert.\n
        priority: the priority to the element.
        '''
        # Binary Search
        left = 0
        right = len(self.data)-1
        while left <= right:
            mid = left+(right-left)//2
            if self.data[mid][1] == priority:
                self.data.insert(mid, (element, priority))
                break
            elif self.data[mid][1] < priority:
                left = mid+1
            else:
                right = mid-1
        else:
            self.data.insert(left, (element, priority))

    def pop(self):
        '''
        Return the top priority.

        return:\n
        element:\n
        priority:
        '''
        if self.data:
            if self.sense == 'min':
                return self.data.pop(0)
            elif self.sense == 'max':
                return self.data.pop(-1)
        else:
            raise Exception('pop on a empty priority queue!')

    def empty(self):
        '''
        Assert the queue is empty or not.
        '''
        return len(self.data) == 0
