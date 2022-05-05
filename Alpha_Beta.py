try:
    from random import choice, randint
    from math import inf

    import game_board as gb
    import globals
    import copy
except ImportError as E:
    print(f'alpha_beta.py => {E}')


class AlphaBeta:
    def __init__(self):
        self.INFINITY     = inf
        self.NEG_INFINITY = self.INFINITY * -1

    # [Dictionary]: Returns columns from game board that are NOT full.
    def get_valid_columns(self, board: dict):
        valid_columns = []

        for i in range(gb.GAME_BOARD_COLS):
            if board.get((0, i)) == None:
                valid_columns.append(i)

        return valid_columns
    
    # [List]: Returns columns from game board that are NOT full.
    def get_valid_columns(self, board: list):
        valid_columns = []

        for i in range(gb.GAME_BOARD_COLS):
            if board[0][i] == None:
                valid_columns.append(i)

        return valid_columns

    def window_counter(self, window: list, player: int):
        window_score = 0
        piece_color = gb.player_colors[player]
        opponent    = gb.player_colors[not bool(player)]

        if window.count(piece_color) == 4:
            window_score += 100
        elif window.count(piece_color) == 3 and window.count(None) == 1:
            window_score += 5
        elif window.count(piece_color) == 2 and window.count(None) == 2:
            window_score += 2

        if window.count(opponent) == 3 and window.count(None) == 1:
            window_score -= 4

        return window_score

    def validate_board_scores(self, board: list, player: int):
        board_score = 0

        # Dimensions for sliding window and board traversal.
        SLIDING_WINDOW_DIM = 4
        WINDOW_TRAVERSE_H  = gb.GAME_BOARD_ROWS - SLIDING_WINDOW_DIM + 1
        WINDOW_TRAVERSE_W  = gb.GAME_BOARD_COLS - SLIDING_WINDOW_DIM + 1

        # Validate board score - CENTER
        center_array = [i for i in list(board[:gb.GAME_BOARD_COLS // 2])]
        center_count = center_array.count(gb.player_colors[player])
        board_score += center_count * 3

        # Validate board score - HORIZONTAL
        for r in range(gb.GAME_BOARD_ROWS):
            row_arr = [i for i in list(board[r:])]
            
            for c in range(WINDOW_TRAVERSE_W):
                window      = row_arr[c:c+SLIDING_WINDOW_DIM]
                board_score += self.window_counter(window, player)

        # Validate board score - VERTICAL
        for c in range(gb.GAME_BOARD_COLS):
            col_arr = [i for i in list(board[:c])]

            for r in range(WINDOW_TRAVERSE_H):
                window      = col_arr[r:r+SLIDING_WINDOW_DIM]
                board_score += self.window_counter(window, player)

        # Validate board score - DIAGONAL
        for r in range(WINDOW_TRAVERSE_H):
            for c in range(WINDOW_TRAVERSE_W):
                window      = [board[r+i][c+i] for i in range(SLIDING_WINDOW_DIM)]
                board_score += self.window_counter(window, player)
        for r in range(WINDOW_TRAVERSE_H):
            for c in range(WINDOW_TRAVERSE_W):
                window      = [board[r+3-i][c+i] for i in range(SLIDING_WINDOW_DIM)]
                board_score += self.window_counter(window, player)

        return board_score

    def validate_winning_move(self, board: list, player: int) -> bool:
        # Dimensions for sliding window and board traversal.
        SLIDING_WINDOW_DIM = 4
        WINDOW_TRAVERSE_H  = gb.GAME_BOARD_ROWS - SLIDING_WINDOW_DIM
        WINDOW_TRAVERSE_W  = gb.GAME_BOARD_COLS - SLIDING_WINDOW_DIM

        piece_color = gb.player_colors[player]

        # Validate winning positions - HORIZONTAL
        for c in range(WINDOW_TRAVERSE_H):
            for r in range(gb.GAME_BOARD_ROWS):
                if board[r][c] == piece_color and board[r][c+1] == piece_color and \
                        board[r][c+2] == piece_color and board[r][c+3] == piece_color:
                    return True

        # Validate winning positions - VERTICAL
        for c in range(gb.GAME_BOARD_COLS):
            for r in range(WINDOW_TRAVERSE_W):
                if board[r][c] == piece_color and board[r+1][c] == piece_color and \
                        board[r+2][c] == piece_color and board[r+3][c] == piece_color:
                    return True

        # Validate winning positions - DIAGONAL
        for c in range(WINDOW_TRAVERSE_H):
            for r in range(WINDOW_TRAVERSE_W):
                if board[r][c] == piece_color and board[r+1][c+1] == piece_color and \
                        board[r+2][c+2] == piece_color and board[r+3][c+3] == piece_color:
                    return True
        for c in range(WINDOW_TRAVERSE_H):
            for r in range(3, gb.GAME_BOARD_ROWS):
                if board[r][c] == piece_color and board[r-1][c+1] == piece_color and \
                        board[r-2][c+2] == piece_color and board[r-3][c+3] == piece_color:
                    return True

    def is_terminal(self, board: list):
        return self.validate_winning_move(board, gb.P1_HUMAN) or \
            self.validate_winning_move(board, gb.P2_AI) or \
            len(self.get_valid_columns(board)) == 0

    def minimax(self, board: list, depth: int, alpha: int, beta: int,
            maximizingPlayer: bool) -> tuple:
        valid_columns = self.get_valid_columns(board)
        terminal      = self.is_terminal(board)

        if depth == 0 or terminal:
            if terminal:
                if self.validate_winning_move(board, gb.P2_AI):
                    return (None, 100000000000000)
                elif self.validate_winning_move(board, gb.P1_HUMAN):
                    return (None, -10000000000000)
                else:
                    # The game has ended. Game over
                    return (None, 0)
            else:
                # The depth has lowered to a value of 0.
                return (None, self.validate_board_scores(board, gb.P2_AI))

        if maximizingPlayer:
            col = choice(valid_columns)
            val = self.NEG_INFINITY

            for c in valid_columns:
                board_temp = copy.deepcopy(board)
                gb.drop_game_piece_temp(board_temp, gb.P2_AI, c)
                curr_score = self.minimax(
                    board_temp, depth - 1, alpha, beta, False)[1]

                if curr_score > val:
                    val = curr_score
                    col = c

                alpha = max(alpha, val)
                if alpha >= beta:
                    break

            return (col, val)

        else:
            col = choice(valid_columns)
            val = self.INFINITY

            for c in valid_columns:
                board_temp = copy.deepcopy(board)
                gb.drop_game_piece_temp(board_temp, gb.P1_HUMAN, c)
                curr_score = self.minimax(
                    board_temp, depth - 1, alpha, beta, True)[1]

                if curr_score < val:
                    val = curr_score
                    col = c

                beta = min(beta, val)
                if alpha >= beta:
                    break

            return (col, val)

    def validate_drop_location(self, board: list, selected_column: int) -> bool:
        return board[0][selected_column] == None

    def ai_move(self, board: list):
        if not globals.game_over:
            (column, score) = self.minimax(board, gb.GAME_BOARD_ROWS - 1,
                self.NEG_INFINITY,self.INFINITY, True)

            # If the game board is not full.
            valid_columns = self.get_valid_columns(board)
            if len(valid_columns) > 0:
                if column == None or column < 0 or column >= gb.GAME_BOARD_COLS:
                    column = valid_columns[randint(0, len(valid_columns)-1)]

            print(f'[AI] Column: {column}, Score: {score}')

            if self.validate_drop_location(board, column):
                gb.validate_winner(gb.P2_AI, column)
