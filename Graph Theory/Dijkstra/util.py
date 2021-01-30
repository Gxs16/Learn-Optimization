'''
@Author: Xinsheng Guo
@Time: 2021年1月29日17:27:39
@File: util.py
'''

class PriorityQueue():
    '''
    PriorityQueue by myself.
    param:
    sense: \'max\' or \'min\'
    '''
    def __init__(self, sense: str):
        '''
        param:
        sense: \'max\' or \'min\'
        '''
        if not sense in ['min', 'max']:
            raise Exception('sense should be \'min\' or \'max\'!')
        else:
            self.data = []
            self.sense = sense

    def push(self, data, priority):
        # Binary Search
        left = 0
        right = len(self.data)-1
        while left <= right:
            mid = left+(right-left)//2
            if self.data[mid][1] == priority:
                self.data.insert(mid, (data, priority))
                break
            elif self.data[mid][1] < priority:
                left = mid+1
            else:
                right = mid-1
        else:
            self.data.insert(left, (data, priority))

    def pop(self):
        if self.data:
            if self.sense == 'min':
                return self.data.pop(0)
            elif self.sense == 'max':
                return self.data.pop(-1)
        else:
            raise Exception('pop on a empty priority queue!')

    def empty(self):
        return len(self.data) == 0

    def print_data(self):
        print(self.data)
