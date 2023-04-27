import json
import random
import datetime
import math

from move import Move


class Pokemon:
    def __init__(self, data, level, poke_base=None):
        self.klass = data['klass']
        self.id = data['id']
        self.dbSymbol = data['dbSymbol']
        self.forms = data['forms']
        self.evolutions = self.forms[0]['evolutions']
        self.type = self.get_types()
        self.baseHp = self.forms[0]['baseHp']
        self.baseAtk = self.forms[0]['baseAtk']
        self.baseDfe = self.forms[0]['baseDfe']
        self.baseSpd = self.forms[0]['baseSpd']
        self.baseAts = self.forms[0]['baseAts']
        self.baseDfs = self.forms[0]['baseDfs']
        self.evHp = self.forms[0]['evHp']
        self.evAtk = self.forms[0]['evAtk']
        self.evDfe = self.forms[0]['evDfe']
        self.evSpd = self.forms[0]['evSpd']
        self.evAts = self.forms[0]['evAts']
        self.evDfs = self.forms[0]['evDfs']
        self.experienceType = self.forms[0]['experienceType']
        self.baseExperience = self.forms[0]['baseExperience']
        self.baseLoyalty = self.forms[0]['baseLoyalty']
        self.catchRate = self.forms[0]['catchRate']
        self.femaleRate = self.forms[0]['femaleRate']
        self.breedGroups = self.forms[0]['breedGroups']
        self.hatchSteps = self.forms[0]['hatchSteps']
        self.babyDbSymbol = self.forms[0]['babyDbSymbol']
        self.babyForm = self.forms[0]['babyForm']
        self.itemHeld = self.forms[0]['itemHeld']
        self.abilities = self.forms[0]['abilities']
        self.frontOffsetY = self.forms[0]['frontOffsetY']
        self.resources = self.forms[0]['resources']
        self.moveSet = self.forms[0]['moveSet']
        self.level = level
        if poke_base:
            self.gender = poke_base.gender
            self.ivs = poke_base.ivs
            self.basestats = poke_base.basestats
            self.maxhp = poke_base.maxhp
            self.hp = poke_base.hp
            self.att = poke_base.att
            self.def_ = poke_base.def_
            self.attspe = poke_base.attspe
            self.defspe = poke_base.defspe
            self.vit = poke_base.vit
            self.fightsstas = poke_base.fightsstas
            self.moves = poke_base.moves
            self.shiny = poke_base.shiny
            self.xp = poke_base.xp
            self.points_ev = poke_base.points_ev

        else:
            self.gender = "female" if random.randint(1, 100) <= self.femaleRate else "male"
            if self.femaleRate == -1:
                self.gender = "genderless"
            self.ivs = {key: random.randint(0, 31) for key in self.get_base_stats().keys()}
            self.basestats = self.get_base_stats()

            self.maxhp = self.update_stats("hp")

            self.hp = self.update_stats("hp")
            self.att = self.basestats['atk']
            self.def_ = self.basestats['dfe']
            self.attspe = self.basestats['ats']
            self.defspe = self.basestats['dfs']
            self.vit = self.basestats['spd']

            self.fightsstas = self.set_battle_stats()
            self.moves: list[Move] = self.setmoves()
            self.shiny = "shiny" if random.randint(1, 10) == 1 else ""
            self.xp = 0
            self.points_ev = 0

        self.status = ""

        self.xp_to_next_level = self.get_xp_to_next_level()

        self.evolution = None

    def get_xp_to_next_level(self):
        if self.level == 100:
            return 0
        if self.experienceType == 1:  # Medium Fast
            return math.floor((4 * (self.level ** 3)) / 5)
        elif self.experienceType == 3:  # Medium Slow
            return math.floor(((6 / 5) * (self.level ** 3)) - (15 * (self.level ** 2)) + (100 * self.level) - 140)
        elif self.experienceType == 0:  # Fast
            return self.level ** 3
        elif self.experienceType == 2:  # Slow
            return 5 * (self.level ** 3) / 4
        elif self.experienceType == 4:  # Erratic
            if self.level <= 50:
                return math.floor((self.level ** 3) * (100 - self.level) / 50)
            elif self.level <= 68:
                return math.floor((self.level ** 3) * (150 - self.level) / 100)
            elif self.level <= 98:
                return math.floor((self.level ** 3) * math.floor((1911 - 10 * self.level) / 3) / 500)
            elif self.level <= 100:
                return math.floor((self.level ** 3) * (160 - self.level) / 100)

    def set_battle_stats(self):
        return {
            "hp": self.hp,
            "atk": self.att,
            "dfe": self.def_,
            "spd": self.vit,
            "ats": self.attspe,
            "dfs": self.defspe,
            "acc": 100
        }

    def setmoves(self):
        list_move: list[dict] = []
        list_attack: list[Move] = []
        for move in self.moveSet:
            try:
                if move["level"] <= self.level:
                    list_move.append(move)
            except:
                pass
        l = 2
        if len(list_move) < l:
            l = len(list_move)
        max = 4
        if (len(list_move) < 4):
            max = len(list_move)
        for i in range(random.randint(l, max)):
            chosed = random.choice(list_move)
            list_move.remove(chosed)
            list_attack.append(Move(json.loads(open("../data/json/moves/" + chosed["move"] + ".json").read())))
        return list_attack

    def update_stats(self, stat):
        base_stat = self.get_base_stats()[stat]
        iv = self.ivs[stat]
        ev = self.get_ev()[stat]
        level = self.level
        nature = 1.0
        if stat == 'hp':
            return math.floor(((2 * base_stat + iv + math.floor(ev / 4)) * level / 100) + level + 10)
        else:
            return math.floor((((2 * base_stat + iv + math.floor(ev / 4)) * level / 100) + 5) * nature)

    def get_base_stats(self):
        return {
            "hp": self.forms[0]["baseHp"],
            "atk": self.forms[0]["baseAtk"],
            "dfe": self.forms[0]["baseDfe"],
            "spd": self.forms[0]["baseSpd"],
            "ats": self.forms[0]["baseAts"],
            "dfs": self.forms[0]["baseDfs"]
        }

    def get_ev(self):
        return {
            "hp": self.forms[0]["evHp"],
            "atk": self.forms[0]["evAtk"],
            "dfe": self.forms[0]["evDfe"],
            "spd": self.forms[0]["evSpd"],
            "ats": self.forms[0]["evAts"],
            "dfs": self.forms[0]["evDfs"]
        }

    def get_types(self):
        type1 = self.forms[0]["type1"]
        type2 = self.forms[0]["type2"]
        if type2 == "__undef__":
            return [type1]
        else:
            return [type1, type2]

    def get_evolution(self, level):
        for evolution in self.evolutions:
            for condition in evolution["conditions"]:
                if condition["type"] == "minLevel" and condition["value"] <= level:
                    return evolution["dbSymbol"]
        return None

    def level_up(self):
        self.level += 1
        self.xp_to_next_level = self.get_xp_to_next_level()
        self.maxhp = self.update_stats("hp")
        self.hp = self.maxhp
        self.att = self.update_stats("atk")
        self.def_ = self.update_stats("dfe")
        self.attspe = self.update_stats("ats")
        self.defspe = self.update_stats("dfs")
        self.vit = self.update_stats("spd")
        self.fightsstas = self.set_battle_stats()
        self.moves = self.setmoves()
        self.evolution = self.get_evolution(self.level)

    def damage(self, dmg):
        self.hp -= dmg


class PokePlayer(Pokemon):
    def __init__(self, data, level, datetime):
        super().__init__(data, level)
        self.capture_date = datetime.datetime.now().strftime("%d/%m/%Y")
