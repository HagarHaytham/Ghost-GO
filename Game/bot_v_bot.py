from dlgo.agent import naive
from dlgo import goboard_slow as goboard
from dlgo import gotypes
from dlgo.utils import print_board, print_move
import time

captures = {
    gotypes.Player.black: 0,
    gotypes.Player.white: 0,
}

def main():
    board_size = 9
    game = goboard.GameState.new_game(board_size)
    bots = {
        gotypes.Player.black: naive.RandomBot(),
        gotypes.Player.white: naive.RandomBot(),
        }
    
    while not game.is_over():
        # time.sleep(1)
        
        # print(chr(27) + "[2J")
        print_board(game.board)
        bot_move = bots[game.next_player].select_move(game)
        print_move(game.next_player, bot_move)
        game,numberOfCaptures = game.apply_move(bot_move)

        if len(numberOfCaptures) > 0:
            if game.next_player == gotypes.Player.black:
                captures[gotypes.Player.black] += numberOfCaptures[0]
            else:
                captures[gotypes.Player.white] += numberOfCaptures[0]

    winner,score = game.winner(captures)

    if winner == gotypes.Player.black:
        # print("Black is the WINNER!!!!")
    else:
        # print("White is the WINNER!!!!")

    # print('Black:', score[gotypes.Player.black] ,'\tWhite:', score[gotypes.Player.white])

if __name__ == '__main__':
    main()