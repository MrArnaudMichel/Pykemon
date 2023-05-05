import time

import pygame


class Night:
    def __init__(self, screen: pygame.display):
        self.screen = screen
        self.night = False
        self.night_surface = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
        self.night_surface.fill((0, 0, 0))
        self.night_surface.set_alpha(0)
        self.clock = time.time()
        self.cycle = ["sunrise", "day", "sunset", "night"]
        self.cycle_index = 1
        self.index = 0
        self.speed_animation_sunrise_sunset = 0.1

    def run(self):
        if self.cycle_index == 0:
            if self.night_surface.get_alpha() > 0:
                self.index -= self.speed_animation_sunrise_sunset
                self.night_surface.set_alpha(int(self.index))
            else:
                self.cycle_index = 1
        elif self.cycle_index == 1:
            if time.time() - self.clock > 600:
                self.cycle_index = 2
                self.clock = time.time()
        elif self.cycle_index == 2:
            if self.night_surface.get_alpha() < 128:
                self.index += self.speed_animation_sunrise_sunset
                self.night_surface.set_alpha(int(self.index))
            else:
                self.cycle_index = 3
                self.clock = time.time()
        elif self.cycle_index == 3:
            if time.time() - self.clock > 150:
                self.cycle_index = 0
                self.clock = time.time()
        if not self.night_surface.get_alpha() == 0:
            self.screen.blit(self.night_surface, (0, 0))
