from logic.game_logic import *
from logic.player_logic import *

p1=Player('Kye')
p2=Player('Alex')
p3=Player('Ashton')

players=[p1,p2,p3]

if len(players) <= 6:
	setupGame(players)



playGame = True

hand=players[0].showHand()

while playGame:
    width = 10

    for card in hand:
        card_display(width, 10, card, 125, 200)
        width = width + 130

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playGame = False
        elif event.type == pygame.MOUSEBUTTONUP:
            mx, my = pygame.mouse.get_pos()
            print(mx,my)
            if (mx % 130 >= 10) and (mx % 130 <= 129) and (my >= 10) and (my <= 200):
                card_num = (mx+130-(mx % 130))/130
                del hand[int(card_num-1)]
                draw_card(hand)
                hand.sort()

    pygame.display.update()
    clock.tick(60)


pygame.quit()
quit()