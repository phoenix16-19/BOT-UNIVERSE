from .BaseBot import Bot
import random
import pygame

class Echo(Bot):
    def __init__(self , name):
        self.name = name
        super().__init__(name)
        #self.history = []
        self.x = random.randint(0 , 750 )
        self.y = random.randint(0 ,550 )
        self.size = 15
        self.color = (225 ,0 ,225)
        self.trail = [] # store previous positions for trail effect

    def act(self,universe):
        # move randomly
        self.x += random.randint(-10, 10)
        self.y += random.randint(-10, 10)
        self.x = max(0, min(self.x, universe.width - 50))
        self.y = max(0, min(self.y, universe.height - 50))

        # add current position to trail
        self.trail.append((self.x, self.y))
        # limit trail length
        if len(self.trail) > 20:
            self.trail.pop(0)
        #last_msgs = [bot.name for bot in universe.bots if bot != self]
        #if last_msgs :
         #   msg = random.choice(last_msgs)

          #  echo_msg = msg + "..."
           # self.history.append(echo_msg)
            #print(f"{self.name} echoes : {echo_msg}")
        #else :
         #   print(f"{self.name} is echoing nothing yet!")

    def draw(self , screen ):
        # draw trail with fading effect
        for i, pos in enumerate(self.trail):
            alpha = int(255 * (i / len(self.trail)))
            s = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, (self.color[0], self.color[1], self.color[2], alpha), (self.size, self.size),
                               self.size)
            screen.blit(s, (pos[0] - self.size, pos[1] - self.size))
        # draw current bot position
        pygame.draw.circle(screen , self.color , (self.x , self.y), self.size)