"Controls input on terminal and gathering necessary information to decide the next move."

import chess, pyautogui
from board import Board, window_swap
from eval import first_move, random_move
import models.research.object_detection.chess_detection_test as cdt
from eval import minimax_recur, naive_eval

if __name__ == "__main__":
    input("Press enter to start game...")
    
    while True:
        side = input("What side are you? ")

        if side.lower() == "white":
            board = Board(chess.WHITE)
            break
        elif side.lower() == "black":
            board = Board(chess.BLACK)
            break
        else:
            print("Not a valid side. Type 'white' or 'black'.")

    if board.side == chess.WHITE:
        while not board.cboard.is_checkmate():
            print(board.cboard)
            board.move(minimax_recur(board, naive_eval), True) # Depth count does not include root; how deep FROM the root
            print(board.cboard)
            window_swap()
            opp_move = cdt.detection(board)
            # opp_move = input("Input AN of black's move: ")
            board.move(opp_move, False)
    
    elif board.side == chess.BLACK:
        while not board.cboard.is_checkmate():
            print(board.cboard)
            opp_move = cdt.detection(board)
            board.move(opp_move, False)
            print(board.cboard)
            board.move(random_move(board.cboard), True)
            window_swap()