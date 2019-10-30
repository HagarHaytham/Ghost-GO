# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 18:39:09 2019

@author: reham
"""
import sevenplanes
import predict
import math
import numpy as np
from dlgo import goboard_slow as goboard
from dlgo import gotypes
from dlgo.utils import print_board, print_move

#sys.path.append('/path/to/application/app/folder')
player ="B"
move_coordinates=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t']
def monte_carlo_tree_search(root,color,timer): 
    global player
    player=color
    num_rounds = 100
    get_legal_moves(root)
    for i in range(num_rounds): 
        leaf = traverse(root,i)  
        simulation_result = rollout(leaf,timer) 
        backpropagate(leaf, simulation_result) 
          
    #return best_child(root) 
  
def traverse(node,total_rollouts): 
    node = None
    if(not node.is_terminal()):
        node = pick_child(node,total_rollouts)  
        node.parent=None
        get_legal_moves(node)
    return node  
  
def pick_child(node,total_rollouts):
    current_value=0
    picked_child=node.children[0]
    temperature=2
    for child in node.childern:
        new_value =child.win_counts[player] + temperature * math.sqrt(math.log(total_rollouts)/child.num_rollouts)
        if(new_value > current_value ):
            picked_child=child
    return picked_child

def get_legal_moves(node):
    legal_moves = node.game_state.legal_moves()
    for i in range(len(legal_moves)):            
        node.children.append(legal_moves[i])

def rollout(node,timer):
    game_state = node.game_state
    winner = player
    while not game_state.is_over():

        state = sevenplanes.SevenPlaneEncoder((19,19))
        state = state.encode(game_state)
        probability_matrix=predict.model.predict(state)
        (x,y)= np.unravel_index( probability_matrix.argmax(), probability_matrix.shape)
        new_game_state= game_state.apply_move(gotypes.Point(x,y))

        # check if game is over
        game_state = new_game_state
    # evaluate game state
    winner,_ = game_state.winner()

    return winner

def update_stats(node,result):
    node.record_win(result)
def backpropagate(node, result): 
    if is_root(node) :
        return 
    update_stats(node, result)  
    backpropagate(node.parent,result) 

def is_root(node):
    if node.parent == None :
        return True
    return False