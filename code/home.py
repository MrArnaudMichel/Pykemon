import pygame


class Home:
    def __init__(self, screen: pygame.display):
        self.screen = screen
        self.activate = True
        self.imageshome = [pygame.transform.scale_by(pygame.image.load(f"../data/image/home/homeimg/home{i}.png"), 1).convert_alpha() for i in range(8)]
        self.index = 1
        self.image_index = {}
        for i in range(8):
            self.image_index[i] = 1080

    def run(self):
        self.screen.blit(self.imageshome[0], (0, 0))
        for i in range(1, self.index + 1):
            if i < 7:
                self.screen.blit(self.imageshome[i], (0, self.image_index[i]))
                if i == self.index or self.image_index[i] > 0:
                    self.image_index[i] -= 20
        if self.image_index[self.index] <= 750:
            self.index += 1

        if pygame.mouse.get_pressed()[0]:
            self.activate = False
