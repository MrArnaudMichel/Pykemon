import pygame
import time

from dialog import Dialog
from sql import SQL
from keylistener import KeyListener
from choice import Choice


def setText(caracChain, x, y, size=25, color=(255, 255, 255), center="center", bold=False, font="Roboto-Regular"):
    font = pygame.font.Font("../data/dialog/" + font + ".ttf", size)
    if bold == True:
        font.set_bold(True)
    text = font.render(caracChain, True, color)
    textRect = text.get_rect()
    if center == "center":
        textRect.center = (x, y)
    elif center == "left":
        textRect.midleft = (x, y)
    elif center == "right":
        textRect.midright = (x, y)
    return text, textRect


class Introduction:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.surface = pygame.Surface((1920, 1080))
        self.surface.fill((0, 32, 38))
        self.sql = SQL()
        self.dialog = Dialog(self.sql.select_where("dialog", "id", 0)[0][1], player_name="Arnaud",
                             npc_name="Professeur")
        self.timecooldown = time.time()
        self.active = True
        self.sprite_boy = pygame.transform.scale_by(pygame.image.load("../data/image/settings/lucas.png"), 0.35)
        self.sprite_boy.set_alpha(128)
        self.sprite_girl = pygame.transform.scale_by(pygame.image.load("../data/image/settings/dawn.png"), 0.40)
        self.sprite_girl.set_alpha(128)
        self.gender_choice = None
        self.choice = Choice(self.screen, "Lucas", "Aurore")

        self.sprite_full = None
        self.x_sprite = 0

        self.box_name = pygame.image.load("../data/image/settings/box_name.png")
        self.draw_dialog = True

        self.name_pseudo = None
        self.name_pseudo_index = 0
        self.name_pseudo_cooldown = None

        self.nuzlocke = False

    def draw(self, keylistener):
        self.screen.blit(self.surface, (0, 0))
        if self.dialog.text_index == 0:
            self.draw_sprite_gender()
            if not self.dialog.enddraw and not time.time() - self.timecooldown > 0.5:
                self.choice.draw()
            else:
                self.choice.run()
            if self.dialog.enddraw and time.time() - self.timecooldown > 0.5 and self.choice.choice is not None:
                self.gender_choice = self.choice.choice
                self.dialog.texts = self.dialog.split_text(self.sql.select_where("dialog", "id", 0)[0][1],
                                                           self.gender_choice)
                self.dialog.next_text()
                self.choice = Choice(self.screen)
                self.timecooldown = time.time()
        elif self.dialog.text_index == 1:
            if self.gender_choice.lower() == "lucas":
                if self.sprite_boy.get_alpha() < 255:
                    self.sprite_boy.set_alpha(self.sprite_boy.get_alpha() + 3)
                    if self.sprite_boy.get_alpha() + 3 > 255:
                        self.sprite_boy.set_alpha(255)
            else:
                if self.sprite_girl.get_alpha() < 255:
                    self.sprite_girl.set_alpha(self.sprite_girl.get_alpha() + 3)
                    if self.sprite_girl.get_alpha() + 3 > 255:
                        self.sprite_girl.set_alpha(255)
            if not self.dialog.enddraw and not time.time() - self.timecooldown > 0.5:
                self.choice.draw()
            else:
                self.choice.run()
            if self.choice.choice is not None:
                if self.choice.choice.lower() == "oui":
                    self.dialog.next_text()
                    if self.gender_choice.lower() == "lucas":
                        self.sprite_full = pygame.transform.scale_by(
                            pygame.image.load(f"../data/image/settings/lucas.png"), 0.7)
                        self.x_sprite = 192
                        self.name_pseudo = "Lucas" + "_" * 6
                        self.name_pseudo_index = 5
                    else:
                        self.sprite_full = pygame.transform.scale_by(
                            pygame.image.load(f"../data/image/settings/dawn.png"), 0.75)
                        self.x_sprite = -256
                        self.name_pseudo = "Aurore" + "_" * 6
                        self.name_pseudo_index = 6
                else:
                    self.choice = Choice(self.screen, "Lucas", "Aurore")
                    self.sprite_girl.set_alpha(128)
                    self.sprite_boy.set_alpha(128)
                    self.dialog.text_index = -1
                    self.dialog.next_text()
                self.timecooldown = time.time()
                self.choice.choice = None
            self.draw_sprite_gender()
        elif self.dialog.text_index == 3:
            if self.draw_dialog is True:
                self.draw_dialog = False
                self.name_pseudo_cooldown = time.time()
            self.screen.blit(self.sprite_full,
                             (self.screen.get_width() / 2 - self.sprite_full.get_width() / 2 + self.x_sprite,
                              self.screen.get_height() / 2 - self.sprite_full.get_height() / 2 + 300))
            self.screen.blit(self.box_name, (self.screen.get_width() / 2 - self.box_name.get_width() / 2,
                                             self.screen.get_height() / 2 - self.box_name.get_height() / 4))
            self.screen.blit(self.surface, (
            0, self.screen.get_height() / 2 - self.box_name.get_height() / 4 + self.box_name.get_height()))
            text, pos = setText("Quel est votre nom ?", int(self.screen.get_width() / 2),
                                self.screen.get_height() / 2 - self.box_name.get_height() / 4 + 64, 28, (106, 176, 126),
                                center="center", font="Roboto-Light")
            self.screen.blit(text, pos)
            rect_box_pseudo = pygame.Rect(self.screen.get_width() / 2 - self.box_name.get_width() / 2 + 192,
                                          self.screen.get_height() / 2 - self.box_name.get_height() / 4 + 128,
                                          self.box_name.get_width() - 384, 64)
            pygame.draw.rect(self.screen, (20, 87, 70), rect_box_pseudo, width=0, border_radius=8)

            for events in keylistener.get():
                if keylistener.key_pressed(pygame.K_BACKSPACE):
                    if self.name_pseudo_index > 0 and time.time() - self.name_pseudo_cooldown > 0.1:
                        self.name_pseudo_index -= 1
                        self.name_pseudo = self.name_pseudo[:self.name_pseudo_index] + "_" + self.name_pseudo[
                                                                                             self.name_pseudo_index + 1:]
                        self.name_pseudo_cooldown = time.time()
                elif keylistener.key_pressed(pygame.K_RETURN):
                    if self.name_pseudo_index > 0:
                        self.name_pseudo = self.name_pseudo[:self.name_pseudo_index].replace("_", "").strip()
                        self.dialog.texts = self.dialog.split_text(self.sql.select_where("dialog", "id", 0)[0][1],
                                                                   self.name_pseudo)
                        self.dialog.next_text()
                        self.timecooldown = time.time()
                        self.draw_dialog = True
                        self.choice = Choice(self.screen)
                elif keylistener.key_pressed(pygame.K_SPACE):
                    if self.name_pseudo_index < 12 and time.time() - self.name_pseudo_cooldown > 1:
                        self.name_pseudo = self.name_pseudo[:self.name_pseudo_index] + " " + self.name_pseudo[
                                                                                             self.name_pseudo_index + 1:]
                        self.name_pseudo_index += 1
                        self.name_pseudo_cooldown = time.time()
                elif keylistener.key_pressed(pygame.K_DELETE):
                    if self.name_pseudo_index < 12 and time.time() - self.name_pseudo_cooldown > 0.1:
                        self.name_pseudo = self.name_pseudo[:self.name_pseudo_index] + "_" + self.name_pseudo[
                                                                                             self.name_pseudo_index + 1:]
                        self.name_pseudo_cooldown = time.time()
                elif keylistener.key_pressed(pygame.K_RIGHT):
                    if self.name_pseudo_index < 12:
                        self.name_pseudo_index += 1
                elif keylistener.key_pressed(pygame.K_LEFT):
                    if self.name_pseudo_index > 0:
                        self.name_pseudo_index -= 1
                else:
                    if self.name_pseudo_index < 12:
                        try:
                            if time.time() - self.timecooldown > 0.15 or self.name_pseudo_index == 0 or \
                                    self.name_pseudo[self.name_pseudo_index - 1] == " ":
                                if keylistener.key_pressed(pygame.K_LSHIFT) or keylistener.key_pressed(pygame.K_RSHIFT):
                                    event = chr(events).upper()
                                else:
                                    event = chr(events).lower()
                                self.name_pseudo = self.name_pseudo[:self.name_pseudo_index] + event + self.name_pseudo[
                                                                                                       self.name_pseudo_index + 1:]
                                self.name_pseudo_index += 1
                                self.timecooldown = time.time()
                        except:
                            pass

            text, pos = setText(self.name_pseudo, int(self.screen.get_width() / 2),
                                self.screen.get_height() / 2 - self.box_name.get_height() / 4 + 160, 64,
                                (106, 176, 126), center="center", font="Roboto-Light")
            self.screen.blit(text, pos)

            text, pos = setText("Utiliser votre clavier pour écrire puis appuyer sur ",
                                int(self.screen.get_width() / 2),
                                self.screen.get_height() / 2 - self.box_name.get_height() / 4 + 256, 28,
                                (106, 176, 126), center="center", font="Roboto-Light")
            self.screen.blit(text, pos)

            text, pos = setText("Entrée pour valider", int(self.screen.get_width() / 2),
                                self.screen.get_height() / 2 - self.box_name.get_height() / 4 + 288, 28,
                                (106, 176, 126), center="center", font="Roboto-Light")
            self.screen.blit(text, pos)
        elif self.dialog.text_index == 4:
            if not self.dialog.enddraw:
                self.choice.draw()
            else:
                self.choice.run()
            if self.choice.choice is not None:
                if self.choice.choice == "Oui":
                    self.dialog.next_text()
                    self.choice = Choice(self.screen)
                    self.choice.active = False
                else:
                    self.dialog.text_index = self.dialog.text_index - 2
                    self.dialog.next_text()
                    self.name_pseudo = self.name_pseudo + (12 - len(self.name_pseudo)) * "_"
        elif self.dialog.text_index == 6:
            if self.choice.active is False:
                self.choice.active = True
            if not self.dialog.enddraw:
                self.choice.draw()
            else:
                self.choice.run()
            if self.choice.choice is not None:
                if self.choice.choice == "Oui":
                    self.nuzlocke = True
                else:
                    self.nuzlocke = False
                self.choice.active = False
                self.dialog.next_text()
        if self.draw_dialog:
            self.dialog.draw(self.screen, 1, draw_npc_name=False)
        if keylistener.key_pressed(
                pygame.K_SPACE) and self.dialog.enddraw and time.time() - self.timecooldown > 0.5 \
                and self.choice.active is False:
            self.dialog.next_text()
        if self.dialog.talking is False:
            self.active = False

    def draw_sprite_gender(self):
        self.screen.blit(self.sprite_girl, (self.screen.get_width() / 4 - self.sprite_girl.get_width() / 2,
                                            self.screen.get_height() - self.sprite_girl.get_height() - 64))
        self.screen.blit(self.sprite_boy, (
            self.screen.get_width() / 1.5, self.screen.get_height() - self.sprite_boy.get_height() - 64))
