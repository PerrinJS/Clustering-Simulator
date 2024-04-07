#!/usr/bin/python
import random
import math
import pygame
from time import sleep
from rainbowPointPlotter import RainbowPointPlotter
from gui import Button

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

def resizeRainbowCircle(rainbowCircle):
    WINDOW_SIZE = main_window.get_size()
    CENTER = (math.floor(WINDOW_SIZE[0]/2), math.floor(WINDOW_SIZE[1]/2))
    MAX_RADIUS = math.floor(min(WINDOW_SIZE[0], WINDOW_SIZE[1])/2)
    if rainbowCircle is None:
        rainbowCircle = RainbowPointPlotter(None, WINDOW_SIZE, CENTER, MAX_RADIUS)
    else:
        rainbowCircle.updateDimens(WINDOW_SIZE, CENTER, MAX_RADIUS)
    clearBackground(main_window)
    return (rainbowCircle)

def convertWebToRGB(color):
    color_str = hex(color)
    #strip off the 0x
    color_str = color_str[2:]
    for i in range(6-len(color_str)):
        color_str = '0' + color_str
    red_str = color_str[:2]
    green_str = color_str[2:4]
    blue_str = color_str[4:6]

    red_int = int(red_str, 16)
    green_int = int(green_str, 16)
    blue_int = int(blue_str, 16)

    ret = (red_int/255, green_int/255, blue_int/255)
    return ret

def runNearestSim(rainbow_point_plotter):
    """ This should trigger the plotter to run the simulation """
    #FIXME: this is just for testing currently we just print randomly colored
    #dots to screen
    #TODO: zero the saturation of the colors
    randColorsWeb = genRandColors(10)
    randColors = []
    for color in randColorsWeb:
        randColors.append(convertWebToRGB(color))
    rainbow_point_plotter.setColors(randColors)

if __name__ == '__main__':
    pygame.init()
    main_window = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE)
    rainbowCircle = RainbowPointPlotter(None, WINDOW_SIZE, CENTER, MAX_RADIUS)
    exit_button = Button(main_window, ( .99-.1, .99-.1, .1, .1), True, "Exit")
    run_button = Button(main_window, (.01, .99-.1, .1, .1), True, "Run")
    screen_buttons = [exit_button, run_button]

    #set window title
    pygame.display.set_caption("Nearest Neighbour Simulator")
    clearBackground(main_window)

    #main loop flags
    shouldExit = False
    randSquares = False
    updated = True

    #TODO: find a neater way of doing this
    def exitFunction():
        global shouldExit
        shouldExit = True
    exit_button.set_func(lambda : exitFunction())
    run_button.set_func(lambda : runNearestSim(rainbowCircle))

    #This is so we can initially draw the circle to the correct size
    resizeRainbowCircle(None)
    while shouldExit is False:
        for element in screen_buttons:
            if element.inc(pygame.mouse.get_pos()):
                updated = True

        if randSquares:
            drawRandSquare(main_window)
            updated = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                shouldExit = True
                break
            elif event.type == pygame.VIDEORESIZE:
                resizeRainbowCircle(rainbowCircle)
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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for element in screen_buttons:
                    element.on_mouse_down()
                updated = True
            elif event.type == pygame.MOUSEBUTTONUP:
                for element in screen_buttons:
                    element.on_mouse_up()
                updated = True

        if (not shouldExit) and updated:
            rainbowCircle.draw(main_window)
            for element in screen_buttons:
                element.draw()
            pygame.display.flip()
        else:
            sleep(.1)

        updated = False
