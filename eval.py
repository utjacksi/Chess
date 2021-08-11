"Contains the evaluation functions and decision making."

from re import S
import chess
import random
from anytree import Node, RenderTree
from stopwatch import Stopwatch

counter = 0
recurr_list = []

piece_value = {
    'P' : 1,
    'N' : 3,
    'B' : 3,
    'R' : 5,
    'Q' : 9,
    'K' : 0, # Kings will always be on the board
    'p' : -1,
    'n' : -3,
    'b' : -3,
    'r' : -5,
    'q' : -9,
    'k' : 0
}

# Constructs minimax tree recursively
def generate_tree(id, prnt, cbrd, mv, depth):
    global counter
    global recurr_list
    counter += 1

    if depth >= 0:
        node = Node(id, parent = prnt, cboard=cbrd, move=mv, score=None)
        id = 0
        for move in cbrd.legal_moves:
            cbrd.push(move)
            if (cbrd.board_fen(),cbrd.castling_rights) not in recurr_list:
                generate_tree(id, node, chess.Board(cbrd.fen()), move, depth-1)
                recurr_list.append((cbrd.board_fen(),cbrd.castling_rights))
            cbrd.pop()
            id += 1

        if (prnt == None):
            # print(counter)
            return node

def recur_func(cboard, eval, node, turn):
    if node.is_leaf:
        # print(node)
        node.score = eval(node.cboard)
        # print(eval_score)
        return node.score
    
    for child in node.children:
        if node.score == None:
            eval_score = recur_func(cboard, eval, child, not turn)
            node.score = eval_score
        elif turn: # White's turn (max node)
            eval_score = recur_func(cboard, eval, child, not turn)
            if node.score < eval_score:
                # print(eval_score)
                node.score = eval_score
        else: # Black's turn (min node)
            eval_score = recur_func(cboard, eval, child, not turn)
            if node.score > eval_score:
                # print(eval_score)
                node.score = eval_score

    return node.score

def minimax_recur(cboard, eval, depth):
    global recurr_list
    recurr_list = [] # Emptying global cache of board states previously seen, find a better way to design this
    root = generate_tree(0, None, cboard, None, depth)
    # print(root, root.cboard, root.is_leaf)
    recur_func(cboard, eval, root, cboard.turn)
    # print(RenderTree(root))
    
    optimal_node = None
    for child in root.children:
        if optimal_node == None:
            optimal_node = child
        else:
            if cboard.turn: # White, therefore maximize
                if child.score > optimal_node.score:
                    optimal_node = child
            else: # Black, therefore minimize
                if child.score < optimal_node.score:
                    optimal_node = child
    
    print("optimal move: ", optimal_node.move, "score: ", optimal_node.score)
    # print(optimal_node.children)
    return cboard.san(optimal_node.move)


###########################################

def minimax(cboard, eval, depth):
    stopwatch = Stopwatch()
    root = generate_tree(0, None, cboard, None, depth)
    stopwatch.stop()
    # print("GENERATING TREE: ", str(stopwatch))
    # print(RenderTree(root))

    stopwatch.restart()

    leaves_list = root.leaves
    to_maximize = False if leaves_list[0].cboard.turn == chess.WHITE else True # It is flipped because this pertains to the layer above the leaf nodes
    layer_list = [[]] # Each elem is a list representing a layer of the tree (starting from the 2nd to bottom)
    optimal_move = None
    optimal_score = None
    parent_score = None
    for leaf_node in leaves_list:
        if leaf_node.parent not in layer_list[0]:
            print("A: ", leaf_node.parent, leaf_node)
            layer_list[0].append(leaf_node.parent)
        eval_score = eval(leaf_node.cboard)
        # print(leaf_node.move, eval_score, parent_score)
        if leaf_node.parent.score == None: # Assuming that leaf is not the root (depth != 1), TODO: should add precondition
            leaf_node.parent.score = eval_score
            optimal_move = leaf_node.move
            optimal_score = eval_score
            # print(parent_score)
        # Parents of the leaf nodes are trying to maximize the score
        elif to_maximize:
            if leaf_node.parent.score < eval_score:
                # print(parent_score)
                leaf_node.parent.score = eval_score
                optimal_move = leaf_node.move
                optimal_score = eval_score
        # Parents of the leaf nodes are trying to minimize the score
        elif leaf_node.parent.score > eval_score:
            # print(parent_score)
            leaf_node.parent.score = eval_score
            optimal_move = leaf_node.move
            optimal_score = eval_score
        # print(parent_score)

    index = 0
    while True:
        if root in layer_list[index]:
            #print(layer_list[index], index)
            break
        else:
            layer_list.append([])
            to_maximize = not to_maximize
            print(cboard.turn. to_maximize)
            for node in layer_list[index]:
                # if node == root:
                #     print("done")
                if node.parent not in layer_list[index+1]:
                    layer_list[index+1].append(node.parent)
                eval_score = eval(node.cboard)
                parent_score = leaf_node.parent.score
            if node.parent.score == None: # Assuming that leaf is not the root (depth != 1), TODO: should add precondition
                node.parent.score = eval_score
                optimal_move = leaf_node.move
                optimal_score = eval_score
            # Parents of the leaf nodes are trying to maximize the score
            elif to_maximize:
                if node.parent.score < eval_score:
                    # print(parent_score)
                    node.parent.score = eval_score
                    optimal_move = leaf_node.move
                    optimal_score = eval_score
            # Parents of the leaf nodes are trying to minimize the score
            elif node.parent.score > eval_score:
                # print(parent_score)
                node.parent.score = eval_score
                optimal_move = leaf_node.move
                optimal_score = eval_score

    for children in root.children:
        print(children.score, children.move)
        
    print("OPTIMAL MOVE: ", optimal_move, "SCORE: ", optimal_score)
    stopwatch.stop()
    # print("GENERATING MOVE: ", str(stopwatch))
    if optimal_score == 0:
        return random_move(cboard)
    return cboard.san(optimal_move)

# Picks the first move and returns an AN string
def first_move(cboard):
    for i in cboard.legal_moves:
        return cboard.san(i)

# Picks a random move
def random_move(cboard):
    return cboard.san(random.choice(list(cboard.legal_moves)))


counter=0 
# Naive evaluation function (piece capture, checkmate)
# White trying to maximize, black is trying to minimize
def naive_eval(cboard):
    # print(cboard.board_fen)
    global counter
    counter += 1
    if cboard.is_checkmate():
        if cboard.turn == chess.WHITE:
            return -100
        elif cboard.turn == chess.BLACK:
            return 100
    if cboard.is_stalemate():
        return 0

    white_count = 0
    black_count = 0
    board_fen = cboard.board_fen()
    for char in board_fen:
        if char.isupper():
            white_count += piece_value[char]
        elif char.islower():
            black_count += piece_value[char]

    return white_count + black_count

# # MAIN
# board = chess.Board("rnb1qr1k/6bp/2p3pn/pp1pp3/5p1P/5N2/PPPPPPP1/RNBQKB1R w Q - 2 21")
board = chess.Board("rnbqkbnr/pppppppp/7N/8/8/8/PPPPPPPP/RNBQKB1R w KQkq - 0 1")

minimax_recur(board, naive_eval, 2)