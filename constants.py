"""
Game constants and configuration settings for Pixel Art Vampire Cave Crawler
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

# Tile colors
SKY_BLUE = (135, 206, 235)
NIGHT_SKY = (25, 25, 50)
GRASS_GREEN = (34, 139, 34)
DIRT_BROWN = (139, 69, 19)
STONE_GRAY = (105, 105, 105)
WOOD_BROWN = (101, 67, 33)
SAND_YELLOW = (238, 214, 175)
IRON_GRAY = (192, 192, 192)
CAVE_DARK = (40, 40, 40)
DIAMOND_CYAN = (0, 255, 255)

# Entity colors
PLAYER_RED = (200, 50, 50)
ZOMBIE_GREEN = (50, 150, 50)
SKELETON_WHITE = (220, 220, 220)

# UI colors
UI_BG = (50, 50, 50, 200)
HEALTH_RED = (255, 0, 0)
HUNGER_ORANGE = (255, 165, 0)
ENERGY_YELLOW = (255, 255, 0)

# Physics
GRAVITY = 0.8
JUMP_STRENGTH = -15
PLAYER_SPEED = 5
MAX_FALL_SPEED = 20

# Player stats
PLAYER_MAX_HEALTH = 100
PLAYER_MAX_HUNGER = 100
HUNGER_DEPLETION_RATE = 0.01  # Per frame
INVENTORY_SIZE = 20

# World generation
WORLD_WIDTH = 200  # In tiles
WORLD_HEIGHT = 100  # In tiles
SURFACE_HEIGHT = 30  # Base surface level
CAVE_START_DEPTH = 40  # Where caves start generating

# Biomes
BIOME_FOREST = "forest"
BIOME_DESERT = "desert"
BIOME_CAVE = "cave"

# Tile types
TILE_AIR = 0
TILE_DIRT = 1
TILE_STONE = 2
TILE_GRASS = 3
TILE_WOOD = 4
TILE_SAND = 5
TILE_IRON_ORE = 6
TILE_DIAMOND_ORE = 7
TILE_CAVE_WALL = 8

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
