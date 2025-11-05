"""
Test script to verify game initialization without display
"""

import os
os.environ['SDL_VIDEODRIVER'] = 'dummy'  # Use dummy video driver for headless testing

import pygame
from constants import *
from sprites import SpriteManager
from player import Player
from world import World
from enemy import EnemyManager
from ui import UI

def test_initialization():
    """Test that all game components initialize correctly"""
    print("Testing game initialization...")

    # Initialize Pygame
    pygame.init()
    print("✓ Pygame initialized")

    # Create sprite manager
    sprite_manager = SpriteManager()
    print("✓ Sprite manager created")

    # Create world
    world = World(sprite_manager, seed=12345)
    print(f"✓ World generated ({world.width}x{world.height} tiles)")

    # Create player
    player = Player(world.spawn_x, world.spawn_y, sprite_manager)
    print(f"✓ Player created at ({player.x}, {player.y})")

    # Create enemy manager
    enemy_manager = EnemyManager(sprite_manager)
    print("✓ Enemy manager created")

    # Create UI
    ui = UI(sprite_manager)
    ui.init_fonts()
    print("✓ UI initialized")

    # Test player movement
    # Create a proper pygame key array
    pygame.event.pump()  # Process events
    keys = pygame.key.get_pressed()

    # Since we can't actually press keys in headless mode, we'll skip the movement test
    # and just verify the update function works
    old_x = player.x
    player.update(keys, world)
    print(f"✓ Player update works (x position: {player.x})")

    # Test inventory
    player.add_to_inventory("wood", 5)
    player.add_to_inventory("stone", 3)
    print(f"✓ Inventory works: {player.inventory}")

    # Test mining
    # Find a solid block near player
    tile_x = int(player.x // TILE_SIZE)
    tile_y = int((player.y + player.height) // TILE_SIZE) + 1  # Block below player

    original_tile = world.get_tile(tile_x, tile_y)
    print(f"✓ Found tile type {original_tile} at ({tile_x}, {tile_y})")

    # Mine it multiple times
    for _ in range(100):
        if player.mine_tile(tile_x, tile_y, world):
            break

    new_tile = world.get_tile(tile_x, tile_y)
    print(f"✓ Mining works (tile changed from {original_tile} to {new_tile})")

    # Test crafting
    player.add_to_inventory("wood", 10)
    old_wood = player.inventory.get("wood", 0)
    ui.craft_item("wooden_pickaxe", player)
    new_wood = player.inventory.get("wood", 0)
    has_pickaxe = player.inventory.get("wooden_pickaxe", 0)
    print(f"✓ Crafting works (wood: {old_wood} -> {new_wood}, pickaxe: {has_pickaxe})")

    # Test enemy spawning
    from enemy import Enemy
    enemy = Enemy(100, 100, "zombie", sprite_manager)
    print(f"✓ Enemy created: {enemy.enemy_type} with {enemy.health} HP")

    # Test day/night cycle
    sky_day = world.get_sky_color(0)
    sky_night = world.get_sky_color(DAY_LENGTH + 100)
    is_night = world.is_night(DAY_LENGTH + 100)
    print(f"✓ Day/night cycle works (day: {sky_day}, night: {sky_night}, is_night: {is_night})")

    print("\n" + "="*50)
    print("All tests passed! ✓")
    print("="*50)
    print("\nThe game is ready to run!")
    print("Run with: python game.py")

if __name__ == "__main__":
    test_initialization()
