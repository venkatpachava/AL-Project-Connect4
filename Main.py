try:
    from game_board import *

    import alpha_beta
    import globals
    import pygame
except ImportError as E:
    print(f'main.py => {E}')


''' Name:    Connect 4 [Reinforcement Learning]
    Class:   Intro to AI - 6612
    School:  University of New Haven,Spring2022
    Authors: Venkata Krishna Pachava,Venkata Sai Yalla
'''

# Window Dimensions
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# Alpha-Beta Object
ab = alpha_beta.AlphaBeta()

# Title Bar Caption
pygame.display.set_caption('[AI-Spring2022] Connect 4 - University of New Haven')

# Color Constants
LIGHT_BLUE = (52, 180, 235)
YELLOW     = (255, 255, 0)
WHITE      = (255, 255, 255)
RED        = (255, 0, 0)

FPS = 60 # Frame Rate

# Set the default game font.
pygame.font.init()

def create_font_text(size: int) -> pygame.font.SysFont:
    return pygame.font.SysFont('Monoscape', size)

# Create and update display window.
def draw_window():
    # Add Background Color
    WIN.fill(LIGHT_BLUE) 
    # Draw Game Board Image
    WIN.blit(GAME_BOARD, (GAME_BOARD_DEFAULT_POSITION))

    # Create column selection surfaces above the game board.
    for i in range(len(COLUMN_SELECTION_SURFACES)):
        WIN.blit(COLUMN_SELECTION_SURFACES[i], COLUMN_SELECTION_SURFACE_POS[i])

    # Draw game pieces in the filled game board slots.
    for (row, col) in globals.GAME_BOARD_FILLED_SLOTS:
        if globals.GAME_BOARD_FILLED_SLOTS[(row, col)] == 'R':
            WIN.blit(RED_PIECE, GAME_BOARD_SLOT_POSITIONS[row][col])
        elif globals.GAME_BOARD_FILLED_SLOTS[(row, col)] == 'Y':
            WIN.blit(YLW_PIECE, GAME_BOARD_SLOT_POSITIONS[row][col])

    # If game board is full -- Game over
    if globals.GAME_BOARD_FILLED_SLOTS.get((0, 0)) and \
            globals.GAME_BOARD_FILLED_SLOTS.get((0, 2)) and \
            globals.GAME_BOARD_FILLED_SLOTS.get((0, 1)) and \
            globals.GAME_BOARD_FILLED_SLOTS.get((0, 3)) and \
            globals.GAME_BOARD_FILLED_SLOTS.get((0, 4)) and \
            globals.GAME_BOARD_FILLED_SLOTS.get((0, 5)) and \
            globals.GAME_BOARD_FILLED_SLOTS.get((0, 6)):
        globals.game_over = True

    # Create text for title and author names.
    title_font = create_font_text(32)
    WIN.blit(title_font.render('Connect 4', 1, (WHITE)),
        (12, HEIGHT - 64))
    WIN.blit(title_font.render('Intro to AI', 1, (WHITE)),
        (12, HEIGHT - 36))
    WIN.blit(title_font.render('Venkata Sai', 1, (WHITE)),
        (WIDTH - 164, HEIGHT - 64))
    WIN.blit(title_font.render('Venkata Krishna', 1, (WHITE)),
        (WIDTH - 184, HEIGHT - 36))

    # Draw game piece when hovering above the game board.
    if not globals.game_over:
        draw_selection_hover()

    if globals.game_over:
        # Create alpha-black overlay.
        s = pygame.Surface((WIDTH, HEIGHT))
        s.set_alpha(200)
        s.fill((0, 0, 0))
        WIN.blit(s, (0, 0))

        pygame.mouse.set_visible(True)

        end_screen_font = create_font_text(75)
        WIN.blit(end_screen_font.render('Game Over!', 1, WHITE),
            ((WIDTH / 2) - 146, 20))

        if globals.winner == player_names[0]:
            winner_color = RED
            winner_name_pos = ((WIDTH / 2) - 175, (HEIGHT / 2) - 50)
        elif globals.winner == player_names[1]:
            winner_color = YELLOW
            winner_name_pos = ((WIDTH / 2) - 105, (HEIGHT / 2) - 50) 
        else:
            winner_name_pos = ((WIDTH / 2) - 145, (HEIGHT / 2) - 50)
        if len(globals.winner) > 0:
            WIN.blit(end_screen_font.render(f'{globals.winner} wins!', 1, winner_color),
                winner_name_pos)
        else:
            WIN.blit(end_screen_font.render('It was a Tie!', 1, WHITE), winner_name_pos)

        WIN.blit(end_screen_font.render('Press SPACE to try again.', 1, WHITE),
            ((WIDTH / 2) - 310, (HEIGHT / 2) + 20))

    pygame.display.update()

def main():
    # Fill gameboard slot positions.
    populate_gameboard_slot_pos()

    clock = pygame.time.Clock()
    run   = True

    while run:
        clock.tick(FPS) # Run at 60 FPS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if not globals.game_over:
                if event.type == pygame.MOUSEBUTTONUP:
                    if detect_selection_click():
                        draw_window()
                        pygame.time.wait(700)
                        ab.ai_move(globals.GAME_BOARD_ALL_SLOTS)
                # if event.type == pygame.KEYDOWN:
                #     if event.key == pygame.K_w:
                #         globals.game_over = True
            else:
                # Key press for restarting.
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        globals.winner = ''
                        globals.game_over = False
                        globals.GAME_BOARD_FILLED_SLOTS = {}
                        globals.GAME_BOARD_ALL_SLOTS = [
                                [None for _ in range(GAME_BOARD_COLS)] \
                                    for _ in range(GAME_BOARD_ROWS)]

        draw_window()

    pygame.quit()

if __name__ == '__main__':
    globals.initialize()
    main()
