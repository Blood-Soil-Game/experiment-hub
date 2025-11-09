"""
World generation and tile management system for top-down explorer
Generates two levels: Jungle and Cave
"""

import random
import pygame
from constants import *

class World:
    """Procedurally generated tile-based world with multiple levels"""

    def __init__(self, sprite_manager, seed=None):
        self.sprite_manager = sprite_manager
        self.seed = seed if seed else random.randint(0, 999999)
        random.seed(self.seed)

        # Create world grids for each level
        self.width = WORLD_WIDTH
        self.height = WORLD_HEIGHT

        # Two levels: jungle (surface) and cave (underground)
        self.jungle_tiles = [[TILE_GRASS for _ in range(self.height)] for _ in range(self.width)]
        self.cave_tiles = [[TILE_CAVE_FLOOR for _ in range(self.height)] for _ in range(self.width)]

        # Portal positions
        self.jungle_portal = None  # (x, y) of cave entrance
        self.cave_portal = None  # (x, y) of cave exit

        # Generate both levels
        self._generate_jungle()
        self._generate_cave()

        # Find spawn point (in jungle)
        self.spawn_x, self.spawn_y = self._find_spawn_point()

    def _generate_jungle(self):
        """Generate the jungle level (surface)"""
        # Fill with grass
        for x in range(self.width):
            for y in range(self.height):
                self.jungle_tiles[x][y] = TILE_GRASS

        # Add water bodies
        self._add_water_bodies()

        # Add trees
        self._add_trees()

        # Add bushes
        self._add_bushes()

        # Add flowers (decoration)
        self._add_flowers()

        # Add cave entrance portal (center of map)
        portal_x = self.width // 2
        portal_y = self.height // 2
        self.jungle_portal = (portal_x, portal_y)
        self.jungle_tiles[portal_x][portal_y] = TILE_CAVE_ENTRANCE

    def _add_water_bodies(self):
        """Add water bodies to jungle"""
        num_lakes = 5

        for _ in range(num_lakes):
            # Random lake center
            cx = random.randint(10, self.width - 10)
            cy = random.randint(10, self.height - 10)

            # Lake size
            radius = random.randint(3, 7)

            # Create circular lake
            for dx in range(-radius, radius + 1):
                for dy in range(-radius, radius + 1):
                    if dx * dx + dy * dy <= radius * radius:
                        x, y = cx + dx, cy + dy
                        if 0 <= x < self.width and 0 <= y < self.height:
                            self.jungle_tiles[x][y] = TILE_WATER

    def _add_trees(self):
        """Add trees to jungle"""
        # Dense forest areas
        num_forests = 10

        for _ in range(num_forests):
            # Forest center
            cx = random.randint(5, self.width - 5)
            cy = random.randint(5, self.height - 5)

            # Forest size
            size = random.randint(5, 12)

            for _ in range(size * size // 2):
                # Random position near center
                x = cx + random.randint(-size, size)
                y = cy + random.randint(-size, size)

                if 0 <= x < self.width and 0 <= y < self.height:
                    if self.jungle_tiles[x][y] == TILE_GRASS:
                        self.jungle_tiles[x][y] = TILE_TREE

        # Scattered trees
        for _ in range(200):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)

            if self.jungle_tiles[x][y] == TILE_GRASS:
                self.jungle_tiles[x][y] = TILE_TREE

    def _add_bushes(self):
        """Add bushes to jungle"""
        for _ in range(150):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)

            if self.jungle_tiles[x][y] == TILE_GRASS:
                self.jungle_tiles[x][y] = TILE_BUSH

    def _add_flowers(self):
        """Add decorative flowers to jungle"""
        for _ in range(100):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)

            if self.jungle_tiles[x][y] == TILE_GRASS:
                self.jungle_tiles[x][y] = TILE_FLOWER

    def _generate_cave(self):
        """Generate the cave level (underground)"""
        # Fill with cave floor
        for x in range(self.width):
            for y in range(self.height):
                self.cave_tiles[x][y] = TILE_CAVE_FLOOR

        # Generate cave walls using cellular automata
        self._generate_cave_walls()

        # Add stone deposits (minable)
        self._add_stone_deposits()

        # Add ore deposits
        self._add_ore_deposits()

        # Add cave exit portal (near center)
        portal_x = self.width // 2 + random.randint(-5, 5)
        portal_y = self.height // 2 + random.randint(-5, 5)
        self.cave_portal = (portal_x, portal_y)
        self.cave_tiles[portal_x][portal_y] = TILE_CAVE_EXIT
        # Clear area around portal
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                x, y = portal_x + dx, portal_y + dy
                if 0 <= x < self.width and 0 <= y < self.height:
                    if self.cave_tiles[x][y] == TILE_CAVE_WALL:
                        self.cave_tiles[x][y] = TILE_CAVE_FLOOR

    def _generate_cave_walls(self):
        """Generate cave walls using cellular automata"""
        # Initial random fill
        for x in range(self.width):
            for y in range(self.height):
                if random.random() < 0.45:
                    self.cave_tiles[x][y] = TILE_CAVE_WALL

        # Apply cellular automata smoothing
        for _ in range(4):
            new_tiles = [[self.cave_tiles[x][y] for y in range(self.height)]
                        for x in range(self.width)]

            for x in range(1, self.width - 1):
                for y in range(1, self.height - 1):
                    # Count wall neighbors
                    wall_count = 0
                    for dx in [-1, 0, 1]:
                        for dy in [-1, 0, 1]:
                            if dx == 0 and dy == 0:
                                continue
                            if self.cave_tiles[x + dx][y + dy] == TILE_CAVE_WALL:
                                wall_count += 1

                    # Apply rules
                    if wall_count > 4:
                        new_tiles[x][y] = TILE_CAVE_WALL
                    elif wall_count < 4:
                        new_tiles[x][y] = TILE_CAVE_FLOOR

            self.cave_tiles = new_tiles

        # Add border walls
        for x in range(self.width):
            self.cave_tiles[x][0] = TILE_CAVE_WALL
            self.cave_tiles[x][self.height - 1] = TILE_CAVE_WALL
        for y in range(self.height):
            self.cave_tiles[0][y] = TILE_CAVE_WALL
            self.cave_tiles[self.width - 1][y] = TILE_CAVE_WALL

    def _add_stone_deposits(self):
        """Add minable stone to cave"""
        for _ in range(100):
            x = random.randint(1, self.width - 2)
            y = random.randint(1, self.height - 2)

            if self.cave_tiles[x][y] == TILE_CAVE_WALL:
                # Create small stone deposit
                size = random.randint(2, 5)
                for _ in range(size):
                    if 0 <= x < self.width and 0 <= y < self.height:
                        if self.cave_tiles[x][y] == TILE_CAVE_WALL:
                            self.cave_tiles[x][y] = TILE_STONE

                    # Move to adjacent tile
                    x += random.choice([-1, 0, 1])
                    y += random.choice([-1, 0, 1])

    def _add_ore_deposits(self):
        """Add ore deposits to cave"""
        # Iron ore (more common)
        for _ in range(80):
            x = random.randint(1, self.width - 2)
            y = random.randint(1, self.height - 2)

            if self.cave_tiles[x][y] in [TILE_CAVE_WALL, TILE_STONE]:
                # Create small iron vein
                size = random.randint(1, 3)
                for _ in range(size):
                    if 0 <= x < self.width and 0 <= y < self.height:
                        if self.cave_tiles[x][y] in [TILE_CAVE_WALL, TILE_STONE]:
                            self.cave_tiles[x][y] = TILE_IRON_ORE

                    x += random.choice([-1, 0, 1])
                    y += random.choice([-1, 0, 1])

        # Diamond ore (rare)
        for _ in range(20):
            x = random.randint(1, self.width - 2)
            y = random.randint(1, self.height - 2)

            if self.cave_tiles[x][y] in [TILE_CAVE_WALL, TILE_STONE]:
                # Single diamond or small cluster
                size = random.randint(1, 2)
                for _ in range(size):
                    if 0 <= x < self.width and 0 <= y < self.height:
                        if self.cave_tiles[x][y] in [TILE_CAVE_WALL, TILE_STONE]:
                            self.cave_tiles[x][y] = TILE_DIAMOND_ORE

                    x += random.choice([-1, 0, 1])
                    y += random.choice([-1, 0, 1])

    def _find_spawn_point(self):
        """Find a safe spawn point in the jungle"""
        # Start near the top-left quadrant
        for attempt in range(100):
            x = random.randint(self.width // 4, self.width // 2)
            y = random.randint(self.height // 4, self.height // 2)

            if self.jungle_tiles[x][y] == TILE_GRASS:
                return x * TILE_SIZE, y * TILE_SIZE

        # Fallback to any grass tile
        for x in range(self.width):
            for y in range(self.height):
                if self.jungle_tiles[x][y] == TILE_GRASS:
                    return x * TILE_SIZE, y * TILE_SIZE

        return (self.width // 2) * TILE_SIZE, (self.height // 2) * TILE_SIZE

    def get_tile(self, tile_x, tile_y, level):
        """Get tile at grid coordinates for a specific level"""
        if not (0 <= tile_x < self.width and 0 <= tile_y < self.height):
            return TILE_CAVE_WALL if level == LEVEL_CAVE else TILE_WATER

        if level == LEVEL_JUNGLE:
            return self.jungle_tiles[tile_x][tile_y]
        elif level == LEVEL_CAVE:
            return self.cave_tiles[tile_x][tile_y]
        else:
            return TILE_AIR

    def set_tile(self, tile_x, tile_y, tile_type, level):
        """Set tile at grid coordinates for a specific level"""
        if 0 <= tile_x < self.width and 0 <= tile_y < self.height:
            if level == LEVEL_JUNGLE:
                self.jungle_tiles[tile_x][tile_y] = tile_type
            elif level == LEVEL_CAVE:
                self.cave_tiles[tile_x][tile_y] = tile_type

    def get_portal_position(self, level, portal_type):
        """Get the position of a portal in a specific level"""
        if level == LEVEL_JUNGLE and portal_type == TILE_CAVE_ENTRANCE:
            return self.jungle_portal
        elif level == LEVEL_CAVE and portal_type == TILE_CAVE_EXIT:
            return self.cave_portal
        return (self.width // 2, self.height // 2)

    def draw(self, screen, camera_x, camera_y, current_level):
        """Draw visible tiles for the current level"""
        # Calculate visible tile range
        start_x = max(0, int(camera_x // TILE_SIZE) - 1)
        end_x = min(self.width, int((camera_x + SCREEN_WIDTH) // TILE_SIZE) + 2)
        start_y = max(0, int(camera_y // TILE_SIZE) - 1)
        end_y = min(self.height, int((camera_y + SCREEN_HEIGHT) // TILE_SIZE) + 2)

        # Get the appropriate tile grid
        if current_level == LEVEL_JUNGLE:
            tiles = self.jungle_tiles
        else:
            tiles = self.cave_tiles

        # Draw tiles
        for x in range(start_x, end_x):
            for y in range(start_y, end_y):
                tile = tiles[x][y]
                sprite = self.sprite_manager.get_tile(tile)
                screen_x = x * TILE_SIZE - camera_x
                screen_y = y * TILE_SIZE - camera_y
                screen.blit(sprite, (screen_x, screen_y))

    def is_night(self, time):
        """Check if it's night time"""
        cycle_time = time % DAY_CYCLE_LENGTH
        return cycle_time >= DAY_LENGTH

    def get_background_color(self, current_level, time):
        """Get background color based on level and time"""
        if current_level == LEVEL_CAVE:
            # Always dark in cave
            return CAVE_DARK

        # Jungle - varies with time
        cycle_time = time % DAY_CYCLE_LENGTH

        if cycle_time < DAY_LENGTH:
            # Day time
            return SKY_BLUE
        else:
            # Night time - interpolate to dark
            progress = (cycle_time - DAY_LENGTH) / NIGHT_LENGTH
            if progress < 0.1:
                # Sunset
                t = progress / 0.1
                return self._lerp_color(SKY_BLUE, NIGHT_SKY, t)
            elif progress > 0.9:
                # Sunrise
                t = (progress - 0.9) / 0.1
                return self._lerp_color(NIGHT_SKY, SKY_BLUE, t)
            else:
                # Full night
                return NIGHT_SKY

    def _lerp_color(self, color1, color2, t):
        """Linear interpolation between two colors"""
        return (
            int(color1[0] + (color2[0] - color1[0]) * t),
            int(color1[1] + (color2[1] - color1[1]) * t),
            int(color1[2] + (color2[2]) * t)
        )
