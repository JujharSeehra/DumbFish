import allFunctions
from evaluation import evaluate_board

nodes_searched = 0

MATE_SCORE = 10000

transpositionTable = {}

def get_position_keys():
    board = tuple(piece for row in allFunctions.pieceArray for piece in row)
    return (board, allFunctions.turn, allFunctions.en_passant_target, allFunctions.white_king_moved, allFunctions.black_king_moved, allFunctions.white_left_rook_moved, allFunctions.white_right_rook_moved, allFunctions.black_left_rook_moved, allFunctions.black_right_rook_moved)
def alpha_beta(depth, alpha, beta, player, ply):

    global nodes_searched

    nodes_searched += 1

    if get_position_keys() in transpositionTable:
        stored_depth, stored_score = transpositionTable[get_position_keys()]
        if stored_depth >= depth:
            return stored_score

    moves = allFunctions.generate_legal_moves(player)

    if len(moves) == 0:

        king = 6 if player == 1 else -6

        if allFunctions.is_in_check(king):

            if player == 1:
                return -MATE_SCORE + ply
            else:
                return MATE_SCORE - ply

        return 0

    if depth == 0:

        return quiescence(alpha, beta, player, ply)

    moves = allFunctions.order_moves(moves)

    if player == 1:

        best_score = -float("inf")

        for move in moves:

            old_row, old_col, new_row, new_col = move

            undo_info = allFunctions.make_search_move(old_row,old_col,new_row,new_col)

            score = alpha_beta(depth - 1,alpha,beta,-1,ply + 1)

            allFunctions.undo_search_move(undo_info)

            best_score = max(best_score,score)

            alpha = max(alpha,best_score)
            if beta <= alpha:
                break
        transpositionTable[get_position_keys()] = (depth, best_score)
        
        return best_score

    else:

        best_score = float("inf")

        for move in moves:

            state = allFunctions.save_game_state()

            old_row, old_col, new_row, new_col = move

            allFunctions.make_engine_move(
                old_row,
                old_col,
                new_row,
                new_col
            )

            score = alpha_beta(
                depth - 1,
                alpha,
                beta,
                1,
                ply + 1
            )

            allFunctions.restore_game_state(state)

            best_score = min(
                best_score,
                score
            )

            beta = min(
                beta,
                best_score
            )

            if beta <= alpha:
                break

        transpositionTable[get_position_keys()] = (depth, best_score)
        return best_score

def find_best_move(depth=5):

    global nodes_searched

    nodes_searched = 0
    transpositionTable.clear()

    player = 1 if allFunctions.turn % 2 == 0 else -1

    moves = allFunctions.generate_legal_moves(player)

    if not moves:
        return None

    moves = allFunctions.order_moves(moves)

    best_move = None

    alpha = -float("inf")
    beta = float("inf")

    if player == 1:

        best_score = -float("inf")

        for move in moves:

            old_row, old_col, new_row, new_col = move

            undo_info = allFunctions.move_leaves_king_in_check(old_row, old_col, new_row, new_col)
            score = alpha_beta(depth - 1, alpha, beta, -1, 1)
            allFunctions.undo_search_move(undo_info)

            print(
                f"{move} -> {round(score, 2)}"
            )

            if score > best_score:

                best_score = score
                best_move = move

            alpha = max(
                alpha,
                best_score
            )

    else:

        best_score = float("inf")

        for move in moves:

            state = allFunctions.save_game_state()

            old_row, old_col, new_row, new_col = move

            allFunctions.make_engine_move(
                old_row,
                old_col,
                new_row,
                new_col
            )

            score = alpha_beta(
                depth - 1,
                alpha,
                beta,
                1,
                1
            )

            allFunctions.restore_game_state(state)

            print(
                f"{move} -> {round(score, 2)}"
            )

            if score < best_score:

                best_score = score
                best_move = move

            beta = min(
                beta,
                best_score
            )

    print()
    print("Nodes searched:", nodes_searched)
    print("Best move:", best_move)
    print("Evaluation:", round(best_score, 2))

    return best_move

def quiescence(alpha, beta, player, ply = 0):
    global nodes_searched

    nodes_searched += 1
    stand_pat = evaluate_board(allFunctions.pieceArray, allFunctions.is_valid_move, allFunctions.move_leaves_king_in_check, allFunctions.is_in_check, allFunctions.can_attack_square)
    if player == 1:
        if stand_pat >= beta:
            return beta
        if stand_pat > alpha:
            alpha = stand_pat
    else:
        if stand_pat <= alpha:
            return alpha
        if stand_pat < beta:
            beta = stand_pat
    moves = allFunctions.generate_legal_moves(player)
    capture_moves = []
    for move in moves:
        old_row, old_col, new_row, new_col = move
        captured_piece = allFunctions.pieceArray[new_row][new_col]
        if captured_piece != 0:
            capture_moves.append(move)
        elif allFunctions.can_en_passant(old_row, old_col, new_row, new_col):
            capture_moves.append(move)
    capture_moves = allFunctions.order_moves(capture_moves)
    for move in capture_moves:
        undo_info = allFunctions.make_search_move(old_row, old_col, new_row, new_col)
        score = quiescence(alpha, beta, -player, ply + 1)
        allFunctions.undo_search_move(undo_info)
        if player == 1:
            if score >= beta:
                return beta
            alpha = max(alpha, score)
        else:
            if score <= alpha:
                return alpha
            beta = min(beta, score)
    if player == 1:
        return alpha
    return beta
