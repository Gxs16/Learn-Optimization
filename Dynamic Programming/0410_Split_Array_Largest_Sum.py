'''
@Author: Xinsheng Guo
@Time: 2021年1月14日16:53:44
@File: 0410_Split_Array_Largest_Sum.py
@Link: https://leetcode-cn.com/problems/split-array-largest-sum/
@Tag: Binary Search; Dynamic Programming
'''
#
# @lc app=leetcode.cn id=410 lang=python3
#
# [410] 分割数组的最大值
#
#%%
# @lc code=start
class Solution:
    def splitArray(self, nums: List[int], m: int) -> int:
        def check(x: int) -> bool:
            total, cnt = 0, 1
            for num in nums:
                if total + num > x:
                    cnt += 1
                    total = num
                else:
                    total += num
            return cnt <= m


        left = max(nums)
        right = sum(nums)
        while left < right:
            mid = (left + right) // 2
            if check(mid):
                right = mid
            else:
                left = mid + 1

        return left
# @lc code=end
class Solution:
    def splitArray(self, nums: List[int], m: int) -> int:
        n = len(nums)
        f = [[10**18] * (m + 1) for _ in range(n + 1)]
        sub = [0]
        for elem in nums:
            sub.append(sub[-1] + elem)
        
        f[0][0] = 0
        for i in range(1, n + 1):
            for j in range(1, min(i, m) + 1):
                for k in range(i):
                    f[i][j] = min(f[i][j], max(f[k][j - 1], sub[i] - sub[k]))
        
        return f[n][m]


class Solution:
    def find_max(self, nums, n, result_dict):
        result = sum(nums)
        for i in range(n, len(nums)):
            if not (i, n-1) in result_dict:
                result_dict[(i, n-1)] = self.find_max(nums[:i], n-1, result_dict)
            result = min(max(result_dict[(i, n-1)], sum(nums[i:])), result)
        return result

    def binary_search(self, nums):
        if len(nums) == 2:
            return max(nums)
        left = 0
        right = len(nums)-1
        sum_half = sum(nums)//2
        while right > left+1:
            mid = left+(right-left)//2
            if sum(nums[0:mid]) >= sum_half:
                right = mid
            else:
                left = mid
        return min(sum(nums[0:right]), sum(nums[left:]))

    def splitArray(self, nums, m: int) -> int:
        if m == 1:
            return sum(nums)
        if m == 2:
            return self.binary_search(nums)
        result_dict = {}
        for i in range(2, len(nums)-m+3):
            result_dict[(i, 1)] = self.binary_search(nums[:i])
        return self.find_max(nums, m-1, result_dict)

#%%
Solution().splitArray([2,3,1,1,1,1,1], 5)

# %%
