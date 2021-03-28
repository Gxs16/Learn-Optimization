'''
@Author: Xinsheng Guo
@Time: 2021年1月31日21:09:42
@File: heap.py
'''
class Heap():
    '''
    Heap
    '''
    def __init__(self):
        self.data = []

    def __str__(self):
        return str(self.data)

    def _get_left_child_index(self, parent_index: int) -> int:
        return 2*parent_index+1

    def _get_right_child_index(self, parent_index: int) -> int:
        return 2*parent_index+2

    def _get_parent_index(self, child_index: int) -> int:
        return (child_index-1)//2

    def _has_left_child(self, parent_index: int) -> bool:
        return self._get_left_child_index(parent_index) < len(self.data)

    def _has_right_child(self, parent_index: int) -> bool:
        return self._get_right_child_index(parent_index) < len(self.data)

    def _has_parent(self, child_index: int) -> bool:
        return self._get_parent_index(child_index) >= 0

    def _get_left_child(self, parent_index: int):
        if self._has_left_child(parent_index):
            return self.data[self._get_left_child_index(parent_index)]
        else:
            raise Exception('no left child!')

    def _get_right_child(self, parent_index: int):
        if self._has_right_child(parent_index):
            return self.data[self._get_right_child_index(parent_index)]
        else:
            raise Exception('no right child!')

    def _get_parent(self, child_index: int):
        if self._has_parent(child_index):
            return self.data[self._get_parent_index(child_index)]
        else:
            raise Exception('no parent!')

    def _heapify_up(self) -> None:
        pass

    def _heapify_down(self) -> None:
        pass

    def insert(self, data) -> None:
        '''
        Insert a new data into heap.\n
        param:\n
        data: the data needed to be inserted.
        '''
        self.data.append(data)
        self._heapify_up()

    def poll(self):
        '''
        Remove the top element.
        '''
        if self.empty():
            raise Exception('MinHeap is empty!')
        else:
            self.data[0] = self.data[-1]
            self.data.pop()
            self._heapify_down()

    def peek(self):
        '''
        Return the top element of the MinHeap
        '''
        if self.empty():
            raise Exception('MinHeap is empty!')
        else:
            return self.data[0]

    def empty(self) -> bool:
        '''
        Indicator whether MinHeap is empty
        '''
        return len(self.data) == 0

class MinHeap(Heap):
    '''
    MinHeap\n
    param:\n
    data_container: None or data in list.
    '''
    def _heapify_up(self) -> None:
        current_index = len(self.data)-1
        while self._has_parent(current_index):
            if self._get_parent(current_index) > self.data[current_index]:
                _parent_index = self._get_parent_index(current_index)
                self.data[current_index], self.data[_parent_index] =\
                    self.data[_parent_index], self.data[current_index]
                current_index = _parent_index
            else:
                break

    def _heapify_down(self) -> None:
        current_index = 0
        while self._has_left_child(current_index):
            if self._has_right_child(current_index) and\
                self._get_left_child(current_index) > self._get_right_child(current_index):
                smaller_child_index = self._get_right_child_index(current_index)
            else:
                smaller_child_index = self._get_left_child_index(current_index)

            if self.data[current_index] > self.data[smaller_child_index]:
                self.data[current_index], self.data[smaller_child_index] =\
                self.data[smaller_child_index], self.data[current_index]
            else:
                break

            current_index = smaller_child_index

class MaxHeap(Heap):
    '''
    MaxHeap\n
    '''
    def _heapify_up(self) -> None:
        current_index = len(self.data)-1
        while self._has_parent(current_index):
            if self._get_parent(current_index) < self.data[current_index]:
                _parent_index = self._get_parent_index(current_index)
                self.data[current_index], self.data[_parent_index] =\
                    self.data[_parent_index], self.data[current_index]
                current_index = _parent_index
            else:
                break

    def _heapify_down(self) -> None:
        current_index = 0
        while self._has_left_child(current_index):
            if self._has_right_child(current_index) and\
                self._get_left_child(current_index) < self._get_right_child(current_index):
                larger_child_index = self._get_right_child_index(current_index)
            else:
                larger_child_index = self._get_left_child_index(current_index)

            if self.data[current_index] < self.data[larger_child_index]:
                self.data[current_index], self.data[larger_child_index] =\
                self.data[larger_child_index], self.data[current_index]
            else:
                break

            current_index = larger_child_index

if __name__ == '__main__':
    import random
    test = MaxHeap()
    test_data = list(range(100))
    random.shuffle(test_data)
    for i in test_data:
        test.insert(i)
    while not test.empty():
        print(test.peek())
        test.poll()
