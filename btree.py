class Tree:
    """
    This class represents a tree that is used in the XO game.
    """
    def __init__(self, root=None):
        self.root = root

    def inorder(self):
        # code from linkedbst.py file
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if isinstance(node, tuple):
                lyst.append(node)
            else:
                recurse(node.left)
                lyst.append(node.value)
                recurse(node.right)

        recurse(self.root)
        return iter(lyst)

    def compute_sum(self):
        # computes sum of scores of leaves that are children of given vertice
        res = 0

        for el in self.inorder():
            if isinstance(el, tuple):
                res += el[1]

        return res
