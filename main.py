#!/usr/bin/python
import random
import math
import colorsys
import pygame
import color_and_position_conversion as CAPConv
from screen_management import InterfaceManager
from rainbow_point_plotter import RainbowPointPlotter
from clustering_and_classification import KMeansClustererRGB
from gui import Button

WINDOW_SIZE = (1000, 600)

def gen_rand_color():
    return random.randrange(0x000000, 0xffffff)

def gen_rand_colors(quantity):
    colors = [None] * quantity
    for i in range(0,quantity):
        colors[i] = gen_rand_color()
    return colors

class SimPointManager:
    def convert_colors(colors):
        converted_colors = []
        for color in colors:
            (r,g,b) = CAPConv.convert_web_to_rgb(color)
            (h,s,_) = colorsys.rgb_to_hsv(r,g,b)
            #fully saturate the colors so the colors match those of the rainbow circle behind it
            color = colorsys.hsv_to_rgb(h,s,1)
            converted_colors.append(color)

        return converted_colors

    def __init__(self):
        self.points = None
        self.converted_points = None
        self.clustered_points = None

    def reset(self):
        self.points = None
        self.converted_points = None
        self.clustered_points = None

    def set_points(self, points):
        self.points = points
        self.converted_points = SimPointManager.convert_colors(self.points)

    def get_conv_points(self):
        return self.converted_points

    def get_conv_points_clustered(self):
        if self.clustered_points:
            return self.clustered_points

        clusterer = KMeansClustererRGB(self.converted_points)
        clusters = clusterer.get_clusters()
        centroids = clusterer.get_centroids()

        self.clustered_points = (centroids, clusters)
        return self.clustered_points

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

    def _gen_rand_square(self):
        top_left = None
        curr_win_size = None
        if self.attached_window:
            curr_win_size = self.attached_window
        else:
            curr_win_size = WINDOW_SIZE

        top_left = (random.randrange(0, curr_win_size[0]), random.randrange(0, curr_win_size[1]))
        side_length = random.randrange(0, math.floor(curr_win_size[0]/2))
        return pygame.Rect(top_left[0], top_left[1], side_length, side_length)

    def _draw_rand_square(self, window):
        rand_square = self._gen_rand_square()
        rand_color = gen_rand_color()
        pygame.draw.rect(window, rand_color, rand_square)

    def update_dimens(self, _window_size=None, _center=None, _max_radius=None):
        pass

    def draw(self, window=None):
        if self.active:
            if window is None:
                if self.attached_window is None:
                    raise ValueError("No attached surface")
                window = self.attached_window
            self._draw_rand_square(window)

def run_nearest_sim(rainbow_point_plotter, _sim_point_manager, show_clusters, _interface_manager):
    """ This should trigger the plotter to run the simulation """
    if not rainbow_point_plotter.get_draw_points():
        rainbow_point_plotter.toggle_draw_points()
        rainbow_point_plotter.set_point_tint(.9)
        rainbow_point_plotter.set_centroid_tint(.3)

    if rainbow_point_plotter.get_colors() is None:
        if sim_point_manager.get_conv_points() is None:
            rand_colors_web = gen_rand_colors(100)
            sim_point_manager.set_points(rand_colors_web)

    if show_clusters:
        rainbow_point_plotter.set_grouped(sim_point_manager.get_conv_points_clustered())
    else:
        rainbow_point_plotter.set_colors(sim_point_manager.get_conv_points())


def new_handler(rainbow_point_plotter, sim_point_manager):
    rainbow_point_plotter.reset()
    sim_point_manager.reset()

def quit_func(_event=None, _screen_elements=None, interface_manager=None):
    if interface_manager is None:
        raise ValueError("No interface_manager given")
    interface_manager.exit_func()

def resize_func(_event, screen_elements, interface_manager):
    for element in screen_elements:
        element.update_dimens()
    interface_manager.set_updated()
    interface_manager.clear_background()

def clear_func(_event, _screen_elements, interface_manager):
    interface_manager.set_updated()
    interface_manager.clear_background()

def toggle_rand_func(_event, screen_elements, _interface_manager):
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

def draw_func(screen_elements, main_window, _interface_manager):
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
    draw_colors_button.set_func(\
                lambda : run_nearest_sim(rainbowCircle, sim_point_manager, False, interface))
    draw_group_button.set_func(\
                lambda : run_nearest_sim(rainbowCircle, sim_point_manager, True, interface))

    interface.run()
    print("EXITING")
