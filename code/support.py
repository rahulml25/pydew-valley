import pygame
from os import walk
from pathlib import Path


def import_folder(path: Path) -> list[pygame.Surface]:
  surface_list = []

  for _, _, img_files in walk(path):
    for image in img_files:
      full_path = path / image
      image_surf = pygame.image.load(full_path).convert_alpha()
      surface_list.append(image_surf)

  return surface_list


def import_folder_dict(path: Path) -> dict[[str]: pygame.Surface]:
  surface_dict = dict()

  for _, _, img_files in walk(path):
    for image in img_files:
      full_path = path / image
      image_surf = pygame.image.load(full_path).convert_alpha()
      surface_dict[image.split('.')[0]] = image_surf

  return surface_dict
