from logic.player_logic import *
from logic.card_logic import *
import random

#GLOBAL VARIABLES
colors=['blue','red','purple','green']
numbers=['1','2','3','4','5','6','7','8','9','10','11','12']
deck=[]
burn_pile=[]
file_path='cards/'
#



def deal(card_deck,players):

	#Go through each player giving them 10 cards each
	for i in range(0,10):
		for p in players:
			p.draw(card_deck.pop())

	#Put the top card onto the burn pile
	burn_pile.append(card_deck.pop())



def shuffle(card_deck):

	#Just to assure that they are shuffled
	for card in card_deck:
		card.getInfo()

	#!!!!Basic shuffle of the cards for now
	random.shuffle(random.shuffle(card_deck))

	#Just to assure that they are shuffled
	for card in card_deck:
		card.getInfo()


def setupGame(players):
	#Make Deck

	##Make the 24 of each color of each number
	for i in range(0,2):
		for c in colors:
			for n in numbers:
				deck.append(makeCard(n,c))

	##Add skip cards
	for i in range(0,4):
		deck.append(makeCard('S'))

	##Add wild cards
	for i in range(0,8):
		deck.append(makeCard('W'))

	#Beginning the dealing
	#shuffle(deck)
	print(len(deck))
	deal(deck,players)
	print(len(deck))


#Merging of Kyelor and Alex's code begins!!

#Display Card
def card_display(x, y, card, w, h):
	c=card
	display_card = pygame.image.load(file_path + c + ".png")
	display_card = pygame.transform.scale(display_card, (w, h))
	gameDisplay.blit(display_card, (x, y))


#Game Variables
pygame.init()

display_width = 1600
display_height = 1200

black = (0, 0, 0)
white = (255, 255, 255)
gray = (200, 200, 200)

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("some cards")
clock = pygame.time.Clock()

gameDisplay.fill(gray)

