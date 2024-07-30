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
