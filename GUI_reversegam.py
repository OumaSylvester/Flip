import random
import sys, pygame
from pygame.locals import *
WINDOWWIDTH =600
WINDOWHEIGHT =600
BOARDWIDTH = 8  # 8 Spaces wide
BOARDHEIGHT = 8  # 8 spaces tall
TILESIZE = 50
BOARDX = 100
BOARDY = 100
FPS = 15

BLACK = (0, 0, 0)  # color of black player
WHITE = (255, 255, 255)  # color of white player and the text
RED = (155, 50, 50)  # color of the hints
BLUE = (0, 0, 255)



def get_new_board():
    board = []
    for x in range(BOARDWIDTH):
        board.append([' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '])

    return board


def draw_circle(x, y, color):
    pixelx, pixely = board_coord_to_pixel_coord(x, y)
    if color == WHITE:
        pygame.draw.circle(DISPLAYSURF, WHITE, (pixelx + TILESIZE/2, pixely + TILESIZE/2), TILESIZE/2 - 10)
    if color == BLACK:
        pygame.draw.circle(DISPLAYSURF, BLACK, (pixelx + TILESIZE/2, pixely + TILESIZE/2), TILESIZE/2 - 10)
    if color == RED:
        pygame.draw.circle(DISPLAYSURF, RED, (pixelx + TILESIZE / 2, pixely + TILESIZE / 2), TILESIZE / 4 - 8)


def draw_board(board: list):
    # Todo: draw grid to the board surface, draw the circles(white, black, hint). Draw the image to the Displaysurf
    # uses the board_coord_to_pixel_coord
    draw_background()

    board_image_surf = IMAGES['board_image']
    board_rect = board_image_surf.get_rect()
    board_rect.topleft = (BOARDX, BOARDY)
    DISPLAYSURF.blit(board_image_surf, board_rect)
    # Draw the grids
    for x in range(BOARDWIDTH):
        pixel_x, pixel_y = board_coord_to_pixel_coord(x, 0)
        pygame.draw.line(DISPLAYSURF, BLACK, (pixel_x, pixel_y), (pixel_x, BOARDY + (BOARDHEIGHT * TILESIZE)), 1)
    for y in range(BOARDHEIGHT):
        pixel_x, pixel_y = board_coord_to_pixel_coord(0, y)
        pygame.draw.line(DISPLAYSURF, BLACK, (pixel_x, pixel_y), (BOARDX + (BOARDWIDTH * TILESIZE), pixel_y), 1)
    # Draw the tiles
    for y in range(BOARDHEIGHT):
       for x in range(BOARDWIDTH):
        if board[x][y] == 'X': # black player
            draw_circle(x, y, BLACK)
        if board[x][y] == 'O': # White player
            draw_circle(x, y, WHITE)
        if board[x][y] == '.': # Hint player
            draw_circle(x, y, RED)


#  Player Section


def is_out_of_board(x, y):
    """Checks if the move input of the user is within the board"""
    # Todo: uses pixel_to_coord algorithm to check if a click is within the board
    if x not in [0, 1, 2, 3, 4, 5, 6, 7]:
        return True
    if y not in [0, 1, 2, 3, 4, 5, 6, 7]:
        return True
    return False


def is_on_board(mousex, mousey):
    """Checks of the clicked point is withing the board"""
    if BOARDX <= mousex <= BOARDX + (BOARDWIDTH * TILESIZE) and \
            mousey >= BOARDY and BOARDY + BOARDHEIGHT * TILESIZE:
        return True
    return False


def space_used(board, x, y):
    """If a user tries to make move in a space a move had already been made"""
    if board[x][y] != ' ':
        return True
    return False


def get_tiles_to_flip(board: list, x, y, player: str):
    if player == 'X':
        other_player = 'O'
    else:
        other_player = 'X'
    tiles_to_flip = []
    # Tiles straight above the move position that can be flipped
    x_start = x
    y_start = y - 1
    count = 0  # number of tiles to flip in this case
    while not is_out_of_board(x_start, y_start) and board[x_start][y_start] == other_player:
        count += 1
        y_start -= 1

    if not is_out_of_board(x_start, y_start) and board[x_start][y_start] == player:
        for tile in range(count):
            y_start += 1
            tiles_to_flip.append([x_start, y_start])
            # print("Tiles to flip: ", tiles_to_flip)
    # Tiles straight below the move tile that can be flipped
    x_start = x
    y_start = y + 1
    count = 0
    while not is_out_of_board(x_start, y_start) and board[x_start][y_start] == other_player:
        count += 1
        y_start += 1

    if not is_out_of_board(x_start, y_start) and board[x_start][y_start] == player:
        for tile in range(count):
            y_start -= 1
            tiles_to_flip.append([x_start, y_start])
            # print("Tiles to flip: ", tiles_to_flip)
    # Tiles straight to the left of the move tile that can be flipped
    x_start = x - 1
    y_start = y
    count = 0
    while not is_out_of_board(x_start, y_start) and board[x_start][y_start] == other_player:
        count += 1
        x_start -= 1

    if not is_out_of_board(x_start, y_start) and board[x_start][y_start] == player:
        for tile in range(count):
            x_start += 1
            tiles_to_flip.append([x_start, y_start])
            # print("Tiles to flip: ", tiles_to_flip)
    # Tiles straight to the right of the move tile that can be flipped
    x_start = x + 1
    y_start = y
    count = 0
    while not is_out_of_board(x_start, y_start) and board[x_start][y_start] == other_player:
        count += 1
        x_start += 1

    if not is_out_of_board(x_start, y_start) and board[x_start][y_start] == player:
        for tile in range(count):
            x_start -= 1
            tiles_to_flip.append([x_start, y_start])
            # print("Tiles to flip: ", tiles_to_flip)
    # Tiles diagonally up(left) the move position that can be flipped
    x_start = x - 1
    y_start = y - 1
    count = 0
    while not is_out_of_board(x_start, y_start) and board[x_start][y_start] == other_player:
        count += 1
        x_start -= 1
        y_start -= 1

    if not is_out_of_board(x_start, y_start) and board[x_start][y_start] == player:
        for tile in range(count):
            x_start += 1
            y_start += 1
            tiles_to_flip.append([x_start, y_start])
            # print("Tiles to flip: ", tiles_to_flip)
    # Tiles diagonally down(right) the move position that can be flipped
    x_start = x + 1
    y_start = y + 1
    count = 0
    while not is_out_of_board(x_start, y_start) and board[x_start][y_start] == other_player:
        count += 1
        x_start += 1
        y_start += 1

    if not is_out_of_board(x_start, y_start) and board[x_start][y_start] == player:
        for tile in range(count):
            x_start -= 1
            y_start -= 1
            tiles_to_flip.append([x_start, y_start])
            # print("Tiles to flip: ", tiles_to_flip)
    # Tiles diagonally up(right) the move position that can be flipped
    x_start = x + 1
    y_start = y - 1
    count = 0
    while not is_out_of_board(x_start, y_start) and board[x_start][y_start] == other_player:
        count += 1
        x_start += 1
        y_start -= 1

    if not is_out_of_board(x_start, y_start) and board[x_start][y_start] == player:
        for tile in range(count):
            x_start -= 1
            y_start += 1
            tiles_to_flip.append([x_start, y_start])
            # print("Tiles to flip: ", tiles_to_flip)
        # Tiles diagonally up(right) the move position that can be flipped
    x_start = x - 1
    y_start = y + 1
    count = 0
    while not is_out_of_board(x_start, y_start) and board[x_start][y_start] == other_player:
        count += 1
        x_start -= 1
        y_start += 1

    if not is_out_of_board(x_start, y_start) and board[x_start][y_start] == player:
        for tile in range(count):
            x_start += 1
            y_start -= 1
            tiles_to_flip.append([x_start, y_start])
            # print("Tiles to flip: ", tiles_to_flip)
    # print("Tiles to flip: ", tiles_to_flip)
    return tiles_to_flip


def get_possible_moves(board, player):
    """Checks all free spaces that a player can make a move to"""
    possible_moves = []
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if board[x][y] == ' ':  # check if tile not occupied
                if len(get_tiles_to_flip(board, x, y, player)) > 0:  # check if there could be any tile flipped incase a
                    #  plater moved there. Get tiles to flip will believe that the player moved there and return the
                    #  tiles if any
                    possible_moves.append([x, y])
    # print("Possible moves: ", moves_that_can_be_made)
    return possible_moves


def is_move_valid(possible_moves: list, move):
    if len(possible_moves) > 0 and move in possible_moves:
        return True

    # print('Move must flip a tile')
    return False


def flip_tiles(board, x, y, player):
    tiles = get_tiles_to_flip(board, x, y, player)
    # print(tiles)
    for tile in tiles:
        # print(tile)
        x = tile[0]
        y = tile[1]
        board[x][y] = player
    return len(tiles)


def make_move(board: list, move: list, player: str, possible_moves: list):
    """The player makes move"""
    x = move[0]
    y = move[1]
    # if is_move_valid(possible_moves, move):
    board[x][y] = player
    flip_tiles(board, x, y, player)


def copy_board(board):
    board_copy = []
    for x in range(BOARDWIDTH):
        board_copy.append([])
        for y in range(BOARDHEIGHT):
            board_copy[x].append(board[x][y])
    return board_copy


def hint_player(board, possible_moves: list):
    """Show player possible move he/she can make"""
    board_copy = copy_board(board)
    for tile in possible_moves:
        x = tile[0]
        y = tile[1]
        board_copy[x][y] = '.'

    draw_board(board_copy)

"""
def get_player_move(board, possible_moves):
    # Todo: get player input from the board. Player clicks a tile to make move. Use algorithm Pixel to boardCords
    mousex, mousey = 0, 0  # initialize with values not on the board
    x, y = pixel_coord_to_board_coord(mousex, mousey)
    while len(possible_moves) > 0: # check if returned coords are in possible moves
        while x not in [0, 1, 2, 3, 4, 5, 6, 7] or y not in [0, 1, 2, 3, 4, 5, 6, 7]:
            # player_move = input('Enter your move, "quit" to end the game, or "hints" to toggle hints.')
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.exit()
                    sys.exit()
                if event.type == MOUSEBUTTONUP:
                    mousex, mousey = event.pos
            x, y = pixel_coord_to_board_coord(mousex, mousey)  # set x and y board coordinate to the new cliked tile
            if HINT_RECT.collidepoint((mousex, mousey)):  # Todo: hint player. If x, y collide with the hint box
                hint_player(board, possible_moves)
                continue
            if NEW_GAME_RECT.collidepoint((mousex, mousey)):
                main()

        if [x, y] in possible_moves:
            return [x, y]  # return move indexed from 0 to 7
        #else:
         #   print('Move does not flip any tile')

    #print('You are in stalemate')

"""
# AI Section


def corner_move(possible_moves: list):
    corners = [[0, 0], [7, 0], [0, 7], [7, 7]]
    for corner in corners:
        if corner in possible_moves:
            return corner
    return []


def stalemate(board, player):
    """Stalemate is a condition where a player has no valid move to make. If this is the condition for a player
    the other player is given a chance to play.
    """
    possible_moves = get_possible_moves(board, player)
    if len(possible_moves) == 0:
        return True
    return False


def ai_move(board, letter, possible_moves):
    random.shuffle(possible_moves)
    best_move = corner_move(possible_moves)
    if not best_move:
        how_many_can_this_move_flip = 0
        board_copy = copy_board(board)
        # Simulate a move using board_copy
        for tile in possible_moves:
            x = tile[0]
            y = tile[1]
            tiles = get_tiles_to_flip(board_copy, x, y, letter)
            if len(tiles) > how_many_can_this_move_flip:
                how_many_can_this_move_flip = len(tiles)
                best_move = tile
    x = best_move[0]
    y = best_move[1]
    board[x][y] = letter
    flip_tiles(board, x, y, letter)


#  Game logic


def who_goes_first():
    if random.randint(0, 1) == 0:
        return 'Computer'
    else:
        return "Player"


def input_player_letter(player_color):

    """Lets the player enter which letter they want to be.

    Returns a list with the player's letter as the first item and the computers letter as the second item
    """
    #letter = ''
    # Todo: Get player letter from the input click. If player clicks black give X, if player click white give O
    #while not (letter == 'X' or letter == 'O'):
     #   letter = input('Do you want to be X or O? ').upper()

    if player_color == 'black':
        return ['X', 'O']

    else:
        return ['O', 'X']


def board_full(board: list):
    """Game ends when the board is full"""
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if board[x][y] == ' ':
                return False
    return True


def get_score_board(board):
    x_score = 0
    o_score = 0
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if board[x][y] == 'X':
                x_score += 1
            if board[x][y] == 'O':
                o_score += 1
    return {"X": x_score, "O": o_score}


def display_score_board(board, player, computer, turn):
    # Todo: use Pygame GUI
    score_board = get_score_board(board)

    score_surf = BASICFONT.render("You: %s, Computer: %s  Turn: %s" % (score_board[player], score_board[computer], turn), True, WHITE)
    score_rect = score_surf.get_rect()
    score_rect.bottomleft = (40, WINDOWHEIGHT - 50)
    DISPLAYSURF.blit(score_surf, score_rect)

    # print("You: %s, Computer: %s" % (score_board[player], score_board[computer]))


# Todo: Start screen algorithm
def start_screen(board):
    # Ste background image

    draw_board(board)
    question_surf = BASICFONT.render('Do you want to be black or white?', True, WHITE, BLUE)
    question_rect = question_surf.get_rect()
    question_rect.center = (BOARDX + (BOARDWIDTH * TILESIZE)/2, BOARDY + (BOARDHEIGHT * TILESIZE)/2)  # center the text in the board
    DISPLAYSURF.blit(question_surf, question_rect)

    black_surf = BASICFONT.render('Black', True, WHITE, BLUE)
    black_rect = black_surf.get_rect()
    black_rect.center = (BOARDX + (BOARDWIDTH * TILESIZE)/2, BOARDY + (BOARDHEIGHT * TILESIZE)/2 + 30)
    DISPLAYSURF.blit(black_surf, black_rect)

    white_surf = BASICFONT.render('White', True, WHITE, BLUE)
    white_rect = white_surf.get_rect()
    white_rect.center = (BOARDX + (BOARDWIDTH * TILESIZE)/2 + 50, BOARDY + (BOARDHEIGHT * TILESIZE)/2 + 30)
    DISPLAYSURF.blit(white_surf, white_rect)

    while True:
        mousex, mousey = -1, -1 # set the initial value to number is not on the board
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                pygame.event.clear()
        if black_rect.collidepoint((mousex, mousey)):
            return 'X', 'O'

        if white_rect.collidepoint((mousex, mousey)):
            return 'O', 'X'
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def pixel_coord_to_board_coord(mousex, mousey):
    """The mousex and mousey must be within the board"""
    x = int((mousex - BOARDX) / TILESIZE)
    y = int((mousey - BOARDY) / TILESIZE)
    return x, y


def board_coord_to_pixel_coord(x, y):
    pixelx = (x * TILESIZE) + BOARDX
    pixely = (y * TILESIZE) + BOARDY

    return pixelx, pixely


def main():
    global DISPLAYSURF, BASICFONT, FPSCLOCK, IMAGES, PLAYERLETTER, COMPUTERLETTER, \
    NEW_GAME_SURF, NEW_GAME_RECT, HINT_SURF, HINT_RECT

    pygame.init()

    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Fllipy')

    BASICFONT = pygame.font.Font('freesansbold.ttf', 16)
    FPSCLOCK = pygame.time.Clock()
    IMAGES = {'bg': pygame.image.load('flippybackground.png'),
              'board_image': pygame.image.load('flippyboard.png'),
              'humanwinner': pygame.image.load('4row_humanwinner.png'),
              'computerwinner': pygame.image.load('4row_computerwinner.png'),
              'tie': pygame.image.load('4row_tie.png'),
              'icon': pygame.image.load('gameicon.png')
              }
    pygame.display.set_icon(IMAGES['icon'])

    NEW_GAME_SURF = BASICFONT.render('New game', True, WHITE, BLUE)
    NEW_GAME_RECT = NEW_GAME_SURF.get_rect()
    NEW_GAME_RECT.topright = (WINDOWWIDTH - 30, 30)

    HINT_SURF = BASICFONT.render('Hint', True, WHITE, BLUE)
    HINT_RECT = HINT_SURF.get_rect()
    HINT_RECT.topright = (WINDOWWIDTH - 30, NEW_GAME_RECT.top + NEW_GAME_RECT.height + 10)

    while True:  # loop for different games
        new_board = get_new_board()
        new_board[3][3] = "O"
        new_board[4][3] = "X"
        new_board[3][4] = "X"
        new_board[4][4] = "O"

        draw_board(new_board)
        PLAYERLETTER, COMPUTERLETTER = start_screen(new_board)
        turn = who_goes_first()

        game_completed = run_game(new_board, turn)
        if game_completed:
            end_game(new_board)  # passing the board by reference
            pygame.time.wait(10000)
        pygame.display.update()


def draw_background():
    DISPLAYSURF.fill(WHITE)
    display_rect = DISPLAYSURF.get_rect()
    display_rect.topleft = (0, 0)
    stretched_bg = pygame.transform.scale(IMAGES['bg'], (WINDOWWIDTH, WINDOWHEIGHT))
    DISPLAYSURF.blit(stretched_bg, display_rect)


    DISPLAYSURF.blit(NEW_GAME_SURF, NEW_GAME_RECT)
    DISPLAYSURF.blit(HINT_SURF, HINT_RECT)


def run_game(new_board, turn):
    # Todo: run_game Algorithm
    mousex, mousey = WINDOWHEIGHT * WINDOWWIDTH, -1  # set to value not on the board



    while not board_full(new_board) and (not stalemate(new_board, PLAYERLETTER) or
                                         not stalemate(new_board, COMPUTERLETTER)):  # main game loop
        """Game ends when board is full  and when both players are in stalemate """
        # Todo: event loop...mousex, mousey -> newgame, hints, x and y board coord entry
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos

        if turn == 'Player':
            if stalemate(new_board, PLAYERLETTER):
                turn = 'Computer'
            else:
                draw_board(new_board)
                player_possible_moves = get_possible_moves(new_board, PLAYERLETTER)
                if is_on_board(mousex, mousey):
                    x, y = pixel_coord_to_board_coord(mousex, mousey)
                    # move = get_player_move(new_board, player_possible_moves)
                    if [x, y] in player_possible_moves:
                        make_move(new_board, [x, y], PLAYERLETTER, player_possible_moves)
                        turn = 'Computer'
                else:  # check if player want hint or start  a new game
                    if HINT_RECT.collidepoint(mousex, mousey):
                        hint_player(new_board, player_possible_moves)
                    elif NEW_GAME_RECT.collidepoint(mousex, mousey):
                        return False  # game not completed

                display_score_board(new_board, PLAYERLETTER, COMPUTERLETTER, turn)
        if turn == 'Computer':

            if stalemate(new_board, COMPUTERLETTER):
                # print("Computer in stalemate")
                turn = 'Player'
            else:
                # print('Computer turn')
                computer_possible_moves = get_possible_moves(new_board, COMPUTERLETTER)
                # print('Computer Possible moves: ', computer_possible_moves)
                ai_move(new_board, COMPUTERLETTER, computer_possible_moves)
                # draw_board(new_board)
                turn = 'Player'
                display_score_board(new_board, PLAYERLETTER, COMPUTERLETTER, turn)

        pygame.display.update()
        FPSCLOCK.tick(FPS)
    return True


def end_game(new_board):
    # Todo: End game algorithm. Who won?, play again
    scores = get_score_board(new_board)
    human_winner_rect = IMAGES['humanwinner'].get_rect()
    human_winner_rect.center = (BOARDX + (BOARDWIDTH * TILESIZE)/2, BOARDY + (BOARDHEIGHT * TILESIZE)/2)

    computer_winner_rect = IMAGES['computerwinner'].get_rect()
    computer_winner_rect.center = (BOARDX + (BOARDWIDTH * TILESIZE)/2, BOARDY + (BOARDHEIGHT * TILESIZE)/2)

    tie_rect = IMAGES['tie'].get_rect()
    tie_rect.center = (BOARDX + (BOARDWIDTH * TILESIZE)/2, BOARDY + (BOARDHEIGHT * TILESIZE)/2)
    if scores[PLAYERLETTER] > scores[COMPUTERLETTER]:
        DISPLAYSURF.blit(IMAGES['humanwinner'], human_winner_rect)
    elif scores[COMPUTERLETTER] > scores[PLAYERLETTER]:
        DISPLAYSURF.blit(IMAGES['computerwinner'], computer_winner_rect)
    else:
        DISPLAYSURF.blit(IMAGES['tie'], tie_rect)
    pygame.display.update()


def terminate():
    pass


if __name__ == '__main__':
    main()

# Invalid player move -> make player enter move till move is valid
# a list of possible moves
# cornerMove - strategizing with corner moves
# get_ai_move
# Todo: defend - which move will make AI lose more? can Ai defend...let say when there are two moves and taking on one
# You can make a move that gives a few tiles and defensive at the same time. If never make it you could end up loosing
# more tiles if the opponent finally take the opportunity you failed to prevent him/her from taking
# would make the other player take a chance that causes it to lose more tiles
# flipping_more than 1 tile in a line  in 1 move -> done
# calc_scores - 2 points for 1 flip
# display-score
# stalemate mode  - no player can make move ...if only one player can make move switch turn to the player
# board-full
# hint_player
# game_play - done
#  can the computer defend itself?
# make it  a web game
# Todo: Design and implement GUI for this Game