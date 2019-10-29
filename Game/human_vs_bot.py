from __future__ import print_function
from dlgo.agent import naive 
from dlgo import goboard_slow as goboard
from dlgo import gotypes
from dlgo.utils import print_board, print_move, point_from_coords
from six.moves import input
import time

captures = {
    gotypes.Player.black: 0,
    gotypes.Player.white: 0,
}

def main():
    board_size = 19
    game = goboard.GameState.new_game(board_size)
    bot = naive.RandomBot()

    while not game.is_over():
        print(chr(27) + "[2J")
        print_board(game.board)
        
        if game.next_player == gotypes.Player.black:
            human_move = input('Your turn: ')
            point = point_from_coords(human_move.strip())
            move = goboard.Move.play(point)
        else:
            move = bot.select_move(game)

        print_move(game.next_player, move)
        game,numberOfCaptures = game.apply_move(move)

        if len(numberOfCaptures) > 0:
            if game.next_player == gotypes.Player.black:
                captures[gotypes.Player.black] += numberOfCaptures[0]
            else:
                captures[gotypes.Player.white] += numberOfCaptures[0]

        # time.sleep(1)

    winner,score = game.winner(captures)

    if winner == gotypes.Player.black:
        print("Black is the WINNER!!!!")
    else:
        print("White is the WINNER!!!!")

    print('Black:', score[gotypes.Player.black] ,'\tWhite:', score[gotypes.Player.white])


if __name__ == '__main__':
    main()