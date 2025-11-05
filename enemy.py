"""
Enemy classes with AI behavior
"""

import pygame
import random
from constants import *

class Enemy:
    """Base enemy class with AI"""

    def __init__(self, x, y, enemy_type, sprite_manager):
        self.x = x
        self.y = y
        self.width = TILE_SIZE
        self.height = TILE_SIZE * 2
        self.enemy_type = enemy_type
        self.sprite_manager = sprite_manager

        # Physics
        self.velocity_x = 0
        self.velocity_y = 0
        self.on_ground = False
        self.facing_right = True

        # Stats based on type
        if enemy_type == "zombie":
            self.health = 30
            self.max_health = 30
            self.speed = 2
            self.damage = 5
            self.detection_range = 200
        elif enemy_type == "skeleton":
            self.health = 20
            self.max_health = 20
            self.speed = 3
            self.damage = 3
            self.detection_range = 250
        else:
            self.health = 20
            self.max_health = 20
            self.speed = 2
            self.damage = 5
            self.detection_range = 200

        # AI state
        self.target = None
        self.wander_timer = 0
        self.wander_direction = random.choice([-1, 1])
        self.attack_cooldown = 0

    def update(self, world, player, dt=1):
        """Update enemy AI and physics"""
        # Apply gravity
        self.velocity_y += GRAVITY
        if self.velocity_y > MAX_FALL_SPEED:
            self.velocity_y = MAX_FALL_SPEED

        # AI behavior
        self._update_ai(player)

        # Move horizontally with collision
        self.x += self.velocity_x
        self._check_horizontal_collisions(world)

        # Move vertically with collision
        self.y += self.velocity_y
        self._check_vertical_collisions(world)

        # Update attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

    def _update_ai(self, player):
        """Update AI behavior"""
        # Calculate distance to player
        dx = player.x - self.x
        dy = player.y - self.y
        distance = (dx * dx + dy * dy) ** 0.5

        if distance < self.detection_range:
            # Chase player
            self.target = player

            if abs(dx) > 10:  # Dead zone to prevent jittering
                if dx > 0:
                    self.velocity_x = self.speed
                    self.facing_right = True
                else:
                    self.velocity_x = -self.speed
                    self.facing_right = False

                # Jump if blocked
                if self.on_ground and self._is_blocked_ahead():
                    self.velocity_y = JUMP_STRENGTH * 0.8
            else:
                self.velocity_x = 0

            # Attack if close enough
            if distance < 40 and self.attack_cooldown == 0:
                self._attack(player)
                self.attack_cooldown = 60  # 1 second cooldown
        else:
            # Wander
            self.target = None
            self.wander_timer += 1

            if self.wander_timer > 120:  # Change direction every 2 seconds
                self.wander_direction = random.choice([-1, 0, 1])
                self.wander_timer = 0

            self.velocity_x = self.wander_direction * self.speed * 0.5

            # Turn around if blocked
            if self._is_blocked_ahead():
                self.wander_direction *= -1

    def _is_blocked_ahead(self):
        """Check if there's a wall ahead"""
        # Simple check - this would need the world reference
        return False

    def _attack(self, player):
        """Attack the player"""
        player.take_damage(self.damage)

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

        # Flip sprite if facing left
        if not self.facing_right:
            sprite = pygame.transform.flip(sprite, True, False)

        # Draw at camera-relative position
        screen.blit(sprite, (self.x - camera_x, self.y - camera_y))

        # Draw health bar
        if self.health < self.max_health:
            bar_x = self.x - camera_x
            bar_y = self.y - camera_y - 8
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
                self.enemies.remove(enemy)

        # Spawn enemies at night
        if world.is_night(time) and len(self.enemies) < MAX_ENEMIES:
            if random.random() < ENEMY_SPAWN_CHANCE:
                self.spawn_enemy_near_player(player, world)

    def spawn_enemy_near_player(self, player, world):
        """Spawn an enemy near the player but off-screen"""
        # Random position around player
        angle = random.uniform(0, 2 * 3.14159)
        distance = random.uniform(400, 600)

        spawn_x = player.x + distance * (1 if angle < 3.14159 else -1)
        spawn_y = player.y - 100  # Spawn above and let fall

        # Clamp to world bounds
        spawn_x = max(0, min(spawn_x, world.width * TILE_SIZE - TILE_SIZE))

        # Choose enemy type
        enemy_type = random.choice(["zombie", "skeleton"])

        enemy = Enemy(spawn_x, spawn_y, enemy_type, self.sprite_manager)
        self.enemies.append(enemy)

    def draw(self, screen, camera_x, camera_y):
        """Draw all enemies"""
        for enemy in self.enemies:
            enemy.draw(screen, camera_x, camera_y)

    def check_player_collision(self, player):
        """Check if any enemy is colliding with player (for continuous damage)"""
        player_rect = player.get_rect()
        for enemy in self.enemies:
            if enemy.get_rect().colliderect(player_rect):
                return True
        return False
