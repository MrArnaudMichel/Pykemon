import pygame


class Mixer:
    def __init__(self, volume):
        # Initialiser Pygame
        pygame.init()
        pygame.mixer.music.set_volume(volume)

        # Créer un dictionnaire pour stocker les sons chargés
        self.sounds = {}

        # Créer une variable pour stocker le nom de la musique en cours
        self.current_music = ""

    def set_volume(self, volume):
        pygame.mixer.music.set_volume(volume)

    def load_sound(self, name, file):
        # Charger un son et l'ajouter au dictionnaire des sons
        sound = pygame.mixer.Sound(file)
        self.sounds[name] = sound

    def play_sound(self, name, loop=False):
        # Récupérer le son du dictionnaire et le jouer
        sound = self.sounds[name]
        if loop:
            sound.play(-1)
        else:
            sound.play()

    def soundplay(self, name) -> bool:
        return self.sounds[name].get_num_channels() > 0

    def stop_sound(self, name):
        # Récupérer le son du dictionnaire et l'arrêter
        sound = self.sounds[name]
        sound.stop()

    def load_music(self, file, active=True):
        # Charger une musique
        if active:
            pygame.mixer.music.fadeout(500)
        pygame.mixer.music.load(f"../data/sound/music/{file}.mp3")

    def play_music(self, loop=False):
        # Jouer la musique en cours
        if loop:
            pygame.mixer.music.play(-1)
        else:
            pygame.mixer.music.play()

    def stop_music(self):
        # Arrêter la musique en cours
        pygame.mixer.music.stop()

    def change_music(self, file, loop=False):
        # Arrêter la musique en cours et charger une nouvelle musique
        self.stop_music()
        self.load_music(file)
        self.play_music(loop)
