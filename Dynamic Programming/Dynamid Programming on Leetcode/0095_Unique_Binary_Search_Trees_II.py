'''
@Author: Xinsheng Guo
@Time: 2021年1月5日11:18:32
@File: 0095_Unique_Binary_Search_Trees_II.py
@Link: https://leetcode-cn.com/problems/unique-binary-search-trees-ii/
@Tag: Tree; Dynamic Programming
'''
#
# @lc app=leetcode.cn id=95 lang=python3
#
# [95] 不同的二叉搜索树 II
#%%
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
# @lc code=start
# Definition for a binary tree node.
# 
#%%
class Solution:
    def trees(self, lower, upper):
        result = []
        for val in range(lower, upper):
            for left in self.trees(lower, val):
                for right in self.trees(val+1, upper):
                    result.append(TreeNode(val, left, right))
        return result or [None]

    def generateTrees(self, n: int):
        if n:
            return self.trees(1, n+1)
        else:
            return []
# @lc code=end
#%%
Solution().generateTrees(0)
#%%
if [None]:
    print(1)
# %%
