from .BaseBot import Bot
import random
import pygame

class MoodSwingBot(Bot):
    def __init__(self , name):
        self.name = name
        super().__init__(name)
        self.x = random.randint(0, 750)
        self.y = random.randint(0, 550)
        self.moods = ["happy", "sad", "angry", "excited", "sleepy"]
        self.current_mood = random.choice(self.moods)
        self.color_map = {
            "happy": (0, 255, 0),
            "sad": (0, 0, 255),
            "angry": (255, 0, 0),
            "excited": (255, 165, 0),
            "sleepy": (128, 128, 128)
        }
        self.size = 20

    #self.moods = ["happy" , "sad" ,"angry","excited" ,"sleepy"]
     #   self.current_mood = random.choice(self.moods)

    def act(self , universe):
        #self.current_mood = random.choice(self.moods)
        #print(f"{self.name} : is now feeling {self.current_mood}")

        # change mood randomly each tick
        self.current_mood = random.choice(self.moods)
        # optional random movement
        self.x += random.randint(-10, 10)
        self.y += random.randint(-10, 10)
        self.x = max(0, min(self.x, universe.width - 50))
        self.y = max(0, min(self.y, universe.height - 50))

    def draw(self , screen):
        pygame.draw.circle(screen , self.color_map[self.current_mood], (self.x , self.y), self.size )