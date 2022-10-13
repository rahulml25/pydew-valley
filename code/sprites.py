import pygame
from settings import *
from random import randint, choice
from typing import Callable


class Generic(pygame.sprite.Sprite):

  def __init__(self, pos, surf, groups, z=LAYERS['main']) -> None:
    super().__init__(groups)
    self.image = surf
    self.rect = self.image.get_rect(topleft=pos)
    self.hitbox = self.rect.copy().inflate(-self.rect.width * .2, -self.rect.height * .75)
    self.z = z


class Interaction(Generic):

  def __init__(self, pos, size, groups, name) -> None:
    surf = pygame.Surface(size)
    super().__init__(pos, surf, groups)
    self.name = name


class Water(Generic):

  def __init__(self, pos, frames, groups) -> None:

    # animation setup
    self.frames = frames
    self.frame_index = 0

    # sprite setup
    super().__init__(
      pos=pos,
      surf=self.frames[self.frame_index],
      groups=groups, z=LAYERS['water']
    )

  def animate(self, dt):
    self.frame_index += 5 * dt
    if self.frame_index >= len(self.frames):
      self.frame_index = 0
    self.image = self.frames[int(self.frame_index)]

  def update(self, dt) -> None:
    self.animate(dt)


class WildFlower(Generic):

  def __init__(self, pos, surf, groups) -> None:
    super().__init__(pos, surf, groups)
    self.hitbox = self.rect.copy().inflate(-20, -self.rect.height * .9)


class Particle(Generic):

  def __init__(self, pos, surf, groups, z, duration=200):
    super().__init__(pos, surf, groups, z)
    self.start_time = pygame.time.get_ticks()
    self.duration = duration

    # white surface
    self.image = pygame.mask.from_surface(surf).to_surface()
    self.image.set_colorkey((0, 0, 0))

  def update(self, dt) -> None:
    current_time = pygame.time.get_ticks()
    if current_time - self.start_time > self.duration:
      self.kill()


class Tree(Generic):

  def __init__(self, pos, surf, groups, name: str, player_add: Callable[[str], None]) -> None:
    super().__init__(pos, surf, groups)

    # tree attributes
    self.health = 5
    self.alive = True
    self.stump_surf = pygame.image.load(
      GRAPHICS_DIR / f'stumps/{name.lower()}.png').convert_alpha()

    # apples
    self.appels_surf = pygame.image.load(GRAPHICS_DIR / 'fruit/apple.png')
    self.appel_pos = APPLE_POS[name]
    self.apple_sprites = pygame.sprite.Group()
    self.create_fruit()

    self.player_add = player_add

    # sounds
    self.axe_sound = pygame.mixer.Sound(AUDIO_DIR / 'axe.mp3')

  def damage(self):

    # damaging the tree
    self.health -= 1

    # play_sound
    self.axe_sound.play()

    # remove a apple
    if len(self.apple_sprites.sprites()) > 0:
      random_apple = choice(self.apple_sprites.sprites())
      Particle(
        pos=random_apple.rect.topleft,
        surf=random_apple.image,
        groups=self.groups()[0],
        z=LAYERS['fruit']
      )
      self.player_add('apple')
      random_apple.kill()

  def check_death(self):
    if self.health <= 0:
      Particle(
        pos=self.rect.topleft,
        surf=self.image,
        groups=self.groups()[0],
        z=LAYERS['fruit'],
        duration=300
      )
      self.image = self.stump_surf
      self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
      self.hitbox = self.rect.copy().inflate(-10, -self.rect.height * 0.6)
      self.alive = False
      self.player_add('wood')

  def update(self, dt) -> None:
    if self.alive:
      self.check_death()

  def create_fruit(self):
    for pos in self.appel_pos:
      if randint(0, 10) < 2:
        pos = self.rect.left + pos[0], self.rect.top + pos[1]
        Generic(pos, self.appels_surf, [
                self.apple_sprites, self.groups()[0]], LAYERS['fruit'])
