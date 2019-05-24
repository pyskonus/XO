from board import Board


class InvalidPosition(Exception):
    """
    Represents an exception when user gives a number too large or less than
    or equal to 0 for any of position integers
    """
    pass


class OccupiedPosition(Exception):
    """
    Represents an exception when user gives a position that is already occupied
    """
    pass


def input_pos(board):
    # input a valid position
    pos = ''
    while not pos:
        try:
            pos = input("Input position (for example, \'3 1\') ")
            pos = (int(pos.split()[0]) - 1, int(pos.split()[1]) - 1)
            if pos[0] > 2 or pos[0] < 0 or pos[1] > 2 or pos[1] < 0:
                pos = ''
                raise InvalidPosition
            if pos not in board.free_positions():
                raise OccupiedPosition

        except InvalidPosition:
            pos = ''
            print("The position integers must be in range from 1 to 3")
        except OccupiedPosition:
            pos = ''
            print("You have entered a position that is already occupied")
        except ValueError:
            pos = ''
            print("The position must be two integers separated by a comma")

    return pos


def main():
    side = input("Do you want to make the first move? (y for yes) ")
    b = Board(lastsign=False)

    if side == 'y':
        b.make_move(input_pos(b))
        print(b)
        print('---')
    else:
        b.lastsign = not b.lastsign

    while True:
        b.lastsign = not b.lastsign
        b.choose_way()
        print(b)
        print('---')
        if b.check() is not None:
            break
        b.make_move(input_pos(b))
        print(b)
        print('---')
        if b.free_positions() == []:
            break
        if b.check() is not None:
            break


if __name__ == "__main__":
    main()
