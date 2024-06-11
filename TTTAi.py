
from math import inf as infinity
from random import choice
import platform
import time
from os import system


HUMAN = -1
COMP = +1
game_board = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]


def evaluate(state):
    """
    Heuristic evaluation of the current board state.
    :param state: current board state
    :return: +1 if the computer wins; -1 if the human wins; 0 if it's a draw
    """
    if check_winner(state, COMP):
        score = +1
    elif check_winner(state, HUMAN):
        score = -1
    else:
        score = 0

    return score


def check_winner(state, player):
    """
    Check if a specific player has won. Possibilities:
    * Three rows    [X X X] or [O O O]
    * Three columns [X X X] or [O O O]
    * Two diagonals [X X X] or [O O O]
    :param state: current board state
    :param player: human or computer
    :return: True if the player has won
    """
    win_state = [
        [state[0][0], state[0][1], state[0][2]],
        [state[1][0], state[1][1], state[1][2]],
        [state[2][0], state[2][1], state[2][2]],
        [state[0][0], state[1][0], state[2][0]],
        [state[0][1], state[1][1], state[2][1]],
        [state[0][2], state[1][2], state[2][2]],
        [state[0][0], state[1][1], state[2][2]],
        [state[2][0], state[1][1], state[0][2]],
    ]
    if [player, player, player] in win_state:
        return True
    else:
        return False


def is_game_over(state):
    """
    Check if the game is over (either human or computer wins).
    :param state: current board state
    :return: True if the game is over
    """
    return check_winner(state, HUMAN) or check_winner(state, COMP)


def get_empty_cells(state):
    """
    Get a list of empty cells in the board.
    :param state: current board state
    :return: list of empty cells
    """
    cells = []

    for x, row in enumerate(state):
        for y, cell in enumerate(row):
            if cell == 0:
                cells.append([x, y])

    return cells


def is_valid_move(x, y):
    """
    Check if a move is valid (i.e., if the chosen cell is empty).
    :param x: X coordinate
    :param y: Y coordinate
    :return: True if the cell is empty
    """
    if [x, y] in get_empty_cells(game_board):
        return True
    else:
        return False


def make_move(x, y, player):
    """
    Place the player's move on the board if the coordinates are valid.
    :param x: X coordinate
    :param y: Y coordinate
    :param player: current player
    """
    if is_valid_move(x, y):
        game_board[x][y] = player
        return True
    else:
        return False


def minimax(state, depth, player):
    """
    AI function to determine the best move.
    :param state: current board state
    :param depth: depth in the game tree (0 <= depth <= 9)
    :param player: human or computer
    :return: list with [best row, best col, best score]
    """
    if player == COMP:
        best = [-1, -1, -infinity]
    else:
        best = [-1, -1, +infinity]

    if depth == 0 or is_game_over(state):
        score = evaluate(state)
        return [-1, -1, score]

    for cell in get_empty_cells(state):
        x, y = cell[0], cell[1]
        state[x][y] = player
        score = minimax(state, depth - 1, -player)
        state[x][y] = 0
        score[0], score[1] = x, y

        if player == COMP:
            if score[2] > best[2]:
                best = score  # maximize the score
        else:
            if score[2] < best[2]:
                best = score  # minimize the score

    return best


def clear_console():
    """
    Clears the console screen.
    """
    os_name = platform.system().lower()
    if 'windows' in os_name:
        system('cls')
    else:
        system('clear')


def display_board(state, comp_marker, human_marker):
    """
    Display the current state of the board in the console.
    :param state: current board state
    :param comp_marker: computer's marker (X or O)
    :param human_marker: human's marker (X or O)
    """
    markers = {
        -1: human_marker,
        +1: comp_marker,
        0: ' '
    }
    line_separator = '---------------'

    print('\n' + line_separator)
    for row in state:
        for cell in row:
            symbol = markers[cell]
            print(f'| {symbol} |', end='')
        print('\n' + line_separator)


def computer_turn(comp_marker, human_marker):
    """
    Computer's turn to play. It uses the minimax function if depth < 9,
    otherwise it selects a random coordinate.
    :param comp_marker: computer's marker (X or O)
    :param human_marker: human's marker (X or O)
    """
    depth = len(get_empty_cells(game_board))
    if depth == 0 or is_game_over(game_board):
        return

    clear_console()
    print(f'Computer turn [{comp_marker}]')
    display_board(game_board, comp_marker, human_marker)

    if depth == 9:
        x = choice([0, 1, 2])
        y = choice([0, 1, 2])
    else:
        move = minimax(game_board, depth, COMP)
        x, y = move[0], move[1]

    make_move(x, y, COMP)
    time.sleep(1)


def human_turn(comp_marker, human_marker):
    """
    Human's turn to play by selecting a valid move.
    :param comp_marker: computer's marker (X or O)
    :param human_marker: human's marker (X or O)
    """
    depth = len(get_empty_cells(game_board))
    if depth == 0 or is_game_over(game_board):
        return

    # Dictionary of valid moves
    move = -1
    moves = {
        1: [0, 0], 2: [0, 1], 3: [0, 2],
        4: [1, 0], 5: [1, 1], 6: [1, 2],
        7: [2, 0], 8: [2, 1], 9: [2, 2],
    }

    clear_console()
    print(f'Human turn [{human_marker}]')
    display_board(game_board, comp_marker, human_marker)

    while move < 1 or move > 9:
        try:
            move = int(input('Use numpad (1..9): '))
            coord = moves[move]
            valid = make_move(coord[0], coord[1], HUMAN)

            if not valid:
                print('Invalid move')
                move = -1
        except (EOFError, KeyboardInterrupt):
            print('Exiting')
            exit()
        except (KeyError, ValueError):
            print('Invalid choice')


def main():
    """
    Main function to run the game.
    """
    clear_console()
    human_marker = ''  # X or O
    comp_marker = ''  # X or O
    first_player = ''  # whether human plays first

    # Human chooses X or O to play
    while human_marker != 'O' and human_marker != 'X':
        try:
            print('')
            human_marker = input('Choose X or O\nSelection: ').upper()
        except (EOFError, KeyboardInterrupt):
            print('Exiting')
            exit()
        except (KeyError, ValueError):
            print('Invalid choice')

    # Set computer's marker
    if human_marker == 'X':
        comp_marker = 'O'
    else:
        comp_marker = 'X'

    # Determine if human starts first
    clear_console()
    while first_player != 'Y' and first_player != 'N':
        try:
            first_player = input('Play first?[y/n]: ').upper()
        except (EOFError, KeyboardInterrupt):
            print('Exiting')
            exit()
        except (KeyError, ValueError):
            print('Invalid choice')

    while len(get_empty_cells(game_board)) > 0 and not is_game_over(game_board):
        if first_player == 'N':
            computer_turn(comp_marker, human_marker)
            first_player = ''

        human_turn(comp_marker, human_marker)
        computer_turn(comp_marker, human_marker)

    # End of game message
    if check_winner(game_board, HUMAN):
        clear_console()
        print(f'Human turn [{human_marker}]')
        display_board(game_board, comp_marker, human_marker)
        print('YOU WIN!')
    elif check_winner(game_board, COMP):
        clear_console()
        print(f'Computer turn [{comp_marker}]')
        display_board(game_board, comp_marker, human_marker)
        print('YOU LOSE!')
    else:
        clear_console()
        display_board(game_board, comp_marker, human_marker)
        print('DRAW!')

    exit()


if __name__ == '__main__':
    main()        
