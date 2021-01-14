'''
@Author: Xinsheng Guo
@Time: 2020年12月29日15:32:32
@File: 0070_Climbing_Stairs.py
@Link: https://leetcode-cn.com/problems/climbing-stairs/
@Tag: Dynamic Programming
'''
#
# @lc app=leetcode.cn id=70 lang=python3
#
# [70] 爬楼梯
#

# @lc code=start
class Solution:
    def get_rec(self, n: int, record: dict) -> int:
        if not n-2 in record:
            record[n-2] = self.get_rec(n-2, record)
        if not n-1 in record:
            record[n-1] = self.get_rec(n-1, record)
        return record[n-1]+record[n-2]

    def climbStairs(self, n: int) -> int:
        if n == 2:
            return 2
        elif n == 1:
            return 1
        else:
            record = {1:1, 2:2}
            return self.get_rec(n, record)
# @lc code=end

