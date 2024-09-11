import pygame
from circleLib import RainbowCircle
import ColorAndPositionConversion as CAPConv

#TODO: convert to be a gui element, so it does not rely on injecting the center and dimentions everywhere
class RainbowPointPlotter:
    def __init__(self, rainbow_circle = None, window_size = None, center = None, max_radius = None):
        self.attached_window = None
        self.rainbow_circle = None
        self.colors = None
        #will only draw circle unless this is true
        self.draw_points = False
        #Selects weather to draw the dots as thair origenal color or in thair grouped color
        self.draw_grouped = False
        #stors the color for the group for a given position in the colors array
        self.grouped_colors = []
        #If we need to create one
        if rainbow_circle is None and not (window_size is None):
            self.rainbow_circle = RainbowCircle(window_size, max_radius, center)
        #if we already have one
        elif rainbow_circle is not None:
            self.rainbow_circle = rainbow_circle
            #if not all are none then we are getting mixed messages about which to use
            if not (window_size is None):
                raise ValueError("You cannot use both rainbow circle and the other values, which would we pick?")
        #if not enough info is provided
        else:
            raise ValueError("Nither rainbow circle nor window size where provided")

    def inc(self, _pos, _interface_manager):
        pass

    def on_mouse_up(self, _window):
        pass

    def on_mouse_down(self, _window):
        pass

    def attach_window(self, surface):
        self.attached_window = surface

    def drawColor(self, color, circle, surface):
        center = (int(circle.DEFF_BUFF_WIDTH/2), int(circle.DEFF_BUFF_WIDTH/2))

        sample_pos_center_ref = CAPConv.samplePointFromRGB(color, circle.MAX_RADIUS)
        sample_pos = CAPConv.toRealScreenPos(sample_pos_center_ref, center)
        self.drawColorAtPos(color, sample_pos, circle, surface)

    def drawColorAtPos(self, color, pos, circle, surface, dot_diamiter = 0):
        if dot_diamiter == 0:
            dot_diamiter = circle.DEFF_BUFF_WIDTH*(1/150)

        pygame.draw.circle(surface, 0xff000000,\
                           pos,\
                           dot_diamiter+1)
        pygame.draw.circle(surface, CAPConv.convertToPygameColor(color),\
                           pos,\
                           dot_diamiter)

    def draw(self, window=None):
        #TODO: every time we draw to the rainbow circle anything outside of the
        #circle is rendered onto the windows background area (an area where
        #nothing is ever rendered to) and thus is not overwritten the next time
        #the circle is drawn
        self.rainbow_circle.draw(window)

        circle = self.rainbow_circle
        #TODO: make this part of the class
        surface = pygame.Surface(circle.blankCircle.get_size()).convert_alpha()
        surface.fill(0x00)

        if self.draw_points:
            if self.draw_grouped:
                if (self.colors is not None) and (len(self.grouped_colors) == 0):
                    for i, color in enumerate(self.colors):
                        pos = self.grouped_colors[i]
                        self.drawColorAtPos(color, pos, circle, surface)
            else:
                #Draw the colors at the points that are given
                if self.colors is not None:
                    for color in self.colors:
                        self.drawColor(color, circle, surface)

        if window is None:
            window = self.attached_window
        elif self.attached_window is None:
            self.attach_window(window)

        if window:
            #Make sure we draw in the same location as the rainbow circle is in
            window.blit(surface, (circle.CENTER[0]-circle.DEFF_BUFF_WIDTH/2,
                                        circle.CENTER[1]-circle.DEFF_BUFF_WIDTH/2))

    def updateDimens(self, window_size=None, center=None, max_radius=None):
        self.rainbow_circle.updateDimens(window_size, center, max_radius)

    def toggleDrawPoints(self):
        #invert the current state
        self.draw_points = False if self.draw_points else True

    def reset(self):
        self.colors = None
        self.draw_points = False
        self.draw_grouped = False
        self.grouped_colors = []

    def setColors(self, colors):
        self.colors = colors
        #since we no longer have the same colors we need to recalculate the groups
        self.grouped_colors = []

    def setGrouped(self, grouped):
        self.draw_grouped = grouped

        if self.draw_grouped:
            if len(self.grouped_colors) == 0:
                self.groupPoints()

    def getDrawPoints(self):
        return self.draw_points

    def getColors(self):
        return self.colors

    def getCircleCenter(self):
        return self.rainbow_circle.CENTER
