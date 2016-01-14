import pygame
from pygame.locals import KEYDOWN, QUIT, MOUSEBUTTONDOWN, K_RETURN, K_ESCAPE
import sys

screen_x = 500
screen_y = 500

city_color = [10,10,200] # blue
city_radius = 3

font_color = [255,255,255] # white

pygame.init() 
window = pygame.display.set_mode((screen_x, screen_y)) 
pygame.display.set_caption('Exemple') 
screen = pygame.display.get_surface() 
font = pygame.font.Font(None,30)

class City:

    def __init__(self, name, pos):
        self.name = name
        self.pos = pos

cities = []

def parseFile(connections):
    lines = connections.split("\n")

    for line in lines:
        word = line.split(" ")
        pos = (int(word[1]), int(word[2]))
        nom = word[0]
        newCity = City(nom, pos)
        cities.append(newCity)

def ga_solve(file=None, gui=True, maxtime=0):
    fileCities = open(file, "r")
    parseFile(fileCities.read())

try:
    ga_solve(sys.argv[1], True, 1)
except:
    file = None

def draw(positions):
    screen.fill(0)
    font = pygame.font.Font(None,20)

    for pos in positions:
        pygame.draw.circle(screen, city_color, pos.pos, city_radius)
        screen.blit(font.render("%s %s" % (pos.name, pos.pos), True, font_color), pos.pos)

    font = pygame.font.Font(None,30)
    text = font.render("Nombre: %i" % len(positions), True, font_color)
    textRect = text.get_rect()
    screen.blit(text, textRect)
    pygame.display.flip()

draw(cities)

collecting = True

while collecting:
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit(0)
        elif event.type == KEYDOWN and event.key == K_RETURN:
            collecting = False
        elif event.type == MOUSEBUTTONDOWN:
            name = "v"+str(len(cities))
            newCity = City(name, pygame.mouse.get_pos())
            cities.append(newCity)
            draw(cities)
			
screen.fill(0)
pygame.draw.lines(screen,city_color,True,cities)
text = font.render("Un chemin, pas le meilleur!", True, font_color)
textRect = text.get_rect()
screen.blit(text, textRect)
pygame.display.flip()


while True:
	event = pygame.event.wait()
	if event.type == KEYDOWN: break
