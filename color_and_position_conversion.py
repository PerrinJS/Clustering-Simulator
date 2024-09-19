#!/usr/bin/python
import math
import colorsys

def convert_web_to_rgb(color):
    color_str = hex(color)
    #strip off the 0x
    color_str = color_str[2:]
    for _ in range(6-len(color_str)):
        color_str = '0' + color_str
    red_str = color_str[:2]
    green_str = color_str[2:4]
    blue_str = color_str[4:6]

    red_int = int(red_str, 16)
    green_int = int(green_str, 16)
    blue_int = int(blue_str, 16)

    ret = (red_int/255, green_int/255, blue_int/255)
    return ret

def convert_to_pygame_color(color):
    red = 255 * color[0]
    green = 255 * color[1]
    blue = 255 * color[2]
    return (red, green, blue)

def convert_from_pygame_color(color):
    red = color[0]/255
    green = color[1]/255
    blue = color[2]/255
    return (red, green, blue)

def hsv_to_rgb(max_radius, color):
    h,s,v = color
    sx = abs(s/max_radius)
    return colorsys.hsv_to_rgb(h/(2*math.pi), sx, v/100)

def sample_hex_color(max_radius, h, s, v = 100):
    color = hsv_to_rgb(max_radius, (h,s,v))
    return convert_to_pygame_color(color)

def sample_point_from_rgb(rgb_color, max_radius):
    r,g,b = rgb_color
    h,s,_ = colorsys.rgb_to_hsv(r,g,b)
    h = h*(2*math.pi)
    s = s*max_radius
    return polar_to_pos((s, h))

def normalize_point(point, center):
    """
    Make the corrdinate system based off where the center of the window rather
    than the top left corner
    """
    (x,y) = point
    (cx,cy) = center
    return (x-cx, y-cy)

def to_real_screen_pos(point, center):
    """ Reverse normalizePoint """
    x, y = point
    cx, cy = center
    return (x+cx, y+cy)

def pos_to_polar(point, center=None):
    """converts cartesian coordinates to polar coordinates using the center as refference"""
    if center is not None:
        (x,y) = normalize_point(point, center)
    else:
        (x,y) = point
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

def polar_to_pos(polar):
    x = polar[0] * math.cos(polar[1])
    y = polar[0] * math.sin(polar[1])
    return (x, y)

def point_in_circle(center, radius, point):
    polar_point = pos_to_polar(point, center)
    return polar_point[0] < radius

def get_location_from_pix(image_size, location):
    (x_len, _y_len) = image_size
    #by using floor, lines start from zero
    y = math.floor(location/x_len)
    #Again pixel count also starts from zero
    x = location%x_len
    return (x,y)

def tint_rgb(color, tint_factor):
    r,g,b = color
    return (r*tint_factor, g*tint_factor, b*tint_factor)
