"""
Player class with movement, physics, and game mechanics
"""

import pygame
from constants import *

class Player:
    """Player character with movement, inventory, and stats"""

    def __init__(self, x, y, sprite_manager):
        self.x = x
        self.y = y
        self.width = TILE_SIZE
        self.height = TILE_SIZE * 2
        self.sprite_manager = sprite_manager

        # Physics
        self.velocity_x = 0
        self.velocity_y = 0
        self.on_ground = False
        self.facing_right = True

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

        # Mining
        self.mining_target = None  # (tile_x, tile_y)
        self.mining_progress = 0
        self.mining_time = 0

    def update(self, keys, world, dt=1):
        """Update player physics and state"""
        # Handle input
        self.velocity_x = 0

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.velocity_x = -PLAYER_SPEED
            self.facing_right = False
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.velocity_x = PLAYER_SPEED
            self.facing_right = True

        # Jumping
        if (keys[pygame.K_w] or keys[pygame.K_UP] or keys[pygame.K_SPACE]) and self.on_ground:
            self.velocity_y = JUMP_STRENGTH
            self.on_ground = False

        # Apply gravity
        self.velocity_y += GRAVITY
        if self.velocity_y > MAX_FALL_SPEED:
            self.velocity_y = MAX_FALL_SPEED

        # Move horizontally with collision
        self.x += self.velocity_x
        self._check_horizontal_collisions(world)

        # Move vertically with collision
        self.y += self.velocity_y
        self._check_vertical_collisions(world)

        # Update animation
        if self.velocity_x != 0:
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

    def _check_horizontal_collisions(self, world):
        """Check and resolve horizontal collisions with tiles"""
        rect = self.get_rect()

        # Get nearby tiles
        start_x = int(rect.left // TILE_SIZE) - 1
        end_x = int(rect.right // TILE_SIZE) + 1
        start_y = int(rect.top // TILE_SIZE)
        end_y = int(rect.bottom // TILE_SIZE) + 1

        for tile_x in range(start_x, end_x):
            for tile_y in range(start_y, end_y):
                tile = world.get_tile(tile_x, tile_y)
                if tile != TILE_AIR:
                    tile_rect = pygame.Rect(tile_x * TILE_SIZE, tile_y * TILE_SIZE,
                                           TILE_SIZE, TILE_SIZE)
                    if rect.colliderect(tile_rect):
                        # Resolve collision
                        if self.velocity_x > 0:  # Moving right
                            self.x = tile_rect.left - self.width
                        elif self.velocity_x < 0:  # Moving left
                            self.x = tile_rect.right

    def _check_vertical_collisions(self, world):
        """Check and resolve vertical collisions with tiles"""
        rect = self.get_rect()
        self.on_ground = False

        # Get nearby tiles
        start_x = int(rect.left // TILE_SIZE)
        end_x = int(rect.right // TILE_SIZE) + 1
        start_y = int(rect.top // TILE_SIZE) - 1
        end_y = int(rect.bottom // TILE_SIZE) + 1

        for tile_x in range(start_x, end_x):
            for tile_y in range(start_y, end_y):
                tile = world.get_tile(tile_x, tile_y)
                if tile != TILE_AIR:
                    tile_rect = pygame.Rect(tile_x * TILE_SIZE, tile_y * TILE_SIZE,
                                           TILE_SIZE, TILE_SIZE)
                    if rect.colliderect(tile_rect):
                        # Resolve collision
                        if self.velocity_y > 0:  # Falling down
                            self.y = tile_rect.top - self.height
                            self.velocity_y = 0
                            self.on_ground = True
                        elif self.velocity_y < 0:  # Moving up
                            self.y = tile_rect.bottom
                            self.velocity_y = 0

    def mine_tile(self, tile_x, tile_y, world):
        """Start or continue mining a tile"""
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
            tile = world.get_tile(tile_x, tile_y)
            if tile != TILE_AIR:
                # Get the resource
                resource = self._get_resource_from_tile(tile)
                if resource:
                    self.add_to_inventory(resource, 1)

                # Remove the tile
                world.set_tile(tile_x, tile_y, TILE_AIR)

            # Reset mining
            self.mining_target = None
            self.mining_progress = 0
            return True

        return False

    def _get_resource_from_tile(self, tile_type):
        """Get the resource item from a tile type"""
        tile_to_resource = {
            TILE_DIRT: ITEM_DIRT,
            TILE_STONE: ITEM_STONE,
            TILE_GRASS: ITEM_DIRT,
            TILE_WOOD: ITEM_WOOD,
            TILE_SAND: ITEM_SAND,
            TILE_IRON_ORE: ITEM_IRON,
            TILE_DIAMOND_ORE: ITEM_DIAMOND,
            TILE_CAVE_WALL: ITEM_STONE,
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
        # Get current sprite
        if self.velocity_x != 0:
            sprite = self.sprite_manager.get_player_sprite("walk", self.animation_frame)
        else:
            sprite = self.sprite_manager.get_player_sprite("idle")

        # Flip sprite if facing left
        if not self.facing_right:
            sprite = pygame.transform.flip(sprite, True, False)

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
