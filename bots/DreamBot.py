from .BaseBot import Bot
import random
import pygame

class Dreamer(Bot):
    def __init__(self , name):
        self.name = name
        super().__init__(name)
        self.x = random.randint(0, 750)
        self.y = random.randint(0, 550)
        self.dreams = [
            "I flew over a mountain made of chocolate 🍫",
            "Spotted a cat riding a bicycle in my dream 🚲😺",
            "Dreamt of coding in zero gravity 🌌",
            "I was a tiny ant in a giant city 🐜🏙️"
        ]
        self.current_dream = random.choice(self.dreams)
        self.color = (0, 255, 255)
        self.size = 15


    def act(self,universe):
        #dream = random.choice(self.sentences)
        #print(f"{self.name} dream diary : {dream}")
        self.current_dream = random.choice(self.dreams)
        self.x += random.randint(-5, 5)
        self.y += random.randint(-5, 5)
        self.x = max(0, min(self.x, universe.width - 50))
        self.y = max(0, min(self.y, universe.height - 50))

    def draw(self , screen ):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size)
        font = pygame.font.SysFont(None, 20)
        text = font.render(self.current_dream, True, (255, 255, 255))
        screen.blit(text, (self.x + 20, self.y))