from dlgo.agent import naive
from dlgo import goboard_slow as goboard
from dlgo import gotypes
from dlgo.utils import print_board, print_move
import time
import MCTS
captures = {
    gotypes.Player.black: 0,
    gotypes.Player.white: 0,
}

def main():
    board_size = 19
    game = goboard.GameState.new_game(board_size)  
    while not game.is_over():
        
        print_board(game.board)
        
        player =game.next_player
        
        num_rounds = 100
        
        prisoners = captures[player] 
        
        game , prisoners= MCTS.monte_carlo_tree_search( game,player,num_rounds,prisoners )
        
        if len(numberOfCaptures) > 0:
            if game.next_player == gotypes.Player.black:
                captures[gotypes.Player.black] += numberOfCaptures[0]
            else:
                captures[gotypes.Player.white] += numberOfCaptures[0]

    winner,score = game.winner(captures)

    if winner == gotypes.Player.black:
        print("Black is the WINNER!!!!")
    else:
        print("White is the WINNER!!!!")

    print('Black:', score[gotypes.Player.black] ,'\tWhite:', score[gotypes.Player.white])

if __name__ == '__main__':
    main()