"""
Enemy classes with AI behavior for top-down movement
Animals for jungle, creatures for cave
"""

import pygame
import random
from constants import *

class Enemy:
    """Base enemy class with top-down AI"""

    def __init__(self, x, y, enemy_type, sprite_manager, level):
        self.x = x
        self.y = y
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.enemy_type = enemy_type
        self.sprite_manager = sprite_manager
        self.level = level  # Which level this enemy belongs to

        # Movement (top-down)
        self.velocity_x = 0
        self.velocity_y = 0

        # Stats based on type
        if enemy_type == "tiger":
            self.health = 40
            self.max_health = 40
            self.speed = 2.5
            self.damage = 8
            self.detection_range = 150
        elif enemy_type == "snake":
            self.health = 15
            self.max_health = 15
            self.speed = 3
            self.damage = 5
            self.detection_range = 120
        elif enemy_type == "bear":
            self.health = 60
            self.max_health = 60
            self.speed = 1.5
            self.damage = 12
            self.detection_range = 180
        elif enemy_type == "bat":
            self.health = 20
            self.max_health = 20
            self.speed = 3.5
            self.damage = 6
            self.detection_range = 200
        else:
            self.health = 20
            self.max_health = 20
            self.speed = 2
            self.damage = 5
            self.detection_range = 150

        # AI state
        self.target = None
        self.wander_timer = 0
        self.wander_direction_x = random.choice([-1, 0, 1])
        self.wander_direction_y = random.choice([-1, 0, 1])
        self.attack_cooldown = 0

    def update(self, world, player, dt=1):
        """Update enemy AI and physics (top-down)"""
        # Only update if on same level as player
        if self.level != player.current_level:
            return

        # AI behavior
        self._update_ai(player, world)

        # Move with collision detection
        if self.velocity_x != 0:
            self.x += self.velocity_x
            self._check_collisions(world, 'x')

        if self.velocity_y != 0:
            self.y += self.velocity_y
            self._check_collisions(world, 'y')

        # Update attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

    def _update_ai(self, player, world):
        """Update AI behavior for top-down movement"""
        # Calculate distance to player
        dx = player.x - self.x
        dy = player.y - self.y
        distance = (dx * dx + dy * dy) ** 0.5

        if distance < self.detection_range:
            # Chase player
            self.target = player

            # Move towards player
            if distance > 0:
                # Normalize direction
                dir_x = dx / distance
                dir_y = dy / distance

                self.velocity_x = dir_x * self.speed
                self.velocity_y = dir_y * self.speed

            # Attack if close enough
            if distance < 20 and self.attack_cooldown == 0:
                self._attack(player)
                self.attack_cooldown = 60  # 1 second cooldown
        else:
            # Wander
            self.target = None
            self.wander_timer += 1

            if self.wander_timer > 120:  # Change direction every 2 seconds
                self.wander_direction_x = random.choice([-1, 0, 1])
                self.wander_direction_y = random.choice([-1, 0, 1])
                self.wander_timer = 0

            self.velocity_x = self.wander_direction_x * self.speed * 0.5
            self.velocity_y = self.wander_direction_y * self.speed * 0.5

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
                tile = world.get_tile(tile_x, tile_y, self.level)

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
                            # Change wander direction
                            self.wander_direction_x *= -1
                        elif axis == 'y':
                            if self.velocity_y > 0:  # Moving down
                                self.y = tile_rect.top - self.height
                            elif self.velocity_y < 0:  # Moving up
                                self.y = tile_rect.bottom
                            # Change wander direction
                            self.wander_direction_y *= -1

    def _is_solid_tile(self, tile_type):
        """Check if a tile type is solid (blocks movement)"""
        solid_tiles = {
            TILE_TREE, TILE_WATER,  # Jungle
            TILE_CAVE_WALL, TILE_STONE, TILE_IRON_ORE, TILE_DIAMOND_ORE  # Cave
        }
        return tile_type in solid_tiles

    def _attack(self, player):
        """Attack the player"""
        player.take_damage(self.damage)

    def take_damage(self, amount):
        """Take damage"""
        self.health -= amount
        if self.health < 0:
            self.health = 0

    def is_alive(self):
        """Check if enemy is alive"""
        return self.health > 0

    def get_rect(self):
        """Get collision rectangle"""
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen, camera_x, camera_y):
        """Draw enemy sprite"""
        sprite = self.sprite_manager.get_enemy_sprite(self.enemy_type)

        # Draw at camera-relative position
        screen.blit(sprite, (self.x - camera_x, self.y - camera_y))

        # Draw health bar if damaged
        if self.health < self.max_health:
            bar_x = self.x - camera_x
            bar_y = self.y - camera_y - 5
            bar_width = self.width
            bar_height = 3

            # Background
            pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
            # Health
            health_width = (self.health / self.max_health) * bar_width
            pygame.draw.rect(screen, HEALTH_RED, (bar_x, bar_y, health_width, bar_height))


class EnemyManager:
    """Manages enemy spawning and updates"""

    def __init__(self, sprite_manager):
        self.sprite_manager = sprite_manager
        self.enemies = []

    def update(self, world, player, time, dt=1):
        """Update all enemies and handle spawning"""
        # Update existing enemies
        for enemy in self.enemies[:]:
            enemy.update(world, player, dt)

            if not enemy.is_alive():
                # Drop meat when killed
                if random.random() < 0.5:
                    player.add_to_inventory(ITEM_MEAT, 1)
                self.enemies.remove(enemy)

        # Spawn enemies based on level and time
        current_level = player.current_level

        if current_level == LEVEL_JUNGLE:
            # Jungle animals spawn at night
            if world.is_night(time) and len(self.enemies) < MAX_ENEMIES:
                if random.random() < ENEMY_SPAWN_CHANCE:
                    self.spawn_jungle_animal(player, world)
        elif current_level == LEVEL_CAVE:
            # Cave creatures spawn anytime
            if len(self.enemies) < MAX_ENEMIES:
                if random.random() < ENEMY_SPAWN_CHANCE * 0.5:
                    self.spawn_cave_creature(player, world)

    def spawn_jungle_animal(self, player, world):
        """Spawn an animal in the jungle"""
        # Random position around player but off-screen
        angle = random.uniform(0, 2 * 3.14159)
        distance = random.uniform(300, 500)

        spawn_x = player.x + distance * pygame.math.Vector2(1, 0).rotate_rad(angle).x
        spawn_y = player.y + distance * pygame.math.Vector2(0, 1).rotate_rad(angle).y

        # Clamp to world bounds
        spawn_x = max(0, min(spawn_x, world.width * TILE_SIZE - TILE_SIZE))
        spawn_y = max(0, min(spawn_y, world.height * TILE_SIZE - TILE_SIZE))

        # Choose animal type
        animal_type = random.choice(["tiger", "snake", "bear"])

        enemy = Enemy(spawn_x, spawn_y, animal_type, self.sprite_manager, LEVEL_JUNGLE)
        self.enemies.append(enemy)

    def spawn_cave_creature(self, player, world):
        """Spawn a creature in the cave"""
        # Random position around player but off-screen
        angle = random.uniform(0, 2 * 3.14159)
        distance = random.uniform(300, 500)

        spawn_x = player.x + distance * pygame.math.Vector2(1, 0).rotate_rad(angle).x
        spawn_y = player.y + distance * pygame.math.Vector2(0, 1).rotate_rad(angle).y

        # Clamp to world bounds
        spawn_x = max(0, min(spawn_x, world.width * TILE_SIZE - TILE_SIZE))
        spawn_y = max(0, min(spawn_y, world.height * TILE_SIZE - TILE_SIZE))

        # Bat is the main cave enemy
        creature_type = "bat"

        enemy = Enemy(spawn_x, spawn_y, creature_type, self.sprite_manager, LEVEL_CAVE)
        self.enemies.append(enemy)

    def draw(self, screen, camera_x, camera_y, current_level):
        """Draw all enemies on the current level"""
        for enemy in self.enemies:
            if enemy.level == current_level:
                enemy.draw(screen, camera_x, camera_y)

    def check_player_collision(self, player):
        """Check if any enemy is colliding with player (for continuous damage)"""
        player_rect = player.get_rect()
        for enemy in self.enemies:
            if enemy.level == player.current_level:
                if enemy.get_rect().colliderect(player_rect):
                    return True
        return False
