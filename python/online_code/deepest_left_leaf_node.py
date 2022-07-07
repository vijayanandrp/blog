class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


def deepestLeftLeafUtil(root, lvl, max_level, isLeft):
    if root is None:
        return
    if isLeft is True:
        if not root.left and not root.right:
            if lvl > max_level:
                deepestLeftLeafUtil.node = root
                max_level = lvl
                return
    deepestLeftLeafUtil(root.left, lvl + 1, max_level, True)
    deepestLeftLeafUtil(root.right, lvl + 1, max_level, False)




root = Node(1)
root.left = Node(2)
root.right = Node(3)
root.left.left = Node(4)
root.right.left = Node(5)
root.right.right = Node(6)
root.right.left.right = Node(7)
root.right.right.right = Node(8)
root.right.left.right.left = Node(9)
root.right.right.right.right = Node(10)



max_level = 0
deepestLeftLeafUtil.node = None
deepestLeftLeafUtil(root, 0, max_level, False)
result = deepestLeftLeafUtil.node

if result is None:
    print("There is not left leaf in the given tree")
else:
    print("The deepst left child is", result.data)

# This code is contributed by Nikhil Kumar Singh(nickzuck_007)
