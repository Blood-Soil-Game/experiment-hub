"""
Sprite generation and management for pixel art graphics
Top-down view
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
        """Generate tile sprites for jungle and cave"""
        # JUNGLE TILES

        # Grass tile
        grass = pygame.Surface((TILE_SIZE, TILE_SIZE))
        grass.fill(GRASS_GREEN)
        # Add some texture
        for i in range(5):
            x, y = (i * 3) % TILE_SIZE, (i * 4) % TILE_SIZE
            pygame.draw.rect(grass, JUNGLE_GREEN, (x, y, 2, 2))
        self.tiles[TILE_GRASS] = grass

        # Tree tile
        tree = pygame.Surface((TILE_SIZE, TILE_SIZE))
        tree.fill(TREE_GREEN)
        # Tree trunk in center
        pygame.draw.rect(tree, TREE_TRUNK, (6, 6, 4, 4))
        # Leaves around
        pygame.draw.circle(tree, TREE_GREEN, (8, 8), 7)
        pygame.draw.circle(tree, JUNGLE_GREEN, (6, 6), 3)
        self.tiles[TILE_TREE] = tree

        # Bush tile
        bush = pygame.Surface((TILE_SIZE, TILE_SIZE))
        bush.fill(GRASS_GREEN)
        # Bush in center
        pygame.draw.circle(bush, BUSH_GREEN, (8, 8), 5)
        pygame.draw.circle(bush, TREE_GREEN, (6, 10), 3)
        self.tiles[TILE_BUSH] = bush

        # Flower tile
        flower = pygame.Surface((TILE_SIZE, TILE_SIZE))
        flower.fill(GRASS_GREEN)
        # Flower
        pygame.draw.circle(flower, FLOWER_RED, (8, 7), 3)
        pygame.draw.circle(flower, FLOWER_YELLOW, (8, 7), 1)
        pygame.draw.rect(flower, JUNGLE_GREEN, (7, 10, 2, 4))
        self.tiles[TILE_FLOWER] = flower

        # Water tile
        water = pygame.Surface((TILE_SIZE, TILE_SIZE))
        water.fill(WATER_BLUE)
        # Add wave pattern
        for i in range(4):
            y = i * 4 + 2
            pygame.draw.line(water, (50, 160, 255), (0, y), (TILE_SIZE, y))
        self.tiles[TILE_WATER] = water

        # Dirt tile
        dirt = pygame.Surface((TILE_SIZE, TILE_SIZE))
        dirt.fill(DIRT_BROWN)
        # Add texture
        for i in range(5):
            x, y = (i * 5) % TILE_SIZE, (i * 3) % TILE_SIZE
            pygame.draw.rect(dirt, (120, 60, 15), (x, y, 2, 2))
        self.tiles[TILE_DIRT] = dirt

        # CAVE TILES

        # Cave floor
        cave_floor = pygame.Surface((TILE_SIZE, TILE_SIZE))
        cave_floor.fill(CAVE_FLOOR)
        # Add texture
        for i in range(3):
            x, y = (i * 6) % TILE_SIZE, (i * 5) % TILE_SIZE
            pygame.draw.rect(cave_floor, (70, 70, 70), (x, y, 2, 2))
        self.tiles[TILE_CAVE_FLOOR] = cave_floor

        # Cave wall
        cave_wall = pygame.Surface((TILE_SIZE, TILE_SIZE))
        cave_wall.fill(CAVE_DARK)
        # Add rock texture
        for i in range(4):
            for j in range(4):
                if (i + j) % 2 == 0:
                    pygame.draw.rect(cave_wall, (50, 50, 50), (i * 4, j * 4, 3, 3))
        self.tiles[TILE_CAVE_WALL] = cave_wall

        # Stone tile
        stone = pygame.Surface((TILE_SIZE, TILE_SIZE))
        stone.fill(STONE_GRAY)
        # Add texture
        for i in range(4):
            for j in range(4):
                if (i + j) % 3 == 0:
                    pygame.draw.rect(stone, DARK_GRAY, (i * 4, j * 4, 3, 3))
        self.tiles[TILE_STONE] = stone

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

        # Cave entrance (portal)
        entrance = pygame.Surface((TILE_SIZE, TILE_SIZE))
        entrance.fill(PORTAL_PURPLE)
        # Add swirl effect
        pygame.draw.circle(entrance, (180, 80, 255), (8, 8), 6)
        pygame.draw.circle(entrance, PORTAL_PURPLE, (8, 8), 3)
        self.tiles[TILE_CAVE_ENTRANCE] = entrance

        # Cave exit (portal)
        exit_tile = pygame.Surface((TILE_SIZE, TILE_SIZE))
        exit_tile.fill(PORTAL_PURPLE)
        # Add swirl effect
        pygame.draw.circle(exit_tile, (180, 80, 255), (8, 8), 6)
        pygame.draw.circle(exit_tile, (100, 50, 150), (8, 8), 3)
        self.tiles[TILE_CAVE_EXIT] = exit_tile

        # Air (transparent)
        air = pygame.Surface((TILE_SIZE, TILE_SIZE))
        air.fill((0, 0, 0))
        air.set_colorkey((0, 0, 0))
        self.tiles[TILE_AIR] = air

    def _generate_player_sprites(self):
        """Generate player sprites for top-down view (4 directions)"""
        # For each direction, create idle and walking sprites
        for direction in ["up", "down", "left", "right"]:
            # Idle sprite
            idle = pygame.Surface((TILE_SIZE, TILE_SIZE))
            idle.set_colorkey(BLACK)
            idle.fill(BLACK)

            # Draw player based on direction
            if direction == "down":
                # Head
                pygame.draw.circle(idle, PLAYER_RED, (8, 6), 4)
                # Body
                pygame.draw.rect(idle, (150, 40, 40), (5, 9, 6, 5))
                # Legs
                pygame.draw.rect(idle, (100, 30, 30), (5, 14, 2, 2))
                pygame.draw.rect(idle, (100, 30, 30), (9, 14, 2, 2))
            elif direction == "up":
                # Head (back of head)
                pygame.draw.circle(idle, (150, 30, 30), (8, 6), 4)
                # Body
                pygame.draw.rect(idle, (100, 30, 30), (5, 9, 6, 5))
                # Legs
                pygame.draw.rect(idle, (80, 20, 20), (5, 14, 2, 2))
                pygame.draw.rect(idle, (80, 20, 20), (9, 14, 2, 2))
            elif direction == "left":
                # Head (side view)
                pygame.draw.circle(idle, PLAYER_RED, (6, 6), 4)
                # Body
                pygame.draw.rect(idle, (150, 40, 40), (4, 9, 5, 5))
                # Legs
                pygame.draw.rect(idle, (100, 30, 30), (4, 14, 2, 2))
                pygame.draw.rect(idle, (100, 30, 30), (7, 14, 2, 2))
            else:  # right
                # Head (side view)
                pygame.draw.circle(idle, PLAYER_RED, (10, 6), 4)
                # Body
                pygame.draw.rect(idle, (150, 40, 40), (7, 9, 5, 5))
                # Legs
                pygame.draw.rect(idle, (100, 30, 30), (7, 14, 2, 2))
                pygame.draw.rect(idle, (100, 30, 30), (10, 14, 2, 2))

            # Add eyes
            if direction == "down":
                pygame.draw.rect(idle, BLACK, (6, 5, 1, 1))
                pygame.draw.rect(idle, BLACK, (9, 5, 1, 1))

            self.player_sprites[f"{direction}_idle"] = idle

            # Walking animation (2 frames)
            walk1 = idle.copy()
            walk2 = idle.copy()

            self.player_sprites[f"{direction}_walk"] = [walk1, walk2]

    def _generate_enemy_sprites(self):
        """Generate enemy sprites (animals for jungle, creatures for cave)"""
        # Tiger (jungle)
        tiger = pygame.Surface((TILE_SIZE, TILE_SIZE))
        tiger.set_colorkey(BLACK)
        tiger.fill(BLACK)
        pygame.draw.ellipse(tiger, TIGER_ORANGE, (2, 4, 12, 8))  # Body
        pygame.draw.circle(tiger, TIGER_ORANGE, (8, 4), 3)  # Head
        # Stripes
        for i in range(3):
            pygame.draw.line(tiger, BLACK, (4 + i * 3, 6), (4 + i * 3, 10))
        self.enemy_sprites["tiger"] = tiger

        # Snake (jungle)
        snake = pygame.Surface((TILE_SIZE, TILE_SIZE))
        snake.set_colorkey(BLACK)
        snake.fill(BLACK)
        # Snake body (S shape)
        points = [(4, 4), (8, 6), (12, 8), (10, 12), (6, 14)]
        for i in range(len(points) - 1):
            pygame.draw.line(snake, SNAKE_GREEN, points[i], points[i + 1], 3)
        pygame.draw.circle(snake, SNAKE_GREEN, (4, 4), 2)  # Head
        self.enemy_sprites["snake"] = snake

        # Bear (jungle)
        bear = pygame.Surface((TILE_SIZE, TILE_SIZE))
        bear.set_colorkey(BLACK)
        bear.fill(BLACK)
        pygame.draw.ellipse(bear, BEAR_BROWN, (2, 5, 12, 9))  # Body
        pygame.draw.circle(bear, BEAR_BROWN, (7, 5), 4)  # Head
        pygame.draw.circle(bear, (100, 50, 10), (6, 4), 1)  # Ear
        pygame.draw.circle(bear, (100, 50, 10), (9, 4), 1)  # Ear
        self.enemy_sprites["bear"] = bear

        # Bat (cave)
        bat = pygame.Surface((TILE_SIZE, TILE_SIZE))
        bat.set_colorkey(BLACK)
        bat.fill(BLACK)
        pygame.draw.circle(bat, BAT_GRAY, (8, 8), 3)  # Body
        # Wings
        pygame.draw.polygon(bat, BAT_GRAY, [(5, 8), (2, 6), (2, 10)])  # Left wing
        pygame.draw.polygon(bat, BAT_GRAY, [(11, 8), (14, 6), (14, 10)])  # Right wing
        self.enemy_sprites["bat"] = bat

    def _generate_item_sprites(self):
        """Generate item icons for inventory"""
        # Wood
        wood = pygame.Surface((TILE_SIZE, TILE_SIZE))
        wood.fill(TREE_TRUNK)
        for i in range(TILE_SIZE):
            if i % 4 < 2:
                pygame.draw.line(wood, (90, 60, 30), (0, i), (TILE_SIZE, i))
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

        # Dirt
        dirt = pygame.Surface((TILE_SIZE, TILE_SIZE))
        dirt.fill(DIRT_BROWN)
        self.item_sprites[ITEM_DIRT] = dirt

    def get_tile(self, tile_type):
        """Get tile sprite by type"""
        return self.tiles.get(tile_type, self.tiles[TILE_AIR])

    def get_player_sprite(self, direction, is_moving, frame=0):
        """Get player sprite by direction and movement state"""
        if is_moving:
            sprites = self.player_sprites.get(f"{direction}_walk", [self.player_sprites[f"{direction}_idle"]])
            return sprites[frame % len(sprites)] if len(sprites) > 0 else self.player_sprites[f"{direction}_idle"]
        else:
            return self.player_sprites.get(f"{direction}_idle", self.player_sprites["down_idle"])

    def get_enemy_sprite(self, enemy_type):
        """Get enemy sprite by type"""
        return self.enemy_sprites.get(enemy_type, self.enemy_sprites.get("tiger"))

    def get_item_sprite(self, item_type):
        """Get item sprite by type"""
        return self.item_sprites.get(item_type, self.item_sprites[ITEM_STONE])
