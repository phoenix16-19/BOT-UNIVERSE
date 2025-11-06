from .BaseBot import Bot
import pygame
import random

class PixelGremlin(Bot):
    def __init__(self,name ):
        self.name = name
        super().__init__(name)

        self.x = random.randint(0 , 750)
        self.y = random.randint(0 , 550 )
        self.color = (225 , 225 , 0 )  # yellow
        self.size = random.randint(5 , 20 )


    def act(self , universe):
        # move randomly
        self.x += random.randint(-20, 20)
        self.y += random.randint(-20, 20)
        # keep inside screen bounds
        self.x = max(0, min(self.x, universe.width - 50))
        self.y = max(0, min(self.y, universe.height - 50))

 #actions = [
 #   "Scribbles a cat",
#  "Draws chaotic lines",
# "types aaaa in notepad",
#"doodles a tiny star"
#]
#print(f"{self.name}:{random.choice(actions)})

    def draw(self , screen ):
        pygame.draw.circle(screen , self.color ,(self.x , self.y) , self.size)