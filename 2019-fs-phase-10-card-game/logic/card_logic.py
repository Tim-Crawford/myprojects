#!/bin/python3
import sys
sys.path.append('./required_python_packages')
import pygame

#This file will contain the logic backbone of the card logic. This includes: the phases,
#how the phases are played, the information about how a card is built, the checks on a
#play made by a player for a phase, and logic for hands; burn pile; and draw pile.

#Class for the Card obj

class Card:
	#'Number' is the number that the card holds (Decided at runtime)
	#'Color' is the color that the card holds (Decided at runtime)
	#'PointValue' is the value the card holds. It will be added to the
	#player's score if it is still in their hand when the round
	#ends.

	def __init__(self, number, color=None):
		self.number = number
		self.color = color

		cardValues={
			"1":5,
			"2":5,
			"3":5,
			"4":5,
			"5":5,
			"6":5,
			"7":5,
			"8":5,
			"9":5,
			"10":10,
			"11":10,
			"12":10,
			"S":15,
			"W":25
		}

		self.pointValue=cardValues.get(number)

	def getInfo(self):
		return self.number, self.color, self.pointValue

	def get_card_name(self):
		return (str(self.color)+str(self.number))

def makeCard(number,color=None):
	test=Card(number,color)
	return test