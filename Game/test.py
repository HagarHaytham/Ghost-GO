# import client_game

# while input('in ') != 'e':
#     client_game.handle_init()
#     print(client_game.states)

import subprocess
import os
# print(os.path.dirname(os.path.realpath(__file__)) + '\\..\\code' )
path = os.path.dirname(os.path.realpath(__file__))
path = path[: path.rfind('\\') + 1] + 'code'
print(path)
subprocess.Popen('pushd ..\\code && npm start && popd', shell=True)