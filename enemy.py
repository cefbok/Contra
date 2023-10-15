import pygame
from setting import *
from pygame.math import Vector2
from entity import Entity

class Enemy(Entity):
    def __init__(self, pos, groups, path, shoot_bullet, player, collision_sprites):
        super().__init__(pos, path, groups, shoot_bullet) 
        self.player = player
        for sprite in collision_sprites.sprites():
            if sprite.rect.collidepoint(self.rect.midbottom):
                self.rect.bottom = sprite.rect.top
        
        self.cooldown = 1000

    
    def get_status(self):
        if self.player.rect.centerx < self.rect.centerx:
            self.status = 'left'
        else:
            self.status = 'right'
    
    def check_fire(self):
        enemy_pos = Vector2(self.rect.center)
        player_pos = Vector2(self.player.rect.center)

        distance = (player_pos - enemy_pos).magnitude()
        same_y = True if self.rect.top - 20 < player_pos.y < self.rect.bottom + 20 else False

        if distance < 600 and same_y and self.can_shoot:
            bullet_direct = Vector2(1, 0) if self.status == 'right' else Vector2(-1, 0)
            y_offest = Vector2(0, -15)
            pos = self.rect.center + bullet_direct * 40
            self.shoot_bullet(pos + y_offest, bullet_direct, self)

            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()

    def update(self, dt):
        self.get_status()
        self.animation(dt)

        self.shoot_timer()
        self.check_fire()