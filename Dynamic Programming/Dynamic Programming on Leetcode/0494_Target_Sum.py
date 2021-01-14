'''
@Author: Xinsheng Guo
@Time: 2020-11-29 18:13:34
@File: 0494_Target_Sum.py
@Link: https://leetcode-cn.com/problems/target-sum/
@Tag: Depth-first Search; Dynamic Programming
'''
#%%
class Solution:
    def findTargetSumWays(self, nums, S: int) -> int:
        sum_all = sum(nums)
        diff = sum_all - S
        if diff < 0 or diff % 2:
            return 0
        else:
            diff = int(diff/2)
        F = [1] + [0]*diff
        for j in nums:
            for k in range(diff, j-1, -1):
                F[k] += F[k-j]
        return F[-1]