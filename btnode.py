class Node:
    """
    This class stores gamefield in a particular moment.
    """
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right
