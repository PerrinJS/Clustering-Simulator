import pygame
from circle_lib import RainbowCircle
import color_and_position_conversion as CAPConv

class RainbowPointPlotter:
    def __init__(self, rainbow_circle = None, window_size = None, center = None,\
                 max_radius = None, point_tint=None, centroid_tint=None):
        self.attached_window = None
        self.rainbow_circle = None
        self.colors = None
        #will only draw circle unless this is true
        self.draw_points = False
        #Selects weather to draw the dots as thair origenal color or in thair grouped color
        self.draw_grouped = False
        #Stores the centroids and grouped data in a tuple
        self.centroids_and_groups = None
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

        #Thease should be a scale factor for how darkend the point on the rainbow circle should be
        #i.e. a value between 0 and 1
        self.point_tint = point_tint
        self.centroid_tint = centroid_tint

    def inc(self, _pos, _interface_manager):
        pass

    def on_mouse_up(self, _window):
        pass

    def on_mouse_down(self, _window):
        pass

    def attach_window(self, surface):
        self.attached_window = surface

    def draw_color(self, circle, surface, color, cluster_color=None):
        center = (int(circle.DEFF_BUFF_WIDTH/2), int(circle.DEFF_BUFF_WIDTH/2))

        sample_pos_center_ref = CAPConv.sample_point_from_rgb(color, circle.MAX_RADIUS)
        sample_pos = CAPConv.to_real_screen_pos(sample_pos_center_ref, center)

        tint_value = self.point_tint
        if cluster_color:
            if cluster_color == color:
                tint_value = self.centroid_tint
            output_color = cluster_color
        else:
            output_color = color

        output_color = CAPConv.tint_rgb(output_color, tint_value)

        self.draw_color_at_pos(output_color, sample_pos, circle, surface)

    def draw_color_at_pos(self, color, pos, circle, surface, dot_diamiter = 0):
        if dot_diamiter == 0:
            dot_diamiter = circle.DEFF_BUFF_WIDTH*(1/150)

        pygame.draw.circle(surface, 0xff000000,\
                           pos,\
                           dot_diamiter+1)
        pygame.draw.circle(surface, CAPConv.convert_to_pygame_color(color),\
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
        surface = pygame.Surface(circle.blank_circle.get_size()).convert_alpha()
        surface.fill(0x00)

        if self.draw_points:
            if self.centroids_and_groups:
                for i, centroid in enumerate(self.centroids_and_groups[0]):
                    for color in self.centroids_and_groups[1][i]:
                        self.draw_color(circle, surface, color, centroid)
            elif self.colors:
                #Draw the colors at the points that are given
                for color in self.colors:
                    self.draw_color(circle, surface, color)

        if window is None:
            window = self.attached_window
        elif self.attached_window is None:
            self.attach_window(window)

        if window:
            #Make sure we draw in the same location as the rainbow circle is in
            window.blit(surface, (circle.CENTER[0]-circle.DEFF_BUFF_WIDTH/2,\
                                        circle.CENTER[1]-circle.DEFF_BUFF_WIDTH/2))

    def update_dimens(self, window_size=None, center=None, max_radius=None):
        self.rainbow_circle.update_dimens(window_size, center, max_radius)

    def toggle_draw_points(self):
        #invert the current state
        self.draw_points = False if self.draw_points else True

    def reset(self):
        self.colors = None
        self.draw_points = False
        self.draw_grouped = False

    def set_colors(self, colors):
        """ This should only be used for non grouped colors """
        self.colors = colors
        self.centroids_and_groups = None

    def set_grouped(self, centroids_and_groups):
        self.centroids_and_groups = centroids_and_groups
        self.colors = None

    def set_point_tint(self, point_tint):
        self.point_tint = point_tint

    def set_centroid_tint(self, centroid_tint):
        self.centroid_tint = centroid_tint

    def get_draw_points(self):
        return self.draw_points

    def get_colors(self):
        return self.colors

    def get_circle_center(self):
        return self.rainbow_circle.CENTER
