#!/usr/bin/python

class button:
    #TODO: implement relative sizing such that when the screen is scalled the buttons are scaled to match
    def __init__(self, shape_pos=(0,0,0,0), relative_size=False, label="", fit_text=True, colors=((0,255,0), (55,69,84), (00,00,00))):
        #TODO: add color maybe
        self.shape_pos = pygame.Rect(shape_pos)
        self.relative_size = relative_size
        self.label = label
        self.fit_text = fit_text
        self.is_button_down = False
        self.is_hover = False
        #FIXME: this is just for testing
        self.font = pygame.font.Font('Caladea-Regular.ttf', 40)
        self.label_surface = None
        self.BUTTON_BORDER = 0.20
        self.colors = colors

        self.func = None

    def __cvt_relative_to_actual_size(self, window_size):
        x,y,w,h = self.shape_pos
        return (int(x*window_size[0]), int(y*window_size[1]), int(w*window_size[0]), int(h*window_size[1]))

    def draw(self, surface):
        if self.is_button_down == True:
            pygame.draw.rect(surface, pygame.Color(self.colors[2]), self.shape_pos)
        else:
            button_box_color = self.colors[1]
            if self.is_hover:
                button_box_color = (min(button_box_color[0] * 2, 255),min(button_box_color[1] * 2, 255), min(button_box_color[2] * 2, 255))
            pygame.draw.rect(surface, button_box_color, self.shape_pos)
        #TODO: or we changed the label ---v
        if self.label_surface is None:
            #True = anti aliasing on
            self.label_surface = self.font.render(self.label, True, self.colors[0])

        text_rect = self.label_surface.get_rect()
        #TODO: do this properly (take into account height)
        butt_size_vs_txt = \
            (self.shape_pos.width - text_rect.width)#) + \
             #(self.shape_pos.height - text_rect.height))

        #NOTE: policy for text scaling is to scale the text to the height of
        # the button then clip
        output_label = self.label_surface
        #button larger then txt so scale up

        if butt_size_vs_txt < 0:
            #FIXME: for now we are just scaling to fit text in button
            fixed_width_height_factor = (1 - ((text_rect.width - self.shape_pos.width)/text_rect.width)) - self.BUTTON_BORDER
            text_rect.width = int(text_rect.width * fixed_width_height_factor)
            text_rect.height = int(text_rect.height * fixed_width_height_factor)
            output_label = pygame.transform.scale(self.label_surface, (text_rect.width, text_rect.height))
        #If the size of the box and the size of the txt are equal we still need to sclae for the BUTTON_BORDER
        else:
            #FIXME: for now we are just scaling to fit text in button
            fixed_width_height_factor = (1 + ((self.shape_pos.width - text_rect.width)/text_rect.width)) - self.BUTTON_BORDER
            text_rect.width = int(text_rect.width * fixed_width_height_factor)
            text_rect.height = int(text_rect.height * fixed_width_height_factor)
            output_label = pygame.transform.scale(self.label_surface, (text_rect.width, text_rect.height))
            print('scaled text up')

        text_rect.center = self.shape_pos.center
        surface.blit(output_label, text_rect)

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
        #new_pos will be the new top left so we need to convert
        center_offset = (self.shape_pos.center[0]-self.shape_pos.left, self.shape_pos.center[1]-self.shape_pos.top)
        self.shape_pos.center = (new_pos[0]+center_offset[0], new_pos[1]+center_offset[1])

    def set_size(self, new_size):
        self.shape_pos.width = new_size[0]
        self.shape_pos.height = new_size[1]




if __name__ == '__main__':
    import random
    import math
    from time import sleep
    import pygame

    WINDOW_SIZE = (1000, 600)
    BACKGROUND_COLOR = 0x000000
    CENTER = (math.floor(WINDOW_SIZE[0]/2), math.floor(WINDOW_SIZE[1]/2))

    def clearBackground(window):
        main_window.fill(BACKGROUND_COLOR)
        pygame.display.flip()

    def find_new_relative_position(elements, new_window_size):
        #TODO: Change how sizes are input, allow for relative % based sizing
        #TODO: the current code is just experimental
        print("in find new relative")
        butt2 = elements[1]
        butt2_box = butt2.shape_pos
        new_pos = new_window_size[0]-butt2_box.width-10, new_window_size[1]-butt2_box.height-10
        butt2.set_pos(new_pos)

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
    #FIXME: we get an overlap issue when they are this size
    #butt = button((10,10,800,100), "Button")
    #butt2 = button((110,210,100,100), "Button two")
    butt = button((10,10,100,100), False, "Button")
    butt2 = button((110,110,100,100), False, "Button two")

    butt.set_func(lambda : print('hello ' + str(id(butt))))
    butt2.set_func(lambda : print('hello ' + str(id(butt2))))

    screen_elements = [butt, butt2]

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
                resize(screen_elements, find_new_relative_position)
                updated = True
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    shouldExit = True
                    break
                elif event.key == pygame.K_F11:
                    butt2.set_size((500, 250))
                    #FIXME: this is just for testing
                    clearBackground(main_window)
                    updated = True
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
                element.draw(main_window)
            pygame.display.flip()
        else:
            sleep(.1)

        updated = False
