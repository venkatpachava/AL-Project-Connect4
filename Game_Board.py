try:
    from main import WIN, WIDTH

    import globals
    import pygame
    import os
except ImportError as E:
    print(f'game_board.py => {E}')


''' CREATE THE BOARD & PIECES:
    The board and game piece images are generated and utilized here.
    The game board slot positions are configured where the pieces can
    then be placed following a column selection from the player.
'''
# Image Assets
GAME_BOARD = pygame.image.load(os.path.join('assets', 'c4-board.png'))
RED_PIECE  = pygame.image.load(os.path.join('assets', 'c4-red-piece.png'))
YLW_PIECE  = pygame.image.load(os.path.join('assets', 'c4-yellow-piece.png'))

# Integer/index values for both players.
P1_HUMAN = 0
P2_AI = 1

# Used to display winning messages.
player_names = ['Player 1', 'AI']

# List of the two player colors.
player_colors = ['R', 'Y']

# Image Asset Dimensions / Constants
GAME_BOARD_WIDTH = 509
GAME_PIECE_DIMEN = 54 # GAME_PIECE WIDTH and HEIGHT are equal.
GAME_BOARD_ROWS  = 6
GAME_BOARD_COLS  = 7

# Game Board Position
GAME_BOARD_DEFAULT_POSITION = (WIDTH-GAME_BOARD_WIDTH)/2, 80

# Populate game board slot positions.
ROW_OFFSET_X = 1.25
ROW_OFFSET_Y = 7

# Column padding values to align the game pieces horizontally.
COL_PADDING = [0, 2, 0, 2, 2, 1.5, 1.25]

def populate_gameboard_slot_pos() -> list:
    temp_slot_positions = [(0, 0)] * (GAME_BOARD_ROWS * GAME_BOARD_COLS)

    # -- Row 1
    temp_slot_positions[0] = (GAME_PIECE_DIMEN*4, (GAME_PIECE_DIMEN*2)-4)

    for i in range(1, 7):
        temp_slot_positions[i] = (temp_slot_positions[i-1][0] +
                                  (GAME_PIECE_DIMEN*ROW_OFFSET_X) + COL_PADDING[i], temp_slot_positions[0][1])

    # -- Rows 2-6
    for i in range(7, 42):
        temp_slot_positions[i] = (temp_slot_positions[i-7][0],
                                  temp_slot_positions[i-7][1] + GAME_PIECE_DIMEN + ROW_OFFSET_Y)

    # Split 1D list into 2D list to separate each row.
    return [temp_slot_positions[i:i+GAME_BOARD_COLS]
            for i in range(0, len(temp_slot_positions), GAME_BOARD_COLS)]

# List of all possible slot positions for game pieces.
GAME_BOARD_SLOT_POSITIONS = populate_gameboard_slot_pos()


''' HEADER COLUMN SELECTION SLOTS:
    These empty surface slots are used when hovering above the board in
    order to indicate where the player would like to drop their game piece.
'''
COLUMN_SELECTION_SURFACES = [pygame.Surface((68, 80))] * 7

COLUMN_SELECTION_SURFACE_POS    = [(0, 0)] * 7
COLUMN_SELECTION_SURFACE_POS[0] = (208, 0)

for s in COLUMN_SELECTION_SURFACES:
    # Add transparent background color for BLACK.
    s.set_colorkey((0, 0, 0))

for i in range(1, len(COLUMN_SELECTION_SURFACE_POS)):
    # Configure all game board selection surface positions.
    COLUMN_SELECTION_SURFACE_POS[i] = (COLUMN_SELECTION_SURFACE_POS[i-1][0] + 69, 0)

def detect_selection_hover() -> int:
    selected_column = -1
    width, height = COLUMN_SELECTION_SURFACES[0].get_width(), \
                    COLUMN_SELECTION_SURFACES[0].get_height()
    x, y = pygame.mouse.get_pos()

    for i in range(len(COLUMN_SELECTION_SURFACES)):
        if x >= COLUMN_SELECTION_SURFACE_POS[i][0] and \
                x <= COLUMN_SELECTION_SURFACE_POS[i][0]+width and \
                y >= 0 and y <= height:
            selected_column = i

    return selected_column

def draw_selection_hover():
    selected_column = detect_selection_hover()

    # Create the game piece above the board on hover.
    if selected_column >= 0:
        pygame.mouse.set_visible(False)
        x, y = COLUMN_SELECTION_SURFACE_POS[selected_column][0], \
                COLUMN_SELECTION_SURFACE_POS[selected_column][1]
        w, h = 68, 80

        WIN.blit(RED_PIECE, dest=(x+w-GAME_PIECE_DIMEN-((w-GAME_PIECE_DIMEN)/2)+1,
                                    y+h-GAME_PIECE_DIMEN-10, w, h))
    elif pygame.mouse.get_visible() == False:
        pygame.mouse.set_visible(True)


''' GAME BOARD FILLED SLOTS:
    Keep track of all filled slots within the game board.
    Add logic for dropping game pieces into the board.
'''
# Used for the dictionary board. No parameter required.
def drop_game_piece(player: int, selected_column: int) -> tuple:
    first_available_slot = 0

    # If column is filled.
    if globals.GAME_BOARD_FILLED_SLOTS.get((first_available_slot, selected_column)):
        print('This column is full. Try another column.')
        return (False, None)

    for row in range(GAME_BOARD_ROWS):
        if globals.GAME_BOARD_FILLED_SLOTS.get((row, selected_column)) == None:
            first_available_slot = row
        else:
            break

    # Add the game piece color to the filled slots map and the 2D-List.
    piece_color = player_colors[player]
    globals.GAME_BOARD_FILLED_SLOTS[(first_available_slot, selected_column)] = piece_color
    globals.GAME_BOARD_ALL_SLOTS[first_available_slot][selected_column] = piece_color

    # Return boolean and row to be used for confirming a winner.
    return (True, first_available_slot)

# Used for dropping a piece into a temporary board.
def drop_game_piece_temp(temp_board: list, player: int, selected_column: int) -> tuple:
    first_available_slot = 0

    # If column is filled.
    if temp_board[first_available_slot][selected_column]:
        print('This column is full. Try another column.')
        return (False, None)

    for row in range(GAME_BOARD_ROWS):
        if temp_board[row][selected_column] == None:
            first_available_slot = row
        else:
            break

    # Add the game piece color to the temporary board (2D-List).
    temp_board[first_available_slot][selected_column] = player_colors[player]

    # Return boolean and row to be used for confirming a winner.
    return (True, first_available_slot)

def validate_winner(player: int, selected_column: int):
    valid_drop = drop_game_piece(player, selected_column)
    if valid_drop[0]:
        winner = confirm_winner(valid_drop[1], selected_column)
        if winner[0]:
            winner_name = player_names[player]

            # End the game and set the winning player name.
            globals.game_over = True
            globals.winner    = winner_name
        return True
    else:
        # Returns False if column is full.
        return False

def detect_selection_click() -> bool:
    selected_column = detect_selection_hover()
    col_width       = COLUMN_SELECTION_SURFACES[0].get_width()

    if selected_column >= 0:
        mouse_x = pygame.mouse.get_pos()[0]
        col_x   = COLUMN_SELECTION_SURFACE_POS[selected_column][0]
        if mouse_x > col_x and mouse_x < col_x + col_width:
            return validate_winner(P1_HUMAN, selected_column)


''' CHECK FOR CONNECT 4:
    Confirm whether or not a player has connected
    four of their game pieces and won the game.
'''
def check_c4_vertical(r: int, c: int) -> tuple:
    slots       = globals.GAME_BOARD_FILLED_SLOTS
    piece_color = slots.get((r, c))
    connect_4   = False

    # The height of the sliding window used
    # to check for a vertical connect 4.
    SLIDING_WINDOW_H = 4

    for row in range(GAME_BOARD_ROWS - SLIDING_WINDOW_H + 1):
        if slots.get((row, c)) == piece_color and \
                slots.get((row+1, c)) == piece_color and \
                slots.get((row+2, c)) == piece_color and \
                slots.get((row+3, c)) == piece_color:
            connect_4 = True

    return (connect_4, piece_color)

def check_c4_horizontal(r: int, c: int) -> tuple:
    slots       = globals.GAME_BOARD_FILLED_SLOTS
    piece_color = slots.get((r, c))
    connect_4   = False

    # The width of the sliding window used
    # to check for a horizontal connect 4.
    SLIDING_WINDOW_W = 4

    for col in range(GAME_BOARD_COLS - SLIDING_WINDOW_W + 1):
        if slots.get((r, col)) == piece_color and \
                slots.get((r, col+1)) == piece_color and \
                slots.get((r, col+2)) == piece_color and \
                slots.get((r, col+3)) == piece_color:
            connect_4 = True

    return (connect_4, piece_color)

def check_c4_diagonal_left(r: int, c: int) -> tuple:
    slots       = globals.GAME_BOARD_FILLED_SLOTS
    piece_color = slots.get((r, c))
    connect_4   = False

    ''' Top-Left -> Bottom-Right Diagonal:
    [X - - - -]
    [- X - - -]
    [- - C - -]
    [- - - X -]
    [- - - - X]
    '''
    diagonal_pieces = [piece_color]

    # Create two pointers to keep track of pieces
    # moving outwards (up-left and down-right.)
    ptr_u = [r-1, c-1]
    ptr_d = [r+1, c+1]

    run_loop = True
    while run_loop:
        # If pointers can no longer move outwards.
        if (ptr_u[0] < 0 or ptr_u[1] < 0) and \
                (ptr_d[0] > GAME_BOARD_ROWS-1 or
                ptr_d[1] > GAME_BOARD_COLS-1):
            run_loop = False
            break

        # Add piece colors to front and back of pieces list.
        diagonal_pieces.insert(0, slots.get((ptr_u[0], ptr_u[1])))
        diagonal_pieces.append(slots.get((ptr_d[0], ptr_d[1])))

        # Search for 4 game pieces in a row diagonally.
        # Return if a winner is found.
        in_a_row = 0
        for color in diagonal_pieces:
            if color == piece_color:
                in_a_row += 1
            else:
                in_a_row = 0

            if in_a_row == 4:
                connect_4 = True
                return (connect_4, piece_color)

        # Update pointers as necessary.
        if ptr_u[0] >= 0: ptr_u[0] -= 1
        if ptr_u[1] >= 0: ptr_u[1] -= 1
        if ptr_d[0] <= GAME_BOARD_ROWS-1: ptr_d[0] += 1
        if ptr_d[1] <= GAME_BOARD_COLS-1: ptr_d[1] += 1

    return (connect_4, piece_color)

def check_c4_diagonal_right(r: int, c: int) -> tuple:
    slots       = globals.GAME_BOARD_FILLED_SLOTS
    piece_color = slots.get((r, c))
    connect_4   = False

    ''' Bottom-Left -> Top-Right Diagonal:
    [- - - - X]
    [- - - X -]
    [- - C - -]
    [- X - - -]
    [X - - - -]
    '''
    diagonal_pieces = [piece_color]

    # Create two pointers to keep track of pieces
    # moving outwards (down-left and up-right.)
    ptr_u = [r-1, c+1]
    ptr_d = [r+1, c-1]

    run_loop = True
    while run_loop:
        # If pointers can no longer move outwards.
        if (ptr_d[0] > GAME_BOARD_ROWS-1 or ptr_d[1] < 0) and \
                (ptr_u[0] < 0 or ptr_u[1] > GAME_BOARD_COLS-1):
            run_loop = False
            break

        # Add piece colors to front and back of pieces list.
        diagonal_pieces.insert(0, slots.get((ptr_d[0], ptr_d[1])))
        diagonal_pieces.append(slots.get((ptr_u[0], ptr_u[1])))

        # Search for 4 game pieces in a row diagonally.
        # Return if a winner is found.
        in_a_row = 0
        for color in diagonal_pieces:
            if color == piece_color:
                in_a_row += 1
            else:
                in_a_row = 0

            if in_a_row == 4:
                connect_4 = True
                return (connect_4, piece_color)

        # Update pointers as necessary.
        if ptr_u[0] >= 0: ptr_u[0] -= 1
        if ptr_u[1] <= GAME_BOARD_COLS-1: ptr_u[1] += 1
        if ptr_d[0] <= GAME_BOARD_ROWS-1: ptr_d[0] += 1
        if ptr_d[1] >= 0: ptr_d[1] -= 1

    return (connect_4, piece_color)

def check_c4_diagonal(r: int, c: int) -> tuple:
    DIAGONAL_L = check_c4_diagonal_left(r, c)
    DIAGONAL_R = check_c4_diagonal_right(r, c)

    if DIAGONAL_L[0]: return DIAGONAL_L
    elif DIAGONAL_R[0]: return DIAGONAL_R

    return (False, None)

def confirm_winner(row: int, col: int) -> bool:
    winner_vertical = check_c4_vertical(row, col)
    winner_horizont = check_c4_horizontal(row, col)
    winner_diagonal = check_c4_diagonal(row, col)

    if (winner_vertical[0] is not None and winner_vertical[0]) or \
        (winner_horizont[0] is not None and winner_horizont[0]) or \
            (winner_diagonal[0] is not None and winner_diagonal[0]):
        if winner_vertical[1]:
            winner_color = winner_vertical[1]
        elif winner_horizont[1]:
            winner_color = winner_horizont[1]
        elif winner_diagonal[1]:
            winner_color = winner_diagonal[1]
        return (True, winner_color)

    return (False, None)
