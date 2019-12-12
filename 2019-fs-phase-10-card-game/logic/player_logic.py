from logic.card_logic import *


class Player:
	def __init__(self,name):
		#Default settings
		self.name= name
		self.points=0
		self.curr_round=1
		self.hand=[]
		self.played=[]

	def draw(self,card):
		try:
			card.getInfo()
			self.hand.append(card)

		except:
			print("Error in Draw: expected a Card_Type")

	def remove_card(self,card_index):
		try:
			tempCard=hand[card_index]
			hand.remove(card_index)
			return tempCard
		except:
			print("Error in Remove: card could not be played from hand")

	def showHand(self):
		temp=[]
		for c in self.hand:
			c=c.get_card_name()
			temp.append(c)
		return temp
