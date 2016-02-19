import pygame
from pygame.locals import KEYDOWN, QUIT, MOUSEBUTTONDOWN, K_RETURN, K_ESCAPE
import sys
import math
import itertools
import time

cassure = 4

class Individu:

    def __init__(self, cities):
        self.orderVisit = cities
        self.distance = self.calcDistance()

    def calcDistance(self):
        distanceTot = 0
        for i in range(0, len(self.orderVisit)):
            city1 = self.orderVisit[i]
            if i+1 < len(self.orderVisit):
                city2 = self.orderVisit[i+1]
            else:
                city2 = self.orderVisit[0]
            distanceTot += math.sqrt(math.pow(city1.pos[0] - city2.pos[0], 2) + math.pow(city1.pos[1] - city2.pos[1], 2))

        return distanceTot

    def __repr__(self):
        return self.distance+""

class City:

    def __init__(self, name, pos):
        self.name = name
        self.pos = pos

cities = []

def parseFile(connections):
    lines = connections.split("\n")

    for line in lines:
        if line:
            word = line.split(" ")
            pos = (int(word[1]), int(word[2]))
            nom = word[0]
            newCity = City(nom, pos)
            cities.append(newCity)

def mutation(indiv1, indiv2):
    newParcours = []
    for i in range(0, cassure):
        newParcours.append(indiv1.orderVisit[i])

    for cityIndiv2 in indiv2.orderVisit:
        if cityIndiv2 not in newParcours:
            newParcours.append(cityIndiv2)

    return Individu(newParcours)

if __name__ == "__main__":

    screen_x = 500
    screen_y = 500

    city_color = [10,10,200] # blue
    city_radius = 3

    link_color = [200,10,10] # red

    font_color = [255,255,255] # white

    pygame.init()
    window = pygame.display.set_mode((screen_x, screen_y))
    pygame.display.set_caption('Exemple')
    screen = pygame.display.get_surface()
    font = pygame.font.Font(None,30)

    def drawParcours(individus):
        for individu in individus:
            draw(individu.orderVisit, individu)

    def draw(positions, individu=None):
        screen.fill(0)
        font = pygame.font.Font(None,20)

        for pos in positions:
            pygame.draw.circle(screen, city_color, pos.pos, city_radius)
            screen.blit(font.render("%s %s" % (pos.name, pos.pos), True, font_color), pos.pos)

        if not(individu is None):
            for i in range(0, len(individu.orderVisit)):
                city1 = individu.orderVisit[i]
                if i+1 < len(individu.orderVisit):
                    city2 = individu.orderVisit[i+1]
                else:
                    city2 = individu.orderVisit[0]
                pygame.draw.line(screen, link_color, city1.pos, city2.pos)

        font = pygame.font.Font(None,30)
        text = font.render("Nombre: %i" % len(positions), True, font_color)
        textRect = text.get_rect()
        screen.blit(text, textRect)
        pygame.display.flip()

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

def ga_solve(file=None, gui=False, maxtime=0):
    fileCities = open(file, "r")
    parseFile(fileCities.read())
    nbPopulation = 50
    #if(gui):
        #draw(cities)
    permutationsCities = list(itertools.islice(itertools.permutations(cities), nbPopulation))
    individus = []

    '''Creation des individus'''
    for permutations in permutationsCities:
        i = Individu(permutations)
        individus.append(i)

    timeStart = time.time()
    actualTime = -1

    while actualTime < maxtime:
        '''Croisement'''
        newIndividus = []

        for i in range(0, len(individus), 2):
            indiv1 = individus[i]
            if i+1 < len(individus):
                indiv2 = individus[i+1]
                newIndividus.append(mutation(indiv1, indiv2))
            else:
                newIndividus.append(mutation(indiv1, individus[0]))


        '''Selection des individus (elitisme)'''
        individus.sort(key = lambda x : x.distance)
        elite = individus[:nbPopulation]

        individus = elite
        #if(gui):
            #drawParcours(individus)

        if maxtime > 0:
            actualTime = time.time() - timeStart

    print(individus[0].distance)
    return individus[0]
