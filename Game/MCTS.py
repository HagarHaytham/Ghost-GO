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
import MCTS_node
#sys.path.append('/path/to/application/app/folder')
player = 0
def monte_carlo_tree_search(state,color,num_rounds,prisoners ,depth): 
    global player
    player = color
    root = MCTS_node(state,None,prisoners)
    get_legal_moves(root)
    for i in range(num_rounds): 
        leaf = traverse(root,i)  
        simulation_result = rollout(leaf,depth) 
        backpropagate(leaf, simulation_result) 
        
    return best_child(root) 
 
def best_child(root):
    best_winning_frac = 0
    best_pick = 0
    for i in range(len(root.childern)):
        
        child_winning_frac = child.winning_frac(player)
        if( child_winning_frac > best_winning_frac):
            best_winning_frac = child_winning_frac
            best_pick = i
    return root.childern[best_pick].game_state , root.childern[best_pick].captures
    
      
def traverse(node,total_rollouts): 
    picked_child=None
    if(not node.game_state.is_over()):
        get_legal_moves(node)        
        picked_child = pick_child(node,total_rollouts)  
    return picked_child  
  
def pick_child(node,total_rollouts):
    current_value=0
    picked_child=node.children[0]
    temperature=2
    for child in node.childern:
        new_value =child.win_counts[player] + temperature * math.sqrt(math.log(total_rollouts)/child.num_rollouts)
        if(new_value > current_value ):
            picked_child=child
    return picked_child

def get_legal_moves(root):
    legal_moves = root.game_state.legal_moves()
    for i in range(len(legal_moves)):
        legal_state , prisoners = root.game_state.apply_move(legal_moves[i])          
        child = MCTS_node(legal_state,root,prisoners)  
        root.children.append(child)

def rollout(node,depth):
    game_state = node.game_state
    winner = player
    parent =node
    i=0
    while not game_state.is_over() and i< depth:
        i+=1
        state = sevenplanes.SevenPlaneEncoder((19,19))
        state = state.encode(game_state)
        probability_matrix=predict.model.predict(state)
        (x,y)= np.unravel_index( probability_matrix.argmax(), probability_matrix.shape)
        new_game_state ,prisoners  = game_state.apply_move(gotypes.Point(x,y))
        new_node = MCTS_node(new_game_state,parent,prisoners)
        # check if game is over
        game_state = new_game_state
        parent = new_node
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