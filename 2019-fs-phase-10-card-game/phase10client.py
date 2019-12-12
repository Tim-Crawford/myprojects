import json
import socket
import time
import random
from struct import pack, unpack
import sys
sys.path.append('./required_python_packages')
import pygame

# dimensions of the game window
display_width = 1600
display_height = 1200

# colors
black = (0, 0, 0)
white = (255, 255, 255)
gray = (200, 200, 200)

HOST = "127.0.0.1"
PORT = 8000

def recv_json(server_socket):
	header = server_socket.recv(8)
	size = unpack("<I", header[4:8])[0]
	if not (header.startswith(b"JSON")):
		raise "Invalid JSON format (Missive)"
	if size < 0 or size > 1024 * 1024:
		raise "Incoming JSON is too large: " + str(size)
	# read incoming size from socket, then remove the trailing newline
	body = server_socket.recv(size)[:-1]
	# parse into json
	return json.loads(body)


def send_json(server_socket, msg_payload):
	if msg_payload[-1] != "\n":
		msg_payload += "\n"
	prefix = "JSON".encode("utf-8")
	size = pack("<I", len(msg_payload))
	message = msg_payload.encode("utf-8")
	server_socket.sendall(prefix + size + message)

	return recv_json(server_socket)


class Client(object):
	def __init__(self, player_id, server_socket):
		super().__init__()
		self.player_id = player_id
		self.server_socket = server_socket

	def recv_json(self):
		return recv_json(self.server_socket)

	def waitForMM(self):
		data = json.dumps(
			{
				"messageType": "connect",
				"data": {
					"game": "default",
					"clientType": "client",
					"configuration": {"id": self.player_id},
				},
			}
		)
		json_response = send_json(self.server_socket, data)
		while json_response.get("messageType") != "connect":
			if json_response.get("messageType") == "error":
				raise Exception(json_response.get("data"))
			if json_response.get("messageType") == "response":
				print("Message:", json_response.get("data"))
				json_response = recv_json(self.server_socket)

		print("Connect:", json_response.get("data"))

	def sendGSInit(self):
		game_connect_payload = json.dumps(
			{
				"messageType": "client-info",
				"data": {"clientInfo": {"id": self.player_id}},
			}
		)
		gs_response = send_json(self.server_socket, game_connect_payload)
		print("GS Init response", gs_response)
		messageType = gs_response.get("messageType")
		messageData = gs_response.get("data")
		if messageType == "error":
			raise Exception(messageData)
		else:
			print("{}: {}".format(messageType, messageData))
			return gs_response

	def updateState(self, state):
		game_state_payload = json.dumps(
			{"messageType": "game-state", "data": {"state": state}}
		)
		gs_response = send_json(self.server_socket, game_state_payload)
		print("update response", gs_response)
		messageType = gs_response.get("messageType")
		messageData = gs_response.get("data")
		if messageType == "error":
			raise Exception(messageData)
		elif messageType == "game-state":
			print("game-state:", messageData)

	def finish(self):
		game_finish_payload = json.dumps({"messageType": "game-finished"})
		gs_response = send_json(self.server_socket, game_finish_payload)
		print("finished response", gs_response)
		messageType = gs_response.get("messageType")
		messageData = gs_response.get("data")
		if messageType == "error":
			raise Exception(messageData)
		elif messageType == "game-finished":
			print("game-finish", messageData)

game_round = 0
client1_hand = []
client1_played = []
client1_phase = 0
client1_score = 0
client1_skipped = False
client2_hand = []
client2_played = []
client2_phase = 0
client2_score = 0
client2_skipped = False
colors = ["red", "blue", "purple", "green"]
wilds = ["wild", "skip"]
burn = []
game_in_progress = True
pygame.init()
#UI
white=(255,255,255)
blue=(161,189,255)
CARD_WIDTH=94
CARD_HEIGHT=150
CARD_PADDING=10
SCOREBOARD_WIDTH=275
SCOREBOARD_HEIGHT=CARD_HEIGHT*3
CROWN_WIDTH= 45
CROWN_HEIGHT=50
GROUP_WIDTH=CARD_WIDTH*3+150
GROUP_HEIGHT=CARD_HEIGHT+10
WINDOW_WIDTH=(CARD_WIDTH+5)*11 + SCOREBOARD_WIDTH
WINDOW_HEIGHT=(CARD_HEIGHT+30)*5
BANNER_HEIGHT = CARD_HEIGHT
RULES_HEIGHT = SCOREBOARD_WIDTH-CARD_WIDTH+30

card_back=pygame.image.load('cards/card_back.png')
card_back=pygame.transform.scale(card_back,(CARD_WIDTH,CARD_HEIGHT))
card_blank=pygame.image.load('cards/card_blank.png')
card_blank=pygame.transform.scale(card_blank,(CARD_WIDTH,CARD_HEIGHT))
played_group_bracket=pygame.image.load('cards/played_group_bracket.png')
played_group_bracket=pygame.transform.scale(played_group_bracket,((CARD_WIDTH*CARD_PADDING)*4,CARD_HEIGHT+10))
scoreboard=pygame.image.load('cards/scoreboard.png')
scoreboard=pygame.transform.scale(scoreboard,(SCOREBOARD_WIDTH,SCOREBOARD_HEIGHT))
played_group=pygame.image.load('cards/played_group_bracket.png')
played_group_bracket=pygame.transform.scale(played_group_bracket,(GROUP_WIDTH,GROUP_HEIGHT))
crown=pygame.image.load('cards/crown.png')
crown=pygame.transform.scale(crown,(CROWN_WIDTH,CROWN_HEIGHT))
waiting_screen = pygame.image.load('cards/waiting_server.png')
waiting_screen = pygame.transform.scale(waiting_screen,(WINDOW_WIDTH,WINDOW_HEIGHT))
banner_waiting = pygame.image.load('cards/banner_waiting.png')
banner_waiting = pygame.transform.scale(banner_waiting,(WINDOW_WIDTH,BANNER_HEIGHT))
banner_skipped = pygame.image.load('cards/banner_skipped.png')
banner_skipped = pygame.transform.scale(banner_skipped,(WINDOW_WIDTH,BANNER_HEIGHT))
banner_your_turn = pygame.image.load('cards/banner_your_turn.png')
banner_your_turn = pygame.transform.scale(banner_your_turn,(WINDOW_WIDTH,BANNER_HEIGHT))
banner_you_won = pygame.image.load('cards/banner_you_won.png')
banner_you_won = pygame.transform.scale(banner_you_won,(WINDOW_WIDTH,BANNER_HEIGHT))
banner_you_lost = pygame.image.load('cards/banner_you_lost.png')
banner_you_lost = pygame.transform.scale(banner_you_lost,(WINDOW_WIDTH,BANNER_HEIGHT))

rule1 = pygame.image.load('cards/rules1-1.png')
rule1 = pygame.transform.scale(rule1,(RULES_HEIGHT, RULES_HEIGHT))
rule2 = pygame.image.load('cards/rules1-2.png')
rule2 = pygame.transform.scale(rule2,(RULES_HEIGHT, RULES_HEIGHT))
rule3 = pygame.image.load('cards/rules1-3.png')
rule3 = pygame.transform.scale(rule3,(RULES_HEIGHT, RULES_HEIGHT))
rules = [rule1, rule2, rule3]

gameDisplay = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption('Phase 10 Game - By AKA ETC')
clock = pygame.time.Clock()
crashed = False
gameDisplay.blit(waiting_screen, (0,0))
pygame.display.update()

#-----------------------> START OF Pygame Stuff


# Images

def getBurnTop():
	return (burn[0][0]+str(burn[0][1]))

def getStats():
	if is_lobby_leader:
		return [str(client1_score), str(client2_score), str(client1_phase+1), str(client2_phase+1)] 
	# MyScore, OtherScore, MyRound, OtherRound
	return [str(client2_score), str(client1_score), str(client2_phase+1), str(client1_phase+1)]

def displayCards(MY_HAND, OTHER_HAND, MY_PLAYED, OTHER_PLAYED):
	global client1_hand
	global client2_hand
	global client1_played
	global client2_played

	temp1=[]
	temp2=[]
	try:
		temp1.append(MY_PLAYED[1][0])
		if len(MY_PLAYED[1]) > 1:
						temp1.append(MY_PLAYED[1][-1])
		temp1.append(MY_PLAYED[3][0])
		if len(MY_PLAYED[3]) > 1:
						temp1.append(MY_PLAYED[3][-1])
	except:
		print(temp1)
	try:
		temp2.append(OTHER_PLAYED[1][0])
		if len(OTHER_PLAYED[1]) > 1:
						temp2.append(OTHER_PLAYED[1][-1])
		temp2.append(OTHER_PLAYED[3][0])
		if len(OTHER_PLAYED[1]) > 1:
						temp2.append(OTHER_PLAYED[3][-1])
	except:
		print(temp2)

	# Display My hand and My played cards
	for n,c in enumerate(MY_HAND,0):
		c=c[0]+str(c[1])
		if(c == 'wild'):
			c = 'NoneW'
		if(c == 'skip'):
			c = 'NoneS'
		my_card=pygame.image.load('cards/'+c+'.png')
		my_card=pygame.transform.scale(my_card,(CARD_WIDTH,CARD_HEIGHT))
		gameDisplay.blit(my_card, (n*(CARD_PADDING+CARD_WIDTH)+5,WINDOW_HEIGHT-CARD_HEIGHT-10))
	if temp1:
		for n,c in enumerate(temp1,0):
			print(c)
			c=c[0]+str(c[1])
			if(c == 'wild'):
				c = 'NoneW'
			if(c == 'skip'):
				c = 'NoneS'
			if(c == 'wild'):
				c = 'NoneW'
			my_card=pygame.image.load('cards/'+c+'.png')
			my_card=pygame.transform.scale(my_card,(CARD_WIDTH,CARD_HEIGHT))
			if(n < 2):
				gameDisplay.blit(my_card, (n*(CARD_PADDING+CARD_WIDTH+50)+100,WINDOW_HEIGHT-CARD_HEIGHT*2-47))
			else:
				gameDisplay.blit(my_card, (2*(CARD_PADDING+CARD_WIDTH)+(n-2)*(CARD_PADDING+CARD_WIDTH+50)+490,WINDOW_HEIGHT-CARD_HEIGHT*2-47))
			gameDisplay.blit(played_group_bracket, (5,WINDOW_HEIGHT-CARD_HEIGHT*2-51))
			gameDisplay.blit(played_group_bracket, (GROUP_WIDTH+175,WINDOW_HEIGHT-CARD_HEIGHT*2-51))

	# Display Opponent's hand and Opponent's played cards
	opp_cards=len(OTHER_HAND)
	for n in range(0,opp_cards):
		gameDisplay.blit(card_back, (n*(CARD_PADDING+CARD_WIDTH)+5,0))
	if temp2:
		for n,c in enumerate(temp2,0):
			c=c[0]+str(c[1])
			if(c == 'wild'):
				c = 'NoneW'
			if(c == 'skip'):
				c = 'NoneS'
			my_card=pygame.image.load('cards/'+c+'.png')
			my_card=pygame.transform.scale(my_card,(CARD_WIDTH,CARD_HEIGHT))
			if(n < 2):
				gameDisplay.blit(my_card, (n*(CARD_PADDING+CARD_WIDTH+50)+100,CARD_HEIGHT+50))
			else:
				gameDisplay.blit(my_card, (2*(CARD_PADDING+CARD_WIDTH)+(n-2)*(CARD_PADDING+CARD_WIDTH+50)+490,CARD_HEIGHT+50))
			gameDisplay.blit(played_group_bracket, (5,CARD_HEIGHT+50))
			gameDisplay.blit(played_group_bracket, (GROUP_WIDTH+175,CARD_HEIGHT+50))


	'''# Display Opponent's hand and Opponent's played cards
	opp_cards=len(client2_hand)
	for n in range(0,opp_cards):
		gameDisplay.blit(card_back, (n*(CARD_PADDING+CARD_WIDTH)+5,0))
	if client2_played:
		for n,c in enumerate(client2_played[1],0):
			c=c[0]+str(c[1])
			if(c == 'wild'):
				c = 'NoneW'
			if(c == 'skip'):
				c = 'NoneS'
			my_card=pygame.image.load('cards/'+c+'.png')
			my_card=pygame.transform.scale(my_card,(CARD_WIDTH,CARD_HEIGHT))
			gameDisplay.blit(my_card, (n*(CARD_PADDING+CARD_WIDTH)+5,CARD_HEIGHT+50))
			gameDisplay.blit(card_blank, ((len(client2_played)*(CARD_PADDING+CARD_WIDTH))+5,CARD_HEIGHT+50))

	else:
		gameDisplay.blit(card_blank, (5,CARD_HEIGHT+50))'''


def displayGame():
	# Scoreboard Displaying
	stats = getStats()
	if stats[2] == "4":
		stats[2] = "YEET"
	if stats[3] == "4":
		stats[3] = "YEET"
		
	gameDisplay.blit(scoreboard, (WINDOW_WIDTH-SCOREBOARD_WIDTH,CARD_HEIGHT))
	if stats[2] is not "YEET":
		gameDisplay.blit(rules[int(stats[2])-1], (WINDOW_WIDTH-RULES_HEIGHT, WINDOW_HEIGHT-RULES_HEIGHT))

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
	if stats[2] == "YEET":
		stats[2] = "4"
	if stats[3] == "YEET":
		stats[3] = "4"
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
	if burn == 'wild':
		burn='NoneW'
	if burn == 'skip':
		burn='NoneS'
	burn=pygame.image.load('cards/'+burn+'.png')
	burn=pygame.transform.scale(burn,(CARD_WIDTH,CARD_HEIGHT))
	gameDisplay.blit(burn, ((4*CARD_WIDTH)+5,(WINDOW_HEIGHT/2)-(CARD_HEIGHT/2)))
	gameDisplay.blit(card_back,((6*CARD_WIDTH)+5,(WINDOW_HEIGHT/2)-(CARD_HEIGHT/2)))

def update_everything(h1, h2, p1, p2):
	gameDisplay.fill(blue)
	displayGame()
	displayCards(h1, h2, p1, p2)
	pygame.display.update()

def pretty_p(msg):
	print('--------------------testing pretty print---------------')
	print(msg['data']['state']['game'])
	print(msg['data']['state']['round'])
	print(msg['data']['state']['client1']['hand'])
	print(msg['data']['state']['client1']['played'])
	print(msg['data']['state']['client1']['phase'])
	print(msg['data']['state']['client1']['score'])
	print(msg['data']['state']['client2']['hand'])
	print(msg['data']['state']['client2']['played'])
	print(msg['data']['state']['client2']['phase'])
	print(msg['data']['state']['client2']['score'])
	print('-------------------------------------------------------')
	return

def draw_card(h):
	color = random.choice(colors)
	if random.randint(1,14) == 1:
		color = ""
		num = random.choice(wilds)
	else:
		num = random.randint(1, 12)
	h.append([color, num])

def play_cards(hand, lst1, lst2, play_num, other_hand, other_played, lst_num, type1, type2):
	for i in range(0,play_num): # Play the first set
		crashed=False
		pygame.event.get()
		while not crashed:

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					crashed = True
					c.updateState({"game": False,
							"round": game_round,
							"burn": burn,
							"client1": { "hand": client1_hand, "played": client1_played, "phase": client1_phase, "score": client1_score, "skipped": client1_skipped },
							"client2": { "hand": client2_hand, "played": client2_played, "phase": client2_phase, "score": client2_score, "skipped": client2_skipped }})
					pygame.quit()
					sys.exit()

				if event.type == pygame.MOUSEBUTTONDOWN:
					x, y=event.pos
					#deck event
					if((x>=((4*CARD_WIDTH)+5) and x<=((5*CARD_WIDTH)+5)) and (y>=((WINDOW_HEIGHT/2)-(CARD_HEIGHT/2)) and y<=((WINDOW_HEIGHT/2)-(CARD_HEIGHT/2)+CARD_HEIGHT))):
						return True
					if(x>=5 and x<=(11*(CARD_PADDING+CARD_WIDTH)+5)) and (y>=(WINDOW_HEIGHT-CARD_HEIGHT-10) and y<=(WINDOW_HEIGHT-10)):
						card_clicked=int((x-5)/(CARD_PADDING+CARD_WIDTH))
						if(card_clicked<=len(hand)-1):
							if lst_num == 0:
								lst1.append(hand.pop(card_clicked))
							else:
								lst2.append(hand.pop(card_clicked))
							crashed = True
							lst = [type1, lst1, type2, lst2]
							update_everything(hand, other_hand, lst, other_played)
			clock.tick(60)
	return False

def play_phase(hand, phase, you_played, other_hand, other_played): # pass in the player hand, player phase, what the player played
	if you_played == []: # playing phases
		if phase == 0: # phase 1 (2 sets)
			set1 = []
			set2 = []
			phase_done = False
			print("Play 2 sets of 3 cards to complete phase 1")
			while(not phase_done):
				print("Play the cards you want for the 1st set in order or type 0 to end turn: ")
				end_turn = play_cards(hand, set1, set2, 3, other_hand, other_played, 0, "set", "set") # play cards
				if (end_turn): # return cards if turn is ended
					for i in range(0,len(set1)):
						hand.append(set1.pop(0))
					update_everything(hand, other_hand, you_played, other_played)
					return phase

				if (is_set(set1)): # play second set if first is a set otherwise start over
					print("Play the cards you want for the 2nd set in order or type 0 to end turn: ")
					end_turn = play_cards(hand, set1, set2, 3, other_hand, other_played, 1, "set", "set") # play cards
					if (end_turn): # return cards of turn is ended without playing phase
						for i in range(0,len(set1)):
							hand.append(set1.pop(0))
						for i in range(0,len(set2)):
							hand.append(set2.pop(0))
						update_everything(hand, other_hand, you_played, other_played)
						return phase
					
					if (is_set(set2)): # update your played cards to your phase otherwise start over
						# using = does not update client_played because python dumb
						you_played.append("set")
						you_played.append(set1)
						you_played.append("set")
						you_played.append(set2)
						convert_wilds(you_played)
						phase += 1
						phase_done = True
					else:
						print("Please enter a valid phase") # return cards if not a set
						for i in range(0,len(set1)):
							hand.append(set1.pop(0))
						for i in range(0,len(set2)):
							hand.append(set2.pop(0))
						update_everything(hand, other_hand, you_played, other_played)
				else:
					print("Please enter a valid phase") # return cards if not a set
					for i in range(0,len(set1)):
						hand.append(set1.pop(0))
					update_everything(hand, other_hand, you_played, other_played)

		elif phase == 1: # phase 2 (1 sets & 1 run)
			set1 = []
			run1 = []
			phase_done = False
			print("Play 1 set of 3 and 1 run of 4 to complete phase 2")
			while(not phase_done):
				print("Play the cards you want for the set in order or type 0 to end turn: ")
				end_turn = play_cards(hand, set1, run1, 3, other_hand, other_played, 0 ,"set", "run") # play cards
				if (end_turn): # return cards if turn is ended
					for i in range(0,len(set1)):
						hand.append(set1.pop(0))
					update_everything(hand, other_hand, you_played, other_played)
					return phase

				if (is_set(set1)): # play second set if first is a set otherwise start over
					print("Play the cards you want for the run in order or type 0 to end turn: ")
					end_turn = play_cards(hand, set1, run1, 4,other_hand, other_played, 1, "set", "run") # play cards
					if (end_turn): # return cards of turn is ended without playing phase
						for i in range(0,len(set1)):
							hand.append(set1.pop(0))
						for i in range(0,len(run1)):
							hand.append(run1.pop(0))
						update_everything(hand, other_hand, you_played, other_played)
						return phase
					
					if (is_run(run1)): # update your played cards to your phase otherwise start over
						# using = does not update client_played because python dumb
						you_played.append("set")
						you_played.append(set1)
						you_played.append("run")
						you_played.append(run1)
						convert_wilds(you_played)
						phase += 1
						phase_done = True
					else:
						print("Please enter a valid phase") # return cards if not a set
						for i in range(0,len(set1)):
							hand.append(set1.pop(0))
						for i in range(0,len(run1)):
							hand.append(run1.pop(0))
						update_everything(hand, other_hand, you_played, other_played)
				else:
					print("Please enter a valid phase") # return cards if not a set
					for i in range(0,len(set1)):
						hand.append(set1.pop(0))
					update_everything(hand, other_hand, you_played, other_played)

		elif phase == 2: # phase 3 (1 sets & 1 run)
			set1 = []
			run1 = []
			phase_done = False
			print("Play 1 set of 4 and 1 run of 4 to complete phase 2")
			while(not phase_done):
				print("Play the cards you want for the set in order or type 0 to end turn: ")
				end_turn = play_cards(hand, set1, run1, 4, other_hand, other_played, 0, "set", "run") # play cards
				if (end_turn): # return cards if turn is ended
					for i in range(0,len(set1)):
						hand.append(set1.pop(0))
					update_everything(hand, other_hand, you_played, other_played)
					return phase

				if (is_set(set1)): # play second set if first is a set otherwise start over
					print("Play the cards you want for the run in order or type 0 to end turn: ")
					end_turn = play_cards(hand, set1, run1, 4, other_hand, other_played, 1, "set", "run") # play cards
					if (end_turn): # return cards of turn is ended without playing phase
						for i in range(0,len(set1)):
							hand.append(set1.pop(0))
						for i in range(0,len(run1)):
							hand.append(run1.pop(0))
						update_everything(hand, other_hand, you_played, other_played)
						return phase
					
					if (is_run(run1)): # update your played cards to your phase otherwise start over
						# using = does not update client_played because python dumb
						you_played.append("set")
						you_played.append(set1)
						you_played.append("run")
						you_played.append(run1)
						convert_wilds(you_played)
						phase += 1
						phase_done = True
					else:
						print("Please enter a valid phase") # return cards if not a set
						for i in range(0,len(set1)):
							hand.append(set1.pop(0))
						for i in range(0,len(run1)):
							hand.append(run1.pop(0))
						update_everything(hand, other_hand, you_played, other_played)
				else:
					print("Please enter a valid phase") # return cards if not a set
					for i in range(0,len(set1)):
						hand.append(set1.pop(0))
					update_everything(hand, other_hand, you_played, other_played)
	return phase

def hit(hand, you_played, opponent_hand, opponent_played):
	if you_played != []:
		playing = True
		while(playing and hand != []):
			crashed=False
			pygame.event.get()
			while not crashed:

				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						crashed = True
						c.updateState({"game": False,
								"round": game_round,
								"burn": burn,
								"client1": { "hand": client1_hand, "played": client1_played, "phase": client1_phase, "score": client1_score, "skipped": client1_skipped },
								"client2": { "hand": client2_hand, "played": client2_played, "phase": client2_phase, "score": client2_score, "skipped": client2_skipped }})
						pygame.quit()
						sys.exit()
						
					if event.type == pygame.MOUSEBUTTONDOWN:
						x, y=event.pos

						if((x>=((4*CARD_WIDTH)+5) and x<=((5*CARD_WIDTH)+5)) and (y>=((WINDOW_HEIGHT/2)-(CARD_HEIGHT/2)) and y<=((WINDOW_HEIGHT/2)-(CARD_HEIGHT/2)+CARD_HEIGHT))):
							group = 0
							crashed = True
						
						if((x>=2 and x<=50) and (y>=607 and y<=650)):
							print('Left most button my played left group')
							group = 1
							side = 1
							crashed = True
						if((x>=387 and x<=441) and (y>=609 and y<=650)):
							print('Right most button my played left group')
							group = 1
							side = 2
							crashed = True
						if((x>=600 and x<=650) and (y>=607 and y<=650)):
							print('Left most button my played right group')
							group = 2
							side = 1
							crashed = True
						if((x>=987 and x<=1050) and (y>=609 and y<=650)):
							print('Right most button my played right group')
							group = 2
							side = 2
							crashed = True

						#Buttons for adding to other played cards
						if (opponent_played != []):
							if((x>=2 and x<=50) and (y>=255 and y<=305)):
								print('Left most button my other left group')
								group = 3
								side = 1
								crashed = True
							if((x>=387 and x<=441) and (y>=255 and y<=305)):
								print('Right most button my other left group')
								group = 3
								side = 2
								crashed = True
							if((x>=600 and x<=650) and (y>=255 and y<=305)):
								print('Left most button my other right group')
								group = 4
								side = 1
								crashed = True
							if((x>=987 and x<=1050) and (y>=255 and y<=305)):
								print('Right most button my other right group')
								group = 4
								side = 2
								crashed = True
				clock.tick(60)

			cards = []
			group_type = "set"
			if group == 0:
				return
			elif group == 1:
				cards = you_played[1]
				group_type = you_played[0]
			elif group == 2:
				cards = you_played[3]
				group_type = you_played[2]
			elif group == 3:
				cards = opponent_played[1]
				group_type = opponent_played[0]
			else:
				cards = opponent_played[3]
				group_type = opponent_played[2]

			if(side == 1):
				crashed=False
				pygame.event.get()
				while not crashed:

					for event in pygame.event.get():
						if event.type == pygame.QUIT:
							crashed = True
							c.updateState({"game": False,
									"round": game_round,
									"burn": burn,
									"client1": { "hand": client1_hand, "played": client1_played, "phase": client1_phase, "score": client1_score, "skipped": client1_skipped },
									"client2": { "hand": client2_hand, "played": client2_played, "phase": client2_phase, "score": client2_score, "skipped": client2_skipped }})
							pygame.quit()
							sys.exit()

						if event.type == pygame.MOUSEBUTTONDOWN:
							x, y=event.pos
							#deck event
							if((x>=((4*CARD_WIDTH)+5) and x<=((5*CARD_WIDTH)+5)) and (y>=((WINDOW_HEIGHT/2)-(CARD_HEIGHT/2)) and y<=((WINDOW_HEIGHT/2)-(CARD_HEIGHT/2)+CARD_HEIGHT))):
								return
							if(x>=5 and x<=(11*(CARD_PADDING+CARD_WIDTH)+5)) and (y>=(WINDOW_HEIGHT-CARD_HEIGHT-10) and y<=(WINDOW_HEIGHT-10)):
								card_clicked=int((x-5)/(CARD_PADDING+CARD_WIDTH))
								if(card_clicked<=len(hand)-1):
									play = card_clicked
									crashed = True
					clock.tick(60)
				cards.insert(0,hand.pop(play))
				if (group_type == "set"):
					if (not is_set(cards)):
						hand.append(cards.pop(0))
						print("This is not a valid set")
				else:
					if (not is_run(cards)):
						hand.append(cards.pop(0))
						print("This is not a valid run")
			else:
				crashed=False
				pygame.event.get()
				while not crashed:

					for event in pygame.event.get():
						if event.type == pygame.QUIT:
							crashed = True
							c.updateState({"game": False,
									"round": game_round,
									"burn": burn,
									"client1": { "hand": client1_hand, "played": client1_played, "phase": client1_phase, "score": client1_score, "skipped": client1_skipped },
									"client2": { "hand": client2_hand, "played": client2_played, "phase": client2_phase, "score": client2_score, "skipped": client2_skipped }})
							pygame.quit()
							sys.exit()

						if event.type == pygame.MOUSEBUTTONDOWN:
							x, y=event.pos
							#deck event
							if((x>=((4*CARD_WIDTH)+5) and x<=((5*CARD_WIDTH)+5)) and (y>=((WINDOW_HEIGHT/2)-(CARD_HEIGHT/2)) and y<=((WINDOW_HEIGHT/2)-(CARD_HEIGHT/2)+CARD_HEIGHT))):
								return
							if(x>=5 and x<=(11*(CARD_PADDING+CARD_WIDTH)+5)) and (y>=(WINDOW_HEIGHT-CARD_HEIGHT-10) and y<=(WINDOW_HEIGHT-10)):
								card_clicked=int((x-5)/(CARD_PADDING+CARD_WIDTH))
								if(card_clicked<=len(hand)-1):
									play = card_clicked
									crashed = True
					clock.tick(60)
				cards.append(hand.pop(play))
				if (group_type == "set"):
					if (not is_set(cards)):
						hand.append(cards.pop(len(cards)-1))
						print("This is not a valid set")
				else:
					if (not is_run(cards)):
						hand.append(cards.pop(len(cards)-1))
						print("This is not a valid run")
			convert_wilds(you_played)
			if opponent_played:
				convert_wilds(opponent_played)
			update_everything(hand, opponent_hand, you_played, opponent_played)
		return
	else:
		return

def is_set(s):
	#check if s is a set

	is_a_set = True
	if (s == []):
		return False
	set_num = 0
	for i in range(0,len(s)):
		if (s[i][1] != 'wild' and is_a_set):
			if (s[i][1] == 'skip'):
				is_a_set = False
			elif (set_num == 0):
				set_num = s[i][1]
			elif (s[i][1] != set_num):
				is_a_set = False
	if (set_num == 0):
		return False
	return is_a_set

def is_run(r):
	# check if r is a run
	if (r == []):
		return False
	is_a_run = True
	first_num = True
	run_num = 0
	for i in range(0,len(r)):
		if is_a_run:
			run_num += 1
			if (r[i][1] == 'skip'): # check for if a skip is played
				is_a_run = False
			elif (r[i][1] != 'wild'):
				if (r[i][1] > run_num):
					if (first_num):
						run_num = r[i][1]
						first_num = False
					else: # check for if there is a break in the run
						is_a_run = False
				elif (r[i][1] < run_num): # check for if number is less than the number before it or if the run starts below 1 using wilds
					is_a_run = False
			elif (run_num > 12): # check for if the run goes past 12 using wilds
				is_a_run = False
	return is_a_run

def convert_set(s):
	set_num = 0
	for i in range(0,len(s)):
		if s[i][1] != 'wild':
			set_num = s[i][1]
	for i in range(0,len(s)):
		if s[i][1] == 'wild':
			s[i] = ['w', set_num]
	return

def convert_run(r):
	run_num = 0
	for i in range(0,len(r)):
		run_num += 1
		if r[i][1] != 'wild':
			if int(r[i][1]) > run_num:
				run_num = int(r[i][1])
	for i in range(0,len(r)):
		if r[i][1] == 'wild':
			r[i] = ['w', i+1+(run_num-len(r))]
	return

def convert_wilds(played):
	if played[0] == "set":
		convert_set(played[1])
	elif played[0] == "run":
		convert_run(played[1])
	if played[2] == "set":
		convert_set(played[3])
	elif played[2] == "run":
		convert_run(played[3])

def update_game_state(msg):

	# this is necessary otherwise it won't update the actual variables
	global game_in_progress
	global game_round
	global burn
	global client1_hand
	global client1_played
	global client1_phase
	global client1_score
	global client1_skipped
	global client2_hand
	global client2_played
	global client2_phase
	global client2_score
	global client2_skipped
	game_in_progress = msg["data"]["state"]["game"]
	game_round = msg["data"]["state"]["round"]
	burn = msg["data"]["state"]["burn"]
	client1_hand = msg["data"]["state"]["client1"]["hand"]
	client1_played = msg["data"]["state"]["client1"]["played"]
	client1_phase = msg["data"]["state"]["client1"]["phase"]
	client1_score = msg["data"]["state"]["client1"]["score"]
	client1_skipped = msg["data"]["state"]["client1"]["skipped"]
	client2_hand = msg["data"]["state"]["client2"]["hand"]
	client2_played = msg["data"]["state"]["client2"]["played"]
	client2_phase = msg["data"]["state"]["client2"]["phase"]
	client2_score = msg["data"]["state"]["client2"]["score"]
	client2_skipped = msg["data"]["state"]["client2"]["skipped"]
	return

def add_score(winner_score, loser_hand):
	for card in loser_hand:
		if card[1] == "wild":
			winner_score += 25
		elif card[1] == "skip":
			winner_score += 15
		elif card[1] == 10 or card[1] == 11 or card[1] == 12:
			winner_score += 10
		else:
			winner_score += 5
	return winner_score

# not tested yet waiting on play cards function
def start_new_round():
	global game_in_progress
	global game_round
	global burn
	global client1_hand
	global client1_played
	global client1_phase
	global client1_score
	global client1_skipped
	global client2_hand
	global client2_played
	global client2_phase
	global client2_score
	global client2_skipped

	client1_skipped = False
	client2_skipped = False

	# add phase/test win condition
	if client1_hand == []:
		client2_score = add_score(client2_score, client2_hand)
		if client1_phase == 3:
			game_in_progress = False
			gameDisplay.blit(banner_you_won, (0,WINDOW_HEIGHT/2))
			pygame.display.update()
			time.sleep(3)
			return
		client2_hand = []
	elif client2_hand == []:
		client1_score += add_score(client1_score, client1_hand)
		if client2_phase == 3:
			game_in_progress = False
			gameDisplay.blit(banner_you_won, (0,WINDOW_HEIGHT/2))
			pygame.display.update()
			time.sleep(3)
			return
		client1_hand = []

	# set up next round
	client1_played = []
	client2_played = []
	game_round += 1
	draw_card(burn)
	for i in range(0, 10):
		draw_card(client1_hand)
		draw_card(client2_hand)
	return


#Drawing card example for UI implementation
#def draw(hand):
#    global burn
	
#    drawing = True
#    while(drawing):
#        if (test_for_event("draw from deck event")): # replace "draw from deck event" with whatever event would be drawing from the deck
#            draw_card(hand)
#            drawing = False
#        elif (test_for_event("draw from burn event") and burn[0] != ['', 'skip']):  # replace "draw from burn event" with whatever event would be drawing from the burn pile
#            hand.append(burn.pop(0))
#            drawing = False
#    "visuals"
#    return

#def test_for_event("Desired event"): # replace "desired event" with whatever event you are looking for (draw, play card, etc.)
#   for event in pygame.event.get():
#       if event.type == "Desired event": # i don't know if this is how you would test for an event but I think you get the idea
#           return True
#   return False

def draw(hand):
	global burn

	crashed=False
	pygame.event.get()
	while not crashed:

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				crashed = True
				c.updateState({"game": False,
						   "round": game_round,
						   "burn": burn,
						   "client1": { "hand": client1_hand, "played": client1_played, "phase": client1_phase, "score": client1_score, "skipped": client1_skipped },
						   "client2": { "hand": client2_hand, "played": client2_played, "phase": client2_phase, "score": client2_score, "skipped": client2_skipped }})
				pygame.quit()
				sys.exit()

			if event.type == pygame.MOUSEBUTTONDOWN:
				x, y=event.pos
				#burn event
				if burn[0] != ['', 'skip']:
					if((x>=((4*CARD_WIDTH)+5) and x<=((5*CARD_WIDTH)+5)) and (y>=((WINDOW_HEIGHT/2)-(CARD_HEIGHT/2)) and y<=((WINDOW_HEIGHT/2)-(CARD_HEIGHT/2)+CARD_HEIGHT))):
						hand.append(burn[0])
						crashed = True
				#deck event
				if((x>=((6*CARD_WIDTH)+5) and x<=((7*CARD_WIDTH)+5)) and (y>=((WINDOW_HEIGHT/2)-(CARD_HEIGHT/2)) and y<=((WINDOW_HEIGHT/2)-(CARD_HEIGHT/2)+CARD_HEIGHT))):
					draw_card(hand)
					crashed = True
		clock.tick(60)
	return    

def end_turn(hand):
	global game_in_progress
	global game_round
	global burn
	global client1_hand
	global client1_played
	global client1_phase
	global client1_score
	global client2_hand
	global client2_played
	global client2_phase
	global client2_score

	skip = False
	# check if player runs out of cards during play part of turn
	if hand == []:
		start_new_round()
		return skip
	print(hand)

	crashed=False
	pygame.event.get()
	while not crashed:

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				crashed = True
				c.updateState({"game": False,
						   "round": game_round,
						   "burn": burn,
						   "client1": { "hand": client1_hand, "played": client1_played, "phase": client1_phase, "score": client1_score, "skipped": client1_skipped },
						   "client2": { "hand": client2_hand, "played": client2_played, "phase": client2_phase, "score": client2_score, "skipped": client2_skipped }})
				pygame.quit()
				sys.exit()

			if event.type == pygame.MOUSEBUTTONDOWN:
				x, y=event.pos
				if(x>=5 and x<=(11*(CARD_PADDING+CARD_WIDTH)+5)) and (y>=(WINDOW_HEIGHT-CARD_HEIGHT-10) and y<=(WINDOW_HEIGHT-10)):
						card_clicked=int((x-5)/(CARD_PADDING+CARD_WIDTH))
						if(card_clicked<=len(hand)-1):
							burn = [hand[card_clicked]]
							del hand[card_clicked]
							crashed = True
				
		clock.tick(60)

	if burn[0] == ['', 'skip']:
		skip = True

	# start new round if player discards last card
	if hand == []:
		start_new_round()
		skip = False
	return skip

#Player's Turn
def take_turn(c, leader):
	global game_in_progress
	global game_round
	global burn
	global client1_hand
	global client1_played
	global client1_phase
	global client1_score
	global client1_skipped
	global client2_hand
	global client2_played
	global client2_phase
	global client2_score
	global client2_skipped
	
	# draw card - done and tested - need further testing by other members
	# play phase or play card (if phase is done)
	# check if empty after phase/play card -> skip discard if true
	# discard (end turn)
	# check if empty after discard 
	# check win condition
	# start new round 

	print("----------Begin Turn----------")
	print(client1_hand)
	print(client2_hand)
	print("------------------------------")
	gameDisplay.blit(banner_your_turn, (0,WINDOW_HEIGHT/2))
	pygame.display.update()
	time.sleep(2)
	if leader:
		if (client1_skipped): # skip player1's turn
			gameDisplay.blit(banner_skipped, (0,WINDOW_HEIGHT/2))
			pygame.display.update()
			time.sleep(3)
			client1_skipped = False
			c.updateState({"game": game_in_progress,
						   "round": game_round,
						   "burn": burn,
						   "client1": { "hand": client1_hand, "played": client1_played, "phase": client1_phase, "score": client1_score, "skipped": client1_skipped },
						   "client2": { "hand": client2_hand, "played": client2_played, "phase": client2_phase, "score": client2_score, "skipped": client2_skipped }})
			return

		update_everything(client1_hand, client2_hand, client1_played, client2_played)

		draw(client1_hand)

		update_everything(client1_hand, client2_hand, client1_played, client2_played)
		
		client1_phase = play_phase(client1_hand, client1_phase, client1_played, client2_hand, client2_played)

		update_everything(client1_hand, client2_hand, client1_played, client2_played)
		
		hit(client1_hand, client1_played, client2_hand, client2_played)

		update_everything(client1_hand, client2_hand, client1_played, client2_played)

		client2_skipped = end_turn(client1_hand)

		update_everything(client1_hand, client2_hand, client1_played, client2_played)
		
	else:
		if (client2_skipped): # skip player2's turn
			gameDisplay.blit(banner_skipped, (0,WINDOW_HEIGHT/2))
			pygame.display.update()
			time.sleep(3)
			client2_skipped = False
			c.updateState({"game": game_in_progress,
						   "round": game_round,
						   "burn": burn,
						   "client1": { "hand": client1_hand, "played": client1_played, "phase": client1_phase, "score": client1_score, "skipped": client1_skipped },
						   "client2": { "hand": client2_hand, "played": client2_played, "phase": client2_phase, "score": client2_score, "skipped": client2_skipped }})
			return
	
		update_everything(client2_hand, client1_hand, client2_played, client1_played)
		
		draw(client2_hand)

		update_everything(client2_hand, client1_hand, client2_played, client1_played)
		
		client2_phase = play_phase(client2_hand, client2_phase, client2_played, client1_hand, client1_played)

		update_everything(client2_hand, client1_hand, client2_played, client1_played)

		hit(client2_hand, client2_played, client1_hand, client1_played)

		update_everything(client2_hand, client1_hand, client2_played, client1_played)

		client1_skipped = end_turn(client2_hand)

		update_everything(client2_hand, client1_hand, client2_played, client1_played)
		
	c.updateState({"game": game_in_progress,
				   "round": game_round,
				   "burn": burn,
				   "client1": { "hand": client1_hand, "played": client1_played, "phase": client1_phase, "score": client1_score, "skipped": client1_skipped },
				   "client2": { "hand": client2_hand, "played": client2_played, "phase": client2_phase, "score": client2_score, "skipped": client2_skipped }})
	return

def wait_for_turn(c):
	gameDisplay.blit(banner_waiting, (0,WINDOW_HEIGHT/2))
	pygame.display.update()
	message = c.recv_json()
	update_game_state(message)
	pretty_p(message)
	if not game_in_progress:
		gameDisplay.blit(banner_you_lost, (0,WINDOW_HEIGHT/2))
		pygame.display.update()
		time.sleep(3)
	return


def main():
	with socket.socket() as s:
		print("Welcome to aka etc Phase 10")
		player_id = "Player" + str(random.randint(0, 999))
		print("Matchmaking has started")

		# initialize pygame - reenable when ui is implemented
#        pygame.init()

		# initializing the game window
#        gameDisplay = pygame.display.set_mode((display_width, display_height))
#        pygame.display.set_caption("some cards")
#        clock = pygame.time.Clock()

		# initialize the diaplay to a gray background
#        gameDisplay.fill(gray)
		
		# Connect to matchmaking server
		s.connect((HOST, PORT))

		client = Client("player-" + player_id, s)
		try:
			client.waitForMM()
			time.sleep(1)
			init_response = client.sendGSInit()
			# What is my ID given to me by the game server
			my_client_id = init_response["data"]["id"]
			# Am I the lobby leader in this match? If so, I need to send the
			# initial state
			my_lobby_leader = False

			# We should receive a 'client-info' message for each client we
			# connect. We are going to assume there are only 2 clients and hard
			# code this for the sake of example, but you should dynamically
			# determine how many clients are connected. Dynamically this can be
			# done with the client-list message or some other method.
			client_infos = [client.recv_json(), client.recv_json()]

			# See if I am the lobby leader by iterating through all of the
			# connected clients, and seeing if my id matches the lobby leaders
			# id. We will attempt to change this to make this easier in the
			# future, but for backwards compatibility we will leave this for now
			global game_in_progress
			global game_round
			global burn
			global client1_hand
			global client1_played
			global client1_phase
			global client1_score
			global client1_skipped
			global client2_hand
			global client2_played
			global client2_phase
			global client2_score
			global client2_skipped
			global is_lobby_leader

			for client_info in client_infos:
				client_id = client_info["data"]["id"]
				is_lobby_leader = client_info["data"]["isLobbyLeader"]

				if my_client_id == client_id and is_lobby_leader:
					my_lobby_leader = True

			# If you are the lobby leader, you need to send the initial state
			if my_lobby_leader:
				is_lobby_leader = True
				#Initialize Game
				draw_card(burn)
				if burn[0] == ['', 'skip']:
					client1_skipped = True
				for i in range(0, 10):
					draw_card(client1_hand)
					draw_card(client2_hand)
#				client1_hand = [['green', 1],['green', 1],['green', 1],['green', 1],['green', 1],['green', 1],['green', 1],['green', 1],['green', 1],['green', 1]]
				#UI Displaying
				gameDisplay.fill(blue)
				print("Displaying Game")
				displayGame()
				print("Displaying Cards")
				displayCards(client1_hand, client2_hand, client1_played, client2_played)
				print("Updating Game")
				pygame.display.update()
				client.updateState({"game": game_in_progress,
									"round": game_round,
									"burn": burn,
									"client1": { "hand": client1_hand, "played": client1_played, "phase": client1_phase, "score": client1_score, "skipped": client1_skipped },
									"client2": { "hand": client2_hand, "played": client2_played, "phase": client2_phase, "score": client2_score, "skipped": client2_skipped }})


				#Game
				while game_in_progress:
					update_everything(client1_hand, client2_hand, client1_played, client2_played)
					take_turn(client, my_lobby_leader)
					if game_in_progress:
						wait_for_turn(client)
					
			# Otherwise, you need to wait for the initial state to be sent
			else:
				is_lobby_leader = False
				#Initialize Game
				wait_for_turn(client)
				#UI Displaying
				gameDisplay.fill(blue)
				print("Displaying Game")
				displayGame()
				print("Displaying Cards")
				displayCards(client2_hand, client1_hand, client2_played, client1_played)
				print("Updating Game")
				pygame.display.update()

				#Game
				while game_in_progress:
					wait_for_turn(client)
					if game_in_progress:
						update_everything(client2_hand, client1_hand, client2_played, client1_played)
						take_turn(client, my_lobby_leader)
				

			# Finish the game
			
#            pygame.quit()
			client.finish()
			print("finish", client.recv_json())
		except Exception as e:
			print("Error:", e)
			return
		print("done")
		return


if __name__ == "__main__":
	main()


#-----------------------> END OF Pygame Stuff
