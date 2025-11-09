"""
Main game file for Pixel Art Vampire Cave Crawler
"""

import pygame
import sys
from constants import *
from sprites import SpriteManager
from player import Player
from world import World
from enemy import EnemyManager
from ui import UI

class Game:
    """Main game class"""

    def __init__(self):
        # Initialize Pygame
        pygame.init()
        pygame.display.set_caption("Vampire Cave Explorer")

        # Create display
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        # Initialize sprite manager
        self.sprite_manager = SpriteManager()

        # Initialize UI
        self.ui = UI(self.sprite_manager)
        self.ui.init_fonts()

        # Game state
        self.state = STATE_MENU
        self.running = True

        # Game time
        self.game_time = 0

        # Camera
        self.camera_x = 0
        self.camera_y = 0

        # Game objects (initialized when game starts)
        self.world = None
        self.player = None
        self.enemy_manager = None

    def new_game(self):
        """Start a new game"""
        # Create world
        self.world = World(self.sprite_manager)

        # Create player at spawn point
        self.player = Player(self.world.spawn_x, self.world.spawn_y, self.sprite_manager)

        # Create enemy manager
        self.enemy_manager = EnemyManager(self.sprite_manager)

        # Reset game time
        self.game_time = 0

        # Change state
        self.state = STATE_PLAYING

    def run(self):
        """Main game loop"""
        while self.running:
            # Handle events
            self.handle_events()

            # Update game state
            self.update()

            # Draw
            self.draw()

            # Maintain frame rate
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

    def handle_events(self):
        """Handle input events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                self.handle_keydown(event.key)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mousedown(event.button, event.pos)

    def handle_keydown(self, key):
        """Handle key press events"""
        if self.state == STATE_MENU:
            if key == pygame.K_SPACE:
                self.new_game()

        elif self.state == STATE_PLAYING:
            if key == pygame.K_ESCAPE:
                self.state = STATE_PAUSED
            elif key == pygame.K_i:
                self.state = STATE_INVENTORY
            elif key == pygame.K_c:
                self.state = STATE_CRAFTING
            elif key == pygame.K_e:
                # Eat food (example: apple)
                self.player.eat_food(ITEM_APPLE)

        elif self.state == STATE_PAUSED:
            if key == pygame.K_ESCAPE:
                self.state = STATE_PLAYING

        elif self.state == STATE_INVENTORY:
            if key == pygame.K_ESCAPE or key == pygame.K_i:
                self.state = STATE_PLAYING

        elif self.state == STATE_CRAFTING:
            if key == pygame.K_ESCAPE or key == pygame.K_c:
                self.state = STATE_PLAYING

        elif self.state == STATE_DEAD:
            if key == pygame.K_r:
                self.new_game()
            elif key == pygame.K_ESCAPE:
                self.state = STATE_MENU

    def handle_mousedown(self, button, pos):
        """Handle mouse button events"""
        if button == 1:  # Left click
            if self.state == STATE_PLAYING:
                # Mining
                mouse_x, mouse_y = pos
                world_x = mouse_x + self.camera_x
                world_y = mouse_y + self.camera_y
                tile_x = int(world_x // TILE_SIZE)
                tile_y = int(world_y // TILE_SIZE)

                # Check if tile is in range
                player_center_x = self.player.x + self.player.width // 2
                player_center_y = self.player.y + self.player.height // 2
                tile_center_x = tile_x * TILE_SIZE + TILE_SIZE // 2
                tile_center_y = tile_y * TILE_SIZE + TILE_SIZE // 2

                distance = ((player_center_x - tile_center_x) ** 2 +
                           (player_center_y - tile_center_y) ** 2) ** 0.5

                if distance <= 100:  # Mining range
                    self.player.mine_tile(tile_x, tile_y, self.world)

            elif self.state == STATE_CRAFTING:
                # Crafting click
                self.ui.handle_crafting_click(pos, self.player)

    def update(self):
        """Update game logic"""
        if self.state == STATE_PLAYING:
            # Get keyboard state
            keys = pygame.key.get_pressed()

            # Update player
            self.player.update(keys, self.world)

            # Check if player is alive
            if not self.player.is_alive():
                self.state = STATE_DEAD

            # Update enemies
            self.enemy_manager.update(self.world, self.player, self.game_time)

            # Update camera to follow player
            self.update_camera()

            # Increment game time
            self.game_time += 1

            # Handle continuous mining
            if pygame.mouse.get_pressed()[0]:  # Left mouse button held
                mouse_x, mouse_y = pygame.mouse.get_pos()
                world_x = mouse_x + self.camera_x
                world_y = mouse_y + self.camera_y
                tile_x = int(world_x // TILE_SIZE)
                tile_y = int(world_y // TILE_SIZE)

                # Check range
                player_center_x = self.player.x + self.player.width // 2
                player_center_y = self.player.y + self.player.height // 2
                tile_center_x = tile_x * TILE_SIZE + TILE_SIZE // 2
                tile_center_y = tile_y * TILE_SIZE + TILE_SIZE // 2

                distance = ((player_center_x - tile_center_x) ** 2 +
                           (player_center_y - tile_center_y) ** 2) ** 0.5

                if distance <= 100:
                    self.player.mine_tile(tile_x, tile_y, self.world)

    def update_camera(self):
        """Update camera position to follow player"""
        # Center camera on player
        target_x = self.player.x + self.player.width // 2 - SCREEN_WIDTH // 2
        target_y = self.player.y + self.player.height // 2 - SCREEN_HEIGHT // 2

        # Clamp camera to world bounds
        max_camera_x = self.world.width * TILE_SIZE - SCREEN_WIDTH
        max_camera_y = self.world.height * TILE_SIZE - SCREEN_HEIGHT

        self.camera_x = max(0, min(target_x, max_camera_x))
        self.camera_y = max(0, min(target_y, max_camera_y))

    def draw(self):
        """Draw everything"""
        if self.state == STATE_MENU:
            self.ui.draw_menu(self.screen)

        elif self.state in [STATE_PLAYING, STATE_PAUSED, STATE_INVENTORY, STATE_CRAFTING]:
            # Clear screen with background color (changes based on level and time)
            bg_color = self.world.get_background_color(self.player.current_level, self.game_time)
            self.screen.fill(bg_color)

            # Draw world for current level
            self.world.draw(self.screen, self.camera_x, self.camera_y, self.player.current_level)

            # Draw enemies on current level
            self.enemy_manager.draw(self.screen, self.camera_x, self.camera_y, self.player.current_level)

            # Draw player
            self.player.draw(self.screen, self.camera_x, self.camera_y)

            # Draw HUD
            self.ui.draw_hud(self.screen, self.player, self.game_time)

            # Draw crosshair when mining
            if pygame.mouse.get_focused():
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.ui.draw_crosshair(self.screen, mouse_x, mouse_y,
                                      self.camera_x, self.camera_y)

            # Draw overlays based on state
            if self.state == STATE_PAUSED:
                self.ui.draw_pause(self.screen)
            elif self.state == STATE_INVENTORY:
                self.ui.draw_inventory(self.screen, self.player)
            elif self.state == STATE_CRAFTING:
                self.ui.draw_crafting(self.screen, self.player)

        elif self.state == STATE_DEAD:
            self.ui.draw_death(self.screen)

        # Update display
        pygame.display.flip()


def main():
    """Entry point"""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
