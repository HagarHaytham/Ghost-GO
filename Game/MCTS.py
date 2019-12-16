# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 18:39:09 2019
@author: reham
"""
import elevenplanes
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
from dlgo.agent.pg import PolicyAgent as Agent
from keras.models import load_model
player = 0
encoding_time=0
cnn_time=0
move_time=0
prisoners_time=0

model = load_model('models\ElevenPlanes_smallarch_model_epoch.h5')
encoder = elevenplanes.ElevenPlaneEncoder((19,19))
agent = Agent(model, encoder)
def monte_carlo_tree_search(state,point,color,num_rounds,captures,depth): 
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
    
    root = MCTS_node(state,None,captures,point)
    for i in range(num_rounds):
        leaf = traverse(root,i)  
        simulation_result , last_node = rollout(leaf,depth)
        backpropagate(root,last_node , simulation_result) 
    # # print('encoding time ',encoding_time)
    # # print('cnn time ',cnn_time)
    # # print('move time ',move_time)
    # # print('prisoners time ',prisoners_time)
    game , captures , play_point =  best_child(root) 
    return game , captures , play_point
 
def best_child(root):
    best_winning_frac = 0
    best_pick = 0
    for i in range(len(root.children)):
        
        child_winning_frac = root.children[i].winning_frac(player)
        if( child_winning_frac > best_winning_frac):
            best_winning_frac = child_winning_frac
            best_pick = i
    return root.children[best_pick].game_state , root.children[best_pick].captures,root.children[best_pick].point
    
      
def traverse(node,total_rollouts): 
    picked_child=None
    if(not node.game_state.is_over()):
        get_best_three(node) 
        picked_child = pick_child(node,total_rollouts)  
    return picked_child  
  
def pick_child(node,total_rollouts):
    if(total_rollouts == 0 and len(node.children) > 0):
        # # print('children = ',len(node.children))
        index = random.randint(0,len(node.children)-1)
        # # print(index)
        return node.children[index]
    current_value=0
    picked_child=node.children[0]
    temperature=2
    for child in node.children:
        new_value =child.win_counts[player] + temperature * math.sqrt(math.log(total_rollouts)/(child.num_rollouts))
        if(new_value > current_value ):
            picked_child = child
    return picked_child

def get_best_three(root):

    moves = agent.select_move(root.game_state, 3)
    for move in moves:
        legal_state , prisoners = root.game_state.apply_move(move) 
        child_captures = copy.copy(root.captures)  
        child_captures[player]+=prisoners
        child = MCTS_node(legal_state,root,child_captures,move.point)
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

        move = agent.select_move(game_state)[0]

        new_game_state , prisoners  = game_state.apply_move(move)

        child_captures = copy.copy(parent.captures)    
        child_captures[player]+=prisoners
        
        new_node = MCTS_node(new_game_state,parent,child_captures,move.point)
        
        game_state = new_game_state
        parent = new_node


    last_captures=copy.copy(parent.captures)
    # # print(last_captures)
    game_captures = {
        gotypes.Player.black : last_captures['0'],
        gotypes.Player.white : last_captures['1']
    }
    winner,_ = game_state.semi_winner(game_captures)
    result = '0'
    if(winner == gotypes.Player.white):
        result ='1'
    return result , parent

    
def backpropagate(root,node, result): 
    
    if node == root :
        return 
    # # print(result)
    node.record_win(result)  # update stats
    backpropagate(root,node.parent,result) 