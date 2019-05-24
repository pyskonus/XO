from random import choice
from copy import deepcopy
from time import sleep
from btnode import Node
from btree import Tree


class Board:
    """
    A class for storing the game board. Contains a list of lists of cells and
    two other values - last changed cell position and a boolean value that
    represents the player who changed it.
    """
    def __init__(self, cells = [[None] * 3, [None] * 3, [None] * 3], lastsign=True):
        self.cells = cells
        # self.lastpos = None
        self.lastsign = lastsign    # True for X and False for O

    def check(self):
        """
        Returns 1 if X won, -1 if O won and 0 if it is draw. If none of
        mentioned above happened, returns None.
        """
        for i in range(3):
            # check vertical
            if self.cells[0][i] == self.cells[1][i] == self.cells[2][i]:
                if self.cells[0][i] == 'X':
                    return 1
                elif self.cells[0][i] == 'O':
                    return -1

            # check horizontal
            if self.cells[i][0] == self.cells[i][1] == self.cells[i][2]:
                if self.cells[i][0] == 'X':
                    return 1
                elif self.cells[i][0] == 'O':
                    return -1

        # check diagonal
        if (self.cells[0][0] == self.cells[1][1] == self.cells[2][2]) or \
           (self.cells[0][2] == self.cells[1][1] == self.cells[2][0]):
            if self.cells[1][1] == 'X':
                return 1
            elif self.cells[1][1] == 'O':
                return -1

        # check draw
        for i in range(3):
            for j in range(3):
                if self.cells[i][j] is None:
                    return None

        return 0

    def __str__(self):
        return '\n'.join(list(map(lambda y: ''.join(list(map(lambda x: ' ' if x is None else x, y))), self.cells)))

    def build_tree(self):
        dct = {True: 'X', False: 'O'}
        root = Node(self, None, None)
        positions = self.free_positions()
        if len(positions) == 1:
            cursign = not self.lastsign    # change the sign
            cells = self.cells
            cells[positions[0][0]][positions[0][1]] = dct[cursign]
            newBoard = Board(cells, cursign)
            root.left = (newBoard, 0)
            root.right = (newBoard, newBoard.check())
        else:
            # in this case, number of free positions >= 2
            cursign = not self.lastsign    # change the sign
            cells1 = deepcopy(self.cells)
            cells2 = deepcopy(self.cells)
            cell1 = choice(positions)
            positions.pop(positions.index(cell1)) # pop to get different choice
            cell2 = choice(positions)
            cells1[cell1[0]][cell1[1]] = dct[cursign]
            cells2[cell2[0]][cell2[1]] = dct[cursign]
            newBoard1 = Board(cells1, cursign)
            newBoard2 = Board(cells2, cursign)
            if newBoard1.check() is not None:
                root.left = (newBoard1, newBoard1.check())
            else:
                root.left = Board.build_tree(newBoard1).root
            if newBoard2.check() is not None:
                root.right = (newBoard2, newBoard2.check())
            else:
                root.right = Board.build_tree(newBoard2).root

        return Tree(root)

    def choose_way(self):
        """
        Makes a move that is more likely to lead to win
        """
        res1 = self.build_tree().root.left
        res2 = self.build_tree().root.right
        t1 = Tree(res1)
        t2 = Tree(res2)
        if t1.compute_sum() > t2.compute_sum():
            if isinstance(res1, tuple):
                self.cells = deepcopy(res1[0].cells)
            else:
                self.cells = deepcopy(t1.root.value.cells)
        else:
            if isinstance(res2, tuple):
                self.cells = deepcopy(res2[0].cells)
            else:
                self.cells = deepcopy(t2.root.value.cells)

    def make_move(self, pos):
        dct = {False: 'X', True: 'O'}
        self.lastsign = not self.lastsign
        self.cells[pos[0]][pos[1]] = dct[self.lastsign]

    # non-public
    def free_positions(self):
        res = []
        for i in range(3):
            for j in range(3):
                if self.cells[i][j] is None:
                    res.append((i, j))

        return res


# b = Board()
# t = b.build_tree()
# print(t.compute_sum())
