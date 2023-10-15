import pygame, sys
from setting import *
from pytmx.util_pygame import load_pygame
from pygame.math import Vector2
from tiled import Tile, CollisionTile, Movingobj
from bullet import Bullet, FireAnimation
from player import Player
from enemy import Enemy

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = Vector2()
        
        # import
        self.fg_sky = pygame.image.load('./graphics/sky/fg_sky.png').convert_alpha()
        self.bg_sky = pygame.image.load('./graphics/sky/bg_sky.png').convert_alpha()
        tmx_map = load_pygame('./data/map.tmx')

        # dimension
        self.sky_width = self.bg_sky.get_width()
        self.padding = window_w / 2
        map_width = tmx_map.tilewidth * tmx_map.width + (2 * self.padding)
        self.sky_num = map_width // self.sky_width

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - window_w / 2
        self.offset.y = player.rect.centery - window_h / 2

        for x in range(int(self.sky_num)):
            x_pos = -self.padding + (x * self.sky_width)
            self.display_surface.blit(self.bg_sky, (x_pos - self.offset.x / 2.5, 850 - self.offset.y / 2.5))
            self.display_surface.blit(self.fg_sky, (x_pos - self.offset.x / 2, 900 - self.offset.y / 2))

        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.z):
            offset_rect = sprite.image.get_rect(center = sprite.rect.center)
            offset_rect.center -= self.offset
            self.display_surface.blit(sprite.image, offset_rect)

class Main:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((window_w, window_h))
        pygame.display.set_caption('Contra')
        self.clock = pygame.time.Clock()

        #groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.platform_sprites = pygame.sprite.Group()
        self.bullet_sprite = pygame.sprite.Group()

        self.setup()
        
        self.bullet_surf = pygame.image.load('./graphics/bullet.png').convert_alpha()
        self.fire_surf = [pygame.image.load('./graphics/fire/0.png').convert_alpha(),
                          pygame.image.load('./graphics/fire/1.png').convert_alpha()]
    
    def setup(self):
        tmx_map = load_pygame('./data/map.tmx')

        # collision tiles
        for x,y,surf in tmx_map.get_layer_by_name('Level').tiles():
            CollisionTile((x * 64, y * 64), surf, [self.all_sprites, self.collision_sprites])
        
        # Tiles
        for layer in ['BG','BG Detail', 'FG Detail Bottom', 'FG Detail Top']:
            for x,y,surf in tmx_map.get_layer_by_name(layer).tiles():
                Tile((x * 64, y * 64), surf, self.all_sprites, LAYERS[layer])
        
        # objects
        for obj in tmx_map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                self.player = Player((obj.x, obj.y), 
                                     self.all_sprites, 
                                     './graphics/player', 
                                     self.collision_sprites,
                                     self.shoot_bullet)
            
            if obj.name == "Enemy":
                self.enemy = Enemy((obj.x, obj.y), 
                                     self.all_sprites, 
                                     './graphics/enemies', 
                                     self.shoot_bullet,
                                     self.player,
                                     self.collision_sprites
                                     )

        self.platform_border_rect = []
        for obj in tmx_map.get_layer_by_name('Platforms'):
            if obj.name == 'Platform':
                Movingobj((obj.x, obj.y), obj.image, [self.all_sprites, self.collision_sprites, self.platform_sprites]) 
            else: # border
                border_rect = pygame.Rect(obj.x , obj.y, obj.width, obj.height)
                self.platform_border_rect.append(border_rect)
    
    def bullet_collision(self):
        for obstacle in self.collision_sprites.sprites():
            pygame.sprite.spritecollide(obstacle, self.bullet_sprite, True)

    def platform_collision(self):
        for platform in self.platform_sprites.sprites():
            for border in self.platform_border_rect:
                if platform.rect.colliderect(border):
                    if platform.direction.y < 0:
                        platform.rect.top = border.bottom
                        platform.pos.y = platform.rect.y
                        platform.direction.y = 1
                    else:
                        platform.rect.bottom = border.top
                        platform.pos.y = platform.rect.y
                        platform.direction.y = -1
            if platform.rect.colliderect(self.player.rect) and self.player.rect.centery > platform.rect.centery:
                platform.rect.bottom = self.player.rect.top
                platform.pos.y = platform.rect.y
                platform.direction.y = -1
    
    def shoot_bullet(self, pos, direction, entity):
        Bullet(pos, self.bullet_surf, direction, [self.all_sprites, self.bullet_sprite])
        FireAnimation(entity, self.fire_surf, direction, self.all_sprites)
    
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit() 
                    sys.exit()
            
            dt = self.clock.tick() / 1000
            self.display_surface.fill((249, 131, 103))

            self.platform_collision()
            self.all_sprites.update(dt)
            #self.all_sprites.draw(self.display_surface)
            self.bullet_collision()
            self.all_sprites.custom_draw(self.player)
        
            pygame.display.update()
            
if __name__ == '__main__':
    main = Main()
    main.run()