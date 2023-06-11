#!/usr/bin/python
import random
import math
from time import sleep
import pygame
from circleLib import drawRainbowCircle, init

WINDOW_SIZE = (1000, 600)
BACKGROUND_COLOR = 0x000000
CENTER = (math.floor(WINDOW_SIZE[0]/2), math.floor(WINDOW_SIZE[1]/2))
MAX_RADIUS = math.floor(max(WINDOW_SIZE[0], WINDOW_SIZE[1])/2)

def genRandColor():
    return random.randrange(0x000000, 0xffffff)

def genRandColors(quantity):
    colors = [None] * quantity
    for i in range(0,quantity):
        colors[i] = genRandColor()
    return colors

def genRandSquare():
    topLeft = (random.randrange(0, WINDOW_SIZE[0]), random.randrange(0, WINDOW_SIZE[1]))
    sideLength = random.randrange(0, math.floor(WINDOW_SIZE[0]/2))
    return pygame.Rect(topLeft[0], topLeft[1], sideLength, sideLength)

def drawRandSquare(window):
    randSquare = genRandSquare()
    randColor = genRandColor()
    pygame.draw.rect(window, randColor, randSquare)

def clearBackground(window):
    main_window.fill(BACKGROUND_COLOR)
    pygame.display.flip()

if __name__ == '__main__':
    pygame.init()
    init(WINDOW_SIZE, CENTER, MAX_RADIUS)
    main_window = pygame.display.set_mode(WINDOW_SIZE)
    #set window title
    pygame.display.set_caption("Nearest Neighbour Simulator")
    clearBackground(main_window)

    #main loop
    shouldExit = False
    randSquares = False
    while shouldExit is False:
        updated = False
        if randSquares:
            drawRandSquare(main_window)
            updated = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                shouldExit = True
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F12:
                    randSquares = not randSquares
                elif event.key == pygame.K_F11:
                    drawRainbowCircle(main_window)
                    updated = True
                elif event.key == pygame.K_c:
                    clearBackground(main_window)
                    updated = True
                elif event.key == pygame.K_q:
                    pygame.quit()
                    shouldExit = True
                    break

        if (not shouldExit) and updated:
            pygame.display.flip()
        else:
            sleep(.1)
