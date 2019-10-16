in this chapter we will implement a self_play script that will simulate the self play games 
and save the experience data to disk.

1-	dlgo.code.pg.py: implements an agent(CNN similar to the one in ch6) based on reinforcement learning 
	and making all needed fns to save and load agents for self play games to save experience 
	and improve itself in next chapters.

2-	dlgo.encoders.simple.py: encoder used in this chapter.


3-	dlgo.rl.experience.py: that records the actions and the states of the agent for every play and save it.

4-	dlgo.rl.simulate.py: simulates the no. of games between 2 agents to generate experience.

5-	dlgo.experience_output: code from book to saves the experience to a file .. 
	we can't reach it on github so I wrote it from book and you will find it in ch9