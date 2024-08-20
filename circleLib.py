#!/usr/bin/python
import pygame
import math
import ColorAndPositionConversion as CAPConv

#TODO: the purpose of drawing it into a buffer so we dont have to re-calc every time
#       Maybe on init accept a start buffer size so we always scale down.
#TODO: convert to be a gui element, so it does not rely on injecting the center and dimentions everywhere

def find_center(window_size):
    return (math.floor(window_size[0]/2), math.floor(window_size[1]/2))

def find_max_radius(window_size):
    return math.floor(min(window_size[0], window_size[1])/2)

def find_buff_width(window_size):
    return min(window_size[0], window_size[1])

class RainbowCircle:
    def __init__(self, window_size, max_radius = None, center = None):
        self.WINDOW_SIZE = []
        self.WINDOW_SIZE.append(window_size[0])
        self.WINDOW_SIZE.append(window_size[1])

        self.CENTER = []
        if center is None:
            center = find_center(window_size)
        self.CENTER.append(center[0])
        self.CENTER.append(center[1])

        if max_radius is None:
            self.MAX_RADIUS = find_max_radius(window_size)
        else:
            self.MAX_RADIUS = max_radius

        self.BUFF_WIDTH = find_buff_width(window_size)
        self.DEFF_BUFF_WIDTH = self.BUFF_WIDTH

        self.scaleBuff = False
        self.attached_window = None
        self.init = False

    def attach_window(self, surface):
        self.attached_window = surface

    #TODO: Try update this to pull data from the surface its self
    def updateDimens(self, window_size=None, center=None, max_radius=None):
        self.WINDOW_SIZE = []
        if window_size is None:
            if self.attach_window is None:
                raise ValueError("No attached window to refference size from")
            window_size = self.attached_window.get_size()
        self.WINDOW_SIZE.append(window_size[0])
        self.WINDOW_SIZE.append(window_size[1])

        self.CENTER = []
        if center is None:
            center = find_center(window_size)
        self.CENTER.append(center[0])
        self.CENTER.append(center[1])

        if max_radius is None:
            self.MAX_RADIUS = find_max_radius(window_size)
        else:
            self.MAX_RADIUS = max_radius

        potential_buff_width = find_buff_width(window_size)
        if self.BUFF_WIDTH <= potential_buff_width:
            self.BUFF_WIDTH = potential_buff_width
            self.DEFF_BUFF_WIDTH = self.BUFF_WIDTH
            self.blankCircle = pygame.Surface((self.BUFF_WIDTH, self.BUFF_WIDTH)).convert_alpha()
            self.blankCircle.fill(0x00)
            self.renderRainbowCircle()
            self.scaleBuff = False
        else:
            self.DEFF_BUFF_WIDTH = potential_buff_width
            self.scaleBuff = True

    def renderRainbowCircle(self):
        for i in range(0,(self.BUFF_WIDTH**2)):
            pos = CAPConv.getLocationFromPix((self.BUFF_WIDTH, self.BUFF_WIDTH), i)
            if CAPConv.pointInCircle((self.BUFF_WIDTH/2, self.BUFF_WIDTH/2), self.BUFF_WIDTH/2, pos):
                polarPos = CAPConv.posToPolar(pos, (self.BUFF_WIDTH/2, self.BUFF_WIDTH/2))
                self.blankCircle.set_at(pos, CAPConv.sampleHexColor(self.MAX_RADIUS, polarPos[1], polarPos[0]))

    def draw(self, window=None):
        if not self.init:
            self.blankCircle = pygame.Surface((self.BUFF_WIDTH, self.BUFF_WIDTH)).convert_alpha()
            self.blankCircle.fill(0x00)
            self.renderRainbowCircle()
            self.init = True

        if self.DEFF_BUFF_WIDTH <= self.BUFF_WIDTH:
            outputCircle = pygame.transform.scale(self.blankCircle, (self.DEFF_BUFF_WIDTH,self.DEFF_BUFF_WIDTH))
        else:
            outputCircle = self.blankCircle

        if window is None:
            #If it's still None then we skip in the next step
            window = self.attached_window
        elif self.attached_window is None:
            self.attach_window(window)

        if window:
            window.blit(outputCircle, (self.CENTER[0]-self.DEFF_BUFF_WIDTH/2,
                                        self.CENTER[1]-self.DEFF_BUFF_WIDTH/2))






#####################TEST FUNCTIONS AND RUNTIME#######################

#NOTE: thease tests where simply being used as a troubleshooting tool and as
#such I have no intention of adding new tests. However I will try keep thease
#working and useful
if __name__ == '__main__':
    import sys
    import math
    from functools import partial

    def baseTest(func, inp, expOut):
        """Note this test can only be used where the == comparator is valid"""
        assert func(*inp) == expOut, f'ERROR: {func.__name__} with input {inp} had value of {func(*inp)} expected: {expOut}'
        print(f'PASS {func.__name__} input was: {inp} and output: {expOut}')

    def testColorConversion():
        print("TESTING COLOR CONVERSIONS:")
        #Testing convertToPygameColor
        toPyColorTest = partial(baseTest, func=CAPConv.convertToPygameColor)
        toPyColorTest(inp = [(1,1,1)], expOut = (255,255,255))
        toPyColorTest(inp = [(0,0,0)], expOut = (0,0,0))
        toPyColorTest(inp = [(0.5,0.5,0.5)], expOut = (255/2,255/2,255/2))
        #to test the order
        toPyColorTest(inp = [(1,0,0.5)], expOut = (255,0,255/2))

        #Testing convertFromPygameColor
        fromPyColorTest = partial(baseTest, func=CAPConv.convertFromPygameColor)
        fromPyColorTest(inp = [(0,0,0)], expOut = (0,0,0))
        fromPyColorTest(inp = [(255,255,255)], expOut = (1.0,1.0,1.0))
        fromPyColorTest(inp = [(255/2,255/2,255/2)], expOut = (0.5,0.5,0.5))
        #to test the order
        fromPyColorTest(inp = [(255,0,255/2)], expOut = (1,0,0.5))

    def testWindowMathFunctions():
        print("TESTING WINDOW MATH FUNCTIONS:")
        #Testing normalizePoint
        normalizePointTest = partial(baseTest, func=CAPConv.normalizePoint)
        normalizePointTest(inp = [(0,0),(0,0)], expOut = (0,0))
        normalizePointTest(inp = [(800,600),(0,0)], expOut = (800,600))
        normalizePointTest(inp = [(1600,1200),(800,600)], expOut = (800,600))
        #Testing posToPolar
        posToPolarTest = partial(baseTest, func=CAPConv.posToPolar)
        posToPolarTest(inp = [(0,0), (0,0)], expOut = (0,0))
        posToPolarTest(inp = [(12, 5), (0,0)], expOut = (13, math.atan(5/12)))

    print("Running Circle Lib Diag & Test:")
    try:
        testColorConversion()
        testWindowMathFunctions()
    except AssertionError as error:
        print(error, file=sys.stderr)
        print("EXITING EARLY", file=sys.stderr)
    print("FINISHED")
