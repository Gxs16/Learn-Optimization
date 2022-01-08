class BinaryIndexedTree:
    def __init__(self, length):
        self.c = [0] * length
        self.length = length

    def low_bit(self, x):
        return x & (-x)
    
    def update(self, pos, value=1):
        while pos < self.length:
            self.c[pos] += value
            pos += self.low_bit(pos)
    
    def query(self, pos):
        ans = 0
        while pos > 0:
            ans += self.c[pos]
            pos -= self.low_bit(pos)
        return ans
