# -*- coding: utf-8 -*-
__author__ = 'Most Wanted'
import warnings

from warnings import warn

from colorama import init
from colorama import Fore, Back, Style


init(autoreset=True)
warnings.simplefilter('always')


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

    def __str__(self):
        result = ''
        for row in self.SHAPE:
            result += ''.join(row) + '\n'
        #result += '\n'
        return result

    def can_locate_piece(self, piece, i_row: int, i_col: int) -> bool:
        pos = (i_row + i_col) % 2
        upper_left = piece[0][0]
        if pos == 1 and upper_left == '^':
            warn('Parity mismatch for up triangle')
            return False

        if pos == 0 and upper_left == 'V':
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
                print(color + self.SHAPE[i][j], end='')
            print()


PIECE1 = [
    ['v', '^', 'v'],
    ['^', 'v', '^'],
]

PIECE2 = [
    ['^', 'v', '^'],
    ['v', '^', 'v'],
]


class Piece(object):
    COLORS = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE]
    TOTAL_PIECES = 0

    def __init__(self, shape):
        self.shape = shape
        self.TOTAL_PIECES += 1
        color_index = len(self.COLORS) % self.TOTAL_PIECES
        self.color = self.COLORS[color_index]

    def __str__(self):
        result = ''
        for row in self.shape:
            result += ''.join(row) + '\n'
        return result

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


def rotate_piece(piece):
    """
    Rotate piece clockwise and return resulting piece
    :param piece: piece to rotate
    :param rotation_point: starting point to rotate around
    :return: rotated piece
    """
    # Find first non-empty point for top-left
    fi, fj = 0, 0
    found = False
    for i in range(piece.height):
        for j in range(piece.width):
            if piece[i][j] != Field.EMPTY:
                fi = i
                fj = j
                found = True
                break
        if found:
            break
    if not found:
        raise ValueError('Empty piece')

    rotation_point = (fi, fj)
    print(rotation_point)
    used = [rotation_point]
    new_coords = [[0, 0]]
    queue = [rotation_point]
    while queue:
        i, j = queue.pop()  # current location
        current_point = piece[i][j]
        li, lj = new_coords[-1]  # last new coordinates of parent

        if current_point == '^':  # look for left, right, and bottom
            if j-1 >= 0 and piece[i][j-1] != Field.EMPTY:  # look left
                new_point = (i, j-1)
                if new_point not in used:
                    queue.append(new_point)
                    used.append(new_point)
                    # left moves on top
                    new_coords.append([li-1, lj])

            if j+1 < piece.width and piece[i][j+1] != Field.EMPTY:  # look right
                new_point = (i, j+1)
                if new_point not in used:
                    queue.append(new_point)
                    used.append(new_point)
                    # right moves right
                    new_coords.append([li, lj+1])

            if i+1 < piece.height and piece[i+1][j] != Field.EMPTY:  # look beneath
                new_point = (i+1, j)
                if new_point not in used:
                    queue.append(new_point)
                    used.append(new_point)
                    # bottom moves left
                    new_coords.append([li, lj-1])

        if current_point == 'v':  # look for left, right and top
            if j-1 >= 0 and piece[i][j-1] != Field.EMPTY:  # look left
                new_point = (i, j-1)
                if new_point not in used:
                    queue.append(new_point)
                    used.append(new_point)
                    # left moves left
                    new_coords.append([li, lj-1])

            if j+1 < piece.width and piece[i][j+1] != Field.EMPTY:  # look right
                new_point = (i, j+1)
                if new_point not in used:
                    queue.append(new_point)
                    used.append(new_point)
                    # right moves down
                    new_coords.append([li+1, lj])

            if i-1 >= 0 and piece[i-1][j] != Field.EMPTY:  # look upward
                new_point = (i-1, j)
                if new_point not in used:
                    queue.append(new_point)
                    used.append(new_point)
                    # top moves right
                    new_coords.append([li, lj+1])

    # All coordinates translated, now normalize them
    min_i = 0
    min_j = 0
    max_i = 0
    max_j = 0

    for coord in new_coords:
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
    for coord in new_coords:
        coord[0] -= min_i
        coord[1] -= min_j

    # Size of field for rotated piece
    max_i -= min_i
    max_j -= min_j

    # Now move all points to their new locations with changing the direction
    new_shape = [[Field.EMPTY for j in range(max_j+1)] for i in range(max_i+1)]
    for old_p, new_p in zip(used, new_coords):
        print('%s -> %s' % (old_p, new_p))
        elem = piece[old_p[0]][old_p[1]]
        if elem == '^':
            new_shape[new_p[0]][new_p[1]] = 'v'

        if elem == 'v':
            new_shape[new_p[0]][new_p[1]] = '^'

    new_piece = Piece(new_shape)
    return new_piece


if __name__ == '__main__':
    field = Field()
    """
    print(field)
    print(field.width)
    print(field.height)

    piece = Piece(PIECE2)
    print(piece)
    print(piece.width)
    print(piece.height)

    # True
    print('===========All to be true============')
    print(field.can_locate_piece(piece, 0, 2))
    print(field.can_locate_piece(piece, 1, 1))
    print(field.can_locate_piece(piece, 2, 0))
    print(field.can_locate_piece(piece, 3, 1))
    print(field.can_locate_piece(piece, 4, 2))

    print(field.can_locate_piece(piece, 0, 6))
    print(field.can_locate_piece(piece, 1, 7))
    print(field.can_locate_piece(piece, 2, 8))
    print(field.can_locate_piece(piece, 3, 7))
    print(field.can_locate_piece(piece, 4, 6))

    # False
    print('===========All to be false============')
    print(field.can_locate_piece(piece, 0, 7))
    print(field.can_locate_piece(piece, 1, 8))
    print(field.can_locate_piece(piece, 0, 0))
    print(field.can_locate_piece(piece, 0, 1))
    print(field.can_locate_piece(piece, 1, 0))
    print(field.can_locate_piece(piece, 5, 1))
    print(field.can_locate_piece(piece, 5, 10))

    field.place_piece(piece, 0, 2)
    field.place_piece(piece, 0, 6)
    print(field)
    """
    piece1 = Piece(PIECE1)
    print(piece1)
    pr1 = rotate_piece(piece1)
    pr2 = rotate_piece(pr1)
    field.place_piece(piece1, 0, 1)
    field.print_me()
