import numpy as np
from board import Board, Move

class Piece(object):
	def __init__(self, board, x, y, color):
		self.board=board
		self.x=x
		self.y=y
		self.color = color
		if self.color=='white':
			self.direction=1
		elif self.color=='black':
			self.direction=-1
		else:
			print(self.color+"?")

	@property
	def pos(self):
		return (self.x, self.y)

class Pawn(Piece):
	def __init__(self, board, x, y, color):
		super().__init__(board, x, y, color)
		self.first_move=True
		self.name='P'
		self.worth = 1

	def generate_moves(self):
		moves=[]
		move_paths = []

		if self.first_move:
			move_paths.append(Move(self, self.x, self.y+2*self.direction).get_path_moves(include_end=True, takes=False))
		else:
			moves.append(Move(self, self.x,self.y+self.direction, takes=False))

		foo = self.board.get_piece(self.x+1,self.y+self.direction)
		if foo is not None:
			if foo.direction==-self.direction:
				moves.append(Move(self, self.x+1,self.y+self.direction))

		foo = self.board.get_piece(self.x-1,self.y+self.direction)
		if foo is not None:
			if foo.direction==-self.direction:
				moves.append(Move(self, self.x-1,self.y+self.direction))

		return self.board.prune_legal(moves, move_paths)

class King(Piece):
	def __init__(self, board, x, y, color):
		super().__init__(board, x, y, color)
		self.name = 'K'
		self.worth = 999

	def generate_moves(self):
		moves = []

		moves.append(Move(self, self.x + 1, self.y + 1))
		moves.append(Move(self, self.x + 1, self.y + 0))
		moves.append(Move(self, self.x + 1, self.y - 1))

		moves.append(Move(self, self.x + 0, self.y + 1))

		moves.append(Move(self, self.x + 0, self.y - 1))

		moves.append(Move(self, self.x - 1, self.y + 1))
		moves.append(Move(self, self.x - 1, self.y + 0))
		moves.append(Move(self, self.x - 1, self.y - 1))


		return self.board.prune_legal(moves, [])

class Queen(Piece):
	def __init__(self, board, x, y, color):
		super().__init__(board, x, y, color)
		self.name = 'Q'
		self.worth = 9

	def generate_moves(self):
		moves = []
		move_paths = []

		move_paths.append(Move(self, self.x, 7).get_path_moves(include_end=True))
		move_paths.append(Move(self, self.x, 0).get_path_moves(include_end=True))
		move_paths.append(Move(self, 7, self.y).get_path_moves(include_end=True))
		move_paths.append(Move(self, 0, self.y).get_path_moves(include_end=True))

		move_paths.append(Move(self, self.x + 7, self.y + 7).get_path_moves(include_end=True))
		move_paths.append(Move(self, self.x + 7, self.y - 7).get_path_moves(include_end=True))
		move_paths.append(Move(self, self.x - 7, self.y + 7).get_path_moves(include_end=True))
		move_paths.append(Move(self, self.x - 7, self.y - 7).get_path_moves(include_end=True))

		return self.board.prune_legal(moves, move_paths)

class Bishop(Piece):
	def __init__(self, board, x, y, color):
		super().__init__(board, x, y, color)
		self.name = 'B'
		self.worth = 3

	def generate_moves(self):
		moves = []
		move_paths = []

		move_paths.append(Move(self, self.x + 7, self.y + 7).get_path_moves(include_end=True))
		move_paths.append(Move(self, self.x + 7, self.y - 7).get_path_moves(include_end=True))
		move_paths.append(Move(self, self.x - 7, self.y + 7).get_path_moves(include_end=True))
		move_paths.append(Move(self, self.x - 7, self.y - 7).get_path_moves(include_end=True))

		return self.board.prune_legal(moves, move_paths)

class Knight(Piece):
	def __init__(self, board, x, y, color):
		super().__init__(board, x, y, color)
		self.name = 'N'
		self.worth = 3

	def generate_moves(self):
		moves = []

		moves.append(Move(self, self.x + 2, self.y + 1))
		moves.append(Move(self, self.x + 2, self.y - 1))
		moves.append(Move(self, self.x - 2, self.y + 1))
		moves.append(Move(self, self.x - 2, self.y - 1))

		moves.append(Move(self, self.x + 1, self.y + 2))
		moves.append(Move(self, self.x + 1, self.y - 2))
		moves.append(Move(self, self.x - 1, self.y + 2))
		moves.append(Move(self, self.x - 1, self.y - 2))

		return self.board.prune_legal(moves, [])

class Rook(Piece):
	def __init__(self, board, x, y, color):
		super().__init__(board, x, y, color)
		self.name = 'R'
		self.worth = 5

	def generate_moves(self):
		moves = []
		move_paths = []

		move_paths.append(Move(self, self.x, 7).get_path_moves(include_end=True))
		move_paths.append(Move(self, self.x, 0).get_path_moves(include_end=True))
		move_paths.append(Move(self, 7, self.y).get_path_moves(include_end=True))
		move_paths.append(Move(self, 0, self.y).get_path_moves(include_end=True))

		return self.board.prune_legal(moves, move_paths)