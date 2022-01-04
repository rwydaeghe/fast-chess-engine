import numpy as np
from board import Board, Move
from pieces import Pawn, King, Queen, Knight, Bishop, Rook

board = Board()

'''
board.add_pawn(4, 4, 'white')

board.add_pawn(4+2, 4, 'white')
board.add_pawn(4+2, 4+2, 'white')
board.add_pawn(4, 4+2, 'white')
board.add_pawn(4-2, 4, 'white')
board.add_pawn(4-2, 4-2, 'white')
board.add_pawn(4, 4-2, 'white')
board.add_pawn(4+2, 4-2, 'white')
board.add_pawn(4-2, 4+2, 'white')

for i in Move(board.pieces[0], 1, 7).get_path_moves():
	print(i.x, i.y)

print("--")
for i in board.prune_legal(Move(board.pieces[0], 1, 7).get_path_moves()):
	print(i.x, i.y)
'''

'''
board.add_piece(Rook(board,4,4,'white'))
board.add_piece(Pawn(board,4+2, 4, 'white'))
board.add_piece(Pawn(board,4+2, 4+2, 'white'))
board.add_piece(Pawn(board,4, 4+2, 'black'))
#board.add_piece(Pawn(board,4-2, 4, 'white'))
#board.add_piece(Pawn(board,4-2, 4-2, 'white'))
board.add_piece(Pawn(board,4, 4-2, 'white'))
board.add_piece(Pawn(board,4+2, 4-2, 'black'))
board.add_piece(Pawn(board,4-2, 4+2, 'white'))
'''

'''
board.add_piece(Pawn(board,3, 4, 'white'))
board.add_piece(Pawn(board,4, 4, 'white'))
board.add_piece(Pawn(board,5, 4, 'white'))

board.add_piece(Pawn(board,3, 6, 'black'))
board.add_piece(Pawn(board,4, 6, 'black'))
board.add_piece(Pawn(board,5, 6, 'black'))
'''

board.add_all_pieces()
board.print()

board.current_eval = board.eval

white_player = 'PC'
black_player = 'PC'

board.start_game(white_player, black_player)
