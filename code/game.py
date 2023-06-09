import copy
import datetime
import json
import os
import random
import sys

import pygame
import pyscroll
import pytmx

import save
from dialog import Dialog
from entity import Entity, Player, WildPoke, NPC
from home import Home
from introduction import Introduction
from item import Item
from keylistener import KeyListener
from mixer import Mixer
from night import Night
from pause import Pause
from pokedex import Pokedex
from save import Save
from smoke import Smoke
from sql import SQL
from wild import Wild
from pokemon import Pokemon


class Game:
    def __init__(self):
        self.group = None
        self.screen = pygame.display.set_mode((1920, 1080), flags=pygame.FULLSCREEN)
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.fps: int = 60
        self.running: bool = True
        self.dt: float = self.clock.tick(self.fps) / 1000

        self.keylistener: KeyListener = KeyListener()
        self.home: Home = Home(self.screen)
        self.player: Player | None = None
        self.introduction: Introduction | None = None
        self.mixer: Mixer = Mixer(0.2)
        self.sql: SQL = SQL()
        self.pause: Pause | None = None
        self.save: Save | None = Save(self.screen)
        self.pokedex: Pokedex | None = None
        self.dialog: Dialog | None = None
        self.night: Night | None = Night(self.screen)
        self.wild: Wild | None = Wild()
        self.home: Home | None = Home(self.screen)

        self.map_layer: pyscroll.orthographic.BufferedRenderer | None = None
        self.tmx_data: pytmx.pytmx.TiledMap | None = None
        self.map: str | None = None
        self.current_map: str | None = None
        self.click: None | tuple[int, int] = None

        self.smoke_list: list[(float, float)] | None = None
        self.switchs: dict | None = None
        self.collisions: list[pygame.Rect] | None = None
        self.smoke: list[(float, float)] | None = None
        self.swimcollision: list[pygame.Rect] | None = None
        self.objects: dict[str, pygame.Rect] | None = None
        self.wildzone: list[pygame.Rect] | None = None

        self.followEntity: Entity | None = None

        self.draw_word_image: bool = False
        self.word_image: pygame.Surface = pygame.image.load("../data/image/display/Word.png")

        self.drawgame: bool = True

        self.mixer.load_music("rosa_title", False)
        self.mixer.play_music(True)

    def setFollowEntity(self, entity: Entity = None):
        if entity is None:
            character_pass = str(self.player.pokemon[0].id)
            while len(character_pass) < 3:
                character_pass = "0" + character_pass
            character_pass += "_0"
            self.followEntity = Entity(self.player.rect.x, self.player.rect.y, character_pass)
            if self.map.split("_")[0] == "map":
                self.placefollowEntity()
        else:
            self.followEntity = entity

    def placefollowEntity(self):
        self.player.updateRect(True)
        self.followEntity.hitbox = self.player.hitbox.copy()
        self.followEntity.setRectbyHitbox()
        self.followEntity.updateRect(True)

    def set_adventure(self):
        if os.listdir("../data/save/"):
            saveinfo = save.load_list(os.listdir("../data/save/")[0])
            self.player = Player(saveinfo[7]["playerRect"].x, saveinfo[7]["playerRect"].y, saveinfo[8]["name"],
                                 saveinfo[8]["gender"])
            self.current_map = saveinfo[7]["currentmap"]
            self.map = saveinfo[7]["map"]
            self.player.pokemon = saveinfo[8]["pokemon"]
            self.player.pokedollars = saveinfo[8]["pokedollars"]
            self.player.timeplayed = saveinfo[8]["timeplayed"]
            self.player.badges = saveinfo[8]["badges"]
            self.player.direction = saveinfo[7]["playerDirection"]
            self.player.inventory = saveinfo[8]["inventory"]
            self.load_map(self.map, (saveinfo[7]["playerRect"].x, saveinfo[7]["playerRect"].y))
            self.pause = Pause(self.screen, self.player)
            self.pokedex = saveinfo[8]["pokedex"]
            self.mixer.load_music(self.sql.select_where("map", "name", self.current_map)[0][0], False)
            self.mixer.play_music(True)
            self.player.pokemon.append(self.setPoke("charizard", 5))
            self.setFollowEntity()
        else:
            self.introduction = Introduction(self.screen)
            self.mixer.load_music("Introduction", False)
            self.mixer.play_music(True)

    def load_map(self, filename: str, pos: tuple | int = None):
        self.player.step = 0
        self.player.animation_i = 0
        self.player.change_animation(self.player.direction, self.dt, self.player.allimg)
        if filename == "map":
            self.tmx_data = pytmx.util_pygame.load_pygame("../data/map/" + self.current_map + ".tmx")
        else:
            self.tmx_data = pytmx.util_pygame.load_pygame("../data/map/" + filename + ".tmx")
        map_data = pyscroll.data.TiledMapData(self.tmx_data)
        self.map_layer = pyscroll.BufferedRenderer(map_data, self.screen.get_size())

        if filename.split("_")[0] != "map":
            self.map_layer.zoom = 4.25
        else:
            self.map_layer.zoom = 3.75

        if pos == 0:
            spawn_point = self.tmx_data.get_object_by_name("spawn")
            self.player.rect.x = spawn_point.x
            self.player.rect.y = spawn_point.y
        elif pos:
            self.player.rect.x = pos[0]
            self.player.rect.y = pos[1]
        else:
            if copy.copy(filename).split("_")[0] == "map":
                if self.map.split("_")[0] == "poke-center":
                    spawn_point = self.tmx_data.get_object_by_name("poke-center")
                    self.mixer.load_music(self.sql.select_where("map", "name", self.current_map)[0][0], True)
                    self.mixer.play_music(True)
                elif self.map.split("_")[0] == "poke-shop":
                    spawn_point = self.tmx_data.get_object_by_name("poke-shop")
                    self.mixer.load_music(self.sql.select_where("map", "name", self.current_map)[0][0], True)
                    self.mixer.play_music(True)
                elif self.map.split("_")[0] == "map":
                    spawn_point = self.tmx_data.get_object_by_name("Enter_" + self.current_map.split("_")[1])
                    self.current_map = filename
                    self.mixer.load_music(self.sql.select_where("map", "name", self.current_map)[0][0], True)
                    self.mixer.play_music(True)
                else:
                    spawn_point = self.tmx_data.get_object_by_name("Enter_" + self.map)

            else:
                if self.map.split("_")[0] == "inter":
                    spawn_point = self.tmx_data.get_object_by_name("Enter_" + self.map)
                else:
                    spawn_point = self.tmx_data.get_object_by_name("Enter")
            self.player.rect.x = spawn_point.x
            self.player.rect.y = spawn_point.y
        self.player.updateRect(True)
        self.map = filename

        self.group: pyscroll.PyscrollGroup = pyscroll.PyscrollGroup(map_layer=self.map_layer,
                                                                    default_layer=5)

        self.group.add(self.player)
        self.player.updateRect(True)
        if self.followEntity and filename.split("_")[0] == "map":
            self.placefollowEntity()
            self.group.add(self.followEntity)
            self.group.change_layer(self.followEntity, 6)

        self.collisions = []
        self.smoke_list = []
        self.switchs = {}
        self.swimcollision = []
        self.objects = {}
        self.wildzone = []

        for obj in self.tmx_data.objects:
            if obj.type == 'collision':
                self.collisions.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            elif obj.type == 'smoke':
                self.smoke_list.append((obj.x, obj.y))
            elif obj.type == 'switch':
                self.switchs[obj.name] = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
            elif obj.type == 'swim':
                self.swimcollision.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            elif obj.type == 'pokeball':
                self.objects[obj.name] = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
            elif obj.type == 'wild_fight':
                self.wildzone.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            elif obj.type == 'npc':
                info = obj.name.split(" ")
                npc = NPC(obj.x, obj.y, info[0])
                self.group.add(npc)
                npc.quest = self.sql.select_where("interaction_npc", "id", info[1])[0][1]
                npc.dialogue = self.sql.select_where("interaction_npc", "id", info[1])[0][2]
                npc.realname = self.sql.select_where("interaction_npc", "id", info[1])[0][3]
                npc.updateRect(True)

        listepoke = self.wild.run(self.map, self.wildzone)
        if listepoke:
            for tuple in listepoke:
                nb = random.randint(0, len(self.wildzone) - 2)
                if self.wildzone[nb].width > 32 and self.wildzone[nb].height > 32:
                    x = random.randint(self.wildzone[nb].x, self.wildzone[nb].x + self.wildzone[nb].width - 16)
                    y = random.randint(self.wildzone[nb].y, self.wildzone[nb].y + self.wildzone[nb].height - 16) - 16
                else:
                    x = self.wildzone[nb].x
                    y = self.wildzone[nb].y - 16
                if not self.player.hitbox.colliderect(pygame.Rect(x, y, 32, 32)):
                    poke = self.setPoke(tuple[0], tuple[1], (x, y))
                    if poke.hitbox.collidelist(self.wildzone):
                        self.group.add(poke)

        self.smoke = Smoke(self.screen, self.smoke_list, self.map_layer.zoom)

    def setdialaog(self, text):
        self.dialog = Dialog(text)

    def setitem(self, name):
        item_line = self.sql.select_where("item", "name", name)[0]
        self.player.inventory.addItem(Item(item_line[1], item_line[2], item_line[4], item_line[3]))

    def setPoke(self, name: str, level: int, wildPoke: bool | tuple = False):
        if wildPoke:
            return WildPoke(wildPoke[0], wildPoke[1], json.loads(open(f"../data/json/pokemon/{name}.json").read()),
                            level, self.wildzone)
        else:
            return Pokemon(json.loads(open(f"../data/json/pokemon/{name}.json").read()), level)

    def followEntityUpdatePos(self):
        if self.followEntity is not None:
            self.followEntity.step = 0
            self.followEntity.rect.x, self.followEntity.rect.y = copy.copy(
                self.player.rect.x) - self.followEntity.rect.width / 2 + self.player.rect.width / 2, self.player.rect.y + 16
            self.followEntity.updateRect(True)

    def interact(self):
        for object, rect in self.objects.items():
            if self.player.hitbox.colliderect(rect):
                self.setdialaog("Vous avez obtenu une " + object + " !")
                # layer: pytmx.pytmx.TiledTileLayer = self.tmx_data.get_layer_by_name("object")
                # for objects in layer:
                #    if objects.name == object:
                #        layer.remove_object(objects)
                self.setitem(object)
                if "find_item" in self.mixer.sounds:
                    self.mixer.sounds["find_item"].play()
                else:
                    self.mixer.load_sound("find_item", "../data/sound/effects/find_item.ogg")
                    self.mixer.sounds["find_item"].play()
                return
        npc = self.check_npc()
        if npc:
            self.dialog = Dialog(self.sql.select_where("dialog", "id", npc.dialogue)[0][1], self.player.name, npc.realname)

    def check_npc(self):
        for npc in self.group.sprites():
            if npc.type == "npc":
                rect = self.player.hitbox.copy()
                if self.player.direction == "up":
                    rect.y -= 16
                elif self.player.direction == "down":
                    rect.y += 16
                elif self.player.direction == "left":
                    rect.x -= 16
                elif self.player.direction == "right":
                    rect.x += 16
                if rect.colliderect(npc.hitbox):
                    return npc

    def update(self):
        group = self.player.movefromkeylistener(self.keylistener, self.collisions, self.swimcollision, self.dt,
                                                self.followEntity)
        if self.followEntity in self.group.sprites():
            if group is True and self.followEntity.layer == 5:
                self.group.change_layer(self.followEntity, 6)
            elif group is False and self.followEntity.layer == 6:
                self.group.change_layer(self.followEntity, 5)
            if self.player.swim is True and self.player.anim_swim_bool is False:
                self.group.remove(self.followEntity)
        else:
            if self.player.swim is False and self.player.anim_swim_bool is False and self.map.split("_")[
                0] == "map" and self.followEntity is not None:
                self.placefollowEntity()
                self.group.add(self.followEntity)

        self.group.update(self.dt)
        for sprite in self.group.sprites():
            if sprite == self.player:
                for key, value in self.switchs.items():
                    if sprite.hitbox.colliderect(value):
                        self.load_map(key)
                        break

    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.drawgame = not self.drawgame
                    self.pause.update_font()
                elif event.key == pygame.KSCAN_APOSTROPHE and self.introduction is None:
                    self.draw_word_image = not self.draw_word_image
                elif event.key == pygame.K_e and self.introduction is None and (
                        self.dialog is None or self.dialog.talking is False):
                    self.interact()
                elif event.key == pygame.K_SPACE and self.introduction is None and self.dialog is not None and self.dialog.enddraw is True:
                    if self.dialog.talking is True:
                        self.dialog.next_text()
                else:
                    self.keylistener.addkey(event.key)
            if event.type == pygame.KEYUP:
                if event.key in self.keylistener.get():
                    self.keylistener.removekey(event.key)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.click = pygame.mouse.get_pos()

    def run(self):
        while self.running:
            self.clock.tick(60)
            if self.player:
                self.player.timeplayed += datetime.timedelta(seconds=self.dt)
            self.event()
            if not self.home.activate:
                if self.drawgame:
                    if self.introduction is None:
                        self.update()
                        self.group.center(self.player.rect.center)
                        self.group.draw(self.screen)
                        if self.smoke:
                            self.smoke.draw(self.map_layer.get_center_offset())
                        self.night.run()
                    else:
                        self.introduction.draw(self.keylistener)
                        if self.introduction.active is False:
                            self.player = Player(-4, 256, self.introduction.name_pseudo,
                                                 self.introduction.gender_choice.lower())
                            self.current_map = "map_0"
                            self.map = "inter_0"
                            self.load_map("inter_0", 0)
                            self.mixer.load_music(self.sql.select_where("map", "name", self.current_map)[0][0], True)
                            self.mixer.play_music(True)
                            self.introduction = None
                            self.pause = Pause(self.screen, self.player)
                            self.pokedex = Pokedex()
                else:
                    self.pause.run(self.click, self.keylistener, self.current_map)
                    if self.pause.save:
                        self.save.activate = True
                        self.save.run(self.keylistener, self.map, self.current_map, self.player, [], self.pokedex,
                                      self.dt)
                        if self.save.activate is False:
                            self.pause.list_info = save.load_list(self.player.name + "'s Save")
                            self.pause.save = False
                            self.save.choice.choice = None
            else:
                self.home.run()
                if self.home.activate is False:
                    self.set_adventure()

            # pygame.draw.rect(self.screen, (255, 0, 0), ((self.player.hitbox.x + self.map_layer.get_center_offset()[0]) * self.map_layer.zoom,
            #                                           (self.player.hitbox.y + self.map_layer.get_center_offset()[1]) * self.map_layer.zoom,
            #                                           self.player.hitbox.width * self.map_layer.zoom,
            #                                           self.player.hitbox.height * self.map_layer.zoom))
            if self.dialog and self.dialog.talking:
                self.dialog.draw(self.screen, 1, True)
            self.click = None
            if self.draw_word_image:
                self.screen.blit(self.word_image, (0, 0))
            pygame.display.flip()
