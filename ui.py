"""
UI system for HUD, inventory, crafting, and menus
"""

import pygame
from constants import *

class UI:
    """User interface manager"""

    def __init__(self, sprite_manager):
        self.sprite_manager = sprite_manager
        self.font = None
        self.small_font = None

    def init_fonts(self):
        """Initialize fonts (must be called after pygame.init())"""
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 18)

    def draw_hud(self, screen, player, time):
        """Draw the main HUD (health, hunger, inventory bar)"""
        # Health bar
        self._draw_bar(screen, 20, 20, 200, 20, player.health, player.max_health,
                      HEALTH_RED, "Health")

        # Hunger bar
        self._draw_bar(screen, 20, 50, 200, 20, player.hunger, player.max_hunger,
                      HUNGER_ORANGE, "Hunger")

        # Time display
        cycle_time = time % DAY_CYCLE_LENGTH
        is_night = cycle_time >= DAY_LENGTH
        time_text = "Night" if is_night else "Day"
        time_surface = self.font.render(time_text, True, WHITE)
        screen.blit(time_surface, (SCREEN_WIDTH - 100, 20))

        # Quick inventory (bottom of screen)
        self._draw_quick_inventory(screen, player)

    def _draw_bar(self, screen, x, y, width, height, value, max_value, color, label):
        """Draw a status bar with label"""
        # Background
        pygame.draw.rect(screen, DARK_GRAY, (x, y, width, height))

        # Fill
        fill_width = (value / max_value) * width
        pygame.draw.rect(screen, color, (x, y, fill_width, height))

        # Border
        pygame.draw.rect(screen, WHITE, (x, y, width, height), 2)

        # Label
        text = self.small_font.render(f"{label}: {int(value)}/{int(max_value)}", True, WHITE)
        screen.blit(text, (x + 5, y + 2))

    def _draw_quick_inventory(self, screen, player):
        """Draw quick inventory bar at bottom of screen"""
        slot_size = 50
        slots = 8
        start_x = (SCREEN_WIDTH - (slot_size * slots)) // 2
        start_y = SCREEN_HEIGHT - slot_size - 20

        # Get first 8 items from inventory
        items = list(player.inventory.items())[:slots]

        for i in range(slots):
            x = start_x + i * slot_size
            y = start_y

            # Draw slot background
            if i == player.selected_slot:
                pygame.draw.rect(screen, (100, 100, 100), (x, y, slot_size, slot_size))
            else:
                pygame.draw.rect(screen, (60, 60, 60), (x, y, slot_size, slot_size))

            # Draw border
            pygame.draw.rect(screen, WHITE, (x, y, slot_size, slot_size), 2)

            # Draw item if present
            if i < len(items):
                item_type, quantity = items[i]
                sprite = self.sprite_manager.get_item_sprite(item_type)
                # Scale sprite to fit slot
                scaled_sprite = pygame.transform.scale(sprite, (slot_size - 10, slot_size - 10))
                screen.blit(scaled_sprite, (x + 5, y + 5))

                # Draw quantity
                qty_text = self.small_font.render(str(quantity), True, WHITE)
                screen.blit(qty_text, (x + slot_size - 20, y + slot_size - 20))

    def draw_inventory(self, screen, player):
        """Draw full inventory screen"""
        # Semi-transparent background
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        # Title
        title = self.font.render("Inventory", True, WHITE)
        screen.blit(title, (SCREEN_WIDTH // 2 - 50, 50))

        # Draw inventory grid
        slot_size = 60
        slots_per_row = 10
        start_x = 100
        start_y = 100

        items = list(player.inventory.items())

        for i, (item_type, quantity) in enumerate(items):
            row = i // slots_per_row
            col = i % slots_per_row

            x = start_x + col * slot_size
            y = start_y + row * slot_size

            # Draw slot
            pygame.draw.rect(screen, (60, 60, 60), (x, y, slot_size, slot_size))
            pygame.draw.rect(screen, WHITE, (x, y, slot_size, slot_size), 2)

            # Draw item sprite
            sprite = self.sprite_manager.get_item_sprite(item_type)
            scaled_sprite = pygame.transform.scale(sprite, (slot_size - 10, slot_size - 10))
            screen.blit(scaled_sprite, (x + 5, y + 5))

            # Draw quantity
            qty_text = self.small_font.render(str(quantity), True, WHITE)
            screen.blit(qty_text, (x + slot_size - 20, y + slot_size - 20))

            # Draw item name
            name_text = self.small_font.render(item_type, True, WHITE)
            screen.blit(name_text, (x, y + slot_size + 2))

        # Instructions
        instruction = self.small_font.render("Press I or ESC to close", True, WHITE)
        screen.blit(instruction, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 50))

    def draw_crafting(self, screen, player):
        """Draw crafting screen"""
        # Semi-transparent background
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        # Title
        title = self.font.render("Crafting", True, WHITE)
        screen.blit(title, (SCREEN_WIDTH // 2 - 50, 50))

        # Draw available recipes
        y = 120
        for item_name, ingredients in RECIPES.items():
            # Check if player can craft
            can_craft = True
            for ingredient, amount in ingredients.items():
                if not player.has_items(ingredient, amount):
                    can_craft = False
                    break

            # Draw recipe
            color = (0, 255, 0) if can_craft else (255, 100, 100)
            recipe_text = self.font.render(f"{item_name}: ", True, color)
            screen.blit(recipe_text, (100, y))

            # Draw ingredients
            ingredients_text = ", ".join([f"{amount}x {ingredient}" for ingredient, amount in ingredients.items()])
            ing_surface = self.small_font.render(ingredients_text, True, WHITE)
            screen.blit(ing_surface, (250, y + 3))

            y += 35

        # Instructions
        instruction = self.small_font.render("Press C or ESC to close", True, WHITE)
        screen.blit(instruction, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 50))

        instruction2 = self.small_font.render("Click on item to craft (green = can craft)", True, WHITE)
        screen.blit(instruction2, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT - 30))

    def draw_menu(self, screen):
        """Draw main menu"""
        screen.fill(BLACK)

        # Title
        title_font = pygame.font.Font(None, 72)
        title = title_font.render("Vampire Cave Crawler", True, PLAYER_RED)
        screen.blit(title, (SCREEN_WIDTH // 2 - 350, 150))

        # Subtitle
        subtitle = self.font.render("A Pixel Art Survival Game", True, WHITE)
        screen.blit(subtitle, (SCREEN_WIDTH // 2 - 150, 230))

        # Instructions
        instructions = [
            "Press SPACE to Start",
            "",
            "Controls:",
            "WASD / Arrow Keys - Move",
            "SPACE - Jump",
            "Left Click - Mine blocks",
            "I - Inventory",
            "C - Crafting",
            "ESC - Pause",
            "",
            "Survive the night!",
            "Gather resources and build your base!"
        ]

        y = 300
        for line in instructions:
            text = self.small_font.render(line, True, WHITE)
            screen.blit(text, (SCREEN_WIDTH // 2 - 150, y))
            y += 25

    def draw_pause(self, screen):
        """Draw pause menu"""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        # Pause text
        pause_font = pygame.font.Font(None, 72)
        pause_text = pause_font.render("PAUSED", True, WHITE)
        screen.blit(pause_text, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 - 50))

        # Instructions
        instruction = self.font.render("Press ESC to resume", True, WHITE)
        screen.blit(instruction, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 20))

    def draw_death(self, screen):
        """Draw death screen"""
        screen.fill(BLACK)

        # Death text
        death_font = pygame.font.Font(None, 72)
        death_text = death_font.render("YOU DIED", True, HEALTH_RED)
        screen.blit(death_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 100))

        # Instructions
        instruction = self.font.render("Press R to Respawn", True, WHITE)
        screen.blit(instruction, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2))

        menu_instruction = self.font.render("Press ESC for Menu", True, WHITE)
        screen.blit(menu_instruction, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 40))

    def draw_crosshair(self, screen, mouse_x, mouse_y, camera_x, camera_y):
        """Draw mining crosshair"""
        # Convert mouse position to tile coordinates
        world_x = mouse_x + camera_x
        world_y = mouse_y + camera_y
        tile_x = int(world_x // TILE_SIZE)
        tile_y = int(world_y // TILE_SIZE)

        # Draw highlight on tile
        screen_x = tile_x * TILE_SIZE - camera_x
        screen_y = tile_y * TILE_SIZE - camera_y

        # Semi-transparent white square
        highlight = pygame.Surface((TILE_SIZE, TILE_SIZE))
        highlight.set_alpha(100)
        highlight.fill(WHITE)
        screen.blit(highlight, (screen_x, screen_y))

        # Border
        pygame.draw.rect(screen, WHITE, (screen_x, screen_y, TILE_SIZE, TILE_SIZE), 2)

    def craft_item(self, item_name, player):
        """Attempt to craft an item"""
        if item_name not in RECIPES:
            return False

        recipe = RECIPES[item_name]

        # Check if player has all ingredients
        for ingredient, amount in recipe.items():
            if not player.has_items(ingredient, amount):
                return False

        # Remove ingredients
        for ingredient, amount in recipe.items():
            player.remove_from_inventory(ingredient, amount)

        # Add crafted item
        player.add_to_inventory(item_name, 1)

        # Update player tool if it's a pickaxe
        if "pickaxe" in item_name:
            tool_map = {
                "wooden_pickaxe": TOOL_WOODEN_PICKAXE,
                "stone_pickaxe": TOOL_STONE_PICKAXE,
                "iron_pickaxe": TOOL_IRON_PICKAXE,
                "diamond_pickaxe": TOOL_DIAMOND_PICKAXE
            }
            if item_name in tool_map:
                player.current_tool = tool_map[item_name]

        return True

    def handle_crafting_click(self, mouse_pos, player):
        """Handle mouse click on crafting screen"""
        mouse_x, mouse_y = mouse_pos

        # Calculate which recipe was clicked
        y = 120
        recipe_height = 35

        for i, (item_name, ingredients) in enumerate(RECIPES.items()):
            if 100 <= mouse_x <= 600 and y <= mouse_y <= y + recipe_height:
                # Clicked on this recipe
                return self.craft_item(item_name, player)
            y += recipe_height

        return False
