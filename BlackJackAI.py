from BlackJackSim import BlackJackSim
import random
import os
import time
import neat
import pickle

def fitness(genomes, config):
	BJS = BlackJackSim()
	BJS.setupGame()
	# print(f"Your Hand: {BJS.hand}, {BJS.hand.bjValue} | Dealerhand: {BJS.dealerHand.getShownCards()}, {BJS.dealerHand.getShownValue()}")

	result = None
	while not result:
		choice = input("Hit or stand? (h/s)")
		result = BJS.doChoice(choice)
		
	# print(result)

def eval_genome(BJSs, nets, ge, x):
	for i in range(100):

		BJSs[x].setupGame()
		while BJSs[x].hand.bjValue == 21 or BJSs[x].dealerHand.bjValue == 21:
			BJSs[x].setupGame() #reset game if starting hand is 21
		# print(f"Your Hand: {BJSs[x].hand}, {BJSs[x].hand.bjValue} | Dealerhand: {BJSs[x].dealerHand.getShownCards()}, {BJSs[x].dealerHand.getShownValue()}")
		result = None
		choices = []
		while not result:
			output = nets[x].activate((BJSs[x].dealerHand.getShownValue(), BJSs[x].hand.bjValue, BJSs[x].hand.aceCanDip(), BJSs[x].dealerHand.dealerCanDip()))[0]
			if output > 0.5:
				choice = "h"
			else:
				choice = "s"
			# choice = input("Hit or stand? (h/s)")
			choices.append(choice)
			result = BJSs[x].doChoice(choice)

		#fitness based on choices?
			if choice == "h" and not result: #if hit and not bust
				ge[x].fitness += 1
			elif choice == "h" and result == "won" or result == "draw": #if hit and won or draw
				ge[x].fitness += .5
			elif choice == "h" and result == "lost": #if hit and lost
				ge[x].fitness += .1
			
			if choice == "s":
				if BJSs[x].hand.bjValue == 18:
					ge[x].fitness += .5
				elif BJSs[x].hand.bjValue == 19:
					ge[x].fitness += 1
				elif BJSs[x].hand.bjValue == 20:
					ge[x].fitness += 2
				elif BJSs[x].hand.bjValue == 21:
					ge[x].fitness += 3

		#or fitness based on wins?
		# if result == "won":
		# 	ge[x].fitness += 1
		# else:
		# 	ge[x].fitness -= .5


	if ge[x].fitness < 0:
		#remove lost sim? prob not
		BJSs.pop(x)
		nets.pop(x)
		ge.pop(x)
	return


def multiFitness(genomes, config):
	nets = []
	ge = []
	BJSs = []

	for genome_id, genome in genomes:
		net = neat.nn.FeedForwardNetwork.create(genome, config)
		nets.append(net)
		BJSs.append(BlackJackSim())
		genome.fitness = 0
		ge.append(genome)

	for x, BJS in enumerate(BJSs):
		eval_genome(BJSs, nets, ge, x)

	bestNet = None
	maxFitness = 0
	for x, genome in enumerate(ge):
		if genome.fitness > maxFitness:
			maxFitness = genome.fitness
			bestNet = nets[x]

	pickle.dump(bestNet,open("best.pickle", "wb"))

def testNet(net, NUM_GAMES=100):
	BJS = BlackJackSim()
	for i in range(NUM_GAMES):
		if i % NUM_GAMES/10 == 0:
			print(f"{i*100/NUM_GAMES}%")
		BJS.setupGame()
		result = None
		choices = []
		hands = [BJS.hand.bjValue]
		dealerHands = ["?", BJS.dealerHand.getShownValue()]
		while not result:
			# print(f"activate stuff: {(BJS.dealerHand.getShownValue(), BJS.hand.bjValue, BJS.hand.aceCanDip(), BJS.dealerHand.dealerCanDip())}")
			output = net.activate((BJS.dealerHand.getShownValue(), BJS.hand.bjValue, BJS.hand.aceCanDip(), BJS.dealerHand.dealerCanDip()))[0]
			if output > 0.5:
				choice = "h"
			else:
				choice = "s"
			# choice = input("Hit or stand? (h/s)")
			choices.append(choice)
			print("hit" if choice == "h" else "stand", end="")
			print(f" at {BJS.hand.bjValue}	Dealer's Shown value: {BJS.dealerHand.getShownValue()}")
			result = BJS.doChoice(choice)
		print(f"Result: {result}, {BJS.hand}, {BJS.dealerHand.bjValue}")
	stats = BJS.getStats()
	print(f"Wins: {stats[0]}, Losses: {stats[1]}, Draws: {stats[2]}, W/L Ratio: {stats[3]}")

def run(config_path):
	config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
								neat.DefaultSpeciesSet, neat.DefaultStagnation,
								config_path)
	p = neat.Population(config)

	p.add_reporter(neat.StdOutReporter(True))
	stats = neat.StatisticsReporter()
	p.add_reporter(stats)

	winner = p.run(multiFitness,1000) # 5 seconds per gen, 5*1000 -> 1hr 23min



if __name__ == "__main__":
	local_dir = os.path.dirname(__file__)
	config_path = os.path.join(local_dir, "config-feedforward.txt")
	#run trainer 
	# run(config_path) #comment out to skip

	#test best net
	testNet(pickle.load(open("best.pickle", "rb")), 1000)
