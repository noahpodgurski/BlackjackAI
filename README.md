# BlackjackAI
Machine Learning AI learns to play Blackjack

# How to run
1. Run `BlackJackAI.py`

# Configurations
1. Comment out line `140` to skip training and begin testing on pre-trained model of 1000 generations. Running line `140` will overwrite the model
2. Generations to train until stopping: line `132`
3. Games to play after training: line `96`
4. Set `printing = True` on line `4` in `BlackJackSim.py` to enable debug logging of cards.

# Training
It seems assigning weights based on decisions at certain points (hit on 17, stand on 19, etc...) trains a smarter model than assigning weights based on wins. This is obvious because wins in blackjack can be circumstantial. The ideal point for the model to reach would be for it to recognize the dealer's shown card and factor that into it's decision. Of course, it's blackjack, so it's all luck anyway.

# Consensus
The horrible sad truth to this neural network is that since there is luck involved, the model will always be skewed. A blackjack after a hit on 20 (although very unlikely) would train the model to almost always hit on 20, which is a very bad move indeed. To see moderate winrates (> 40%), the model has to run through quite a bit of games to understand how the game works.
