#TODO: this will be a library that holds a rainbow circle and after blitting to what we want to draw to will then overlay its colored points in its own surface over the top
from circleLib import RainbowCircle
import circleLib as cirLib
import pygame

class RainbowPointPlotter:
    def __init__(self, rainbow_circle = None, window_size = None, center = None, max_radius = None):
        self.rainbow_circle = None
        self.colors = None
        #If we need to create one
        if rainbow_circle is None and not (window_size is None or center is None or max_radius is None):
            self.rainbow_circle = RainbowCircle(window_size, center, max_radius)
        #if we already have one
        elif rainbow_circle is not None:
            self.rainbow_circle = rainbow_circle
            #if not all are none then we are getting mixed messages about which to use
            if not (window_size is None and center is None and max_radius is None):
                raise ValueError("You cannot use both rainbow circle and the other values, which would we pick?")
        #if not enough info is provided
        else:
            raise ValueError("Nither rainbow circle nor window size, center and radius where provided")

    def drawColor(self, color, circle, surface):
        center = (int(circle.DEFF_BUFF_WIDTH/2), int(circle.DEFF_BUFF_WIDTH/2))

        sample_pos_center_ref = cirLib.samplePointFromRGB(cirLib.convertFromPygameColor(color), circle.MAX_RADIUS)
        sample_pos = cirLib.toRealScreenPos(sample_pos_center_ref, center)
        dot_diamiter = circle.DEFF_BUFF_WIDTH*(1/100)
        pygame.draw.circle(surface, 0xff000000,\
                           sample_pos,\
                           dot_diamiter+1)
        pygame.draw.circle(surface, cirLib.convertToPygameColor(color),\
                        sample_pos,\
                        dot_diamiter)

    def draw(self, window):
        #TODO: every time we draw to the rainbow circle anything outside of the
        #circle is rendered onto the windows background area (an area where
        #nothing is ever rendered to) and thus is not overwritten the next time
        #the circle is drawn
        self.rainbow_circle.draw(window)

        circle = self.rainbow_circle
        #FIXME: make this part of the class
        surface = pygame.Surface(circle.blankCircle.get_size()).convert_alpha()
        surface.fill(0x00)

        if self.colors is not None:
            for color in self.colors:
                self.drawColor(color, circle, surface)

        #Make sure we draw in the same location as the rainbow circle is in
        window.blit(surface, (circle.CENTER[0]-circle.DEFF_BUFF_WIDTH/2,
                                       circle.CENTER[1]-circle.DEFF_BUFF_WIDTH/2))

    def updateDimens(self, window_size, center, max_radius):
        self.rainbow_circle.updateDimens(window_size, center, max_radius)

    def setColors(self, colors):
        self.colors = colors
