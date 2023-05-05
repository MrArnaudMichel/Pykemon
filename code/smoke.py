import random

import pygame


class Smoke:
    def __init__(self, screen, listsmoke: list[(float, float)], maplayerzoom):
        self.maplayerzoom = maplayerzoom
        self.screen = screen
        self.decale_x = [10, 5, 14, 7, 2]
        self.listsmoke = listsmoke
        self.smoke_strip = [pygame.transform.scale_by(
            pygame.image.load("../data/image/Chimney Smoke/chimneysmoke_0" + str(i) + "_strip30.png"),
            int(maplayerzoom)).convert_alpha() for i in range(1, 6)]
        self.pos_smoke = {}
        self.smoke = []
        for smoke_strip in self.smoke_strip:
            image_width = smoke_strip.get_width() // 30
            list = []
            for j in range(30):
                list.append(
                    smoke_strip.subsurface(pygame.Rect(j * image_width, 0, image_width, smoke_strip.get_height())))
            self.smoke.append(list)
        for i in range(len(self.listsmoke)):
            self.pos_smoke[i] = random.randint(0, 4)
        self.cooldown = 0
        self.i: int = 0

        for i in range(len(self.listsmoke)):
            self.listsmoke[i] = (self.listsmoke[i][0] - self.smoke[self.pos_smoke[i]][0].get_width() / maplayerzoom,
                                 self.listsmoke[i][1] - self.smoke[self.pos_smoke[i]][0].get_height() / maplayerzoom)

    def draw(self, maplayeroffset):
        for i in range(len(self.listsmoke)):
            self.screen.blit(self.smoke[self.pos_smoke[i]][self.i], (
                (self.listsmoke[i][0] + maplayeroffset[0]) * self.maplayerzoom + self.decale_x[self.pos_smoke[i]],
                (self.listsmoke[i][1] + maplayeroffset[1]) * self.maplayerzoom))
        if self.cooldown % 10 == 0:
            self.i += 1
            if self.i >= 30:
                self.i = 0
        self.cooldown += 1
