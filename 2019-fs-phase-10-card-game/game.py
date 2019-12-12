import sys
sys.path.append('./required_python_packages')
import pygame
import random


file_path = "cards/"
colors = ["red", "red", "blue", "blue", "purple", "purple", "green", "green", ""]
wilds = ["wild", "skip"]


def card_display(x, y, c, w, h):
    display_card = pygame.image.load(file_path + c + ".png")
    display_card = pygame.transform.scale(display_card, (w, h))
    gameDisplay.blit(display_card, (x, y))


def draw_card(h):
    color = random.choice(colors)
    if color == "":
        num = random.choice(wilds)
    else:
        num = random.randint(1, 12)
    h.append(color + str(num))


pygame.init()

display_width = 1600
display_height = 1200

black = (0, 0, 0)
white = (255, 255, 255)
gray = (200, 200, 200)

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("some cards")
clock = pygame.time.Clock()

hand = []

for i in range(0, 10):
    draw_card(hand)

hand.sort()
gameDisplay.fill(gray)
playGame = True

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
            if (mx % 130 >= 10) and (mx % 130 <= 129) and (my >= 10) and (my <= 200):
                card_num = (mx+130-(mx % 130))/130
                del hand[int(card_num-1)]
                draw_card(hand)
                hand.sort()

    pygame.display.update()
    clock.tick(60)


pygame.quit()
quit()
