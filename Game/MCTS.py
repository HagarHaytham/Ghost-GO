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
from dlgo import goboard_fast as goboard
from dlgo import gotypes
from dlgo.utils import print_board, print_move , point_from_coords
from MCTS_node import MCTS_node
import time
player = 0
encoding_time=0
cnn_time=0
move_time=0
prisoners_time=0
def monte_carlo_tree_search(state,color,num_rounds,captures,depth): 
    global player
    global encoding_time
    global move_time
    global cnn_time
    global prisoners_time
    
    encoding_time=0
    cnn_time=0
    move_time=0
    prisoners_time=0
    player = color
    
    root = MCTS_node(state,None,captures)
    get_legal_moves(root)
    for i in range(num_rounds): 
        leaf = traverse(root,i)  
        simulation_result , last_node = rollout(leaf,depth)
        backpropagate(root,last_node , simulation_result) 
    print('encoding time ',encoding_time)
    print('cnn time ',cnn_time)
    print('move time ',move_time)
    print('prisoners time ',prisoners_time)
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
    global encoding_time
    global move_time
    global cnn_time
    global prisoners_time

    prisoners =0 
    while not game_state.is_over() and j < depth:
        
        j+=1
        t1=time.time()
        state = sevenplanes.SevenPlaneEncoder((19,19))
        state = state.encode(game_state)
        t2 =time.time()
        state = np.expand_dims(state,axis=0)
        
        probability_matrix=predict.model.predict(state)[0]
        probability_matrix = np.reshape(probability_matrix, (-1, 19))
        
        t3 = time.time()
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
        
        t4 =time.time()
        
        if len(prisoners) > 0:
            capture = prisoners[0]
        else:
            capture = 0
        child_captures = copy.copy(parent.captures)    
        child_captures[player]+=capture
        
        t5 =time.time()
        new_node = MCTS_node(new_game_state,parent,child_captures)
        # check if game is over
        game_state = new_game_state
        parent = new_node
        encoding_time +=(t2-t1)
        cnn_time+=(t3-t2)
        move_time+=(t4-t3)
        prisoners_time+=(t5-t4)
    # evaluate game state


    last_captures=copy.copy(parent.captures)
    winner,_ = game_state.semi_winner(last_captures)
    return winner , parent

    
def backpropagate(root,node, result): 
    
    if node == root :
        return 
    node.record_win(result)  # update stats
    backpropagate(root,node.parent,result) 
