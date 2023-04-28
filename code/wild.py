from sql import SQL
import pygame
import json
import random

class Wild:
    def __init__(self):
        self.map = map
        self.sql = SQL()

    def run(self, map: str, listzone: list[pygame.Rect]):
        try:
            realname = self.sql.select_where("map", "name", map)[0][0]
        except:
            return []
        listpoke = []
        try:
            total: int = 0
            tupleinfo = self.sql.select_where("pokezone", "zone", realname)[0]
        except:
            return listpoke
        for surface in listzone:
            total += int(surface.width / 16)
            total += int(surface.height / 16 - 1)
        total = int(total / 5)
        for i in range(total):
            listeproba = json.loads(tupleinfo[2], object_hook=list[int]).copy()
            proba = random.randint(0, len(listeproba) - 1)
            if random.randint(1, 100) < listeproba[proba]:
                poke = json.loads(tupleinfo[1])[proba]
                lvl = json.loads(tupleinfo[3], object_hook=list[int]).copy()
                listpoke.append((poke, random.randint(lvl[0], lvl[1])))
        return listpoke
