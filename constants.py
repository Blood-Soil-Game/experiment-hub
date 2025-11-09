"""
Game constants and configuration settings for Vampire Cave Explorer
Top-down world exploration game
"""

# Display settings
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
TILE_SIZE = 16  # 16x16 pixel tiles

# Colors (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
LIGHT_GRAY = (192, 192, 192)

# Tile colors - Jungle
SKY_BLUE = (135, 206, 235)
NIGHT_SKY = (25, 25, 50)
GRASS_GREEN = (34, 139, 34)
JUNGLE_GREEN = (0, 100, 0)
DIRT_BROWN = (139, 69, 19)
TREE_GREEN = (0, 128, 0)
TREE_TRUNK = (101, 67, 33)
BUSH_GREEN = (60, 179, 113)
FLOWER_RED = (255, 0, 127)
FLOWER_YELLOW = (255, 215, 0)
WATER_BLUE = (30, 144, 255)

# Tile colors - Cave
STONE_GRAY = (105, 105, 105)
IRON_GRAY = (192, 192, 192)
CAVE_DARK = (40, 40, 40)
CAVE_FLOOR = (60, 60, 60)
DIAMOND_CYAN = (0, 255, 255)
PORTAL_PURPLE = (138, 43, 226)

# Entity colors
PLAYER_RED = (200, 50, 50)
TIGER_ORANGE = (255, 140, 0)
SNAKE_GREEN = (50, 150, 50)
BEAR_BROWN = (139, 69, 19)
BAT_GRAY = (100, 100, 100)

# UI colors
UI_BG = (50, 50, 50, 200)
HEALTH_RED = (255, 0, 0)
HUNGER_ORANGE = (255, 165, 0)
ENERGY_YELLOW = (255, 255, 0)

# Physics (Top-down movement)
PLAYER_SPEED = 3
PLAYER_DIAGONAL_SPEED = 2.1  # Speed when moving diagonally (sqrt(2) factor)

# Player stats
PLAYER_MAX_HEALTH = 100
PLAYER_MAX_HUNGER = 100
HUNGER_DEPLETION_RATE = 0.01  # Per frame
INVENTORY_SIZE = 20

# World generation
WORLD_WIDTH = 150  # In tiles
WORLD_HEIGHT = 150  # In tiles (for each level)

# World levels
LEVEL_JUNGLE = "jungle"
LEVEL_CAVE = "cave"

# Biomes
BIOME_JUNGLE = "jungle"
BIOME_CAVE = "cave"

# Tile types - Jungle
TILE_AIR = 0
TILE_GRASS = 1
TILE_TREE = 2  # Trees to cut for wood
TILE_BUSH = 3  # Decorative
TILE_FLOWER = 4  # Decorative
TILE_WATER = 5  # Impassable
TILE_DIRT = 6

# Tile types - Cave
TILE_CAVE_FLOOR = 10
TILE_CAVE_WALL = 11
TILE_STONE = 12  # Minable stone
TILE_IRON_ORE = 13
TILE_DIAMOND_ORE = 14
TILE_CAVE_ENTRANCE = 15  # Portal between levels
TILE_CAVE_EXIT = 16  # Portal between levels

# Item types
ITEM_WOOD = "wood"
ITEM_STONE = "stone"
ITEM_IRON = "iron"
ITEM_DIAMOND = "diamond"
ITEM_DIRT = "dirt"
ITEM_SAND = "sand"
ITEM_APPLE = "apple"
ITEM_MEAT = "meat"

# Tool types
TOOL_NONE = 0
TOOL_WOODEN_PICKAXE = 1
TOOL_STONE_PICKAXE = 2
TOOL_IRON_PICKAXE = 3
TOOL_DIAMOND_PICKAXE = 4

# Tool properties (mining speed multiplier)
TOOL_SPEEDS = {
    TOOL_NONE: 1.0,
    TOOL_WOODEN_PICKAXE: 2.0,
    TOOL_STONE_PICKAXE: 3.0,
    TOOL_IRON_PICKAXE: 5.0,
    TOOL_DIAMOND_PICKAXE: 8.0
}

# Mining times (in frames)
MINING_BASE_TIME = 60  # 1 second at 60 FPS

# Day/night cycle
DAY_LENGTH = 3600  # 60 seconds at 60 FPS
NIGHT_LENGTH = 2400  # 40 seconds at 60 FPS
DAY_CYCLE_LENGTH = DAY_LENGTH + NIGHT_LENGTH

# Enemy spawning
ENEMY_SPAWN_CHANCE = 0.01  # Per frame during night
MAX_ENEMIES = 20

# Crafting recipes (item: {ingredient: quantity})
RECIPES = {
    "wooden_pickaxe": {"wood": 3},
    "stone_pickaxe": {"wood": 2, "stone": 3},
    "iron_pickaxe": {"wood": 2, "iron": 3},
    "diamond_pickaxe": {"wood": 2, "diamond": 3},
    "wooden_sword": {"wood": 2},
    "stone_sword": {"wood": 1, "stone": 2},
    "workbench": {"wood": 4},
    "furnace": {"stone": 8},
    "chest": {"wood": 8},
    "wall": {"stone": 1},
    "door": {"wood": 2},
}

# Game states
STATE_MENU = "menu"
STATE_PLAYING = "playing"
STATE_INVENTORY = "inventory"
STATE_CRAFTING = "crafting"
STATE_PAUSED = "paused"
STATE_DEAD = "dead"
