import numpy as np
import sys
from copy import copy
from time import time
from tqdm import tqdm
#from numba import njit, jit, int32, bool_
#from numba.experimental import jitclass
#import numba as nb
#from functools import lru_cache
#from cachetools import cached

class Board(object):
	def __init__(self):
		self.pieces=[]
		self.taken_pieces=[]
		self.squares=np.empty((8,8),dtype=object)
		self.current_eval = None
		self.white_player = None
		self.black_player = None

	def play_turn(self, who, color):
		if who=='PC':
			start_time = time()
			move, _ = self.get_best_move(color, verbose=True, squares=self.squares_as_string)
			print('The move is:')
			move.print()
		elif who=='User':
			valid=False
			start_time = time()
			while not valid:
				move, OK = self.user_move()
				if not OK:
					valid=False
					continue
				print('The move is:')
				move.print()
				move_legal = False
				for available_move in move.piece.generate_moves():
					if move.piece == available_move.piece and move.start == available_move.start and move.stop == available_move.stop:
						move_legal=True
				if not move_legal:
					print("Illegal move. Try again.")
				elif self.white_player=='User' and move.piece.color=='black':
					print('You can not play with the black pieces, you play with white. Try again.')
				elif self.black_player=='User' and move.piece.color=='white':
					print('You can not play with the white pieces, you play with black. Try again.')
				else:
					valid=True

		stop_time = time()
		print('Execution/thinking time: %.2f s' % (stop_time - start_time))
		if move:
			undo_data = self.do_move(move)
			self.update_eval_after_do_move(undo_data)
			print("Eval: " + str(self.current_eval))
			self.print()
		else:
			print('No more moves: remise.')
			sys.exit()

	def user_move(self):
		print('Choose start x coordinate (0->7):')
		start_x = int(input())

		print('Choose start y coordinate (0->7):')
		start_y = int(input())

		print('Choose stop x coordinate (0->7):')
		stop_x = int(input())

		print('Choose stop y coordinate (0->7):')
		stop_y = int(input())

		foo = self.get_piece(start_x, start_y)
		if foo is not None:
			return Move(foo, stop_x, stop_y), True
		else:
			print("There is no piece at the start location.")
			return None, False

	def start_game(self, white_player, black_player):
		self.white_player=white_player
		self.black_player=black_player
		i=1
		while i<4:
			if i % 2 == 1:
				print("White plays move " + str(i) + "...")
				self.play_turn(white_player, 'white')
			else:
				print("Black plays move " + str(i) + "...")
				self.play_turn(black_player, 'black')
			i+=1

	def get_piece(self, x, y):
		if x>=0 and x<=7 and y>=0 and y<=7:
			return self.squares[x, y]
		else:
			return None
		'''
		for piece in self.pieces:
			if x==piece.x and y==piece.y:
				return piece
		return None
		'''

	def add_piece(self, piece):
		assert piece.x >= 0
		assert piece.x <= 7
		assert piece.y >= 0
		assert piece.y <= 7
		assert self.get_piece(piece.x, piece.y) is None
		self.pieces.append(piece)
		self.squares[piece.x, piece.y] = piece

	def add_pawn_lines(self):
		from pieces import Pawn

		self.add_piece(Pawn(self, 0, 1, 'white'))
		self.add_piece(Pawn(self, 1, 1, 'white'))
		self.add_piece(Pawn(self, 2, 1, 'white'))
		self.add_piece(Pawn(self, 3, 1, 'white'))
		self.add_piece(Pawn(self, 4, 1, 'white'))
		self.add_piece(Pawn(self, 5, 1, 'white'))
		self.add_piece(Pawn(self, 6, 1, 'white'))
		self.add_piece(Pawn(self, 7, 1, 'white'))

		self.add_piece(Pawn(self, 0, 6, 'black'))
		self.add_piece(Pawn(self, 1, 6, 'black'))
		self.add_piece(Pawn(self, 2, 6, 'black'))
		self.add_piece(Pawn(self, 3, 6, 'black'))
		self.add_piece(Pawn(self, 4, 6, 'black'))
		self.add_piece(Pawn(self, 5, 6, 'black'))
		self.add_piece(Pawn(self, 6, 6, 'black'))
		self.add_piece(Pawn(self, 7, 6, 'black'))

	def add_all_pieces(self):
		from pieces import Rook, Knight, Bishop, Queen, King

		self.add_pawn_lines()
		self.add_piece(Rook(self, 0, 0, 'white'))
		self.add_piece(Knight(self, 1, 0, 'white'))
		self.add_piece(Bishop(self, 2, 0, 'white'))
		self.add_piece(Queen(self, 3, 0, 'white'))
		self.add_piece(King(self, 4, 0, 'white'))
		self.add_piece(Bishop(self, 5, 0, 'white'))
		self.add_piece(Knight(self, 6, 0, 'white'))
		self.add_piece(Rook(self, 7, 0, 'white'))

		self.add_piece(Rook(self, 0, 7, 'black'))
		self.add_piece(Knight(self, 1, 7, 'black'))
		self.add_piece(Bishop(self, 2, 7, 'black'))
		self.add_piece(Queen(self, 3, 7, 'black'))
		self.add_piece(King(self, 4, 7, 'black'))
		self.add_piece(Bishop(self, 5, 7, 'black'))
		self.add_piece(Knight(self, 6, 7, 'black'))
		self.add_piece(Rook(self, 7, 7, 'black'))

	def generate_moves(self, color):
		moves=[]
		for piece in self.pieces:
			if piece.color == color:
				for move in piece.generate_moves():
					moves.append(move)
		return moves

	def generate_best_moves(self, color):
		if type(color) is int:
			if color==1:
				color='white'
			elif color==-1:
				color='black'

		moves = np.array(self.generate_moves(color))
		evals = np.zeros(len(moves))
		for i,move in enumerate(moves):
			undo_data = self.do_move(move)
			#evals[i] = self.eval
			self.update_eval_after_do_move(undo_data)
			evals[i] = self.current_eval
			self.undo_move(undo_data)
			self.update_eval_after_undo_move(undo_data)
		if color=='white':
			return list(moves[np.argsort(evals)[::-1]])
		elif color=='black':
			return list(moves[np.argsort(evals)])

	def prune_legal(self, moves, move_paths):
		illegal_moves=[]

		for move in moves:
			if move.x < 0 or move.x>7 or move.y<0 or move.y>7:
				illegal_moves.append(move)
				continue
			#foo = self.get_piece(move.x, move.y)
			foo = self.squares[move.x, move.y]
			if foo is not None:
				if move.piece.color==foo.color:
					illegal_moves.append(move)
					continue
				elif move.piece.color!=foo.color and move.takes==False:
					illegal_moves.append(move)
					continue
			'''
			for path_move in move.get_path_moves():
				if self.get_piece(path_move.x, path_move.y) is not None:
					illegal_moves.append(move)
					continue
			'''
		for i,path in enumerate(move_paths):
			for j,path_move in enumerate(path):
				if path_move.x < 0 or path_move.x > 7 or path_move.y < 0 or path_move.y > 7:
					break
				#foo = self.get_piece(path_move.x, path_move.y)
				foo = self.squares[path_move.x, path_move.y]
				if foo is not None:
					if path_move.piece.color == foo.color:
						break
					elif path_move.piece.color != foo.color and path_move.takes == False:
						break
					else:
						moves.append(path_move)
						break
				else:
					moves.append(path_move)

		illegal_moves = list(set(illegal_moves))

		for move in illegal_moves:
			moves.remove(move)

		return moves

	def do_move(self, move):
		undo_data = {'Move': move,
					 'It was a first move': False,
		             'Piece taken': False,
		             'Original position': None}
		if move.piece.name == 'P':
			if move.piece.first_move:
				move.piece.first_move = False
				undo_data['It was a first move'] = True
		foo = self.squares[move.x, move.y]
		if foo is not None and move.takes:
			self.pieces.remove(foo)
			undo_data['Piece taken'] = foo
		undo_data['Original position'] = copy(move.piece.pos)
		self.squares[move.piece.x, move.piece.y] = None
		self.squares[move.x, move.y] = move.piece
		move.piece.x = move.x
		move.piece.y = move.y

		return undo_data

	def undo_move(self, undo_data):
		if undo_data['It was a first move']:
			undo_data['Move'].piece.first_move=True
		foo = self.get_piece(undo_data['Move'].x, undo_data['Move'].y)
		#foo = self.squares[undo_data['Move'].x, undo_data['Move'].y]
		foo.x = undo_data['Original position'][0]
		foo.y = undo_data['Original position'][1]
		self.squares[foo.x, foo.y] = foo
		if undo_data['Piece taken'] is not False:
			self.pieces.insert(0,undo_data['Piece taken'])
			#self.pieces.append(undo_data['Piece taken'])
			self.squares[undo_data['Move'].x, undo_data['Move'].y] = undo_data['Piece taken']
		else:
			self.squares[undo_data['Move'].x, undo_data['Move'].y] = None

	def show_move(self, move):
		print('Showing move:')
		move.print()
		undo_data = self.do_move(move)
		self.print()
		self.undo_move(undo_data)

	@property
	def eval(self):
		eval = 0 #for white
		for piece in self.pieces:
			piece_eval=1

			if piece.x >= 1 and piece.x <= 6 and piece.y >= 1 and piece.y <= 6:
				piece_eval += 0.015
				if piece.x >= 2 and piece.x <= 5 and piece.y >= 2 and piece.y <= 5:
					piece_eval += 0.03
					if piece.x >= 3 and piece.x <= 4 and piece.y >= 3 and piece.y <= 4:
						piece_eval += 0.05

			eval += piece_eval*piece.worth*piece.direction

		return eval

	#https://stackoverflow.com/questions/41769100/how-do-i-use-numba-on-a-member-function-of-a-class
	#@staticmethod
	#@njit
	def piece_eval(self, x, y, dir, worth):
		eval=0

		if x >= 1 and x <= 6 and y >= 1 and y <= 6:
			eval += 0.015
			if x >= 2 and x <= 5 and y >= 2 and y <= 5:
				eval += 0.03
				if x >= 3 and x <= 4 and y >= 3 and y <= 4:
					eval += 0.05

		eval *= dir * worth

		return eval

	def update_eval_after_do_move(self, undo_data):
		undo_data['Old eval'] = self.current_eval
		new_eval = undo_data['Old eval']

		moved_piece = undo_data['Move'].piece
		moved_piece_start = undo_data['Move'].start
		moved_piece_stop = undo_data['Move'].stop
		if moved_piece.name != 'K':
			new_eval -= self.piece_eval(moved_piece_start[0], moved_piece_start[1], moved_piece.direction, moved_piece.worth)
			new_eval += self.piece_eval(moved_piece_stop[0], moved_piece_stop[1], moved_piece.direction, moved_piece.worth)

		if undo_data['Piece taken'] is not False:
			taken_piece = undo_data['Piece taken']

			new_eval -= taken_piece.worth*taken_piece.direction
			new_eval -= self.piece_eval(taken_piece.x, taken_piece.y, taken_piece.direction, taken_piece.worth)

		#new_eval = round(new_eval,3)

		self.current_eval = new_eval

	def update_eval_after_undo_move(self, undo_data):
		self.current_eval = undo_data['Old eval']

	#@cached(cache={})
	#@njit
	def get_best_move(self, color, depth=3, verbose=False, squares=None):
		if color=='white':
			color=1
		elif color=='black':
			color=-1

		eval = None
		best_move = None
		the_best_move = None

		best_moves = self.generate_best_moves(color)
		if verbose:
			best_moves = tqdm(best_moves)
		for move in best_moves:
			undo_data_move = self.do_move(move)
			self.update_eval_after_do_move(undo_data_move)
			#self.print()
			#print(self.current_eval)
			if depth!=0:
				best_move, eval_here = self.get_best_move(-color, depth-1, verbose=False, squares=self.squares_as_string)
				if best_move is not None:
					#print('ik beslis')
					undo_data = self.do_move(best_move)
					#eval_here = self.eval
					self.update_eval_after_do_move(undo_data)
					eval_here = self.current_eval
					#self.print()
					#print(self.current_eval)

					if eval is None:
						eval = eval_here
						the_best_move = move
					else:
						if color == 1 and eval_here >= eval:
							eval = eval_here
							the_best_move = move
						elif color == -1 and eval_here <= eval:
							eval = eval_here
							the_best_move = move
					self.undo_move(undo_data)
					self.update_eval_after_undo_move(undo_data)
				else:
					eval = eval_here
			elif depth==0:
				the_best_move = best_moves[0]
				#eval = self.eval
				#self.update_eval_after_do_move(undo_data_move)
				eval = self.current_eval
			self.undo_move(undo_data_move)
			self.update_eval_after_undo_move(undo_data_move)

		if verbose:
			print('\n')

		if the_best_move is None:
			return None, 0

		return the_best_move, eval

	@property
	def squares_as_string(self):
		str=''
		for i in range(8):
			for j in range(8):
				foo = self.squares[i,j]
				if foo is not None:
					if foo.color=='white':
						str += foo.name.upper()
					else:
						str += foo.name.lower()
				else:
					str+=' '
		return str

	def print(self):
		out=""
		vertical_counter=7
		for i,data_line in enumerate(np.transpose(self.squares)[::-1]):
			line = "    "+str(vertical_counter)+" "
			for j in data_line:
				if j is None:
					line+="·"
				else:
					if j.color == 'white':
						line+='\x1b[93m'+j.name+'\x1b[0m'
					elif j.color == 'black':
						line+='\x1b[33m'+j.name+'\x1b[0m'
					'''
					line+=j.name
					if j.color == 'white':
						line+='w'
					elif j.color == 'black':
						line+='b'
					'''
				line+=" "
			line+="\n"
			out+=line
			vertical_counter-=1
		out+="      0 1 2 3 4 5 6 7"
		print(out)

'''
@jitclass(
	spec=[
		('piece',nb.types.string),
		('start',int32[:]),
		('stop',int32[:]),
		('x',int32),
		('y',int32),
		('takes',bool_),
	]
)
'''
class Move(object):
	def __init__(self, piece, end_x, end_y, takes=True):
		self.piece = piece
		self.start = (piece.x, piece.y)
		self.stop = (end_x, end_y)
		self.x = end_x
		self.y = end_y
		self.takes=takes

	def get_path_moves(self, include_end=False, takes=True):
		if include_end:
			extender=1
		else:
			extender=0
		iter_x = np.arange(self.start[0], self.x+extender)
		if len(iter_x)==0:
			iter_x = np.arange(self.start[0], self.x-extender, -1)
			if len(iter_x) == 0:
				iter_x = [self.x]

		iter_y = np.arange(self.start[1], self.y+extender)
		if len(iter_y) == 0:
			iter_y = np.arange(self.start[1], self.y-extender, -1)
			if len(iter_y) == 0:
				iter_y = [self.y]

		if len(iter_x) == len(iter_y):
			return [Move(self.piece, i[0], i[1], takes=takes) for i in zip(iter_x[1:], iter_y[1:])]
		elif len(iter_x) == 1:
			return [Move(self.piece, iter_x[0], i, takes=takes) for i in iter_y[1:]]
		elif len(iter_y) == 1:
			return [Move(self.piece, i, iter_y[0], takes=takes) for i in iter_x[1:]]

		return []

	def print(self):
		print(self.piece.name, self.start, self.stop)
