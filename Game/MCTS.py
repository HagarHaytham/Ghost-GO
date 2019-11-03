# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 18:39:09 2019

@author: reham
"""
import sevenplanes
import predict
import copy 
import math
import random
import numpy as np
from dlgo import goboard_slow as goboard
from dlgo import gotypes
from dlgo.utils import print_board, print_move , point_from_coords
from MCTS_node import MCTS_node

#sys.path.append('/path/to/application/app/folder')
player = 0
def monte_carlo_tree_search(state,color,num_rounds,captures,depth): 
    global player
    player = color
    root = MCTS_node(state,None,captures)
    get_legal_moves(root)
    for i in range(num_rounds): 
        leaf = traverse(root,i)  
        simulation_result , last_node = rollout(leaf,depth)
        backpropagate(root,last_node , simulation_result) 
    return best_child(root) 
 
def best_child(root):
    best_winning_frac = 0
    best_pick = 0
    for i in range(len(root.children)):
        
        child_winning_frac = root.children[i].winning_frac(player)
        if( child_winning_frac > best_winning_frac):
            best_winning_frac = child_winning_frac
            best_pick = i
    return root.children[best_pick].game_state , root.children[best_pick].captures
    
      
def traverse(node,total_rollouts): 
    picked_child=None
    if(not node.game_state.is_over()):
        get_legal_moves(node)        
        picked_child = pick_child(node,total_rollouts)  
    return picked_child  
  
def pick_child(node,total_rollouts):
    if(total_rollouts == 0 and len(node.children) > 0):
        return node.children[random.randint(0,len(node.children))]
    current_value=0
    picked_child=node.children[0]
    temperature=2
    for child in node.children:
        new_value =child.win_counts[player] + temperature * math.sqrt(math.log(total_rollouts)/(child.num_rollouts))
        if(new_value > current_value ):
            picked_child=child
    return picked_child

def get_legal_moves(root):
    legal_moves = root.game_state.legal_moves()
    for i in range(len(legal_moves)):
        legal_state , prisoners = root.game_state.apply_move(legal_moves[i]) 
        if(not legal_state.is_over()):
            if len(prisoners) > 0:
                capture = prisoners[0]
            else:
                capture = 0
            child_captures = copy.copy(root.captures)    
            child_captures[player]+=capture
            child = MCTS_node(legal_state,root,child_captures)  
            root.children.append(child)

def rollout(node,depth):
    game_state = node.game_state
    parent = node
    j=0
    while not game_state.is_over() and j < depth:
        j+=1
        state = sevenplanes.SevenPlaneEncoder((19,19))
        state = state.encode(game_state)
        state = np.expand_dims(state,axis=0)
        probability_matrix=predict.model.predict(state)[0]
        probability_matrix = np.reshape(probability_matrix, (-1, 19))
        
        
        while True:
            max = probability_matrix.max()
            coordinates = np.where(probability_matrix == max)
            row = coordinates[0][0]
            col = coordinates[1][0]
            probability_matrix[row][col]= 0
            point = gotypes.Point(row=row+1, col=col+1)
            move = goboard.Move(point)
            if game_state.is_valid_move(move):
                break
       
        new_game_state , prisoners  = game_state.apply_move(move)
        if len(prisoners) > 0:
            capture = prisoners[0]
        else:
            capture = 0
        child_captures = copy.copy(parent.captures)    
        child_captures[player]+=capture
        new_node = MCTS_node(new_game_state,parent,child_captures)
        # check if game is over
        game_state = new_game_state
        parent = new_node
    # evaluate game state
    last_captures=copy.copy(parent.captures)
    winner,_ = game_state.semi_winner(last_captures)
    return winner , parent

    
def backpropagate(root,node, result): 
    
    if node == root :
        return 
    node.record_win(result)  # update stats
    backpropagate(root,node.parent,result) 

