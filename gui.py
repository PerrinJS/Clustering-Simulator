#!/usr/bin/python
import pygame

class Button:
    #TODO: implement relative sizing such that when the screen is scalled the buttons are scaled to match
    def __init__(self, surface, shape_pos=(0,0,0,0), relative_size=False, label="", fit_text=True, colors=((0,255,0), (55,69,84), (00,00,00))):
        #TODO: add color maybe
        self.surface = surface
        self.relative_size = relative_size
        #We keep the orrigenal for when we input relative sizeing values such that we can then resize based on new screen sizes
        self.inp_shape_pos = shape_pos
        self.shape_pos = pygame.Rect(shape_pos)
        self.label = label
        self.fit_text = fit_text
        self.is_button_down = False
        self.is_hover = False
        #FIXME: this is just for testing
        self.font = pygame.font.Font('Caladea-Regular.ttf', 40)
        self.label_surface = None
        self.BUTTON_BORDER = 0.90
        self.colors = colors

        self.func = None

    def _adjust_for_relative_sizing(self, window_size):
        ret = pygame.Rect(self.shape_pos)
        if self.relative_size:
            x,y,w,h = self.inp_shape_pos
            ret = pygame.Rect(int(x*window_size[0]), int(y*window_size[1]), int(w*window_size[0]), int(h*window_size[1]))
        return ret

    def draw(self):
        if self.is_button_down == True:
            pygame.draw.rect(self.surface, pygame.Color(self.colors[2]), self._adjust_for_relative_sizing(self.surface.get_size()))
        else:
            button_box_color = self.colors[1]
            if self.is_hover:
                button_box_color = (min(button_box_color[0] * 2, 255),min(button_box_color[1] * 2, 255), min(button_box_color[2] * 2, 255))
            pygame.draw.rect(self.surface, button_box_color, self._adjust_for_relative_sizing(self.surface.get_size()))
        #TODO: or we changed the label ---v
        if self.label_surface is None:
            #True = anti aliasing on
            self.label_surface = self.font.render(self.label, True, self.colors[0])

        text_rect = self.label_surface.get_rect()
        #TODO: do this properly (take into account height)
        real_shape_pos = self._adjust_for_relative_sizing(self.surface.get_size())
        butt_size_vs_txt = \
            (real_shape_pos.width - text_rect.width)#) + \
             #(self.shape_pos.height - text_rect.height))

        #NOTE: policy for text scaling is to scale the text to the height of
        # the button then clip
        output_label = self.label_surface
        #button larger then txt so scale up

        if butt_size_vs_txt < 0:
            #FIXME: for now we are just scaling to fit text in button
            fixed_width_height_factor = (1 - ((text_rect.width - real_shape_pos.width)/text_rect.width)) * self.BUTTON_BORDER
            text_rect.width = int(text_rect.width * fixed_width_height_factor)
            text_rect.height = int(text_rect.height * fixed_width_height_factor)
            output_label = pygame.transform.scale(self.label_surface, (text_rect.width, text_rect.height))
        #If the size of the box and the size of the txt are equal we still need to sclae for the BUTTON_BORDER
        else:
            #FIXME: for now we are just scaling to fit text in button
            fixed_width_height_factor = (1 + ((real_shape_pos.width - text_rect.width)/text_rect.width)) - self.BUTTON_BORDER
            text_rect.width = int(text_rect.width * fixed_width_height_factor)
            text_rect.height = int(text_rect.height * fixed_width_height_factor)
            output_label = pygame.transform.scale(self.label_surface, (text_rect.width, text_rect.height))

        text_rect.center = real_shape_pos.center
        self.surface.blit(output_label, text_rect)

    def set(self):
        self.is_button_down = True
        if self.func is not None:
            self.func()

    def reset(self):
        self.is_button_down = False
        self.is_hover = False

    def is_pos_inside(self, pos):
        x,y = pos
        pos_rect = pygame.Rect(x,y,1,1)
        if self.relative_size:
            real_shape_pos = self._adjust_for_relative_sizing(self.surface.get_size())
            return real_shape_pos.contains(pos_rect)
        else:
            return self.shape_pos.contains(pos_rect)

    def on_mouse_down(self):
        if self.is_pos_inside(pygame.mouse.get_pos()):
            self.set()

    def on_mouse_up(self):
        self.reset()

    def hover_check(self, pos):
        if self.is_pos_inside(pos):
            self.is_hover = True
        else:
            self.is_hover = False
        return self.is_hover

    def inc(self, pos):
        if self.is_hover != self.hover_check(pos):
            return True
        return False

    def set_func(self, func):
        self.func = func

    def set_pos(self, new_pos):
        #FIXME: get this to work with relative sizing
        #new_pos will be the new top left so we need to convert
        center_offset = (self.shape_pos.center[0]-self.shape_pos.left, self.shape_pos.center[1]-self.shape_pos.top)
        self.shape_pos.center = (new_pos[0]+center_offset[0], new_pos[1]+center_offset[1])

    def set_size(self, new_size):
        #FIXME: get this to work with relative sizing
        self.shape_pos.width = new_size[0]
        self.shape_pos.height = new_size[1]




if __name__ == '__main__':
    import random
    import math
    from time import sleep

    WINDOW_SIZE = (1000, 600)
    BACKGROUND_COLOR = 0x000000
    CENTER = (math.floor(WINDOW_SIZE[0]/2), math.floor(WINDOW_SIZE[1]/2))

    def clearBackground(window):
        main_window.fill(BACKGROUND_COLOR)
        pygame.display.flip()

    def resize(elements = None, resize_callback = None):
        findCenter = lambda x : (math.floor(x[0]/2), math.floor(x[1]/2))
        WINDOW_SIZE = main_window.get_size()
        CENTER = findCenter(WINDOW_SIZE)
        clearBackground(main_window)
        if (elements is not None) and (resize_callback is not None):
            resize_callback(elements, WINDOW_SIZE)


    pygame.init()
    main_window = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE)
    #set window title
    pygame.display.set_caption("Nearest Neighbour Simulator")
    clearBackground(main_window)

    #main loop
    shouldExit = False
    resize()
    updated = True
    buff_size = 0.008

    #NOTE: with relative sizeing if the width of the window is greater then the
    #height then spacing will be larger allong the width then height for the
    #same percentage
    butt = Button(main_window, (5,5,250,100), False, "Button")
    butt2 = Button(main_window, (1-.275-buff_size,buff_size,.275,.18), True, "Button two")
    butt3 = Button(main_window, (buff_size,1-.18-buff_size,.275,.18), True, "Button 3")
    butt4 = Button(main_window, (1-.275-buff_size,1-.18-buff_size,.275,.18), True, "Button 4")

    butt.set_func(lambda : print('hello 1 ' + str(id(butt))))
    butt2.set_func(lambda : print('hello 2 ' + str(id(butt2))))
    butt3.set_func(lambda : print('hello 3 ' + str(id(butt3))))
    butt4.set_func(lambda : print('hello 4 ' + str(id(butt4))))

    screen_elements = [butt, butt2, butt3, butt4]

    while shouldExit is False:
        for element in screen_elements:
            if element.inc(pygame.mouse.get_pos()):
                updated = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                shouldExit = True
                break
            elif event.type == pygame.VIDEORESIZE:
                resize()
                updated = True
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    shouldExit = True
                    break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for element in screen_elements:
                    element.on_mouse_down()
                updated = True
            elif event.type == pygame.MOUSEBUTTONUP:
                for element in screen_elements:
                    element.on_mouse_up()
                updated = True

        if (not shouldExit) and updated:
            for element in screen_elements:
                element.draw()
            pygame.display.flip()
        else:
            sleep(.1)

        updated = False
