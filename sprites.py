"""
Sprite generation and management for pixel art graphics
"""

import pygame
from constants import *

class SpriteManager:
    """Manages all game sprites and textures"""

    def __init__(self):
        self.tiles = {}
        self.player_sprites = {}
        self.enemy_sprites = {}
        self.item_sprites = {}
        self._generate_all_sprites()

    def _generate_all_sprites(self):
        """Generate all game sprites"""
        self._generate_tile_sprites()
        self._generate_player_sprites()
        self._generate_enemy_sprites()
        self._generate_item_sprites()

    def _generate_tile_sprites(self):
        """Generate tile sprites using simple colored rectangles"""
        # Grass tile (green top, brown bottom)
        grass = pygame.Surface((TILE_SIZE, TILE_SIZE))
        grass.fill(DIRT_BROWN)
        pygame.draw.rect(grass, GRASS_GREEN, (0, 0, TILE_SIZE, 4))
        self.tiles[TILE_GRASS] = grass

        # Dirt tile
        dirt = pygame.Surface((TILE_SIZE, TILE_SIZE))
        dirt.fill(DIRT_BROWN)
        # Add some texture dots
        for i in range(3):
            for j in range(3):
                if (i + j) % 2 == 0:
                    pygame.draw.rect(dirt, (120, 60, 15), (i * 5 + 2, j * 5 + 2, 2, 2))
        self.tiles[TILE_DIRT] = dirt

        # Stone tile
        stone = pygame.Surface((TILE_SIZE, TILE_SIZE))
        stone.fill(STONE_GRAY)
        # Add texture
        for i in range(4):
            for j in range(4):
                if (i + j) % 3 == 0:
                    pygame.draw.rect(stone, DARK_GRAY, (i * 4, j * 4, 3, 3))
        self.tiles[TILE_STONE] = stone

        # Wood tile
        wood = pygame.Surface((TILE_SIZE, TILE_SIZE))
        wood.fill(WOOD_BROWN)
        # Add wood grain
        for i in range(TILE_SIZE):
            if i % 4 < 2:
                pygame.draw.line(wood, (90, 60, 30), (0, i), (TILE_SIZE, i))
        self.tiles[TILE_WOOD] = wood

        # Sand tile
        sand = pygame.Surface((TILE_SIZE, TILE_SIZE))
        sand.fill(SAND_YELLOW)
        # Add texture
        for i in range(5):
            for j in range(5):
                if (i * j) % 3 == 0:
                    pygame.draw.rect(sand, (220, 200, 160), (i * 3, j * 3, 1, 1))
        self.tiles[TILE_SAND] = sand

        # Iron ore
        iron = pygame.Surface((TILE_SIZE, TILE_SIZE))
        iron.fill(STONE_GRAY)
        # Add iron specks
        pygame.draw.rect(iron, IRON_GRAY, (4, 4, 3, 3))
        pygame.draw.rect(iron, IRON_GRAY, (9, 8, 4, 4))
        pygame.draw.rect(iron, IRON_GRAY, (6, 11, 2, 2))
        self.tiles[TILE_IRON_ORE] = iron

        # Diamond ore
        diamond = pygame.Surface((TILE_SIZE, TILE_SIZE))
        diamond.fill(STONE_GRAY)
        # Add diamond
        pygame.draw.rect(diamond, DIAMOND_CYAN, (6, 5, 4, 4))
        pygame.draw.rect(diamond, (0, 200, 200), (7, 6, 2, 2))
        self.tiles[TILE_DIAMOND_ORE] = diamond

        # Cave wall
        cave = pygame.Surface((TILE_SIZE, TILE_SIZE))
        cave.fill(CAVE_DARK)
        # Add texture
        for i in range(3):
            for j in range(3):
                pygame.draw.rect(cave, (50, 50, 50), (i * 5, j * 5, 3, 3))
        self.tiles[TILE_CAVE_WALL] = cave

        # Air (transparent)
        air = pygame.Surface((TILE_SIZE, TILE_SIZE))
        air.fill((0, 0, 0))
        air.set_colorkey((0, 0, 0))
        self.tiles[TILE_AIR] = air

    def _generate_player_sprites(self):
        """Generate player sprites (idle and walking animation)"""
        # Idle sprite
        idle = pygame.Surface((TILE_SIZE, TILE_SIZE * 2))
        idle.set_colorkey(BLACK)
        idle.fill(BLACK)
        # Head
        pygame.draw.rect(idle, PLAYER_RED, (4, 2, 8, 8))
        # Body
        pygame.draw.rect(idle, (150, 40, 40), (4, 10, 8, 12))
        # Legs
        pygame.draw.rect(idle, (100, 30, 30), (4, 22, 3, 8))
        pygame.draw.rect(idle, (100, 30, 30), (9, 22, 3, 8))
        # Eyes (vampire!)
        pygame.draw.rect(idle, (255, 0, 0), (6, 5, 1, 1))
        pygame.draw.rect(idle, (255, 0, 0), (9, 5, 1, 1))
        self.player_sprites["idle"] = idle

        # Walking animation (2 frames)
        walk1 = pygame.Surface((TILE_SIZE, TILE_SIZE * 2))
        walk1.set_colorkey(BLACK)
        walk1.fill(BLACK)
        pygame.draw.rect(walk1, PLAYER_RED, (4, 2, 8, 8))
        pygame.draw.rect(walk1, (150, 40, 40), (4, 10, 8, 12))
        pygame.draw.rect(walk1, (100, 30, 30), (4, 22, 3, 8))  # Left leg forward
        pygame.draw.rect(walk1, (100, 30, 30), (9, 24, 3, 6))  # Right leg back
        pygame.draw.rect(walk1, (255, 0, 0), (6, 5, 1, 1))
        pygame.draw.rect(walk1, (255, 0, 0), (9, 5, 1, 1))

        walk2 = pygame.Surface((TILE_SIZE, TILE_SIZE * 2))
        walk2.set_colorkey(BLACK)
        walk2.fill(BLACK)
        pygame.draw.rect(walk2, PLAYER_RED, (4, 2, 8, 8))
        pygame.draw.rect(walk2, (150, 40, 40), (4, 10, 8, 12))
        pygame.draw.rect(walk2, (100, 30, 30), (4, 24, 3, 6))  # Left leg back
        pygame.draw.rect(walk2, (100, 30, 30), (9, 22, 3, 8))  # Right leg forward
        pygame.draw.rect(walk2, (255, 0, 0), (6, 5, 1, 1))
        pygame.draw.rect(walk2, (255, 0, 0), (9, 5, 1, 1))

        self.player_sprites["walk"] = [walk1, walk2]

    def _generate_enemy_sprites(self):
        """Generate enemy sprites"""
        # Zombie
        zombie = pygame.Surface((TILE_SIZE, TILE_SIZE * 2))
        zombie.set_colorkey(BLACK)
        zombie.fill(BLACK)
        pygame.draw.rect(zombie, ZOMBIE_GREEN, (4, 2, 8, 8))  # Head
        pygame.draw.rect(zombie, (40, 120, 40), (4, 10, 8, 12))  # Body
        pygame.draw.rect(zombie, (30, 100, 30), (4, 22, 3, 8))  # Legs
        pygame.draw.rect(zombie, (30, 100, 30), (9, 22, 3, 8))
        pygame.draw.rect(zombie, (200, 0, 0), (6, 5, 1, 1))  # Eyes
        pygame.draw.rect(zombie, (200, 0, 0), (9, 5, 1, 1))
        self.enemy_sprites["zombie"] = zombie

        # Skeleton
        skeleton = pygame.Surface((TILE_SIZE, TILE_SIZE * 2))
        skeleton.set_colorkey(BLACK)
        skeleton.fill(BLACK)
        pygame.draw.rect(skeleton, SKELETON_WHITE, (4, 2, 8, 8))  # Head
        pygame.draw.rect(skeleton, (180, 180, 180), (6, 10, 4, 12))  # Body (thinner)
        pygame.draw.rect(skeleton, (180, 180, 180), (5, 22, 2, 8))  # Legs
        pygame.draw.rect(skeleton, (180, 180, 180), (9, 22, 2, 8))
        pygame.draw.rect(skeleton, BLACK, (6, 5, 1, 1))  # Eyes
        pygame.draw.rect(skeleton, BLACK, (9, 5, 1, 1))
        self.enemy_sprites["skeleton"] = skeleton

    def _generate_item_sprites(self):
        """Generate item icons for inventory"""
        # Wood
        wood = pygame.Surface((TILE_SIZE, TILE_SIZE))
        wood.fill(WOOD_BROWN)
        self.item_sprites[ITEM_WOOD] = wood

        # Stone
        stone = pygame.Surface((TILE_SIZE, TILE_SIZE))
        stone.fill(STONE_GRAY)
        self.item_sprites[ITEM_STONE] = stone

        # Iron
        iron = pygame.Surface((TILE_SIZE, TILE_SIZE))
        iron.fill(IRON_GRAY)
        self.item_sprites[ITEM_IRON] = iron

        # Diamond
        diamond = pygame.Surface((TILE_SIZE, TILE_SIZE))
        diamond.fill(DIAMOND_CYAN)
        self.item_sprites[ITEM_DIAMOND] = diamond

        # Apple (food)
        apple = pygame.Surface((TILE_SIZE, TILE_SIZE))
        apple.set_colorkey(BLACK)
        apple.fill(BLACK)
        pygame.draw.circle(apple, (255, 0, 0), (8, 8), 6)
        pygame.draw.rect(apple, (0, 128, 0), (7, 2, 2, 4))  # Stem
        self.item_sprites[ITEM_APPLE] = apple

        # Meat
        meat = pygame.Surface((TILE_SIZE, TILE_SIZE))
        meat.set_colorkey(BLACK)
        meat.fill(BLACK)
        pygame.draw.rect(meat, (180, 100, 100), (4, 5, 8, 6))
        self.item_sprites[ITEM_MEAT] = meat

    def get_tile(self, tile_type):
        """Get tile sprite by type"""
        return self.tiles.get(tile_type, self.tiles[TILE_AIR])

    def get_player_sprite(self, state, frame=0):
        """Get player sprite by state and frame"""
        if state == "idle":
            return self.player_sprites["idle"]
        elif state == "walk":
            return self.player_sprites["walk"][frame % 2]
        return self.player_sprites["idle"]

    def get_enemy_sprite(self, enemy_type):
        """Get enemy sprite by type"""
        return self.enemy_sprites.get(enemy_type, self.enemy_sprites["zombie"])

    def get_item_sprite(self, item_type):
        """Get item sprite by type"""
        return self.item_sprites.get(item_type, self.item_sprites[ITEM_STONE])
