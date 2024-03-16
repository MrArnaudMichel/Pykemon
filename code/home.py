import os

import pygame

from dialog import Dialog
from sql import SQL


class Home:
    def __init__(self, screen: pygame.display):
        self.screen = screen
        self.activate = True
        self.image_home = pygame.image.load("../data/image/home/mainImageHome.png").convert_alpha()
        self.index = 1
        self.image_index = {}
        for i in range(8):
            self.image_index[i] = 1080
        self.surface = pygame.Surface((1920, 1080))
        self.surface.fill((0, 32, 38))
        self.decale = 0
        self.decaleBool = False
        self.drawintro_bool = False
        self.dialog = Dialog()
        self.sql = SQL()

    def run(self):
        self.screen.blit(self.image_home, (0, 0))

        if pygame.mouse.get_pressed()[0] and self.decale < 1080:
            if self.pklInFolder():
                self.activate = False
            self.decaleBool = True
        self.screen.blit(self.surface, (0, 1080 - self.decale))
        if self.decaleBool:
            self.decale += 10
            if self.decale >= 1080:
                self.decaleBool = False
                if self.pklInFolder():
                    self.activate = False
                else:
                    self.drawintro_bool = True
                    self.dialog = Dialog(self.sql.select_where("dialog", "id", 1)[0][1])
        if self.drawintro_bool:
            self.dialog.draw(self.screen, 1, height=400)
            if pygame.mouse.get_pressed()[0] and self.dialog.enddraw:
                self.dialog.next_text()
                if not self.dialog.talking:
                    self.activate = False

    def pklInFolder(self):
        for fichier in os.listdir("../data/save"):
            if fichier.endswith(".pkl"):
                return True
        return False
