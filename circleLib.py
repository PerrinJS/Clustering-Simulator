#!/usr/bin/python
import math
import colorsys
import pygame

def convertToPygameColor(color):
    red = 255 * color[0]
    green = 255 * color[1]
    blue = 255 * color[2]
    return (red, green, blue)

def convertFromPygameColor(color):
    red = color[0]/255
    green = color[1]/255
    blue = color[2]/255
    return (red, green, blue)

def sampleHexColor(max_radius, h, s, v = 100):
    sx = abs(s/max_radius)
    color = colorsys.hsv_to_rgb(h/(2*math.pi), sx, v/100)
    return convertToPygameColor(color)

def samplePointFromRGB(rgb_color, max_radius):
    r,g,b = rgb_color
    h,s,v = colorsys.rgb_to_hsv(r,g,b)
    h = h*(2*math.pi)
    s = s*max_radius
    return polarToPos((s, h))

def normalizePoint(point, center):
    """
    Make the corrdinate system based off where the center of the window rather
    than the top left corner
    """
    (x,y) = point
    (cX,cY) = center
    return (x-cX, y-cY)

def toRealScreenPos(point, center):
    """ Reverse normalizePoint """
    x, y = point
    cX, cY = center
    return (x+cX, y+cY)

def posToPolar(point, center):
    """converts cartesian coordinates to polar coordinates using the center as refference"""
    (x,y) = normalizePoint(point, center)
    r = math.sqrt(abs(x*x + y*y))
    if x == 0:
        if y == 0:
            theta = 0
        elif y > 0:
            theta = math.pi/2
        elif y < 0:
            theta = math.pi+(math.pi/2)
    else:
        theta = math.atan(y/x)
        if ((y >= 0) and (x < 0)) or ((x < 0) and (y <= 0)):
            theta += math.pi
        elif (x > 0) and (y <= 0):
            theta += 2*math.pi

    return(r,theta)

def polarToPos(polar):
    x = polar[0] * math.cos(polar[1])
    y = polar[0] * math.sin(polar[1])
    return (x, y)

def pointInCircle(center, radius, point):
    polarPoint = posToPolar(point, center)
    return polarPoint[0] < radius

def getLocationFromPix(imageSize, location):
    (xLen, yLen) = imageSize
    #by using floor, lines start from zero
    y = math.floor(location/xLen)
    #Again pixel count also starts from zero
    x = location%xLen
    return (x,y)

#TODO: the purpose of drawing it into a buffer so we dont have to re-calc every time
#       Maybe on init accept a start buffer size so we always scale down.
class RainbowCircle:
    def __init__(self, window_size, center, max_radius):
        self.WINDOW_SIZE = []
        self.WINDOW_SIZE.append(window_size[0])
        self.WINDOW_SIZE.append(window_size[1])

        self.CENTER = []
        self.CENTER.append(center[0])
        self.CENTER.append(center[1])

        self.MAX_RADIUS = max_radius

        self.BUFF_WIDTH = min(self.WINDOW_SIZE[0], self.WINDOW_SIZE[1])
        self.DEFF_BUFF_WIDTH = self.BUFF_WIDTH
        self.blankCircle = pygame.Surface((self.BUFF_WIDTH, self.BUFF_WIDTH)).convert_alpha()
        self.blankCircle.fill(0x00)
        self.renderRainbowCircle()
        self.scaleBuff = False

    def updateDimens(self, window_size, center, max_radius):
        self.WINDOW_SIZE = []
        self.WINDOW_SIZE.append(window_size[0])
        self.WINDOW_SIZE.append(window_size[1])

        self.CENTER = []
        self.CENTER.append(center[0])
        self.CENTER.append(center[1])

        self.MAX_RADIUS = max_radius

        potential_buff_width = min(self.WINDOW_SIZE[0], self.WINDOW_SIZE[1])
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
            pos = getLocationFromPix((self.BUFF_WIDTH, self.BUFF_WIDTH), i)
            if pointInCircle((self.BUFF_WIDTH/2, self.BUFF_WIDTH/2), self.BUFF_WIDTH/2, pos):
                polarPos = posToPolar(pos, (self.BUFF_WIDTH/2, self.BUFF_WIDTH/2))
                self.blankCircle.set_at(pos, sampleHexColor(self.MAX_RADIUS, polarPos[1], polarPos[0]))

    def draw(self, window):
        if self.DEFF_BUFF_WIDTH <= self.BUFF_WIDTH:
            outputCircle = pygame.transform.scale(self.blankCircle, (self.DEFF_BUFF_WIDTH,self.DEFF_BUFF_WIDTH))
        else:
            outputCircle = self.blankCircle
        window.blit(outputCircle, (self.CENTER[0]-self.DEFF_BUFF_WIDTH/2,
                                       self.CENTER[1]-self.DEFF_BUFF_WIDTH/2))






#####################TEST FUNCTIONS AND RUNTIME#######################

#NOTE: thease tests where simply being used as a troubleshooting tool and as
#such I have no intention of adding new tests. However I will try keep thease
#working and useful
if __name__ == '__main__':
    import sys
    from functools import partial

    def baseTest(func, inp, expOut):
        """Note this test can only be used where the == comparator is valid"""
        assert func(*inp) == expOut, f'ERROR: {func.__name__} with input {inp} had value of {func(*inp)} expected: {expOut}'
        print(f'PASS {func.__name__} input was: {inp} and output: {expOut}')

    def testColorConversion():
        print("TESTING COLOR CONVERSIONS:")
        #Testing convertToPygameColor
        toPyColorTest = partial(baseTest, func=convertToPygameColor)
        toPyColorTest(inp = [(1,1,1)], expOut = (255,255,255))
        toPyColorTest(inp = [(0,0,0)], expOut = (0,0,0))
        toPyColorTest(inp = [(0.5,0.5,0.5)], expOut = (255/2,255/2,255/2))
        #to test the order
        toPyColorTest(inp = [(1,0,0.5)], expOut = (255,0,255/2))

        #Testing convertFromPygameColor
        fromPyColorTest = partial(baseTest, func=convertFromPygameColor)
        fromPyColorTest(inp = [(0,0,0)], expOut = (0,0,0))
        fromPyColorTest(inp = [(255,255,255)], expOut = (1.0,1.0,1.0))
        fromPyColorTest(inp = [(255/2,255/2,255/2)], expOut = (0.5,0.5,0.5))
        #to test the order
        fromPyColorTest(inp = [(255,0,255/2)], expOut = (1,0,0.5))

    def testWindowMathFunctions():
        print("TESTING WINDOW MATH FUNCTIONS:")
        #Testing normalizePoint
        normalizePointTest = partial(baseTest, func=normalizePoint)
        normalizePointTest(inp = [(0,0),(0,0)], expOut = (0,0))
        normalizePointTest(inp = [(800,600),(0,0)], expOut = (800,600))
        normalizePointTest(inp = [(1600,1200),(800,600)], expOut = (800,600))
        #Testing posToPolar
        posToPolarTest = partial(baseTest, func=posToPolar)
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
