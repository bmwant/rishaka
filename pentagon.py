# -*- coding: utf-8 -*-
__author__ = 'Most Wanted'
import copy
import warnings

from warnings import warn

from colorama import init
from colorama import Fore, Back, Style


init(autoreset=True)
warnings.simplefilter('ignore')


class Field(object):
    SHAPE = [
        ['#', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#', '#'],
        ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
        ['#', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#', '#'],
    ]
    EMPTY = ' '

    @property
    def width(self):
        # Assuming that all rows are of the same width
        return len(self.SHAPE[0])

    @property
    def height(self):
        return len(self.SHAPE)

    def __init__(self):
        self.pieces = {}  # Contains top left position of piece on the field as key and a piece as value

    def __getitem__(self, index):
        return self.SHAPE[index]

    def __str__(self):
        result = ''
        for row in self.SHAPE:
            result += ''.join(row) + '\n'
        #result += '\n'
        return result

    def can_locate_piece(self, piece, i_row: int, i_col: int) -> bool:
        col_pos, first_item = piece.get_first_row_item()

        pos = (i_row + i_col + col_pos) % 2

        if pos == 1 and first_item == '^':
            warn('Parity mismatch for up triangle')
            return False

        if pos == 0 and first_item == 'v':
            warn('Parity mismatch for down triangle')
            return False

        if i_col + piece.width > self.width:
            warn('To long for field')
            return False

        if i_row + piece.height > self.height:
            warn('To high for field')
            return False

        field = self.SHAPE
        for i in range(piece.height):
            for j in range(piece.width):
                if piece[i][j] == self.EMPTY:
                    continue
                i_field = i_row + i
                j_field = i_col + j
                if field[i_field][j_field] != self.EMPTY:
                    return False
        return True
    
    def place_piece(self, piece, i_row, i_col):
        if not self.can_locate_piece(piece, i_row, i_col):
            return
        
        field = self.SHAPE
        for i in range(piece.height):
            for j in range(piece.width):
                i_field = i_row + i
                j_field = i_col + j
                field[i_field][j_field] = piece[i][j]

        piece_location = (i_row, i_col)
        self.pieces[piece_location] = piece

    def get_color(self, i, j):
        for location, piece in self.pieces.items():
            p_i, p_j = location
            rel_i = i - p_i
            rel_j = j - p_j
            if 0 <= rel_i < piece.height and 0 <= rel_j < piece.width:
                if piece.check_hit(rel_i, rel_j):
                    return piece.color
        return ''

    def print_me(self):
        for i in range(self.height):
            for j in range(self.width):
                color = self.get_color(i, j)
                if self[i][j] == Field.EMPTY:
                    print('_', end='')
                else:
                    print(color + self[i][j], end='')
            print()


PIECE1 = [
    ['v', '^', 'v'],
    ['^', 'v', '^'],
]

PIECE2 = [
    ['^', 'v', '^'],
    ['v', '^', 'v'],
]

PIECE3 = [
    ['v', '^', 'v', '^', 'v', '^']
]

PIECE4 = [
    ['^', ' ', ' ', ' ', ' '],
    ['v', '^', 'v', '^', 'v'],
]

PIECE5 = [
    [' ', ' ', '^', 'v', '^'],
    ['v', '^', 'v', ' ', ' '],
]

PIECE6 = [
    ['v', '^', 'v', ' '],
    [' ', 'v', '^', 'v'],
]

PIECE7 = [
    [' ', ' ', ' ', '^', ' '],
    ['^', 'v', '^', 'v', '^'],
]

PIECE8 = [
    ['v', '^', ' ', ' ', ' '],
    [' ', 'v', '^', 'v', '^'],
]

PIECE9 = [
    [' ', '^', ' '],
    [' ', 'v', '^'],
    ['v', '^', 'v'],
]


class Piece(object):
    COLORS = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE]
    TOTAL_PIECES = 0

    def __init__(self, shape, color=None):
        self.shape = shape
        if color is None:
            color_index = Piece.TOTAL_PIECES % len(self.COLORS)
            Piece.TOTAL_PIECES += 1
            self.color = self.COLORS[color_index]
        else:
            # It's just a rotation of itself
            self.color = color

    def __str__(self):
        result = ''
        for row in self.shape:
            result += ''.join(row) + '\n'
        return result

    def __eq__(self, other):
        return self.shape == other.shape

    @property
    def width(self):
        max_width = 0
        for row in self.shape:
            if len(row) > max_width:
                max_width = len(row)
        return max_width

    @property
    def height(self):
        return len(self.shape)
    
    def __getitem__(self, index):
        return self.shape[index]

    def check_hit(self, i, j):
        if self.shape[i][j] != Field.EMPTY:
            return True
        return False

    def get_first_row_item(self):
        for index in range(self.width):
            if self[0][index] != Field.EMPTY:
                return index, self[0][index]

    def get_rotation_point(self):
        # Find first non-empty point from top-left in first row
        for j in range(self.width):
            if self[0][j] != Field.EMPTY:
                return 0, j

        raise ValueError('Corrupted piece. First row is empty')

    def print_me(self):
        for i in range(self.height):
            for j in range(self.width):
                print(self.color + self[i][j], end='')
            print()


def rotate_piece(piece):
    """
    Rotate piece clockwise and return resulting piece
    :param piece: piece to rotate
    :param rotation_point: starting point to rotate around
    :return: rotated piece
    """
    rotation_point = piece.get_rotation_point()
    # print('Rotate around', rotation_point)
    ni, nj = rotation_point
    new_coords = {
        rotation_point: [ni, nj]
    }  # begin from rotation points
    queue = [rotation_point]
    while queue:
        i, j = queue.pop()  # current location
        current_point = piece[i][j]
        li, lj = new_coords[(i, j)]

        if current_point == '^':  # look for left, right, and bottom
            if j-1 >= 0 and piece[i][j-1] != Field.EMPTY:  # look left
                new_point = (i, j-1)
                if new_point not in new_coords:
                    queue.append(new_point)
                    # left moves on top
                    new_coords[new_point] = [li-1, lj]

            if j+1 < piece.width and piece[i][j+1] != Field.EMPTY:  # look right
                new_point = (i, j+1)
                if new_point not in new_coords:
                    queue.append(new_point)
                    # right moves right
                    new_coords[new_point] = [li, lj+1]

            if i+1 < piece.height and piece[i+1][j] != Field.EMPTY:  # look beneath
                new_point = (i+1, j)
                if new_point not in new_coords:
                    queue.append(new_point)
                    # bottom moves left
                    new_coords[new_point] = [li, lj-1]

        if current_point == 'v':  # look for left, right and top
            if j-1 >= 0 and piece[i][j-1] != Field.EMPTY:  # look left
                new_point = (i, j-1)
                if new_point not in new_coords:
                    queue.append(new_point)
                    # left moves left
                    new_coords[new_point] = [li, lj-1]

            if j+1 < piece.width and piece[i][j+1] != Field.EMPTY:  # look right
                new_point = (i, j+1)
                if new_point not in new_coords:
                    queue.append(new_point)
                    # right moves down
                    new_coords[new_point] = [li+1, lj]

            if i-1 >= 0 and piece[i-1][j] != Field.EMPTY:  # look upward
                new_point = (i-1, j)
                if new_point not in new_coords:
                    queue.append(new_point)
                    # top moves right
                    new_coords[new_point] = [li, lj+1]

    # for old_p, new_p in new_coords.items():
    #     print('::%s->%s' % (old_p, new_p))
    # All coordinates translated, now normalize them
    min_i = 0
    min_j = 0
    max_i = 0
    max_j = 0

    for coord in new_coords.values():
        i, j = coord
        if i < min_i:
            min_i = i
        elif i > max_i:
            max_i = i

        if j < min_j:
            min_j = j
        elif j > max_j:
            max_j = j

    # Normalize coords
    for old_p in new_coords:
        new_coords[old_p][0] -= min_i
        new_coords[old_p][1] -= min_j

    # Size of field for rotated piece
    max_i -= min_i
    max_j -= min_j

    # Now move all points to their new locations with changing the direction
    new_shape = [[Field.EMPTY for j in range(max_j+1)] for i in range(max_i+1)]
    for old_p, new_p in new_coords.items():
        # print('%s -> %s' % (old_p, new_p))
        old_i, old_j = old_p
        new_i, new_j = new_p
        elem = piece[old_i][old_j]
        if elem == '^':
            new_shape[new_i][new_j] = 'v'

        if elem == 'v':
            new_shape[new_i][new_j] = '^'

    new_piece = Piece(new_shape, color=piece.color)
    return new_piece


def piece_rotation(piece):
    """
    Yield rotated piece while rotation produces unique elements
    """
    initial_piece = piece
    while True:
        yield piece
        piece = rotate_piece(piece)
        if piece == initial_piece:
            return


class Game(object):
    def __init__(self, field, pieces):
        self.field = field
        self.pieces = pieces

    def solve(self):
        self.locate_next(self.field, self.pieces)

    def locate_next(self, field, pieces):
        if not pieces:  # No pieces available
            print('Solution found!')
            field.print_me()
            return

        piece = pieces.pop()
        print('Trying to locate on field:')
        print(piece)
        for i in range(field.height):
            for j in range(field.width):
                if field[i][j] == Field.EMPTY:
                    for rp in piece_rotation(piece):
                        if field.can_locate_piece(rp, i, j):
                            same_field = copy.deepcopy(field)
                            same_field.place_piece(rp, i, j)
                            same_field.print_me()
                            self.locate_next(same_field, pieces)


if __name__ == '__main__':
    field = Field()
    pieces = [Piece(globals().get('PIECE%d' % num)) for num in range(1, 10)]

    g = Game(field, pieces)
    g.solve()
