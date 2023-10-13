import pygame, sys
from setting import *
from pytmx.util_pygame import load_pygame
from pygame.math import Vector2
from tiled import Tile, CollisionTile
from player import Player

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = Vector2()

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - window_w / 2
        self.offset.y = player.rect.centery - window_h / 2

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

        self.setup()
    
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
                self.player = Player((obj.x, obj.y), self.all_sprites, './graphics/player', self.collision_sprites)
            
    
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            dt = self.clock.tick() / 1000
            self.display_surface.fill((249, 131, 103))

            self.all_sprites.update(dt)
            #self.all_sprites.draw(self.display_surface)
            self.all_sprites.custom_draw(self.player)
        
            pygame.display.update()
            
if __name__ == '__main__':
    main = Main()
    main.run()