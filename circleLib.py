#!/usr/bin/python
import math
import colorsys

WINDOW_SIZE = [0, 0]
CENTER = [0,0]
MAX_RADIUS = [0]

#TODO: this is a temp fix
def init(window_size, center, max_radius):
    WINDOW_SIZE[0] = window_size[0]
    WINDOW_SIZE[1] = window_size[1]

    CENTER[0] = center[0]
    CENTER[1] = center[1]

    MAX_RADIUS[0] = max_radius

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

def sampleHexColor(h, s, v = 100):
    sx = abs(s/MAX_RADIUS[0])
    color = colorsys.hsv_to_rgb(h/(2*math.pi), sx, v/100)
    return convertToPygameColor(color)

def normalizePoint(point, center):
    """
    Make the corrdinate system based off where the center of the window rather
    than the top left corner
    """
    (x,y) = point
    (cX,cY) = center
    return (x-cX, y-cY)

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

def drawRainbowCircle(window):
    for i in range(0,(WINDOW_SIZE[0]*WINDOW_SIZE[1])):
        pos = getLocationFromPix(WINDOW_SIZE, i)
        if pointInCircle(CENTER, min(WINDOW_SIZE[0], WINDOW_SIZE[1])/2, pos):
            polarPos = posToPolar(pos, CENTER)
            window.set_at(pos, sampleHexColor(polarPos[1], polarPos[0]))
        #else:
        #    window.set_at(pos, 0x0)


#####################TEST FUNCTIONS AND RUNTIME#######################

if __name__ == '__main__':
    import sys

    def baseTest(func, inp, expOut):
        """Note this test can only be used where the == comparator is valid"""
        if (func(*inp) == expOut):
            print(f'PASS {func} with input of {inp}')
        else:
            print(f'ERROR: {func} had value of {func(*inp)}', file=sys.stderr)
            print("EXITING EARLY", file=sys.stderr)
            sys.exit()

    def testColorConversion():
        print("TESTING COLOR CONVERSIONS:")
        #Testing convertToPygameColor
        baseTest(func = convertToPygameColor, inp = [(1,1,1)], expOut = (255,255,255))
        baseTest(func = convertToPygameColor, inp = [(0,0,0)], expOut = (0,0,0))
        baseTest(func = convertToPygameColor, inp = [(0.5,0.5,0.5)], expOut = (255/2,255/2,255/2))
        #to test the order
        baseTest(func = convertToPygameColor, inp = [(1,0,0.5)], expOut = (255,0,255/2))

        #Testing convertFromPygameColor
        baseTest(func = convertFromPygameColor, inp = [(0,0,0)], expOut = (0,0,0))
        baseTest(func = convertFromPygameColor, inp = [(255,255,255)], expOut = (1.0,1.0,1.0))
        baseTest(func = convertFromPygameColor, inp = [(255/2,255/2,255/2)], expOut = (0.5,0.5,0.5))
        #to test the order
        baseTest(func = convertFromPygameColor, inp = [(255,0,255/2)], expOut = (1,0,0.5))

    def testWindowMathFunctions():
        print("TESTING WINDOW MATH FUNCTIONS:")
        #Testing normalizePoint
        baseTest(func = normalizePoint, inp = [(0,0),(0,0)], expOut = (0,0))
        baseTest(func = normalizePoint, inp = [(800,600),(0,0)], expOut = (800,600))
        baseTest(func = normalizePoint, inp = [(1600,1200),(800,600)], expOut = (800,600))
        #Testing posToPolar
        baseTest(func = posToPolar, inp = [(0,0)], expOut = (0,0))
        baseTest(func = posToPolar, inp = [(12, 5)], expOut = (13, math.atan(5/12)))

    print("Running Circle Lib Diag & Test")
    testColorConversion()
    testWindowMathFunctions()
