import random
from dlgo.agent.base import Agent
from dlgo.agent.helpers import is_point_an_eye
from dlgo.goboard_slow import Move
from dlgo.gotypes import Point

__all__ = ['RandomBot']


class RandomBot(Agent):
    def select_move(self, game_state):
        # Choose a random valid move that preserves our eyes
        candidates = []
        for r in range(1, game_state.board.num_rows + 1):
            for c in range(1, game_state.board.num_cols + 1):
                candidate = Point(row=r, col=c)
                # If a point is empty, not a self-capture, doesn't violate ko and preserve eyes
                if game_state.is_valid_move(Move.play(candidate)) and \
                    not is_point_an_eye(game_state.board,candidate,game_state.next_player):
                        candidates.append(candidate)
                        
        
        # No valid moves then pass
        if not candidates:
            return Move.pass_turn()
        # Play a random move from the candidates 
        return Move.play(random.choice(candidates))