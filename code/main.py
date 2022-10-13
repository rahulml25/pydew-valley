import pygame
import sys
from settings import *
from level import Level
import win32gui
import win32con

class Game:

  def __init__(self):
    # hiding the console
    fore_ground = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(fore_ground, win32con.SW_HIDE)

    # init
    pygame.init()
    self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_icon(pygame.image.load(GRAPHICS_DIR / 'icon/icon.png'))
    pygame.display.set_caption('Sprout land')
    self.clock = pygame.time.Clock()
    self.level = Level()

  def run(self):
    while True:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()

      dt = self.clock.tick() / 1000
      self.level.run(dt)
      pygame.display.update()


if __name__ == '__main__':
  game = Game()
  game.run()
