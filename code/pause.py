import datetime
import os
import sys

import PIL.Image
import PIL.ImageFilter
import PIL.ImageGrab
import pygame

import dialog
import save
from entity import Player
from sql import SQL


def blur(image):
    image = image.filter(PIL.ImageFilter.GaussianBlur(radius=5))
    return image


def pilImgToPygameImg(pilImg) -> pygame.Surface:
    return pygame.image.fromstring(pilImg.tobytes(), pilImg.size, pilImg.mode).convert_alpha()


class Pause:
    def __init__(self, screen: pygame.Surface, player: Player):
        self.screen = screen
        self.buttons_options = {}
        self.click = None
        self.quit = False
        self.selected = None
        self.player = player
        self.selected = "menu"
        self.unlockedoption = {
            "Quit": "Quitter",
            "Save": "Sauvegarder",
            "Inventory": "Inventaire",
            "Map": "Carte",
            "Pokemon": "Pokémon",
            "Option": "Options",
            "Pokedex": "Pokédex",
        }

        self.screenshot = pygame.image.save(self.screen, "../data/image/settings/screenshot.png")
        self.imagefontblur = PIL.Image.open("../data/image/settings/screenshot.png")
        self.imagefontblur = blur(self.imagefontblur)
        self.imagefontblur = pilImgToPygameImg(self.imagefontblur)

        self.image_map = pygame.transform.scale_by(pygame.image.load("../data/UI/worldmap/worldmaps/world_map_2.png"),
                                                   4).convert_alpha()
        self.map_decale_x = 0
        self.map_decale_y = 0

        self.nodata = pygame.transform.scale(pygame.image.load("../data/image/settings/nodata.png"),
                                             (128, 128)).convert_alpha()

        self.cardUnselected = pygame.transform.scale(pygame.image.load("../data/image/settings/cardUnselected.png"),
                                                     (self.screen.get_width() / 3, 42)).convert_alpha()
        self.cardUnselectedoption = pygame.transform.scale(
            pygame.image.load("../data/image/settings/cardUnselected.png"), (1280, 48)).convert_alpha()
        self.cardselectedoption = pygame.transform.scale_by(
            pygame.image.load("../data/image/settings/cardUnselected.png"), 2).convert_alpha()

        self.pos_mouse_before = None
        self.save = False

        self.list_save = ["", "Pokédex", "Position actuelle", "Temps de jeu", "Date", "Argent", "Badge"]
        if os.listdir("../data/save/"):
            self.list_info = save.load_list(os.listdir("../data/save/")[0])
        else:
            self.list_info = ["", "", "", "", "", "", ""]

        self.lucas = pygame.transform.scale_by(pygame.image.load("../data/image/settings/lucas.png"),
                                               0.35).convert_alpha()
        self.aurore = pygame.transform.scale_by(pygame.image.load("../data/image/settings/dawn.png"),
                                                0.35).convert_alpha()

        self.sql = SQL()

        self.image_pause: dict[str:pygame.Surface] = {
            "quit": pygame.transform.scale(pygame.image.load("../data/image/settings/quit.png"),
                                           (64, 64)).convert_alpha(),
            "save": pygame.transform.scale(pygame.image.load("../data/image/settings/save.png"),
                                           (64, 64)).convert_alpha(),
            "inventory": pygame.transform.scale(
                pygame.image.load("../data/image/settings/inventory.png").convert_alpha(),
                (64, 64)),
            "map": pygame.transform.scale(pygame.image.load("../data/image/settings/map.png"),
                                          (64, 64)).convert_alpha(),
            "pokemon": pygame.transform.scale(pygame.image.load("../data/image/settings/pokemon.png"),
                                              (64, 64)).convert_alpha(),
            "option": pygame.transform.scale(pygame.image.load("../data/image/settings/option.png"),
                                             (64, 64)).convert_alpha(),
            "pokedex": pygame.transform.scale(pygame.image.load("../data/image/settings/pokedex.png"),
                                              (64, 64)).convert_alpha()}

    def update_font(self):
        pygame.image.save(self.screen, "../data/image/settings/screenshot.png")
        self.imagefontblur = PIL.Image.open("../data/image/settings/screenshot.png")
        self.imagefontblur = blur(self.imagefontblur)
        self.imagefontblur = pilImgToPygameImg(self.imagefontblur)

    def draw_pause(self, map):
        self.screen.fill((0, 0, 0))
        if self.selected == "menu":
            self.draw_map()
        elif self.selected == "save":
            self.draw_save()
        elif self.selected == "option":
            self.draw_option()

        rect = pygame.Rect(0, 0, self.screen.get_width(), 128)
        pygame.draw.rect(self.screen, (4, 18, 18), rect)
        rect = pygame.Rect(0, self.screen.get_height() - 128, self.screen.get_width(), 128)
        pygame.draw.rect(self.screen, (4, 18, 18), rect)

        date = ""
        date += str(datetime.datetime.now().day) + "/"
        date += str(datetime.datetime.now().month) + "/" if datetime.datetime.now().month >= 10 else "0" + str(
            datetime.datetime.now().month) + "/"
        date += str(datetime.datetime.now().year)

        text, pos = dialog.setText(date, 32, 42, 32, (20, 87, 70), "left", font="Roboto-Light")
        self.screen.blit(text, pos)

        hour = ""
        hour += str(datetime.datetime.now().hour) + ":"
        hour += str(datetime.datetime.now().minute) if datetime.datetime.now().minute >= 10 else "0" + str(
            datetime.datetime.now().minute)
        hour += ":" + str(datetime.datetime.now().second) if datetime.datetime.now().second >= 10 else ":0" + str(
            datetime.datetime.now().second)

        text, pos = dialog.setText(hour, 32, 84, 32, (20, 87, 70), "left", font="Roboto-Light")
        self.screen.blit(text, pos)

        timeplayed = ""
        timeplayed += str(self.player.timeplayed.seconds // 3600) + ":"
        timeplayed += str((self.player.timeplayed.seconds // 60) % 60) if (
                                                                                  self.player.timeplayed.seconds // 60) % 60 >= 10 else "0" + str(
            (self.player.timeplayed.seconds // 60) % 60) + ":"
        timeplayed += str(
            self.player.timeplayed.seconds % 60) if self.player.timeplayed.seconds % 60 >= 10 else "0" + str(
            self.player.timeplayed.seconds % 60)

        text, pos = dialog.setText(timeplayed, self.screen.get_width() - 32, 32, 32, (20, 87, 70), "right",
                                   font="Roboto-Light")
        self.screen.blit(text, pos)

        text, pos = dialog.setText(str(self.player.pokedollars) + " P", self.screen.get_width() - 32, 84, 32,
                                   (20, 87, 70), "right", font="Roboto-Light")
        self.screen.blit(text, pos)

        text, pos = dialog.setText("Lieu actuel", self.screen.get_width() - 32, self.screen.get_height() - 96, 32,
                                   (20, 87, 70), "right", font="Roboto-Light")
        self.screen.blit(text, pos)
        try:
            text, pos = dialog.setText(self.sql.select_where("map", "name", map)[0][0], self.screen.get_width() - 32,
                                       self.screen.get_height() - 64, 32, (179, 176, 71), "right",
                                       font="Roboto-Regular", )
            self.screen.blit(text, pos)
        except:
            pass

        text, pos = dialog.setText("Aucune quête suivie", self.screen.get_width() / 2, self.screen.get_height() - 74,
                                   32,
                                   (20, 87, 70), "center", font="Roboto-Light")
        self.screen.blit(text, pos)

        self.buttons_options.clear()
        nb_image_pause = len(self.unlockedoption.keys())
        i = 0
        for key, value in self.image_pause.items():
            self.buttons_options[key] = pygame.Rect(self.screen.get_width() / 2 - (nb_image_pause * 128) / 2 + (128 * i)
                                                    + 32, 16, 128, 128)
            i += 1
        i = 0
        for key, value in self.image_pause.items():
            if key.title() in self.unlockedoption.keys():
                color = (20, 87, 70)
                if self.buttons_options[key].collidepoint(pygame.mouse.get_pos()) or (
                        (self.selected == "menu" and key == "map") or self.selected == key):
                    self.screen.blit(value,
                                     (self.screen.get_width() / 2 - (nb_image_pause * 128) / 2 + (128 * i) + 32, 16))
                    color = (106, 176, 126)
                    if (self.selected == "menu" and key == "map") or self.selected == key:
                        rect = pygame.Rect(self.screen.get_width() / 2 - (nb_image_pause * 128) / 2 + (128 * i) + 32,
                                           120,
                                           64, 4)
                        pygame.draw.rect(self.screen, (106, 176, 126), rect)
                else:
                    image_alpha_128 = value.copy()
                    image_alpha_128.set_alpha(128)
                    self.screen.blit(image_alpha_128,
                                     (self.screen.get_width() / 2 - (nb_image_pause * 128) / 2 + (128 * i) + 32, 16))

                text, pos = dialog.setText(key.title(),
                                           self.screen.get_width() / 2 - (nb_image_pause * 128) / 2 + (128 * i) + 64,
                                           100,
                                           26,
                                           color, "center", font="Roboto-Light")
                self.screen.blit(text, pos)
                i += 1

    def draw_save(self):
        self.screen.blit(self.imagefontblur, (0, 0))

        surface = pygame.Surface((self.screen.get_width() / 3, 64))
        surface.fill((1, 47, 43))
        self.screen.blit(surface, (self.screen.get_width() / 2 - self.screen.get_width() / 6,
                                   self.screen.get_height() / 4 - 24))

        if os.listdir("../data/save"):
            text, pos = dialog.setText(self.list_info[0], self.screen.get_width() / 2, self.screen.get_height() / 4 + 8,
                                       32,
                                       (255, 255, 255), "center", font="Roboto-Light")
            self.screen.blit(text, pos)
            for i in range(1, 7):
                self.screen.blit(self.cardUnselected, (self.screen.get_width() / 2 - self.screen.get_width() / 6,
                                                       self.screen.get_height() / 2 - self.screen.get_height() / 12 + (
                                                               i * 56)))
                text, pos = dialog.setText(self.list_save[i],
                                           self.screen.get_width() / 2 - self.screen.get_width() / 6 + 16,
                                           self.screen.get_height() / 2 - self.screen.get_height() / 12 + 20 + (
                                                   i * 56), 32, (106, 176, 126), "left", font="Roboto-Light")
                self.screen.blit(text, pos)
                if i == 2:
                    text, pos = dialog.setText(self.sql.select_where("map", "name", self.list_info[i])[0][0],
                                               self.screen.get_width() / 2 + 16,
                                               self.screen.get_height() / 2 - self.screen.get_height() / 12 + 20 + (
                                                       i * 56), 32, (255, 255, 255), "left", font="Roboto-Light")
                    self.screen.blit(text, pos)
                elif i == 3:
                    timeplayed = ""
                    timeplayed += str(self.list_info[i].seconds // 3600) + ":"
                    timeplayed += str((self.list_info[i].seconds // 60) % 60) if (
                                                                                         self.list_info[
                                                                                             i].seconds // 60) % 60 >= 10 else "0" + str(
                        (self.list_info[i].seconds // 60) % 60) + ":"
                    timeplayed += str(
                        self.list_info[i].seconds % 60) if self.list_info[i].seconds % 60 >= 10 else "0" + str(
                        self.list_info[i].seconds % 60)
                    text, pos = dialog.setText(timeplayed, self.screen.get_width() / 2 + 16,
                                               self.screen.get_height() / 2 - self.screen.get_height() / 12 + 20 + (
                                                       i * 56), 32, (255, 255, 255), "left", font="Roboto-Light")
                elif i == 6:
                    text, pos = dialog.setText(str(len(self.list_info[i])), self.screen.get_width() / 2 + 16,
                                               self.screen.get_height() / 2 - self.screen.get_height() / 12 + 20 + (
                                                       i * 56), 32, (255, 255, 255), "left", font="Roboto-Light")
                else:
                    text, pos = dialog.setText(str(self.list_info[i]), self.screen.get_width() / 2 + 16,
                                               self.screen.get_height() / 2 - self.screen.get_height() / 12 + 20 + (
                                                       i * 56), 32, (255, 255, 255), "left", font="Roboto-Light")
                self.screen.blit(text, pos)
                if self.player.gender == "lucas":
                    self.screen.blit(self.lucas, (self.screen.get_width() / 2 + self.screen.get_width() / 4,
                                                  self.screen.get_height() - self.lucas.get_height()))
                else:
                    self.screen.blit(self.aurore, (self.screen.get_width() / 16,
                                                   self.screen.get_height() - self.aurore.get_height()))
        else:
            text, pos = dialog.setText("Sauvegarde", self.screen.get_width() / 2, self.screen.get_height() / 4 + 8,
                                       32,
                                       (255, 255, 255), "center", font="Roboto-Light")
            self.screen.blit(text, pos)
            surface = pygame.Surface((self.screen.get_width() / 3, self.screen.get_height() / 3.5))
            surface.fill((1, 47, 43))
            self.screen.blit(surface, (self.screen.get_width() / 2 - self.screen.get_width() / 6,
                                       self.screen.get_height() / 2 - self.screen.get_height() / 16))
            self.screen.blit(self.nodata, (self.screen.get_width() / 2 - self.nodata.get_width() / 2,
                                           self.screen.get_height() / 2 - self.screen.get_height() / 16 + 48))
            texts = dialog.split_text(
                "Vous pouvez sauvegarder sur cet emplacement sans avoir peur d'écraser une autre partie, ouf !",
                length=50)
            for i in range(len(texts[0])):
                text, pos = dialog.setText(texts[0][i], self.screen.get_width() / 2 - self.screen.get_width() / 6 + 10,
                                           self.screen.get_height() / 2 - self.screen.get_height() / 16 + self.nodata.get_height() + 96 + 24 * i,
                                           24,
                                           (106, 176, 126), "left", font="Roboto-Light")
                self.screen.blit(text, pos)

    def draw_map(self):
        self.screen.blit(self.image_map, (0 + self.map_decale_x, 128 + self.map_decale_y))

    def draw_option(self):
        self.screen.blit(self.imagefontblur, (0, 0))
        for i in range(5):
            self.screen.blit(self.cardUnselectedoption,
                             (self.screen.get_width() / 2 - self.cardUnselectedoption.get_width() / 2,
                              self.screen.get_height() / 2 - self.screen.get_height() / 4 + (
                                      i * 64)))

    def check_action(self, click, keylistener):
        if click is not None:
            for k, v in self.buttons_options.items():
                if v.collidepoint(click):
                    if k == "quit":
                        pygame.quit()
                        sys.exit()
                    elif k == "save":
                        self.selected = "save"
                    elif k == "inventory":
                        self.selected = "inventory"
                    elif k == "map":
                        self.selected = "menu"
                    elif k == "pokemon":
                        self.selected = "pokemon"
                    elif k == "option":
                        self.selected = "option"
                    elif k == "pokedex":
                        self.selected = "pokedex"
        if keylistener and self.selected == "save" and pygame.K_c in keylistener.get():
            self.save = True

    def run(self, click, keylistener, map=None):
        self.draw_pause(map)
        self.check_action(click, keylistener)
        if self.selected == "menu":
            if pygame.mouse.get_pressed()[0]:
                if self.pos_mouse_before is not None:
                    if self.pos_mouse_before != pygame.mouse.get_pos():
                        if pygame.mouse.get_pos()[0] - self.pos_mouse_before[
                            0] + self.map_decale_x + self.image_map.get_width() > self.screen.get_width() and \
                                pygame.mouse.get_pos()[0] - self.pos_mouse_before[0] + self.map_decale_x < 0:
                            self.map_decale_x += pygame.mouse.get_pos()[0] - self.pos_mouse_before[0]
                        if pygame.mouse.get_pos()[1] - self.pos_mouse_before[
                            1] + self.map_decale_y + self.image_map.get_height() > self.screen.get_height() - 256 and \
                                pygame.mouse.get_pos()[1] - self.pos_mouse_before[1] + self.map_decale_y < 0:
                            self.map_decale_y += pygame.mouse.get_pos()[1] - self.pos_mouse_before[1]
            self.pos_mouse_before = pygame.mouse.get_pos()
