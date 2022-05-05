import game_board as gb

def initialize():
    global GAME_BOARD_FILLED_SLOTS
    global GAME_BOARD_ALL_SLOTS

    global game_over
    global winner

    # Create a map for all filled slots within the game board.
    GAME_BOARD_FILLED_SLOTS = {}

    # A 2D-List containing all empty/non-empty slots within the game board.
    GAME_BOARD_ALL_SLOTS = [[None for _ in range(gb.GAME_BOARD_COLS)] \
        for _ in range(gb.GAME_BOARD_ROWS)]

    game_over = False
    winner    = ''
