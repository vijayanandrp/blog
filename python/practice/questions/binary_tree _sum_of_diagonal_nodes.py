"""
Diagonal Sum of a Binary Tree

                            1
                       /        \
                     2           3
                   /   \       /   \
                  9     6     4     5
                  \     /    /  \
                  10   11   12   7

"""


class BinaryTree:
    def __init__(self, data):
        self.data = data
        self.left = self.right = None


def diagonal_recursive(root, distance, store):
    if not root:
        return

    print('data - {} distance - {}'. format(root.data, distance))
    if distance in store.keys():
        store[distance] += root.data
    else:
        store[distance] = root.data

    # since we cut diagonally from left side the left node will get incremental
    diagonal_recursive(root.left, distance + 1, store)
    diagonal_recursive(root.right, distance, store)


def diagonal_sum(root):
    store = dict()
    distance = 0
    diagonal_recursive(root, distance, store)

    print('Diagonal sum of values - ', store.values())


if __name__ == '__main__':
    root = BinaryTree(1)
    root.left = BinaryTree(2)
    root.right = BinaryTree(3)
    root.left.left = BinaryTree(9)
    root.left.right = BinaryTree(6)
    root.right.left = BinaryTree(4)
    root.right.right = BinaryTree(5)
    root.right.left.right = BinaryTree(7)
    root.right.left.left = BinaryTree(12)
    root.left.right.left = BinaryTree(11)
    root.left.left.right = BinaryTree(10)

    diagonal_sum(root)
