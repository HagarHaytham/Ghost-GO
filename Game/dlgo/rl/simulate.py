from dlgo import scoring
from dlgo import goboard_fast as goboard
from dlgo.gotypes import Player
from dlgo import gotypes

from collections import namedtuple

from dlgo.rl.experience import combine_experience
from dlgo.rl.experience import ExperienceCollector

from dlgo.agent.pg import PolicyAgent

from keras.models import load_model

from dlgo.encoders.elevenplanes import ElevenPlaneEncoder

from dlgo.utils import print_board_file, print_move_file

import os
import h5py

class GameRecord(namedtuple('GameRecord', 'moves winner margin')):
    pass


def simulate_game(black_player, white_player, model_index = -1, game_index = -1):

    game_file = None
    if model_index != -1 and game_index != -1:
        directory = 'games/model_' + str(model_index) + '/'
        if not os.path.exists(directory):
            os.makedirs(directory)
        game_file = open('games/model_' + str(model_index) + '/game_' + str(game_index + 1) + '.txt', 'w')

    moves = []
    game = goboard.GameState.new_game(19)
    agents = {
        Player.black: black_player,
        Player.white: white_player,
    }
    captures = {
        gotypes.Player.black: 0,
        gotypes.Player.white: 0,
    }
    while not game.is_over():
        # print_board(game.board)
        next_move = agents[game.next_player].select_move(game)
        moves.append(next_move)

        if game_file is not None:
            print_move_file(game.next_player, next_move, game_file)

        game,numberOfCaptures = game.apply_move(next_move)
        
        if game_file is not None:
            print_board_file(game.board, game_file)

        if game.next_player == gotypes.Player.white:
            captures[gotypes.Player.black] += numberOfCaptures
        else:
            captures[gotypes.Player.white] += numberOfCaptures

        if game_file is not None:
            game_result, score = scoring.compute_game_result(game,captures)
            game_file.write(str(score));
            game_file.write('\n')
            if numberOfCaptures != 0:
                game_file.write('capture event')
                game_file.write('\n')
            game_file.write('game_result ')
            game_file.write('W: ' + str(game_result.w + game_result.komi) + '\t' + 'B: ' + str(game_result.b) )
            game_file.write('\n\n')
    if game_file is not None:
        game_file.close()

    game_result,_ = scoring.compute_game_result(game,captures)
    print(game_result)

    return GameRecord(
        moves=moves,
        winner=game_result.winner,
        margin=game_result.winning_margin,
    )


def experience_simulation(num_games, agent1, agent2,with_experience = True, model_index = -1):
    if with_experience:
        collector1 = ExperienceCollector()
        collector2 = ExperienceCollector()

    agent1_wins = 0
    agent2_wins = 0

    color1 = Player.black
    for game_index in range(num_games):
        print('Game ', game_index)
        if with_experience:
            collector1.begin_episode()
            agent1.set_collector(collector1)

            collector2.begin_episode()
            agent2.set_collector(collector2)

        if color1 == Player.black:
            black_player, white_player = agent1, agent2
        else:
            white_player, black_player = agent1, agent2

        game_record = simulate_game(black_player, white_player, model_index = model_index, game_index = game_index)

        if game_record.winner == color1:
            if with_experience:
                collector1.complete_episode(reward=1)
                collector2.complete_episode(reward=-1)
            agent1_wins += 1
        else:
            if with_experience:
                collector2.complete_episode(reward=1)
                collector1.complete_episode(reward=-1)
            agent2_wins += 1

        color1 = color1.other

    if with_experience:
        return combine_experience([collector1, collector2]), (agent1_wins, agent2_wins)
    else:
        return (agent1_wins, agent2_wins)


def train(model_index, model, no_self_games = 10, epsilon = 0.5,learning_ratio = 0.000001, save_experience = True, save_games = True, wave_index = 0):

    encoder = ElevenPlaneEncoder(board_size = (19, 19))

    agent1 = PolicyAgent(model, encoder)
    agent2 = PolicyAgent(model, encoder)

    if save_experience:
        directory = 'experiences/model_' + str(model_index) + '/'
        if not os.path.exists(directory):
            os.makedirs(directory)

    agent1.set_temperature(epsilon)
    agent2.set_temperature(epsilon)

    experience, _ = experience_simulation(no_self_games, agent1, agent2, with_experience = True, model_index = model_index if save_games else -1)
    
    if save_experience:
        self_games_h5file = h5py.File('experiences/model_' + str(model_index) + '/self_games_experience_' + str(wave_index) + '.hdf5', 'w')
        experience.serialize(self_games_h5file)
        self_games_h5file.close()

    agent1.train(experience, learning_ratio)



def is_baba_voss(model1, model2, no_trials = 5, wins_ratio = 0.6, save_experience = False):
    # check if the model improved
    encoder = ElevenPlaneEncoder(board_size = (19, 19))
    agent = PolicyAgent(model1, encoder)
    old_agent = PolicyAgent(model2, encoder)

    agent.set_temperature(0)
    old_agent.set_temperature(0)

    if save_experience:
        experience, (agent1_wins, agent2_wins) = experience_simulation(no_trials, agent, old_agent, with_experience = True)
        
        trials_h5file = h5py.File('experiences/model_' + str(model_index) + '/trials_experience_' + str(wave_index) + '.hdf5', 'w')
        experience.serialize(trials_h5file)
        trials_h5file.close()
    else:
        (agent1_wins, agent2_wins) = experience_simulation(no_trials, agent, old_agent, with_experience = False)

    assert agent1_wins + agent2_wins == no_trials

    return (agent1_wins / no_trials) > wins_ratio