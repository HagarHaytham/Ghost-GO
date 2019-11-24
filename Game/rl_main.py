from dlgo.rl.simulate import train, is_baba_voss
from keras.models import load_model

current_index = 48

for _ in range(10):
    no_games = 10
    no_games_in_bucket = 2
    no_trials = 2
    epsilon = 0.5
    wins_ratio = 0.5
    save_experience = False
    save_games = False

    model = load_model('models/ElevenPlanes_smallarch_model_epoch_' + str(current_index) + '.h5')
    old_model = load_model('models/ElevenPlanes_smallarch_model_epoch_' + str(current_index) + '.h5')

    wave_index = 0

    while True:
        for bucket in range(no_games // no_games_in_bucket):
            print(no_games // no_games_in_bucket)
            print(bucket)
            train(model_index = current_index, model = model, no_self_games = no_games_in_bucket, save_experience = save_experience, save_games = save_games, epsilon = epsilon, wave_index = wave_index)


        if is_baba_voss(model1 = model, model2 = old_model, no_trials = no_trials, wins_ratio = wins_ratio, save_experience = save_experience):
            # save the model
            print('Here we go')
            model.save('models/ElevenPlanes_smallarch_model_epoch_' + str(current_index + 1) + '.h5')
            break
        else:
            print('Try harder')
            wave_index += 1

    current_index += 1