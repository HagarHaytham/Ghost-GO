from dlgo.agent import naive
from dlgo import goboard_fast as goboard
from dlgo import gotypes, scoring
from dlgo.utils import print_board, print_board_file, print_move, print_move_file
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
    
    file = open('log_score_check.txt', 'w')
    while not game.is_over():
        # time.sleep(1)
        
        # print(chr(27) + "[2J")
        bot_move = bots[game.next_player].select_move(game)
        print_move_file(game.next_player, bot_move, file)
        game,numberOfCaptures = game.apply_move(bot_move)
        print_move_file(game.next_player, bot_move, file)

        if game.next_player == gotypes.Player.white:
            captures[gotypes.Player.black] += numberOfCaptures
        else:
            captures[gotypes.Player.white] += numberOfCaptures

        game_result, score = scoring.compute_game_result(game,captures)
        print_board_file(game.board, file)
        file.write(str(score));
        file.write('\n')
        if numberOfCaptures != 0:
            file.write('testcaptures')
            file.write('\n')
        file.write('game_result ')
        file.write('W: ' + str(game_result.w) + '\t' + 'B: ' + str(game_result.b) )
        file.write('\n')
    file.close()

if __name__ == '__main__':
    main()