import pygame

from mixer import Mixer


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


def split_text(text, player="", length=120):
    # Séparer le texte en mots
    words = text.split()

    # Initialiser la liste des groupes de lignes
    line_groups = []

    # Initialiser le groupe de lignes courant
    current_line_group = []

    # Initialiser la ligne courante
    current_line = ""
    current_length = 0

    # Pour chaque mot...
    for word in words:
        # Si le mot est égal au caractère '£', ajouter la ligne courante au groupe de lignes courant et créer une nouvelle ligne
        if word == '£':
            current_line_group.append(current_line)
            current_line = ""
            current_length = 0
        # Si le mot est égal au caractère '§', ajouter le groupe de lignes courant à la liste des groupes de lignes et créer un nouveau groupe de lignes et une nouvelle ligne
        elif word == '§':
            current_line_group.append(current_line)
            line_groups.append(current_line_group)
            current_line_group = []
            current_line = ""
            current_length = 0
        # Si le mot est égal au caractère 'ù', remplacer le mot par le joueur
        elif word == 'ù':
            if current_length + len(player) + 1 <= length:
                current_line += player + " "
                current_length += len(player) + 1
            # Sinon, ajouter la ligne courante au groupe de lignes courant et créer une nouvelle ligne
            else:
                current_line_group.append(current_line)
                current_line = player + " "
                current_length = len(player)
        # Si le mot ne dépasse pas la limite de longueur de ligne, l'ajouter à la ligne courante
        elif current_length + len(word) + 1 <= length:
            current_line += word + " "
            current_length += len(word) + 1
        # Sinon, ajouter la ligne courante au groupe de lignes courant et créer une nouvelle ligne
        else:
            current_line_group.append(current_line)
            current_line = word + " "
            current_length = len(word)

        # Si le groupe de lignes courant contient 3 lignes, l'ajouter à la liste des groupes de lignes et créer un nouveau groupe de lignes
        # if len(current_line_group) == 3:
        #    line_groups.append(current_line_group)
        #    current_line_group = []

    # Ajouter la dernière ligne au groupe de lignes courant (si elle existe)
    if current_line:
        current_line_group.append(current_line)

    # Ajouter le dernier groupe de lignes à la liste des groupes de lignes (si il existe)
    if current_line_group:
        line_groups.append(current_line_group)

    return line_groups


class Dialog:
    def __init__(self, text: str = "", player_name=None, npc_name: str = None):
        self.texts = split_text(text, player_name) if text != "" else None
        self.npc_name = npc_name
        self.dialogue_box = pygame.image.load("../data/dialog/Dialog_Box.png").convert_alpha()
        self.box_npc_name = pygame.transform.scale_by(
            pygame.image.load("../data/dialog/name_speaker.png").convert_alpha(), 2)
        self.font = pygame.font.Font("../data/dialog/Roboto-Regular.ttf", 28)
        self.talking = True
        self.line_index = 0
        self.letter_index = {}
        self.text_index = 0
        self.player_name = player_name
        self.enddraw = False
        if self.texts:
            for i in range(len(self.texts[self.text_index])):
                self.letter_index[i] = 0

        self.surface = pygame.Surface((self.dialogue_box.get_width() / 1.2, 34))
        self.surface.fill((11, 56, 53))
        self.animationup_text_index = 0
        self.animationup_text_bool = False
        self.count_dt = 0

        self.mixer = Mixer(0.2)
        self.mixer.load_sound("button", "../data/sound/effects/button.mp3")

    def get_current_text(self):
        try:
            return self.texts[self.text_index][self.line_index]
        except:
            return self.texts[self.text_index][self.line_index - 1]

    def next_text(self):
        self.text_index += 1
        self.enddraw = False
        if self.text_index == len(self.texts):
            self.talking = False
            self.texts = None
        else:
            self.mixer.play_sound("button")
            self.letter_index = {}
            self.line_index = 0
            for i in range(len(self.texts[self.text_index])):
                self.letter_index[i] = 0

    def draw(self, screen, dt, draw_npc_name=True, height=0):
        if self.texts is not None:
            if height == 0:
                screen.blit(self.dialogue_box, (0, screen.get_height() - self.dialogue_box.get_height() - 16))
            if self.npc_name is not None and draw_npc_name:
                screen.blit(self.box_npc_name, (screen.get_width() - self.box_npc_name.get_width(),
                                                screen.get_height() - self.dialogue_box.get_height() - self.box_npc_name.get_height() - 32))
                text, pos = setText(self.npc_name, screen.get_width() - self.box_npc_name.get_width() / 2,
                                    screen.get_height() - self.dialogue_box.get_height() - 32 - self.box_npc_name.get_height() / 2,
                                    28, (247, 249, 249), "center")
                screen.blit(text, pos)
            text = {}
            for i in range(len(self.letter_index)):
                text[i] = self.font.render(self.texts[self.text_index][i][:self.letter_index[i]], True, (247, 249, 249))
            for i in range(len(text)):
                screen.blit(text[i], (
                    200,
                    screen.get_height() - self.dialogue_box.get_height() + 16 + i * 32 - self.animationup_text_index - height))
            if self.line_index == 3:
                try:
                    if self.texts[self.text_index][self.line_index] != "":
                        self.animationup_text_bool = True
                except:
                    pass
            if self.animationup_text_bool:
                self.animationup_text_index += 1
                if self.animationup_text_index == 32:
                    self.animationup_text_bool = False
                    self.animationup_text_index = 0
                    self.texts[self.text_index][0] = ""
                    for i in range(len(self.texts[self.text_index]) - 1):
                        self.texts[self.text_index][i] = self.texts[self.text_index][i + 1]
                    self.texts[self.text_index][len(self.texts[self.text_index]) - 1] = ""
                    self.line_index = 0
                    for i in range(len(self.letter_index) - 1):
                        self.letter_index[i] = self.letter_index[i + 1]
                    self.letter_index[len(self.letter_index) - 1] = 0
            try:
                if self.enddraw is False:
                    self.count_dt += dt
                    if self.letter_index[self.line_index] < len(self.texts[self.text_index][self.line_index]) and \
                            self.texts[self.text_index][self.line_index] != "":
                        if self.count_dt >= 1:
                            self.letter_index[self.line_index] += int(self.count_dt)
                            self.count_dt = 0
                    else:
                        self.count_dt = 0
                        self.line_index += 1
                        if self.line_index >= len(self.texts[self.text_index]):
                            self.enddraw = True
            except KeyError:
                self.enddraw = True
            if height == 0:
                screen.blit(self.surface, (200, screen.get_height() - self.dialogue_box.get_height() - 16))

    def update(self, screen):
        self.draw(screen, 1)
        if self.enddraw:
            self.next_text()
        return self.talking

    def split_text(self, text: str, player_name: str = None):
        return split_text(text, player_name)
