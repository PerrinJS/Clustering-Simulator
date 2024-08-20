#!/usr/bin/env python3
import pygame
import math
from time import sleep

class InterfaceManager:
    def __init__(self, event_table, screen_elements, window_size, window_name = "Nearest Neighbour Simulator"):
        self.window_name = window_name
        self.main_window = None
        self.event_table = event_table
        self.screen_elements = screen_elements
        self.window_size = window_size
        self.should_exit = False
        self.updated = True

        self.preloop_init_hook = None
        self.draw_hook = None

        self.BACKGROUND_COLOR = 0x000000

    def clear_background(self):
        self.main_window.fill(self.BACKGROUND_COLOR)
        pygame.display.flip()

    def exit_func(self):
        """ should only be called after run """
        self.should_exit = True

    def set_init_hook(self, preloop_init_hook):
        self.preloop_init_hook = preloop_init_hook

    def set_draw_hook(self, draw_hook):
        self.draw_hook = draw_hook

    def set_updated(self):
        self.updated = True

    def get_main_window(self):
        return self.main_window

    def run(self):
        pygame.init()
        self.main_window = pygame.display.set_mode(self.window_size, pygame.RESIZABLE)

        #set window title
        pygame.display.set_caption(self.window_name)
        self.clear_background()

        #main loop flags
        self.shouldExit = False

        if self.preloop_init_hook:
            self.preloop_init_hook(self.main_window, self)
        while self.should_exit is False:
            if self.screen_elements:
                for element in self.screen_elements:
                    if element.inc(pygame.mouse.get_pos(), self):
                        self.updated = True

            for event in pygame.event.get():
                if self.event_table:
                    if event.type in self.event_table:
                        callback_list = self.event_table[event.type]
                        for callback in callback_list:
                            callback(event, self.screen_elements, self)

            if (not self.should_exit) and self.updated:
                if self.draw_hook:
                    self.draw_hook(self.screen_elements, self.main_window, self)
                pygame.display.flip()
            else:
                sleep(.1)

            self.updated = False
        pygame.quit()


if __name__ == '__main__':
    def quit_func(event, interface_manager):
        pygame.quit()
        interface_manager.exit_func()

    WINDOW_SIZE = (1000, 600)

    event_table = {pygame.QUIT:[quit_func]}

    interface = InterfaceManager(event_table, None, WINDOW_SIZE)
    interface.run()
    print("EXITING")
