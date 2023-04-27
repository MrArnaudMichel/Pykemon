import time
import datetime
import pygame
import pickle

import dialog
from choice import Choice
from dialog import Dialog
from keylistener import KeyListener

def save_list(lst, fic):
    # Ouvrir le fichier en mode écriture binaire
    with open("../data/save/" + fic + ".pkl", "wb") as f:
        # Sérialiser la liste et l'écrire dans le fichier
        pickle.dump(lst, f)


def load_list(fic):
    # Ouvrir le fichier en mode lecture binaire
    if fic[-4:] != ".pkl":
        fic += ".pkl"
    with open("../data/save/" + fic, "rb") as f:
        # Charger la liste depuis le fichier et la retourner
        return pickle.load(f)

class Save:
    def __init__(self, screen: pygame.display):
        self.dialog = Dialog()
        self.screen = screen
        self.activate = False
        self.dialog = Dialog("Voulez-vous sauvegarder la partie ?")
        self.saved = True
        self.choice = Choice(self.screen)

    def run(self, keylistner: KeyListener, map, currentmap, player, settings, pokedex, dt):
        if self.dialog.talking is False:
            self.dialog.talking = True
        self.dialog.draw(self.screen, 1)
        self.choice.run()
        #if pygame.K_RETURN in keylistner.get() or pygame.K_SPACE in keylistner.get():
        if self.choice.choice == "Oui":
            self.save_info(map, currentmap, player, settings, pokedex)
            self.activate = False
            self.dialog.letter_i = 0
        elif self.choice.choice == "Non":
            self.activate = False
            self.dialog.letter_i = 0

    def save_info(self, map, currentmap, player, settings, pokedex):
        map_info = {"map": map, "currentmap": currentmap, "playerRect": player.rect, "playerDirection": player.direction}
        player_info = {"name": player.name, "pokedex": pokedex, "pokemon": player.pokemon , "timeplayed": player.timeplayed, "pokedollars": player.pokedollars, "badges": player.badges, "gender": player.gender}
        list_save = [player.name+"0", len(pokedex.pokemon_seen), currentmap, player.timeplayed, datetime.datetime.now().strftime("%d/%m/%Y"), player.pokedollars, player.badges, map_info, player_info, settings]
        save_list(list_save, list_save[0])
