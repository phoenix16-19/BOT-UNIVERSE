from bots.MoodSwing import MoodSwingBot
from bots.TravellerBot import TravellerBot
from universe import Universe
from bots.pixel_Gremlin import PixelGremlin
from bots.DreamBot import Dreamer
from bots.EchoBot import Echo
import pygame

class BotUniverse:
    def __init__(self):
        self.bots = []

def main():
     uni = Universe()

     # creating bots
     gremlin = PixelGremlin("Gremlin")
     moody = MoodSwingBot("Moody")
     traveller = TravellerBot("rover")
     dream_bot = Dreamer("Dreamy")
     echo_bot = Echo("Reverb")

     # adding bots
     uni.add_bot(gremlin)
     uni.add_bot(moody)
     uni.add_bot(traveller)
     uni.add_bot(dream_bot)
     uni.add_bot(echo_bot)

    # for _ in range(3):
     #    uni.tick()
     running = True
     while running:
         for event in pygame.event.get():
             if event.type == pygame.QUIT:
                 running = False
         uni.tick()

     pygame.quit()


if __name__ == "__main__":
     main()