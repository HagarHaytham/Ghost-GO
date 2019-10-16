1-	dlgo.encoders.base.py: base encoder to encode the board so that it would be an input to NN.

2-	dlgo.encoders.oneplane.py: implements the base encoder class in one plane as a matrix.

3-	we will see different encoders in next chapters.

4-	to have initial data to be fed to the NN we will first generate games with the mcts algorithm

5-	generate_mcts_games.py: used to generate those games.

6-	to generate 20 games --> python generate_mcts_games.py -n 20 --board-out features.npy --move-out labels.npy

Note: here the book usues another version of the board called dlgo.goboard_fast.py which is even faster than goboard.py 


7-	chapter_6_cnn.mcts_go_mlp.py: loads the presaved games and usues them to train keras nueral network to predict the best next move.

8-	chapter_6_cnn.mcts_go_cnn_simple.py: loads the presaved games and uses them to train keras convolutional Nueral Network to get more accurate results.

9-	chapter_6_cnn.mcts_go_cnn.py: the final efficient convolutional Nueral Network that modifies the last one for efficiency.