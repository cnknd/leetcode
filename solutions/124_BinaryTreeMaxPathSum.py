# problem: https://leetcode.com/problems/binary-tree-maximum-path-sum/

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

# strategy: The first throught is that we want to use recursion, something like
#           maxPathSum(root) = maxPathSum(root.left) + maxPathSum(root.right) + root.val
#           But immediately we can see some issues with this:
#           * the best path might not go through root (especially if root has negative value)
#           * the best path in either subtree might not go through the root of that subtree,
#             in which case we can't even consider adding current root to the path.
#           * the best path in either subtree might span both sub-subtrees, in which case
#             again we can't consider adding current root to the path.
#
# To make things manageable, we can keep track of the max path sum in each of these cases. 
# Specifically, we want 3 max path sums at each node: 
#           1) one that spans both left and right subtrees through the node
#           2) one that only spans on subtree (still goes through node)
#           3) and one that doesn't go through the node at all
#           this is sufficient for recursion:
#           at any node, max1(node) = max2(left) + max2(right) + node.val if both exist, otherwise it's None
#                        max2(node) = max(max2(left), max2(right)) + node.val
#                        max3(node) = max(max1(left), max1(right), max2(left), max2(right), max3(left), max3(right))
# Now to get the max path sum of the full tree, we evaluate these 3 maximums at rootand pick the max among these 3


def max_with_none(vals):
    return max([v for v in vals if v is not None])


class Solution:
    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        if root is None:
            return 0
        else:
            return max_with_none(self.maxPathSumHelper(root))

    def maxPathSumHelper(self, root: Optional[TreeNode]) -> int:
        if root.left is None and root.right is None:
            ms1 = None
            ms2 = root.val
            ms3 = None
        elif root.left is None:
            ms1 = None
            right1, right2, right3 = self.maxPathSumHelper(root.right)
            ms2 = max(right2, 0) + root.val
            ms3 = max_with_none([right1, right2, right3])
        elif root.right is None:
            ms1 = None
            left1, left2, left3 = self.maxPathSumHelper(root.left)
            ms2 = max(left2, 0) + root.val
            ms3 = max_with_none([left1, left2, left3])
        else:
            left1, left2, left3 = self.maxPathSumHelper(root.left)
            right1, right2, right3 = self.maxPathSumHelper(root.right)
            ms1 = left2 + right2 + root.val
            ms2 = max(left2, right2, 0) + root.val
            ms3 = max_with_none([left1, left2, left3, right1, right2, right3])
        return ms1, ms2, ms3