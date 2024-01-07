import numpy as np
from numpy import random

import copy

def is_full_board(board, mini = False):
    if not mini:
        for cell in board:
            if cell == 0:
                return False
    else:
        for row in board:
            for cell in row:
                if cell == 0:
                    return False
    return True

def eval_mini_board(state, board):
    eval_map = [
        [3, 2, 3],
        [2, 4, 2],
        [3, 2, 3]
    ]
    
    temp_result = state.game_result(board)
    if temp_result == state.player_to_move:
        return 24
    elif temp_result == -state.player_to_move:
        return -24
    
    elif temp_result == 0.:
        return 0
    else:
        result = 0
        for i in range(3):
            for j in range(3):
                if (board[i][j] == state.player_to_move):
                    result += eval_map[i][j]
                elif (board[i][j] == -state.player_to_move):
                    result -= eval_map[i][j]
        return result


def eval(state):
    eval_map = [3, 2, 3, 2, 4, 2, 3, 2, 3]
    temp_result = state.game_result(state.global_cells.reshape(3,3))
    if temp_result == state.player_to_move:
        return 150000
    elif temp_result == -state.player_to_move:
        return -150000
    elif temp_result == 0.:
        return 0
    else:
        result = 0

        for i in range(len(state.blocks)):
            result += eval_mini_board(state, state.blocks[i]) * eval_map[i]
        return result


def minimax_alpha_beta(state, a, b, depth, depth_limit, is_minimum = True):
    valid_moves = state.get_valid_moves


    if not len(valid_moves) or depth == depth_limit:
        return eval(state)
    else:
        alpha = -np.inf
        beta = np.inf
        if is_minimum:
            for successor_move in valid_moves:

                new_state = copy.deepcopy(state)
                new_state.act_move(successor_move)

                val = minimax_alpha_beta(new_state, a, min(b, beta), depth + 1, depth_limit, not is_minimum)
                beta = min(beta, val)
                if a >= beta:
                    return beta
            return beta
        else:
            for successor_move in valid_moves:
                
                new_state = copy.deepcopy(state)
                new_state.act_move(successor_move)

                val = minimax_alpha_beta(new_state, max(a, alpha), b, depth + 1, depth_limit, not is_minimum)
                alpha = max(alpha, val)
                if alpha >= b:
                    return alpha
            return alpha



class UltimateTTT_Move:
    
    def __init__(self, index_local_board, x_coordinate, y_coordinate, value):
        self.index_local_board = index_local_board
        self.x = x_coordinate
        self.y = y_coordinate
        self.value = value
    

    def __repr__(self):
        return "local_board:{0}, (x:{1} y:{2}), value:{3}".format(
                self.index_local_board,
                self.x,
                self.y,
                self.value       
            )


x = 0
y = 0
i = 0



def get_block(x, y):
    return 3*x + y


def ultimate_move(cur_state):
    global i,x,y
    if cur_state.blocks[4, 1, 1] == 0:
        i = 1
        
        return UltimateTTT_Move(4, 1, 1, cur_state.player_to_move)
    else:
        
        if i < 8:
            b = get_block(cur_state.previous_move.x, cur_state.previous_move.y)
            i += 1
            return UltimateTTT_Move(b, 1, 1, cur_state.player_to_move)
        if i == 8:
            x = cur_state.previous_move.x
            y = cur_state.previous_move.y
            i += 1
            return UltimateTTT_Move(get_block(x, y), x, y, cur_state.player_to_move)
        else:
            if cur_state.previous_move.x == 1 and cur_state.previous_move.y == 1:
                cur_state.free_move = True
                op_x = 2 - x
                op_y = 2 - y
                b = get_block(op_x, op_y)
                if cur_state.blocks[b, x, y] == 0:
                    return UltimateTTT_Move(b, x, y, cur_state.player_to_move)
                else:
                    return UltimateTTT_Move(b, op_x, op_y, cur_state.player_to_move)
            else:
                b = get_block(cur_state.previous_move.x,
                             cur_state.previous_move.y)
                if cur_state.blocks[b, x, y] == 0:
                    return UltimateTTT_Move(b, x, y, cur_state.player_to_move)
                else:
                    return UltimateTTT_Move(b, 2 - x, 2 - y, cur_state.player_to_move)



def select_move(cur_state, remain_time): 
    # if cur_state.player_to_move == 1:
    #     print(0)
    #     return ultimate_move(cur_state)
    # else:
    #     print(1)
    #     valid_moves = cur_state.get_valid_moves

    #     cur_max = -np.inf
    #     result_index = -1

    #     if cur_state.previous_move == None:
    #         depth_limit = 1
    #     else:
    #         depth_limit = 3
        
    #     if len(valid_moves) != 0:
    #         for i in range(len(valid_moves)):
    #             new_state = copy.deepcopy(cur_state)
    #             new_state.act_move(valid_moves[i])
    #             temp = minimax_alpha_beta(new_state, -np.inf, np.inf, 0, depth_limit)
                
    #             if temp > cur_max:
    #                 cur_max = temp
    #                 result_index = i
    #         return valid_moves[result_index]
    #     return None
    valid_moves = cur_state.get_valid_moves

    cur_max = -np.inf
    result_index = -1

    if cur_state.previous_move == None:
        depth_limit = 1
    else:
        depth_limit = 3
        
    if len(valid_moves) != 0:
        for i in range(len(valid_moves)):
            new_state = copy.deepcopy(cur_state)
            new_state.act_move(valid_moves[i])
            temp = minimax_alpha_beta(new_state, -np.inf, np.inf, 0, depth_limit)
                
            if temp > cur_max:
                cur_max = temp
                result_index = i
        return valid_moves[result_index]
    return None