import pygame


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


class Choice:
    def __init__(self, screen, choice1="Oui", choice2="Non"):
        self.screen = screen
        self.choice = None
        self.choice1 = choice1
        self.choice2 = choice2
        self.choice_box = pygame.transform.scale(pygame.image.load("../data/image/settings/box_name.png"), (128, 96))
        self.font = pygame.font.Font("../data/dialog/Roboto-Regular.ttf", 28)
        self.textchoice1 = self.font.render(self.choice1, True, (247, 249, 249))
        self.textchoice2 = self.font.render(self.choice2, True, (247, 249, 249))
        self.choice1_rect = pygame.Rect(self.screen.get_width() - self.choice_box.get_width() + 32,
                                        self.screen.get_height() - self.choice_box.get_height() - 180 - 80 - 32,
                                        self.textchoice1.get_width(), self.textchoice1.get_height())
        self.choice2_rect = pygame.Rect(self.screen.get_width() - self.choice_box.get_width() + 32,
                                        self.screen.get_height() - self.choice_box.get_height() - 180 - 48 - 32,
                                        self.textchoice2.get_width(), self.textchoice2.get_height())
        self.active = True

    def run(self):
        if pygame.mouse.get_pressed()[0]:
            if self.choice1_rect.collidepoint(pygame.mouse.get_pos()):
                self.choice = self.choice1
                self.active = False
            elif self.choice2_rect.collidepoint(pygame.mouse.get_pos()):
                self.choice = self.choice2
                self.active = False
        self.draw()

    def draw(self):
        self.screen.blit(self.choice_box, (self.screen.get_width() - self.choice_box.get_width(),
                                           self.screen.get_height() - self.choice_box.get_height() - 180 - 128))
        self.screen.blit(self.textchoice1, (self.screen.get_width() - self.choice_box.get_width() + 32,
                                            self.screen.get_height() - self.choice_box.get_height() - 180 - 112))
        self.screen.blit(self.textchoice2, (self.screen.get_width() - self.choice_box.get_width() + 32,
                                            self.screen.get_height() - self.choice_box.get_height() - 180 - 80))
        pygame.draw.rect(self.screen, (255, 255, 255), self.choice1_rect, 1)
        pygame.draw.rect(self.screen, (255, 255, 255), self.choice2_rect, 1)
