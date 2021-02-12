"""BLACKJACK SIM"""

import random
printing = False

class Wallet:
	def __init__(self, value):
		self.value = value

	def spend(self, amount):
		self.value -= amount

	def gain(self, amount):
		self.value += amount

class Card:
	def __init__(self, bjValue, suit):
		self.num = bjValue
		self.suit = suit
		self.value = self.num + " of " + self.suit
		self.up = True

		if bjValue == "A":
			self.bjValue = 11
		elif bjValue in ["J", "Q", "K"]:
			self.bjValue = 10
		else:
			self.bjValue = int(bjValue)

	def __repr__(self):
		return self.value

class Deck:
	def __init__(self, suits, values):
		self.cards = []
		for suit in suits:
			for value in values:
				self.add(Card(value, suit))
		
	def add(self, card):
		self.cards.append(card)

	def shuffle(self):
		for i in range(len(self.cards)):
			i = random.choice([i for i in range(len(self.cards))])
			j = random.choice([i for i in range(len(self.cards))])
			tmp = self.cards[i]
			self.cards[i] = self.cards[j]
			self.cards[j] = tmp

	def draw(self):
		return self.cards.pop()

	def __repr__(self):
		x = ""
		for card in self.cards:
			if card.up:
				x += card.value + ", "
			else:
				x += "X, "
		return x

class Hand:
	def __init__(self):
		self.cards = []
		self.bjValue = 0


	def draw(self, deck, num, player="player", show=True):
		for i in range(num):
			tmp = deck.draw()
			if show:
				if player == "player":
					if printing:
						print(f"You drew a {tmp.value}")
				else:
					if printing:
						print(f"==========================The dealer drew a {tmp.value}")
			elif not show and player != "player":
				if printing:
					print(f"==========================The dealer drew ?")

			self.cards.append(tmp)
			self.bjValue += tmp.bjValue
		self.updateAces()

	def aceCanDip(self):
		dip = 0
		for card in self.cards:
			if card.bjValue == 11:
				dip += 1
		return dip

	def dealerCanDip(self):
		dip = 0
		for i in range(1, len(self.cards)):
			if self.cards[i].bjValue == 11:
				dip += 1
		return dip

	def setBJValue(self):
		self.bjValue = 0
		for card in self.cards:
			self.bjValue += card.bjValue

	def getShownValue(self):
		shownValue = 0
		for i in range(1, len(self.cards)):
			shownValue += self.cards[i].bjValue
		return shownValue

	def getShownCards(self):
		shownCards = ["?"]
		for i in range(1, len(self.cards)):
			shownCards.append(self.cards[i])
		return str(shownCards)

	def updateAces(self):
		if self.bjValue > 21:
			for card in self.cards:
				if card and card.bjValue == 11:
					card.bjValue = 1
					break
		self.setBJValue()

	def __repr__(self):
		return str(self.cards)
		# x = ""
		# for card in self.cards:
		# 	x += card.value + ", "
		# return x

class BlackJackSim:
	def __init__(self):
		self.wallet = Wallet(100)
		self.values = ["2", "3", "4", "5", "6", "7", "8", "9", "J", "Q", "K", "A"]
		self.suits = ["Spades", "Hearts", "Clubs", "Diamonds"]
		self.DEALERLIMIT = 17
		self.wins = 0
		self.losses = 0
		self.draws = 0
		self.deck = None
		self.hand = Hand()	
		self.dealerHand = Hand()

	def getStats(self):
		return (self.wins, self.losses, self.draws, self.wins/(self.wins+self.losses))

	def setDEALERLIMIT(DEALERLIMIT):
		self.DEALERLIMIT = DEALERLIMIT

	def setupGame(self, wager=0):
		global losses
		self.won = False
		self.draw = False
		self.lost = False
		# self.choice = "h"
		self.deck = Deck(self.suits, self.values)
		self.deck.shuffle()
		self.hand = Hand()
		self.hand.draw(self.deck, 2)
		self.dealerHand = Hand()
		self.dealerHand.draw(self.deck, 1, "dealer", False)
		self.dealerHand.draw(self.deck, 1, "dealer")
		if printing:
			print()

	def getState(self):
		return {
			"hand": self.hand,
			"hand_bjValue": self.hand.bjValue,
			"dealerHand": self.dealerHand.getShownCards()[1:],
			"dealerHand_bjValue": self.dealerHand.getShownValue(),
			"won": self.won,
			"draw": self.draw,
			"lost": self.lost
		}

	def finishDealer(self):
		while (self.dealerHand.bjValue <= self.DEALERLIMIT and self.dealerHand.bjValue <= self.hand.bjValue) and self.dealerHand.bjValue < 22:
			self.dealerHand.draw(self.deck, 1, "dealer")
		if printing:
			print(f"Dealer's hand: {self.dealerHand}")

	def determineResults(self):
		if self.hand.bjValue < 22 and (self.dealerHand.bjValue > 21 or self.hand.bjValue > self.dealerHand.bjValue):
			self.won = True

		elif self.hand.bjValue < 22 and self.hand.bjValue == self.dealerHand.bjValue:
			self.draw = True

		else:
			self.lost = True

		if printing:
			print(f"{self.hand.bjValue} | {self.dealerHand.bjValue}", end="")

		if self.draw:
			if printing:
				print("--- DRAW")
			self.draws += 1
			return "draw"

		elif self.lost:
			# self.wallet.spend(wager)
			if printing:
				print("--- YOU LOSE")
			self.losses += 1
			return "lost"
		elif self.won:
			# self.wallet.gain(wager)
			if printing:
				print("--- YOU WIN")
			self.wins += 1
			return "won"
		return "ERROR"

	def doChoice(self, choice):
		if choice == "h" and self.hand.bjValue < 21:
			self.hand.draw(self.deck, 1)
			if printing:
				print(f"Your Hand: {self.hand}, {self.hand.bjValue} | Dealerhand: {self.dealerHand.getShownCards()}, {self.dealerHand.getShownValue()}")
		
		if self.hand.bjValue >= 21 or choice == "s":
			self.finishDealer()
			return self.determineResults()

	def game(self, wager):
		self.setupGame(wager)
		
		#play game
		# while self.choice == "h" and self.hand.bjValue < 21:
		# 	print(f"Your Hand: {self.hand}, {self.hand.bjValue} | Dealerhand: {self.dealerHand.getShownCards()}, {self.dealerHand.getShownValue()}")
		# 	# print(self.dealerHand.cards)
		# 	self.choice = input("Hit or stand? (h/s)")
		# 	if self.choice == "s":
		# 		break
		# 	self.hand.draw(self.deck, 1)

		self.finishDealer()
		
		return self.determineResults()

	def play(self, wager=0):
		print(f"Wins: {self.wins} | Losses: {self.losses}")
		if wager <= self.wallet.value:
			return self.game(wager)
		else:
			print("You don't have enough money")