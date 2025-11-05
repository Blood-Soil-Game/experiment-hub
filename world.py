"""
World generation and tile management system
"""

import random
import pygame
from constants import *

class World:
    """Procedurally generated tile-based world"""

    def __init__(self, sprite_manager, seed=None):
        self.sprite_manager = sprite_manager
        self.seed = seed if seed else random.randint(0, 999999)
        random.seed(self.seed)

        # Create world grid
        self.width = WORLD_WIDTH
        self.height = WORLD_HEIGHT
        self.tiles = [[TILE_AIR for _ in range(self.height)] for _ in range(self.width)]

        # Biome map
        self.biomes = [BIOME_FOREST] * self.width

        # Generate world
        self._generate_world()

        # Find spawn point
        self.spawn_x, self.spawn_y = self._find_spawn_point()

    def _generate_world(self):
        """Generate the procedural world"""
        # Generate biomes first
        self._generate_biomes()

        # Generate terrain
        self._generate_terrain()

        # Generate caves
        self._generate_caves()

        # Generate ores
        self._generate_ores()

        # Generate trees
        self._generate_trees()

    def _generate_biomes(self):
        """Generate biome distribution"""
        biome_size = 30  # Tiles per biome
        current_biome = BIOME_FOREST

        for x in range(self.width):
            if x % biome_size == 0:
                # Change biome
                current_biome = random.choice([BIOME_FOREST, BIOME_DESERT])
            self.biomes[x] = current_biome

    def _generate_terrain(self):
        """Generate surface terrain using perlin-like noise"""
        height_map = []

        # Generate height map
        for x in range(self.width):
            # Simple sine-wave based terrain
            base_height = SURFACE_HEIGHT
            variation = int(10 * (0.5 + 0.5 * (
                0.5 * self._noise(x * 0.05) +
                0.3 * self._noise(x * 0.1) +
                0.2 * self._noise(x * 0.2)
            )))

            height = base_height + variation
            height_map.append(height)

        # Fill tiles based on height map
        for x in range(self.width):
            surface_y = height_map[x]
            biome = self.biomes[x]

            for y in range(self.height):
                if y < surface_y:
                    # Air
                    self.tiles[x][y] = TILE_AIR
                elif y == surface_y:
                    # Surface layer
                    if biome == BIOME_DESERT:
                        self.tiles[x][y] = TILE_SAND
                    else:
                        self.tiles[x][y] = TILE_GRASS
                elif y < surface_y + 5:
                    # Dirt layer
                    if biome == BIOME_DESERT:
                        self.tiles[x][y] = TILE_SAND
                    else:
                        self.tiles[x][y] = TILE_DIRT
                else:
                    # Stone layer
                    self.tiles[x][y] = TILE_STONE

    def _generate_caves(self):
        """Generate cave systems using cellular automata"""
        # Only generate caves below a certain depth
        for x in range(self.width):
            for y in range(CAVE_START_DEPTH, self.height):
                # Random initial state
                if random.random() < 0.45:
                    self.tiles[x][y] = TILE_AIR

        # Apply cellular automata rules (smoothing)
        for iteration in range(3):
            new_tiles = [[self.tiles[x][y] for y in range(self.height)] for x in range(self.width)]

            for x in range(1, self.width - 1):
                for y in range(CAVE_START_DEPTH, self.height - 1):
                    # Count solid neighbors
                    solid_count = 0
                    for dx in [-1, 0, 1]:
                        for dy in [-1, 0, 1]:
                            if dx == 0 and dy == 0:
                                continue
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < self.width and 0 <= ny < self.height:
                                if self.tiles[nx][ny] != TILE_AIR:
                                    solid_count += 1

                    # Apply rules
                    if solid_count > 4:
                        new_tiles[x][y] = TILE_STONE
                    elif solid_count < 4:
                        new_tiles[x][y] = TILE_AIR

            self.tiles = new_tiles

    def _generate_ores(self):
        """Generate ore deposits"""
        # Iron ore (common, medium depth)
        for _ in range(200):
            x = random.randint(0, self.width - 1)
            y = random.randint(SURFACE_HEIGHT + 10, self.height - 10)
            self._place_ore_vein(x, y, TILE_IRON_ORE, 3)

        # Diamond ore (rare, deep)
        for _ in range(50):
            x = random.randint(0, self.width - 1)
            y = random.randint(SURFACE_HEIGHT + 40, self.height - 5)
            self._place_ore_vein(x, y, TILE_DIAMOND_ORE, 2)

    def _place_ore_vein(self, x, y, ore_type, size):
        """Place a small vein of ore"""
        for _ in range(size):
            if 0 <= x < self.width and 0 <= y < self.height:
                if self.tiles[x][y] == TILE_STONE:
                    self.tiles[x][y] = ore_type

            # Move to adjacent tile
            x += random.choice([-1, 0, 1])
            y += random.choice([-1, 0, 1])

    def _generate_trees(self):
        """Generate trees on the surface"""
        for x in range(0, self.width, 4):
            if self.biomes[x] == BIOME_FOREST and random.random() < 0.3:
                # Find surface
                surface_y = None
                for y in range(self.height):
                    if self.tiles[x][y] == TILE_GRASS:
                        surface_y = y
                        break

                if surface_y and surface_y > 5:
                    # Place tree trunk (3 blocks high)
                    tree_height = random.randint(3, 5)
                    for i in range(tree_height):
                        if surface_y - i - 1 >= 0:
                            self.tiles[x][surface_y - i - 1] = TILE_WOOD

    def _noise(self, x):
        """Simple pseudo-random noise function"""
        # Simple hash-based noise
        n = int(x * 1000)
        n = (n << 13) ^ n
        return (1.0 - ((n * (n * n * 15731 + 789221) + 1376312589) & 0x7fffffff) / 1073741824.0)

    def _find_spawn_point(self):
        """Find a safe spawn point on the surface"""
        # Start near the middle
        spawn_x = self.width // 2

        # Find surface
        for y in range(self.height):
            if self.tiles[spawn_x][y] != TILE_AIR:
                # Found ground, spawn above it
                return spawn_x * TILE_SIZE, (y - 3) * TILE_SIZE

        return spawn_x * TILE_SIZE, 10 * TILE_SIZE

    def get_tile(self, tile_x, tile_y):
        """Get tile at grid coordinates"""
        if 0 <= tile_x < self.width and 0 <= tile_y < self.height:
            return self.tiles[tile_x][tile_y]
        return TILE_STONE  # Return solid tile outside bounds

    def set_tile(self, tile_x, tile_y, tile_type):
        """Set tile at grid coordinates"""
        if 0 <= tile_x < self.width and 0 <= tile_y < self.height:
            self.tiles[tile_x][tile_y] = tile_type

    def get_tile_at_pos(self, x, y):
        """Get tile at world position"""
        tile_x = int(x // TILE_SIZE)
        tile_y = int(y // TILE_SIZE)
        return self.get_tile(tile_x, tile_y)

    def draw(self, screen, camera_x, camera_y):
        """Draw visible tiles"""
        # Calculate visible tile range
        start_x = max(0, int(camera_x // TILE_SIZE) - 1)
        end_x = min(self.width, int((camera_x + SCREEN_WIDTH) // TILE_SIZE) + 2)
        start_y = max(0, int(camera_y // TILE_SIZE) - 1)
        end_y = min(self.height, int((camera_y + SCREEN_HEIGHT) // TILE_SIZE) + 2)

        # Draw tiles
        for x in range(start_x, end_x):
            for y in range(start_y, end_y):
                tile = self.tiles[x][y]
                if tile != TILE_AIR:
                    sprite = self.sprite_manager.get_tile(tile)
                    screen_x = x * TILE_SIZE - camera_x
                    screen_y = y * TILE_SIZE - camera_y
                    screen.blit(sprite, (screen_x, screen_y))

    def is_night(self, time):
        """Check if it's night time"""
        cycle_time = time % DAY_CYCLE_LENGTH
        return cycle_time >= DAY_LENGTH

    def get_sky_color(self, time):
        """Get sky color based on time of day"""
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
            int(color1[2] + (color2[2] - color1[2]) * t)
        )
