#!/bin/python3
import sys
sys.path.append('./required_python_packages')
import pygame

# UI Beginning

pygame.init()

white=(255,255,255)
blue=(161,189,255)
CARD_WIDTH=94
CARD_HEIGHT=150
CARD_PADDING=10
SCOREBOARD_WIDTH=275
SCOREBOARD_HEIGHT=CARD_HEIGHT*3
CROWN_WIDTH= 45
CROWN_HEIGHT=50
WINDOW_WIDTH=(CARD_WIDTH+5)*11 + SCOREBOARD_WIDTH
WINDOW_HEIGHT=(CARD_HEIGHT+30)*5
GROUP_WIDTH=CARD_WIDTH*3+150
GROUP_HEIGHT=CARD_HEIGHT+10
MY_HAND=['blue1','green4','red3','NoneS','NoneW','blue1','green4','red3','purple10']
MY_PLAYED=[]
OTHER_PLAYED=[]

card_back=pygame.image.load('cards/card_back.png')
card_back=pygame.transform.scale(card_back,(CARD_WIDTH,CARD_HEIGHT))
card_blank=pygame.image.load('cards/card_blank.png')
card_blank=pygame.transform.scale(card_blank,(CARD_WIDTH,CARD_HEIGHT))
played_group_bracket=pygame.image.load('cards/played_group_bracket.png')
played_group_bracket=pygame.transform.scale(played_group_bracket,((CARD_WIDTH*CARD_PADDING)*4,CARD_HEIGHT+10))
scoreboard=pygame.image.load('cards/scoreboard.png')
scoreboard=pygame.transform.scale(scoreboard,(SCOREBOARD_WIDTH,SCOREBOARD_HEIGHT))
crown=pygame.image.load('cards/crown.png')
crown=pygame.transform.scale(crown,(CROWN_WIDTH,CROWN_HEIGHT))
played_group=pygame.image.load('cards/played_group_bracket.png')
played_group_bracket=pygame.transform.scale(played_group_bracket,(GROUP_WIDTH,GROUP_HEIGHT))
gameDisplay = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption('Phase 10 Game - By AKA ETC')
clock = pygame.time.Clock()
crashed = False

# Images

def getHand():
	# Draw Function Here
	return MY_HAND
def drawCard(c):
	if c == 'D':
		MY_HAND.append('blue1')
	if c == 'B':
		MY_HAND.append('green8')

def getPlayed():
	return ['red3','red3','green8','green8']

def getOppNum():
	return 10

def getOtherPlayed():
	return ['red3','red3','green8','green8']

def getStats():
	# MyScore, OtherScore, MyRound, OtherRound
	return ["100","1","2","2"]

def getBurnTop():
	return 'green8'

def displayCards():
	global MY_HAND
	global MY_PLAYED
	global OTHER_PLAYED

	# Display My hand and My played cards
	MY_HAND=getHand()
	for n,c in enumerate(MY_HAND,0):
		my_card=pygame.image.load('cards/'+c+'.png')
		my_card=pygame.transform.scale(my_card,(CARD_WIDTH,CARD_HEIGHT))
		gameDisplay.blit(my_card, (n*(CARD_PADDING+CARD_WIDTH)+5,WINDOW_HEIGHT-CARD_HEIGHT-10))
	MY_PLAYED=getPlayed()
	if MY_PLAYED:
		for n,c in enumerate(MY_PLAYED,0):
			my_card=pygame.image.load('cards/'+c+'.png')
			my_card=pygame.transform.scale(my_card,(CARD_WIDTH,CARD_HEIGHT))
			if(n < 2):
				gameDisplay.blit(my_card, (n*(CARD_PADDING+CARD_WIDTH+50)+100,WINDOW_HEIGHT-CARD_HEIGHT*2-47))
			else:
				gameDisplay.blit(my_card, (2*(CARD_PADDING+CARD_WIDTH)+(n-2)*(CARD_PADDING+CARD_WIDTH+50)+490,WINDOW_HEIGHT-CARD_HEIGHT*2-47))
			gameDisplay.blit(played_group_bracket, (5,WINDOW_HEIGHT-CARD_HEIGHT*2-51))
			gameDisplay.blit(played_group_bracket, (GROUP_WIDTH+175,WINDOW_HEIGHT-CARD_HEIGHT*2-51))



	# Display Opponent's hand and Opponent's played cards
	opp_cards=getOppNum()
	for n in range(0,opp_cards):
		gameDisplay.blit(card_back, (n*(CARD_PADDING+CARD_WIDTH)+5,0))
	OTHER_PLAYED=getOtherPlayed()
	if OTHER_PLAYED:
		for n,c in enumerate(OTHER_PLAYED,0):
			my_card=pygame.image.load('cards/'+c+'.png')
			my_card=pygame.transform.scale(my_card,(CARD_WIDTH,CARD_HEIGHT+5))
			if(n < 2):
				gameDisplay.blit(my_card, (n*(CARD_PADDING+CARD_WIDTH+50)+100,CARD_HEIGHT+50))
			else:
				gameDisplay.blit(my_card, (2*(CARD_PADDING+CARD_WIDTH)+(n-2)*(CARD_PADDING+CARD_WIDTH+50)+490,CARD_HEIGHT+50))
			gameDisplay.blit(played_group_bracket, (5,CARD_HEIGHT+50))
			gameDisplay.blit(played_group_bracket, (GROUP_WIDTH+175,CARD_HEIGHT+50))


def displayGame():
	# Scoreboard Displaying
	stats=getStats()
	gameDisplay.blit(scoreboard, (WINDOW_WIDTH-SCOREBOARD_WIDTH,CARD_HEIGHT))
	font=pygame.font.Font('cards/COMIC.ttf',40)
        # stats
	my_score=font.render(stats[0],True,(0,0,0))
	gameDisplay.blit(my_score,(WINDOW_WIDTH-SCOREBOARD_WIDTH + 150, CARD_HEIGHT + 365))
	other_score=font.render(stats[1],True,(0,0,0))
	gameDisplay.blit(other_score,(WINDOW_WIDTH-SCOREBOARD_WIDTH + 150, CARD_HEIGHT + 165))
	my_phase=font.render(stats[2],True,(0,0,0))
	gameDisplay.blit(my_phase,(WINDOW_WIDTH-SCOREBOARD_WIDTH + 150, CARD_HEIGHT + 315))
	other_phase=font.render(stats[3],True,(0,0,0))
	gameDisplay.blit(other_phase,(WINDOW_WIDTH-SCOREBOARD_WIDTH + 150, CARD_HEIGHT + 115))
	
	# Crown Winning Idicator
	if(int(stats[2])>int(stats[3])):
		gameDisplay.blit(crown,(WINDOW_WIDTH-SCOREBOARD_WIDTH + 120, CARD_HEIGHT + 260))
	elif(int(stats[2])<int(stats[3])):
		gameDisplay.blit(crown,(WINDOW_WIDTH-SCOREBOARD_WIDTH + 120, CARD_HEIGHT + 60))
	else:
		if(int(stats[0])<int(stats[1])):
			gameDisplay.blit(crown,(WINDOW_WIDTH-SCOREBOARD_WIDTH + 120, CARD_HEIGHT + 260))
		elif(int(stats[0])>int(stats[1])):
			gameDisplay.blit(crown,(WINDOW_WIDTH-SCOREBOARD_WIDTH + 120, CARD_HEIGHT + 60))
	
	#Decks Displaying
	burn=getBurnTop()
	burn=pygame.image.load('cards/'+burn+'.png')
	burn=pygame.transform.scale(burn,(CARD_WIDTH,CARD_HEIGHT))
	gameDisplay.blit(burn, ((4*CARD_WIDTH)+5,(WINDOW_HEIGHT/2)-(CARD_HEIGHT/2)))
	gameDisplay.blit(card_back,((6*CARD_WIDTH)+5,(WINDOW_HEIGHT/2)-(CARD_HEIGHT/2)))

gameDisplay.fill(blue)



displayGame()
displayCards()

state=0

while not crashed:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			crashed = True

		if event.type == pygame.MOUSEBUTTONDOWN:
			x, y=event.pos
			if(state==0 and (x>=((4*CARD_WIDTH)+5) and x<=((5*CARD_WIDTH)+5)) and (y>=((WINDOW_HEIGHT/2)-(CARD_HEIGHT/2)) and y<=((WINDOW_HEIGHT/2)-(CARD_HEIGHT/2)+CARD_HEIGHT))):
				print("Draw From BURN")
				drawCard('B')
				gameDisplay.fill(blue)
				displayGame()
				displayCards()
				state = state+1
			if(state==0 and (x>=((6*CARD_WIDTH)+5) and x<=((7*CARD_WIDTH)+5)) and (y>=((WINDOW_HEIGHT/2)-(CARD_HEIGHT/2)) and y<=((WINDOW_HEIGHT/2)-(CARD_HEIGHT/2)+CARD_HEIGHT))):
				print("Draw From PILE")
				drawCard('D')
				gameDisplay.fill(blue)
				displayGame()
				displayCards()
				state = state+1
			if(state==1 and x>=5 and x<=(11*(CARD_PADDING+CARD_WIDTH)+5)) and (y>=(WINDOW_HEIGHT-CARD_HEIGHT-10) and y<=(WINDOW_HEIGHT-10)):
				card_clicked=int((x-5)/(CARD_PADDING+CARD_WIDTH))
				if(card_clicked<=len(MY_HAND)-1):
					print('CARD '+str(card_clicked)+' WAS CLICKED')

			#Buttons for adding to my played cards
			if((x>=2 and x<=50) and (y>=607 and y<=650)):
				print('Left most button my played left group')
			if((x>=387 and x<=441) and (y>=609 and y<=650)):
				print('Right most button my played left group')
			if((x>=600 and x<=650) and (y>=607 and y<=650)):
				print('Left most button my played right group')
			if((x>=987 and x<=1050) and (y>=609 and y<=650)):
				print('Right most button my played right group')

			#Buttons for adding to other played cards
			if((x>=2 and x<=50) and (y>=255 and y<=305)):
				print('Left most button my other left group')
			if((x>=387 and x<=441) and (y>=255 and y<=305)):
				print('Right most button my other left group')
			if((x>=600 and x<=650) and (y>=255 and y<=305)):
				print('Left most button my other right group')
			if((x>=987 and x<=1050) and (y>=255 and y<=305)):
				print('Right most button my other right group')


			print(x,y)
	pygame.display.update()
	clock.tick(60)
pygame.quit()

quit()
