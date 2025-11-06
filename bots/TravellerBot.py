from .BaseBot import Bot
import random
import pygame

class TravellerBot(Bot):
    def __init__(self , name):
        self.name = name
        super().__init__(name)
        self.x = random.randint(0 , 750 )
        self.y = random.randint(0 , 550)
        self.messages = [
            "Greetings from 3025! 🚀",
            "The stars are aligning oddly tonight ✨",
            "I saw a robot doing yoga in 3050 🤖🧘",
            "Warning: Time paradox detected!"
        ]
        self.color = (255 , 0 , 255)
        self.size = 15
        self.current_msg = random.choice(self.messages)

    def act(self, universe):
        #message = random.choice(self.messages)
        #print(f"{self.name}: {message}")

        self.current_msg = random.choice(self.messages)
        # float slightly
        self.y += random.randint(-5, 5)
        self.x += random.randint(-5, 5)
        self.x = max(0, min(self.x, universe.width - 50))
        self.y = max(0, min(self.y, universe.height - 50))


    def draw(self, screen):
        pygame.draw.circle(screen , self.color , (self.x ,self.y ) , self.size)
        font = pygame.font.SysFont(None , 20 )
        text = font.render(self.current_msg , True , (225,225,225))
        screen.blit(text , (self.x+20 , self.y))