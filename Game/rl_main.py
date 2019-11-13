from dlgo.rl.simulate import train

current_index = 48

for _ in range(10):
    assert train(model_index = current_index, no_self_games = 5, no_trials = 2, save_experience = False, save_games = False) == True
    current_index += 1