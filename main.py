from board import Board

board = Board()

board.add_all_pieces()
board.print()

board.current_eval = board.eval

white_player = 'PC'
black_player = 'PC'

board.start_game(white_player, black_player, max_nbr_turns=4)
