#!/usr/bin/python
import random
import math
from time import sleep
import pygame
from circleLib import RainbowCircle

WINDOW_SIZE = (1000, 600)
BACKGROUND_COLOR = 0x000000
CENTER = (math.floor(WINDOW_SIZE[0]/2), math.floor(WINDOW_SIZE[1]/2))
MAX_RADIUS = math.floor(min(WINDOW_SIZE[0], WINDOW_SIZE[1])/2)

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

def resize(rainbowCircle):
    WINDOW_SIZE = main_window.get_size()
    CENTER = (math.floor(WINDOW_SIZE[0]/2), math.floor(WINDOW_SIZE[1]/2))
    MAX_RADIUS = math.floor(min(WINDOW_SIZE[0], WINDOW_SIZE[1])/2)
    if rainbowCircle is None:
        rainbowCircle = RainbowCircle(WINDOW_SIZE, CENTER, MAX_RADIUS)
    else:
        rainbowCircle.updateDimens(WINDOW_SIZE, CENTER, MAX_RADIUS)
    clearBackground(main_window)
    return (rainbowCircle)

if __name__ == '__main__':
    pygame.init()
    main_window = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE)
    rainbowCircle = RainbowCircle(WINDOW_SIZE, CENTER, MAX_RADIUS)
    #set window title
    pygame.display.set_caption("Nearest Neighbour Simulator")
    clearBackground(main_window)

    #main loop
    shouldExit = False
    randSquares = False

    #This is so we can initially draw the circle to the correct size
    resize(None)
    updated = True
    while shouldExit is False:
        if randSquares:
            drawRandSquare(main_window)
            updated = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                shouldExit = True
                break
            elif event.type == pygame.VIDEORESIZE:
                resize(rainbowCircle)
                updated = True
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F12:
                    randSquares = not randSquares
                elif event.key == pygame.K_c:
                    clearBackground(main_window)
                    updated = True
                elif event.key == pygame.K_q:
                    pygame.quit()
                    shouldExit = True
                    break

        if (not shouldExit) and updated:
            rainbowCircle.drawRainbowCircle(main_window)
            pygame.display.flip()
        else:
            sleep(.1)

        updated = False
