import time
import pygame


def make_sound(filename):
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    # time.sleep(.9)
    pygame.event.wait()


make_sound('take.mp3')