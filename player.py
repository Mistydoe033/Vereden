import os

import pygame

from abc import ABC, abstractmethod
from _types import EventInfo




class BaseCharacter:
	def __init__(self, player_type):
		self.name = ""
		self.image = pygame.Surface((100, 100))
		self.image.fill((0,0,0))

		self.rect = self.image.get_rect()

		self.direction = pygame.math.Vector2()

		self.pos = pygame.math.Vector2(self.rect.center)

		self.speed = 3



	def movement(self):
		keys = pygame.key.get_pressed()

		if keys[pygame.K_w]:
			self.direction.y = -1

		elif keys[pygame.K_s]:
			self.direction.y = 1

		else:
			self.direction.y = 0

		if keys[pygame.K_d]:
			self.direction.x = 1

		elif keys[pygame.K_a]:
			self.direction.x = -1

		else:
			self.direction.x = 0

	def move(self,dt):
		self.pos += self.direction * self.speed
		self.rect.center = self.pos

		print(dt)

	def update_movement(self, dt):
		self.movement()

	def draw(self, screen, pos):
		screen.blit(self.image,(pos))

	def update(self, event_info: EventInfo) -> None:

		self.update_movement(event_info["dt"])
		self.move(event_info["dt"])
		print(self.pos)


class PlayerState(ABC):
	def __init__(self):
		self.base = None

	def select_character(self, character_type):
		if character_type == "mage":
			self.base = Mage()
		elif character_type == "knight":
			self.base = Knight()
		elif character_type == "archer":
			self.base = Archer()
		elif character_type == "none":
			self.base = None

	def update(self, event_info):
		self.base.update(event_info)

	def draw(self,screen) -> None:

		if self.base is not None:
			self.base.draw(screen, self.base.pos)	

# Then create one here
player = PlayerState()


class Mage(BaseCharacter):
	def __init__(self):
		super().__init__("mage")

		self.name = "Maz"
		self.image = pygame.image.load("assets/images/sprites/kuro.gif")
  


class Knight(BaseCharacter):
	def __init__(self):
		super().__init__("knight")

		name = "Knox"
		image = pygame.image.load("assets/images/sprites/knight.png")


class Archer(BaseCharacter):
	def __init__(self):
		super().__init__("archer")

		name = "Aro"
		image = pygame.image.load("assets/images/sprites/archer.png")



characters = BaseCharacter.__subclasses__()