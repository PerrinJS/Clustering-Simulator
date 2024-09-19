#!/usr/bin/python
import math
import pygame
import color_and_position_conversion as CAPConv

#The purpose of drawing it into a buffer so we dont have to re-calc every time
#       on init accept a start buffer size so we always scale down.
#
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

        self.scale_buff = False
        self.attached_window = None
        self.blank_circle = None

    def attach_window(self, surface):
        self.attached_window = surface

    #TODO: Try update this to pull data from the surface its self
    def update_dimens(self, window_size=None, center=None, max_radius=None):
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
            self.blank_circle = pygame.Surface((self.BUFF_WIDTH, self.BUFF_WIDTH)).convert_alpha()
            self.blank_circle.fill(0x00)
            self.render_rainbow_circle()
            self.scale_buff = False
        else:
            self.DEFF_BUFF_WIDTH = potential_buff_width
            self.scale_buff = True

    def render_rainbow_circle(self):
        for i in range(0,(self.BUFF_WIDTH**2)):
            pos = CAPConv.get_location_from_pix((self.BUFF_WIDTH, self.BUFF_WIDTH), i)
            center = (self.BUFF_WIDTH/2, self.BUFF_WIDTH/2)
            if CAPConv.point_in_circle(center, self.BUFF_WIDTH/2, pos):
                polar_pos = CAPConv.pos_to_polar(pos, center)
                self.blank_circle.set_at(pos,\
                            CAPConv.sample_hex_color(self.MAX_RADIUS, polar_pos[1], polar_pos[0]))

    def draw(self, window=None):
        if not self.blank_circle:
            self.blank_circle = pygame.Surface((self.BUFF_WIDTH, self.BUFF_WIDTH)).convert_alpha()
            self.blank_circle.fill(0x00)
            self.render_rainbow_circle()

        if self.DEFF_BUFF_WIDTH <= self.BUFF_WIDTH:
            def_buff_dimentions = (self.DEFF_BUFF_WIDTH,self.DEFF_BUFF_WIDTH)
            output_circle = pygame.transform.scale(self.blank_circle, def_buff_dimentions)
        else:
            output_circle = self.blank_circle

        if window is None:
            #If it's still None then we skip in the next step
            window = self.attached_window
        elif self.attached_window is None:
            self.attach_window(window)

        if window:
            window.blit(output_circle, (self.CENTER[0]-self.DEFF_BUFF_WIDTH/2,
                                        self.CENTER[1]-self.DEFF_BUFF_WIDTH/2))






#####################TEST FUNCTIONS AND RUNTIME#######################

#NOTE: thease tests where simply being used as a troubleshooting tool and as
#such I have no intention of adding new tests. However I will try keep thease
#working and useful
if __name__ == '__main__':
    import sys
    from functools import partial

    def base_test(func, inp, exp_out):
        """Note this test can only be used where the == comparator is valid"""
        assert func(*inp) == exp_out, f'ERROR: {func.__name__} with input {inp} had value of {func(*inp)} expected: {exp_out}'
        print(f'PASS {func.__name__} input was: {inp} and output: {exp_out}')

    def test_color_conversion():
        print("TESTING COLOR CONVERSIONS:")
        #Testing convertToPygameColor
        to_py_color_test = partial(base_test, func=CAPConv.convert_to_pygame_color)
        to_py_color_test(inp = [(1,1,1)], exp_out = (255,255,255))
        to_py_color_test(inp = [(0,0,0)], exp_out = (0,0,0))
        to_py_color_test(inp = [(0.5,0.5,0.5)], exp_out = (255/2,255/2,255/2))
        #to test the order
        to_py_color_test(inp = [(1,0,0.5)], exp_out = (255,0,255/2))

        #Testing convertFromPygameColor
        from_py_color_test = partial(base_test, func=CAPConv.convert_from_pygame_color)
        from_py_color_test(inp = [(0,0,0)], exp_out = (0,0,0))
        from_py_color_test(inp = [(255,255,255)], exp_out = (1.0,1.0,1.0))
        from_py_color_test(inp = [(255/2,255/2,255/2)], exp_out = (0.5,0.5,0.5))
        #to test the order
        from_py_color_test(inp = [(255,0,255/2)], exp_out = (1,0,0.5))

    def test_window_math_functions():
        print("TESTING WINDOW MATH FUNCTIONS:")
        #Testing normalizePoint
        normalize_point_test = partial(base_test, func=CAPConv.normalize_point)
        normalize_point_test(inp = [(0,0),(0,0)], exp_out = (0,0))
        normalize_point_test(inp = [(800,600),(0,0)], exp_out = (800,600))
        normalize_point_test(inp = [(1600,1200),(800,600)], exp_out = (800,600))
        #Testing posToPolar
        pos_to_polar_test = partial(base_test, func=CAPConv.pos_to_polar)
        pos_to_polar_test(inp = [(0,0), (0,0)], exp_out = (0,0))
        pos_to_polar_test(inp = [(12, 5), (0,0)], exp_out = (13, math.atan(5/12)))

    print("Running Circle Lib Diag & Test:")
    try:
        test_color_conversion()
        test_window_math_functions()
    except AssertionError as error:
        print(error, file=sys.stderr)
        print("EXITING EARLY", file=sys.stderr)
    print("FINISHED")
