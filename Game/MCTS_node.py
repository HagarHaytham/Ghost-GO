# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 18:38:17 2019

@author: reham
"""
class MCTS_node :
    def __init__(self, game_state, parent=None):
        self.game_state = game_state
        self.parent = parent
        self.children = []
        self.win_counts = {
            'B': 0,
            'W': 0,
        }
        self.num_rollouts = 0
        
        
    def record_win(self, winner):
        self.win_counts[winner] += 1
        self.num_rollouts += 1     

    def winning_frac(self, player):
        return float(self.win_counts[player]) / float(self.num_rollouts)