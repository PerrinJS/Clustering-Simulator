#!/usr/bin/python
import pygame
import random
import math
import colorsys
import ColorAndPositionConversion as CAPConv
from ScreenManagement import InterfaceManager
from rainbowPointPlotter import RainbowPointPlotter
from circleLib import find_center
from clusteringAndClassification import KMeansClusterer
from gui import Button

WINDOW_SIZE = (1000, 600)

def genRandColor():
    return random.randrange(0x000000, 0xffffff)

def genRandColors(quantity):
    colors = [None] * quantity
    for i in range(0,quantity):
        colors[i] = genRandColor()
    return colors

class SimPointManager:
    def convert_colors(colors):
        converted_colors = []
        for color in colors:
            (r,g,b) = CAPConv.convertWebToRGB(color)
            (h,s,_) = colorsys.rgb_to_hsv(r,g,b)
            #value is .9 to add a little tint to the inside of the circles
            color = colorsys.hsv_to_rgb(h,s,.9)
            converted_colors.append(color)

        return converted_colors

    def __init__(self):
        self.points = None
        self.converted_points = None
        self.clustered_points = None
        self.ungrouped_clusterd = None

    def reset(self):
        self.points = None
        self.converted_points = None
        self.clustered_points = None
        self.ungrouped_clusterd = None

    def set_points(self, points):
        self.points = points
        self.converted_points = SimPointManager.convert_colors(self.points)

    def get_conv_points(self):
        return self.converted_points

    def get_conv_points_clustered(self):
        if self.clustered_points:
            return self.ungrouped_clusterd

        center = (0,0) #Thease data points are just colors and the way they will be used in clustering will not relate to any spesific relative position.
        hsv_converted_points = [colorsys.rgb_to_hsv(r,g,b) for r,g,b in self.converted_points]

        clusterer = KMeansClusterer(data=hsv_converted_points)
        self.clustered_points = clusterer.getClusters(center)
        ungrouped_clusterd_points_hsv = []
        for cluster in self.clustered_points:
            ungrouped_clusterd_points_hsv = ungrouped_clusterd_points_hsv + cluster

        centroids = clusterer.getCentroids(center)
        #FIXME: this is inificient
        for i in range(len(ungrouped_clusterd_points_hsv)):
            h,s = ungrouped_clusterd_points_hsv[i]
            #Dark point is a centroid, light point is a standard point
            if ungrouped_clusterd_points_hsv[i] in centroids:
                ungrouped_clusterd_points_hsv[i] = (h,s,.6)
            else:
                ungrouped_clusterd_points_hsv[i] = (h,s,.9)

        ungrouped_clusterd_points = []
        for i in range(len(ungrouped_clusterd_points_hsv)):
            h,s,v = ungrouped_clusterd_points_hsv[i]
            color = colorsys.hsv_to_rgb(h,s,v)
            ungrouped_clusterd_points.append(color)

        self.ungrouped_clusterd = ungrouped_clusterd_points
        return ungrouped_clusterd_points


class RandSquareDrawer:
    def __init__(self):
        self.active = False
        self.attached_window = None

    def inc(self, _pos, interface_manager):
        if self.active:
            interface_manager.set_updated()

    def on_mouse_up(self, _window):
        pass

    def on_mouse_down(self, _window):
        pass

    def toggle(self):
        if self.active:
            self.active = False
        else:
            self.active = True

    def is_active(self):
        return self.active

    def attach_window(self, surface):
        self.attached_window = surface

    def _genRandSquare():
        topLeft = (random.randrange(0, WINDOW_SIZE[0]), random.randrange(0, WINDOW_SIZE[1]))
        sideLength = random.randrange(0, math.floor(WINDOW_SIZE[0]/2))
        return pygame.Rect(topLeft[0], topLeft[1], sideLength, sideLength)

    def _drawRandSquare(self, window):
        randSquare = RandSquareDrawer._genRandSquare()
        randColor = genRandColor()
        pygame.draw.rect(window, randColor, randSquare)

    def updateDimens(self, _window_size=None, _center=None, _max_radius=None):
        pass

    def draw(self, window=None):
        if self.active:
            if window is None:
                if self.attached_window is None:
                    raise ValueError("No attached surface")
                window = self.attached_window
            self._drawRandSquare(window)

def runNearestSim(rainbow_point_plotter, sim_point_manager, show_clusters, interface_manager):
    """ This should trigger the plotter to run the simulation """
    #FIXME: this is just for testing currently we just print randomly colored
    #dots to screen
    if not rainbow_point_plotter.getDrawPoints():
        rainbow_point_plotter.toggleDrawPoints()

    if rainbow_point_plotter.getColors() == None:
        if sim_point_manager.get_conv_points() is None:
            randColorsWeb = genRandColors(100)
            sim_point_manager.set_points(randColorsWeb)

    if show_clusters:
        rainbow_point_plotter.setColors(sim_point_manager.get_conv_points_clustered())
    else:
        rainbow_point_plotter.setColors(sim_point_manager.get_conv_points())


def new_handler(rainbow_point_plotter, sim_point_manager):
    rainbow_point_plotter.reset()
    sim_point_manager.reset()

def quit_func(event=None, screen_elements=None, interface_manager=None):
    if interface_manager is None:
        raise ValueError("No interface_manager given")
    interface_manager.exit_func()

def resize_func(event, screen_elements, interface_manager):
    for element in screen_elements:
        element.updateDimens()
    interface_manager.set_updated()
    interface_manager.clear_background()

def clear_func(event, screen_elements, interface_manager):
    interface_manager.set_updated()
    interface_manager.clear_background()

def toggle_rand_func(event, screen_elements, interface_manager):
    screen_elements[1].toggle()

def key_down(event, screen_elements, interface_manager):
    if event.key == pygame.K_F12:
        toggle_rand_func(event, screen_elements, interface_manager)
    elif event.key == pygame.K_c:
        clear_func(event, screen_elements, interface_manager)
    elif event.key == pygame.K_q:
        quit_func(event, screen_elements, interface_manager)

def on_mouse_down(_event, screen_elements, interface_manager):
    for element in screen_elements:
        element.on_mouse_down(interface_manager.get_main_window())
    interface_manager.set_updated()

def on_mouse_up(_event, screen_elements, interface_manager):
    for element in screen_elements:
        element.on_mouse_up(interface_manager.get_main_window())
    interface_manager.set_updated()

def draw_func(screen_elements, main_window, interface_manager):
    #we always want the buttons on top
    for element in screen_elements:
        element.draw(main_window)

if __name__ == '__main__':
    WINDOW_SIZE = (1000, 600)
    rainbowCircle = RainbowPointPlotter(None, WINDOW_SIZE)
    sim_point_manager = SimPointManager()
    exit_button = Button(None, ( .99-.1, .99-.1, .1, .1), True, "Exit")
    new_button = Button(None, ( .99-.1, .99-.1-.11, .1, .1), True, "New")
    draw_group_button = Button(None, (.01, .99-.1, .15, .1), True, "Draw Group Color")
    draw_colors_button = Button(None, (.01, .99-.1-.11, .15, .1), True, "Draw Real Color")
    screen_elements = [rainbowCircle, RandSquareDrawer(), exit_button,\
                       draw_group_button, draw_colors_button, new_button]

    event_table = {
        pygame.QUIT :           [quit_func],
        pygame.KEYDOWN  :       [key_down],
        pygame.VIDEORESIZE:     [resize_func],
        pygame.MOUSEBUTTONUP:   [on_mouse_up],
        pygame.MOUSEBUTTONDOWN:   [on_mouse_down]
    }

    interface = InterfaceManager(event_table, screen_elements, WINDOW_SIZE)

    interface.set_draw_hook(draw_func)
    exit_button.set_func(lambda : quit_func(interface_manager=interface))
    new_button.set_func(lambda : new_handler(screen_elements[0], sim_point_manager))
    draw_colors_button.set_func(lambda : runNearestSim(rainbowCircle, sim_point_manager, False, interface))
    draw_group_button.set_func(lambda : runNearestSim(rainbowCircle, sim_point_manager, True, interface))

    interface.run()
    print("EXITING")
