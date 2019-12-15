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
player = 0
encoding_time=0
cnn_time=0
move_time=0
prisoners_time=0
agent = None
encoder = None
def monte_carlo_tree_search(main_agent,main_encoder,state,point,color,num_rounds,captures,depth,available_moves): 
    global player
    global encoding_time
    global move_time
    global cnn_time
    global prisoners_time
    global agent
    global encoder
    encoding_time=0
    cnn_time=0
    move_time=0
    prisoners_time=0
    player = color
    agent = main_agent
    encoder = main_encoder
    root = MCTS_node(state,None,captures,point)
    game =state
    play_point = point
    for i in range(num_rounds): 
        result ,leaf = traverse(root,i,available_moves)  
        if(not result):
            break
        simulation_result , last_node = rollout(leaf,depth)
        backpropagate(root,last_node , simulation_result) 
    # print('encoding time ',encoding_time)
    # print('cnn time ',cnn_time)
    # print('move time ',move_time)
    # print('prisoners time ',prisoners_time)
    if( result ):
        game , captures , play_point =  best_child(root)
    return result , game , captures , play_point
 
def best_child(root):
    best_winning_frac = 0
    best_pick = 0
    for i in range(len(root.children)):
        
        child_winning_frac = root.children[i].winning_frac(player)
        if( child_winning_frac > best_winning_frac):
            best_winning_frac = child_winning_frac
            best_pick = i
    return root.children[best_pick].game_state , root.children[best_pick].captures,root.children[best_pick].point
    
      
def traverse(node,total_rollouts,available_moves): 
    picked_child=None
    if(not node.game_state.is_over()):
        result = get_best_three(node,available_moves) 
        if(not result):
            return False , None
        picked_child = pick_child(node,total_rollouts)  
    return True ,picked_child  
  
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

def get_best_three(root,available_moves):
    global agent 
    global encoder
    num_moves = 3
    if(available_moves  == 0):
        return False
    if(available_moves < num_moves):
        num_moves = available_moves
    for i in range(num_moves):
        move = agent.predict(root.game_state)
        print('move ',move)
        if(not move.is_play):
            return False
        legal_state , prisoners = root.game_state.apply_move(move) 
        capture = 0
        ## print('prisoners',prisoners)
        child_captures = copy.copy(root.captures)    
        child_captures[player]+=prisoners
        child = MCTS_node(legal_state,root,child_captures,new_point)
        root.children.append(child)
    # print(probability_matrix)
    return True
def rollout(node,depth):
    game_state = node.game_state
    parent = node
    j=0
    global agent
    global encoder    
    global encoding_time
    global move_time
    global cnn_time
    global prisoners_time
    prisoners =0 
    while not game_state.is_over() and j < depth:
        j+=1
        t1=time.time()
        state = elevenplanes.ElevenPlaneEncoder((19,19))
        state = state.encode(game_state)
        t2 =time.time()
        state = np.expand_dims(state,axis=0)
        
        probability_matrix=predict.model.predict(state)[0]
        probability_matrix = np.reshape(probability_matrix, (-1, 19))
        
        t3 = time.time()
        new_point = 0
        move = agent.predict(game_state)
        #print('move ',move)
        if(not move.is_play):
            break
        new_game_state , prisoners  = game_state.apply_move(move)
        
        t4 =time.time()
        capture = 0 
        child_captures = copy.copy(parent.captures)    
        child_captures[player]+=prisoners
        
        t5 = time.time()
        new_node = MCTS_node(new_game_state,parent,child_captures,new_point)
        # check if game is over
        game_state = copy.deepcopy(new_game_state)
        parent = new_node
        encoding_time +=(t2-t1)
        cnn_time+=(t3-t2)
        move_time+=(t4-t3)
        prisoners_time+=(t5-t4)
    # evaluate game state


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

