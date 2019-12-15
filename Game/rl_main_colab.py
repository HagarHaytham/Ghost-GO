from dlgo.rl.simulate import train, is_baba_voss
from keras.models import load_model
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from google.colab import auth
from oauth2client.client import GoogleCredentials

# 1. Authenticate and create the PyDrive client.
auth.authenticate_user()
gauth = GoogleAuth()
gauth.credentials = GoogleCredentials.get_application_default()
drive = GoogleDrive(gauth)
current_index = 50

for _ in range(10):
    no_games = 5000
    no_games_in_bucket = 100
    no_trials = 600
    epsilon = 0.4
    wins_ratio = 0.6
    save_experience = False
    save_games = False

    model = load_model('models/ElevenPlanes_smallarch_model_epoch_' + str(current_index) + '.h5')
    old_model = load_model('models/ElevenPlanes_smallarch_model_epoch_' + str(current_index) + '.h5')

    wave_index = 0

    while True:
        for bucket in range(no_games // no_games_in_bucket):
            # print(no_games // no_games_in_bucket)
            # print(bucket)
            train(model_index = current_index, model = model, no_self_games = no_games_in_bucket, save_experience = save_experience, save_games = save_games, epsilon = epsilon, wave_index = wave_index)

        state = ""
        if is_baba_voss(model1 = model, model2 = old_model, no_trials = no_trials, wins_ratio = wins_ratio, save_experience = save_experience):
        #     # save the model
            # print('Here we go')
            state = "W"
            break;
        else:
            # print('Try Harder')
            state = "L"

        model.save('models/ElevenPlanes_smallarch_model_epoch_' + str(current_index + 1) + '.h5')
        uploaded = drive.CreateFile({'title': state +'_'+ 'ElevenPlanes_smallarch_model_epoch_' + str(current_index + 1) + '.h5'})
        uploaded.SetContentFile('models/ElevenPlanes_smallarch_model_epoch_' + str(current_index + 1) + '.h5')
        uploaded.Upload()
        wave_index += 1

    current_index += 1