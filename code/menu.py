import pygame
from settings import *
from player import Player
from timer import Timer


class Menu:

  def __init__(self, player: Player, toggle_menu) -> None:

    # general setup
    self.player = player
    self.toggle_menu = toggle_menu
    self.display_surface = pygame.display.get_surface()
    self.font = pygame.font.Font(BASE_DIR / 'font/LycheeSoda.ttf', 30)

    # options
    self.width = 400
    self.space = 10
    self.padding = 8

    # entries
    self.options = list(self.player.item_inventory.keys()) + \
        list(self.player.seed_inventory.keys())
    self.sell_border = len(self.player.item_inventory) - 1
    self.setup()

    # movement
    self.index = 0
    self.timer = Timer(200)

  def display_money(self):
    text_surf = self.font.render(f'${self.player.money}', False, 'black')
    text_rect = text_surf.get_rect(midbottom=(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 20))

    pygame.draw.rect(self.display_surface, 'white',
                     text_rect.inflate(15, 10), border_radius=4)
    self.display_surface.blit(text_surf, text_rect)

  def setup(self):

    # create the text surfaces
    self.text_surfs: list[pygame.surface.Surface] = []
    self.total_height = 0
    for item in self.options:
      text_surf = self.font.render(item, True, 'black')
      self.text_surfs.append(text_surf)
      self.total_height += text_surf.get_height() + (self.padding * 2)

    self.total_height += (len(self.text_surfs) - 1) * self.space
    self.menu_top = (SCREEN_HEIGHT - self.total_height) / 2
    self.main_rect = pygame.Rect(
      (SCREEN_WIDTH - self.total_height) / 2, self.menu_top,
      self.width, self.total_height
    )

    # buy / sell text surface
    text_color = (134, 156, 26)
    self.buy_text = self.font.render('buy', False, text_color)
    self.sell_text = self.font.render('sell', False, text_color)

  def input(self):
    keys = pygame.key.get_pressed()
    self.timer.update()

    if keys[pygame.K_ESCAPE]:
      self.toggle_menu()

    elif not self.timer.active:
      if keys[pygame.K_UP]:
        self.index -= 1
        self.timer.activate()
      elif keys[pygame.K_DOWN]:
        self.index += 1
        self.timer.activate()

      elif keys[pygame.K_SPACE]:
        self.timer.activate()

        # get item
        current_item = self.options[self.index]

        # sell
        if self.index <= self.sell_border:
          if self.player.item_inventory[current_item] > 0:
            self.player.item_inventory[current_item] -= 1
            self.player.money += SALE_PRICES[current_item]

        # buy
        else:
          seed_price = PURCHASE_PRICES[current_item]
          if self.player.money >= seed_price:
            self.player.seed_inventory[current_item] += 1
            self.player.money -= seed_price

    # clamo the values
    if self.index < 0:
      self.index = len(self.options) - 1
    elif self.index >= len(self.options):
      self.index = 0

  def show_entry(self, text_surf: pygame.surface.Surface, amount: int, top: float, selected):
    # background
    bg_rect = pygame.Rect(
      self.main_rect.left, top,
      self.width, text_surf.get_height() + (self.padding * 2)
    )
    pygame.draw.rect(self.display_surface, 'white', bg_rect, border_radius=4)

    # text
    text_rect = text_surf.get_rect(midleft=(self.main_rect.left + 20, bg_rect.centery))
    self.display_surface.blit(text_surf, text_rect)

    # amount
    amount_surf = self.font.render(str(amount), False, 'black')
    amount_rect = amount_surf.get_rect(
      midright=(self.main_rect.right - 20, bg_rect.centery))
    self.display_surface.blit(amount_surf, amount_rect)

    # selected
    if selected:
      pygame.draw.rect(self.display_surface, 'black', bg_rect, 4, 4)
      if self.index <= self.sell_border:
        pos_rect = self.sell_text.get_rect(
          center=(self.main_rect.centerx, bg_rect.centery))
        self.display_surface.blit(self.sell_text, pos_rect)
      else:
        pos_rect = self.buy_text.get_rect(
          center=(self.main_rect.centerx, bg_rect.centery))
        self.display_surface.blit(self.buy_text, pos_rect)

  def update(self):
    self.input()
    self.display_money()

    amount_list = list(self.player.item_inventory.values()) + \
        list(self.player.seed_inventory.values())
    for idx, text_surf in enumerate(self.text_surfs):
      top = self.main_rect.top + \
        idx * (text_surf.get_height() + (self.padding * 2) + self.space)
      self.show_entry(text_surf, amount_list[idx], top, self.index == idx)
