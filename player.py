"""
Player class with top-down movement and game mechanics
"""

import pygame
from constants import *

class Player:
    """Player character with top-down movement, inventory, and stats"""

    def __init__(self, x, y, sprite_manager):
        self.x = x
        self.y = y
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.sprite_manager = sprite_manager

        # Movement (top-down)
        self.velocity_x = 0
        self.velocity_y = 0
        self.direction = "down"  # down, up, left, right

        # Current level
        self.current_level = LEVEL_JUNGLE

        # Stats
        self.health = PLAYER_MAX_HEALTH
        self.max_health = PLAYER_MAX_HEALTH
        self.hunger = PLAYER_MAX_HUNGER
        self.max_hunger = PLAYER_MAX_HUNGER

        # Inventory
        self.inventory = {}  # {item_type: quantity}
        self.selected_slot = 0
        self.current_tool = TOOL_NONE

        # Animation
        self.animation_frame = 0
        self.animation_timer = 0
        self.animation_speed = 8  # Frames per animation frame

        # Mining/Cutting
        self.mining_target = None  # (tile_x, tile_y)
        self.mining_progress = 0

    def update(self, keys, world, dt=1):
        """Update player movement and state"""
        # Handle input - 4-directional movement
        self.velocity_x = 0
        self.velocity_y = 0
        moving = False

        # Check for movement keys
        move_up = keys[pygame.K_w] or keys[pygame.K_UP]
        move_down = keys[pygame.K_s] or keys[pygame.K_DOWN]
        move_left = keys[pygame.K_a] or keys[pygame.K_LEFT]
        move_right = keys[pygame.K_d] or keys[pygame.K_RIGHT]

        # Calculate movement direction
        if move_up:
            self.velocity_y = -PLAYER_SPEED
            self.direction = "up"
            moving = True
        if move_down:
            self.velocity_y = PLAYER_SPEED
            self.direction = "down"
            moving = True
        if move_left:
            self.velocity_x = -PLAYER_SPEED
            self.direction = "left"
            moving = True
        if move_right:
            self.velocity_x = PLAYER_SPEED
            self.direction = "right"
            moving = True

        # Adjust speed for diagonal movement
        if self.velocity_x != 0 and self.velocity_y != 0:
            self.velocity_x = PLAYER_DIAGONAL_SPEED if self.velocity_x > 0 else -PLAYER_DIAGONAL_SPEED
            self.velocity_y = PLAYER_DIAGONAL_SPEED if self.velocity_y > 0 else -PLAYER_DIAGONAL_SPEED

        # Move with collision detection
        if self.velocity_x != 0:
            self.x += self.velocity_x
            self._check_collisions(world, 'x')

        if self.velocity_y != 0:
            self.y += self.velocity_y
            self._check_collisions(world, 'y')

        # Update animation
        if moving:
            self.animation_timer += 1
            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0
                self.animation_frame = (self.animation_frame + 1) % 2
        else:
            self.animation_frame = 0
            self.animation_timer = 0

        # Hunger depletion
        self.hunger -= HUNGER_DEPLETION_RATE
        if self.hunger < 0:
            self.hunger = 0
            self.health -= 0.05  # Take damage when hungry

        # Clamp health
        if self.health > self.max_health:
            self.health = self.max_health
        if self.health < 0:
            self.health = 0

        # Check for portal tiles to switch levels
        self._check_portals(world)

    def _check_collisions(self, world, axis):
        """Check and resolve collisions with solid tiles"""
        rect = self.get_rect()

        # Get nearby tiles
        start_x = int(rect.left // TILE_SIZE) - 1
        end_x = int(rect.right // TILE_SIZE) + 2
        start_y = int(rect.top // TILE_SIZE) - 1
        end_y = int(rect.bottom // TILE_SIZE) + 2

        for tile_x in range(start_x, end_x):
            for tile_y in range(start_y, end_y):
                tile = world.get_tile(tile_x, tile_y, self.current_level)

                # Check if tile is solid
                if self._is_solid_tile(tile):
                    tile_rect = pygame.Rect(tile_x * TILE_SIZE, tile_y * TILE_SIZE,
                                           TILE_SIZE, TILE_SIZE)
                    if rect.colliderect(tile_rect):
                        # Resolve collision
                        if axis == 'x':
                            if self.velocity_x > 0:  # Moving right
                                self.x = tile_rect.left - self.width
                            elif self.velocity_x < 0:  # Moving left
                                self.x = tile_rect.right
                        elif axis == 'y':
                            if self.velocity_y > 0:  # Moving down
                                self.y = tile_rect.top - self.height
                            elif self.velocity_y < 0:  # Moving up
                                self.y = tile_rect.bottom

    def _is_solid_tile(self, tile_type):
        """Check if a tile type is solid (blocks movement)"""
        solid_tiles = {
            TILE_TREE, TILE_WATER,  # Jungle
            TILE_CAVE_WALL, TILE_STONE, TILE_IRON_ORE, TILE_DIAMOND_ORE  # Cave
        }
        return tile_type in solid_tiles

    def _check_portals(self, world):
        """Check if player is on a portal tile and switch levels"""
        tile_x = int((self.x + self.width // 2) // TILE_SIZE)
        tile_y = int((self.y + self.height // 2) // TILE_SIZE)

        tile = world.get_tile(tile_x, tile_y, self.current_level)

        if tile == TILE_CAVE_ENTRANCE and self.current_level == LEVEL_JUNGLE:
            # Switch to cave
            self.current_level = LEVEL_CAVE
            # Find exit portal in cave and spawn there
            spawn_x, spawn_y = world.get_portal_position(LEVEL_CAVE, TILE_CAVE_EXIT)
            self.x = spawn_x * TILE_SIZE
            self.y = spawn_y * TILE_SIZE
        elif tile == TILE_CAVE_EXIT and self.current_level == LEVEL_CAVE:
            # Switch to jungle
            self.current_level = LEVEL_JUNGLE
            # Find entrance portal in jungle and spawn there
            spawn_x, spawn_y = world.get_portal_position(LEVEL_JUNGLE, TILE_CAVE_ENTRANCE)
            self.x = spawn_x * TILE_SIZE
            self.y = spawn_y * TILE_SIZE

    def mine_tile(self, tile_x, tile_y, world):
        """Start or continue mining/cutting a tile"""
        if self.mining_target != (tile_x, tile_y):
            # New target
            self.mining_target = (tile_x, tile_y)
            self.mining_progress = 0

        # Calculate mining time based on tool
        tool_speed = TOOL_SPEEDS.get(self.current_tool, 1.0)
        mining_time_needed = MINING_BASE_TIME / tool_speed

        self.mining_progress += 1

        if self.mining_progress >= mining_time_needed:
            # Mining complete!
            tile = world.get_tile(tile_x, tile_y, self.current_level)
            if self._can_mine_tile(tile):
                # Get the resource
                resource = self._get_resource_from_tile(tile)
                if resource:
                    self.add_to_inventory(resource, 1)

                # Remove the tile (replace with appropriate floor)
                if self.current_level == LEVEL_JUNGLE:
                    world.set_tile(tile_x, tile_y, TILE_GRASS, self.current_level)
                else:
                    world.set_tile(tile_x, tile_y, TILE_CAVE_FLOOR, self.current_level)

            # Reset mining
            self.mining_target = None
            self.mining_progress = 0
            return True

        return False

    def _can_mine_tile(self, tile_type):
        """Check if a tile can be mined"""
        minable_tiles = {
            TILE_TREE, TILE_BUSH,  # Jungle
            TILE_STONE, TILE_IRON_ORE, TILE_DIAMOND_ORE  # Cave
        }
        return tile_type in minable_tiles

    def _get_resource_from_tile(self, tile_type):
        """Get the resource item from a tile type"""
        tile_to_resource = {
            TILE_TREE: ITEM_WOOD,
            TILE_BUSH: ITEM_WOOD,
            TILE_STONE: ITEM_STONE,
            TILE_IRON_ORE: ITEM_IRON,
            TILE_DIAMOND_ORE: ITEM_DIAMOND,
        }
        return tile_to_resource.get(tile_type)

    def add_to_inventory(self, item_type, quantity):
        """Add items to inventory"""
        if item_type in self.inventory:
            self.inventory[item_type] += quantity
        else:
            self.inventory[item_type] = quantity

    def remove_from_inventory(self, item_type, quantity):
        """Remove items from inventory"""
        if item_type in self.inventory:
            self.inventory[item_type] -= quantity
            if self.inventory[item_type] <= 0:
                del self.inventory[item_type]
            return True
        return False

    def has_items(self, item_type, quantity):
        """Check if player has enough of an item"""
        return self.inventory.get(item_type, 0) >= quantity

    def eat_food(self, food_type):
        """Consume food to restore hunger"""
        food_values = {
            ITEM_APPLE: 20,
            ITEM_MEAT: 40
        }

        if food_type in food_values and self.has_items(food_type, 1):
            self.remove_from_inventory(food_type, 1)
            self.hunger += food_values[food_type]
            if self.hunger > self.max_hunger:
                self.hunger = self.max_hunger
            return True
        return False

    def take_damage(self, amount):
        """Take damage"""
        self.health -= amount
        if self.health < 0:
            self.health = 0

    def is_alive(self):
        """Check if player is alive"""
        return self.health > 0

    def get_rect(self):
        """Get collision rectangle"""
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen, camera_x, camera_y):
        """Draw player sprite"""
        # Get current sprite based on direction and movement
        is_moving = self.animation_frame != 0 or self.animation_timer != 0
        sprite = self.sprite_manager.get_player_sprite(self.direction, is_moving, self.animation_frame)

        # Draw at camera-relative position
        screen.blit(sprite, (self.x - camera_x, self.y - camera_y))

        # Draw mining progress
        if self.mining_target:
            tile_x, tile_y = self.mining_target
            tool_speed = TOOL_SPEEDS.get(self.current_tool, 1.0)
            mining_time_needed = MINING_BASE_TIME / tool_speed
            progress = self.mining_progress / mining_time_needed

            # Draw progress bar
            bar_x = tile_x * TILE_SIZE - camera_x
            bar_y = tile_y * TILE_SIZE - camera_y - 5
            bar_width = TILE_SIZE
            bar_height = 3

            pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
            pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, bar_width * progress, bar_height))
