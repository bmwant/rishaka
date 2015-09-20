__author__ = 'Most Wanted'
from pentagon import Field, Piece, PIECE2

field = Field()

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
