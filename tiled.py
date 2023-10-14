import pygame
from setting import *
from pygame.math import Vector2

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, z):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.z = z

class CollisionTile(Tile):
    def __init__(self,pos, surf, groups):
        super().__init__(pos, surf, groups, LAYERS['Level'])
        self.old_rect = self.rect.copy()

class Movingobj(CollisionTile):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)

        self.direction = Vector2(0, -1)
        self.speed = 80
        self.pos = Vector2(self.rect.topleft)
    
    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.topleft = (round(self.pos.x),(round(self.pos.y)))
