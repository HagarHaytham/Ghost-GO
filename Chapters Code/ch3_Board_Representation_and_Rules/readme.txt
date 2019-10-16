1-	dlgo.goboard_slow.py: Representation of the board and the rules implementation.

2-	dlgo.gotypes.py: player class and point class --> game elements.

3-	dlgo.utils.py: prints the board.

4-	dlgo.agent.base.py: basic agent ot be implemented in agent.naive.py.

5-	dlgo.agent.naive.py: implements an agent that plays a random valid move.

6-	dlgo.agent.helpers.py: implements the eye rule just check ch.3.

7-	human_v_bot.py: enables you to play with the naive slow agent.

------------------------------ Till here we can run the random agent that playes a valid move from a given set of moves.

making it faster using zobrist hashing....

1-	generate_zobrist.py: generates hashes to be used with faster version of the board.

2-	dlgo.goboard.py: faster version of the board integrated with zobrist hashings.

