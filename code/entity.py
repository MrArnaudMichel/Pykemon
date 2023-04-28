import pygame
import copy
import datetime
import time
import random

from keylistener import KeyListener
from mixer import Mixer
from inventory import Inventory
from pokemon import Pokemon


class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y, name, gender="characters"):
        super().__init__()
        self.change_rect = False
        self.name = name
        self.sprite = pygame.image.load(f"../data/sprite/{gender}/{name}.png")
        self.sprite_allimg = self.change_image(self.sprite)
        self.allimg = self.sprite_allimg
        self.image = self.allimg["down"][0]
        self.rect = self.image.get_rect()
        self.position = [float(x), float(y)]
        self.type = None
        self.rect.x = x
        self.rect.y = y

        self.swim = False

        self.speed = 1
        self.speed_anim = 8
        self.animation_i = 0
        self.step = 0

        self.hitbox = pygame.Rect(0, 0, 16, 16)
        self.lastposition = self.rect.copy()
        self.direction = "down"

        self.water_sprite_sheet = pygame.image.load("../data/sprite/lochlass.png").convert_alpha()
        self.lochlass_allimg = self.change_image(self.water_sprite_sheet)

        self.anim_swim_bool = False
        self.move_auto = True

        self.updateinstante = False
        self.hitbox_bump = pygame.Rect(0, 0, 16, 16)

    def change_image(self, sprite: pygame.Surface):
        return {
            "down": [sprite.subsurface(0, 0, sprite.get_width() / 4, sprite.get_height() / 4),
                     sprite.subsurface(sprite.get_width() / 4, 0, sprite.get_width() / 4,
                                       sprite.get_height() / 4),
                     sprite.subsurface(sprite.get_width() / 2, 0, sprite.get_width() / 4,
                                       sprite.get_height() / 4),
                     sprite.subsurface(int(sprite.get_width() / 1.33), 0, sprite.get_width() / 4,
                                       sprite.get_height() / 4)],
            "left": [sprite.subsurface(0, sprite.get_height() / 4, sprite.get_width() / 4,
                                       sprite.get_height() / 4),
                     sprite.subsurface(sprite.get_width() / 4, sprite.get_height() / 4,
                                       sprite.get_width() / 4, sprite.get_height() / 4),
                     sprite.subsurface(sprite.get_width() / 2, sprite.get_height() / 4,
                                       sprite.get_width() / 4, sprite.get_height() / 4),
                     sprite.subsurface(int(sprite.get_width() / 1.33), sprite.get_height() / 4,
                                       sprite.get_width() / 4, sprite.get_height() / 4)],
            "right": [sprite.subsurface(0, int(sprite.get_height() / 2), sprite.get_width() / 4,
                                        sprite.get_height() / 4),
                      sprite.subsurface(sprite.get_width() / 4, int(sprite.get_height() / 2),
                                        sprite.get_width() / 4, sprite.get_height() / 4),
                      sprite.subsurface(sprite.get_width() / 2, int(sprite.get_height() / 2),
                                        sprite.get_width() / 4, sprite.get_height() / 4),
                      sprite.subsurface(int(sprite.get_width() / 1.33), int(sprite.get_height() / 2),
                                        sprite.get_width() / 4, sprite.get_height() / 4)],
            "up": [sprite.subsurface(0, int(sprite.get_height() / 1.33), sprite.get_width() / 4,
                                     sprite.get_height() / 4),
                   sprite.subsurface(sprite.get_width() / 4, int(sprite.get_height() / 1.33),
                                     sprite.get_width() / 4, sprite.get_height() / 4),
                   sprite.subsurface(sprite.get_width() / 2, int(sprite.get_height() / 1.33),
                                     sprite.get_width() / 4, sprite.get_height() / 4),
                   sprite.subsurface(int(sprite.get_width() / 1.33), int(sprite.get_height() / 1.33),
                                     sprite.get_width() / 4, sprite.get_height() / 4)]
        }

    def change_animation(self, direction, dt, img, respawn=False):
        if respawn:
            self.animation_i = 0
            self.image = img["down"][self.animation_i]
        else:
            self.direction = direction
            self.animation_i += self.speed_anim * dt
            if self.animation_i >= len(img[direction]):
                self.animation_i = 0
            self.image = img[direction][int(self.animation_i)]

    def check_collision(self, rect: pygame.Rect, collisions: list[pygame.Rect]):
        for collision in collisions:
            if rect.colliderect(collision):
                return True
        return False

    def move(self, direction, collisions: list[pygame.Rect], dt):
        if self.move_auto:
            if direction == "up":
                if self.step == 0:
                    copyrect = copy.copy(self.hitbox)
                    copyrect.y -= 16
                    if self.check_collision(copyrect, collisions):
                        self.step = 0
                        self.animation_i = 0
                        self.change_animation(direction, dt, self.allimg)
                        return False
                self.rect.y -= self.speed
                self.check_step()
            elif direction == "down":
                if self.step == 0:
                    copyrect = copy.copy(self.hitbox)
                    copyrect.y += 16
                    if self.check_collision(copyrect, collisions):
                        self.step = 0
                        self.animation_i = 0
                        self.change_animation(direction, dt, self.allimg)
                        return False
                self.rect.y += self.speed
                self.anim_swim()
                self.check_step()
            elif direction == "left":
                if self.step == 0:
                    copyrect = copy.copy(self.hitbox)
                    copyrect.x -= 16
                    if self.check_collision(copyrect, collisions):
                        self.step = 0
                        self.animation_i = 0
                        self.change_animation(direction, dt, self.allimg)
                        return False
                self.rect.x -= self.speed
                self.check_step()
            elif direction == "right":
                if self.step == 0:
                    copyrect = copy.copy(self.hitbox)
                    copyrect.x += 16
                    if self.check_collision(copyrect, collisions):
                        self.step = 0
                        self.animation_i = 0
                        self.change_animation(direction, dt, self.allimg)
                        return False
                self.rect.x += self.speed
                self.check_step()
            # if self.type == "player":
            self.change_animation(direction, dt, self.allimg)
            return True

    def check_step(self):
        self.anim_swim()
        self.step += 1
        if self.step >= 16 and self.anim_swim_bool is False:
            self.step = 0
        if self.anim_swim_bool:
            if self.swim is False:
                if self.step == 16:
                    self.allimg = self.sprite_allimg
                    self.rect.x += 4
                    self.change_rect = True

            if self.step >= 32:
                self.step = 0
                self.anim_swim_bool = False

    def anim_swim(self):
        if self.swim is True and self.allimg == self.sprite_allimg and self.step == 8:
            self.allimg = self.lochlass_allimg
            self.rect.x -= 4
            self.change_rect = True
            self.anim_swim_bool = True

    def update(self, dt):
        if self.change_rect and self.anim_swim_bool is False:
            self.rect.width, self.rect.height = self.allimg["down"][0].get_size()
        if self.step != 0:
            self.move(self.direction, [], dt)
        else:
            if self.step == 0 and self.anim_swim_bool is False:
                self.updateRect()
        self.hitbox.midbottom = self.rect.midbottom
        if self.anim_swim_bool and self.step == 0:
            self.anim_swim_bool = False
        if self.swim:
            pass
        self.lastposition = self.rect.copy()
        if self.type != "player":
            if self.step == 0:
                self.change_animation(self.direction, dt, self.allimg)

    def updateRect(self, instante=False):
        self.hitbox.midbottom = self.rect.midbottom
        if self.hitbox.x % 16 != 0 and self.anim_swim_bool is False:
            if self.updateinstante or instante:
                if self.hitbox.x % 16 > 8:
                    self.rect.x = self.rect.x + self.hitbox.x % 16
                else:
                    self.rect.x = self.rect.x - self.hitbox.x % 16
            else:
                self.move_auto = False
                if self.hitbox.x % 16 > 8:
                    self.rect.x = self.rect.x + 1
                else:
                    self.rect.x = self.rect.x - 1
        elif self.hitbox.y % 16 != 0 and self.anim_swim_bool is False:
            if self.updateinstante or instante:
                if self.hitbox.y % 16 > 8:
                    self.rect.y = self.rect.y + self.hitbox.y % 16
                else:
                    self.rect.y = self.rect.y - self.hitbox.y % 16
            else:
                self.move_auto = False
                if self.hitbox.y % 16 > 8:
                    self.rect.y = self.rect.y + 1
                else:
                    self.rect.y = self.rect.y - 1
        else:
            self.move_auto = True
            self.updateinstante = False


class Player(Entity):
    def __init__(self, x, y, name, gender):
        super().__init__(x, y, gender + "_walk", gender)
        self.name = name
        self.gender = gender
        self.mixer = Mixer(0.2)
        self.mixer.load_sound("bump", "../data/sound/effects/bump.mp3")
        self.timeplayed = datetime.timedelta()
        self.type = "player"
        self.pokemon = []
        self.pokedollars = 0
        self.inventory: Inventory = Inventory()
        self.badges = []

    def movefromkeylistener(self, keylistener: KeyListener, collisions: list[pygame.Rect],
                            swimcollision: list[pygame.Rect], dt, followentity):
        grouphigh = None
        if self.step == 0 and self.anim_swim_bool is False:
            if keylistener.key_pressed(pygame.K_z):
                self.direction = "up"
                rect = copy.copy(self.hitbox)
                rect.y -= 32
                self.checkswimcollision(rect, swimcollision, collisions)
                if self.move("up", collisions, dt) and followentity is not None:
                    grouphigh = self.movefollowentity("up", followentity, collisions, dt)
                else:
                    self.checkbump()
            elif keylistener.key_pressed(pygame.K_s):
                self.direction = "down"
                rect = copy.copy(self.hitbox)
                rect.y += 32
                self.checkswimcollision(rect, swimcollision, collisions)
                if self.move("down", collisions, dt) and followentity is not None:
                    grouphigh = self.movefollowentity("down", followentity, collisions, dt)
                else:
                    self.checkbump()
            elif keylistener.key_pressed(pygame.K_q):
                self.direction = "left"
                rect = copy.copy(self.hitbox)
                rect.x -= 32
                self.checkswimcollision(rect, swimcollision, collisions)
                if self.move("left", collisions, dt) and followentity is not None:
                    grouphigh = self.movefollowentity("left", followentity, collisions, dt)
                else:
                    self.checkbump()
            elif keylistener.key_pressed(pygame.K_d):
                self.direction = "right"
                rect = copy.copy(self.hitbox)
                rect.x += 32
                self.checkswimcollision(rect, swimcollision, collisions)
                if self.move("right", collisions, dt) and followentity is not None:
                    grouphigh = self.movefollowentity("right", followentity, collisions, dt)
                else:
                    self.checkbump()
            if len(keylistener.get()) == 0:
                if self.animation_i >= 4:
                    self.animation_i = 0
                    self.change_animation(self.direction, dt, self.allimg)
        return grouphigh

    def checkbump(self):
        if self.mixer.soundplay("bump") is False and self.hitbox_bump != self.hitbox:
            self.mixer.play_sound("bump")
            self.hitbox_bump = self.hitbox.copy()

    def checkswimcollision(self, rect, swimcollision, collisions):
        if self.swim is False:
            for collision in swimcollision:
                if rect.colliderect(collision):
                    for collision in collisions:
                        if rect.colliderect(collision):
                            return False
                    self.swim = True
                    return True
        else:
            for collision in swimcollision:
                if rect.colliderect(collision):
                    return False
            fakerect = copy.copy(rect)
            if self.direction == "up":
                fakerect.y += 16
            elif self.direction == "down":
                fakerect.y -= 16
            elif self.direction == "left":
                fakerect.x += 16
            elif self.direction == "right":
                fakerect.x -= 16
            if fakerect.collidelist(collisions) > -1:
                return False
            for swimcollision in swimcollision:
                if fakerect.colliderect(swimcollision):
                    return
            self.swim = False
            self.anim_swim_bool = True

            return False
        return False

    def movefollowentity(self, direction, followentity, collisions: list[pygame.Rect], dt):
        grouphigher = False
        if direction == "up":
            if followentity.hitbox.x < self.hitbox.x:
                followentity.move("right", collisions, dt)
            elif followentity.hitbox.x > self.hitbox.x:
                followentity.move("left", collisions, dt)
            elif followentity.hitbox.y < self.hitbox.y:
                followentity.move("down", collisions, dt)
            elif followentity.hitbox.y > self.hitbox.y:
                followentity.move("up", collisions, dt)
            grouphigher = True
        elif direction == "down":
            if followentity.hitbox.x < self.hitbox.x:
                followentity.move("right", collisions, dt)
            elif followentity.hitbox.x > self.hitbox.x:
                followentity.move("left", collisions, dt)
            elif followentity.hitbox.y < self.hitbox.y:
                followentity.move("down", collisions, dt)
            elif followentity.hitbox.y > self.hitbox.y:
                followentity.move("up", collisions, dt)
        elif direction == "left":
            if followentity.hitbox.y < self.hitbox.y:
                followentity.move("down", collisions, dt)
            elif followentity.hitbox.y > self.hitbox.y:
                followentity.move("up", collisions, dt)
            elif followentity.hitbox.x < self.hitbox.x:
                followentity.move("right", collisions, dt)
            elif followentity.hitbox.x > self.hitbox.x:
                followentity.move("left", collisions, dt)
        elif direction == "right":
            if followentity.hitbox.y < self.hitbox.y:
                followentity.move("down", collisions, dt)
            elif followentity.hitbox.y > self.hitbox.y:
                followentity.move("up", collisions, dt)
            elif followentity.hitbox.x < self.hitbox.x:
                followentity.move("right", collisions, dt)
            elif followentity.hitbox.x > self.hitbox.x:
                followentity.move("left", collisions, dt)
        return grouphigher

class NPC(Entity):
    def __init__(self, x, y, name):
        super().__init__(x, y, name)

class WildPoke(Pokemon, Entity):
    def __init__(self, x, y, data, level: int, area: list[pygame.Rect]):
        Pokemon.__init__(self, data, level)
        gender = self.gender
        self.grp = None
        if self.shiny:
            name = str(self.resources["characterShiny"])
        else:
            name = str(self.resources["character"])
        Entity.__init__(self, x, y, name)
        self.area = area
        self.gender = gender
        self.choice = ["up", "down", "left", "right"]
        self.direction = random.choice(self.choice)
        self.time = time.time()
        self.cooldown = random.randint(1, 3)
        self.updateRect(True)

    def update(self, dt):
        super().update(dt)
        if time.time() - self.time > self.cooldown:
            self.time = time.time()
            self.cooldown = random.randint(1, 3)
            self.direction = random.choice(self.choice)
            if self.direction == "up":
                rect = copy.copy(self.hitbox)
                rect.y -= 16
                if rect.collidelist(self.area) >= 0:
                    self.move("up", [], dt)
            elif self.direction == "down":
                rect = copy.copy(self.hitbox)
                rect.y += 16
                if rect.collidelist(self.area) >= 0:
                    self.move("down", [], dt)
            elif self.direction == "left":
                rect = copy.copy(self.hitbox)
                rect.x -= 16
                if rect.collidelist(self.area) >= 0:
                    self.move("left", [], dt)
            elif self.direction == "right":
                rect = copy.copy(self.hitbox)
                rect.x += 16
                if rect.collidelist(self.area) >= 0:
                    self.move("right", [], dt)

