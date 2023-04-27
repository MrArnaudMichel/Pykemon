import json


class Pokedex:
    def __init__(self):
        with open('../data/json/regional.json') as f:
            pokedex_data = json.load(f)
        self.klass = pokedex_data["klass"]
        self.id = pokedex_data["id"]
        self.dbSymbol = pokedex_data["dbSymbol"]
        self.startId = pokedex_data["startId"]
        self.csv = pokedex_data["csv"]
        self.creatures = pokedex_data["creatures"]

        self.pokemon_seen = []
        self.pokemon_captured = []

    def add_pokemon_seen(self, pokemon):
        self.pokemon_seen.append(pokemon)

    def add_pokemon_captured(self, pokemon):
        self.pokemon_captured.append(pokemon.id)
        if pokemon not in self.pokemon_seen:
            self.add_pokemon_seen(pokemon.id)
