# Vampire Cave Explorer

A top-down pixel art exploration game built with Pygame where you explore a procedurally generated jungle, fight animals, gather resources, descend into caves to mine stones and ores, and survive!

## Features

### Core Gameplay
- **Top-Down Exploration** with smooth 4-directional movement
- **Two Distinct Levels**:
  - **Jungle** - Cut trees, fight animals (tigers, snakes, bears), explore during day/night cycle
  - **Cave** - Mine stones and ores (iron, diamond), fight bats in dark caverns
- **Portal System** - Seamlessly travel between jungle and cave levels
- **Resource Gathering** - Cut trees for wood in jungle, mine stones in caves
- **Crafting System** - Create tools, weapons, and structures
- **Inventory Management** - Store and manage your items
- **Survival Mechanics** - Manage health and hunger
- **Animal AI** - Jungle animals hunt you down at night!

### World Features
- 150x150 tile procedurally generated world for each level
- **Jungle Level**:
  - Dense forests with trees to cut
  - Water bodies (impassable)
  - Bushes and flowers
  - Day/night cycle
  - Animals spawn at night (tigers, snakes, bears)
- **Cave Level**:
  - Procedurally generated cave systems
  - Minable stone walls
  - Iron and diamond ore deposits
  - Bat creatures
  - Always dark atmosphere

### Player Mechanics
- **WASD** movement (up, down, left, right)
- Top-down view with 4-directional sprites
- Mining/cutting system with progress indicators
- Tool progression (Wooden → Stone → Iron → Diamond)
- Health and Hunger bars
- Level switching via portals

## Installation

### Requirements
- Python 3.7 or higher
- Pygame 2.0 or higher

### Setup
1. Clone the repository:
```bash
git clone <repository-url>
cd experiment-hub
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the game:
```bash
python game.py
```

## Controls

### Movement
- **W / Up Arrow** - Move Up
- **S / Down Arrow** - Move Down
- **A / Left Arrow** - Move Left
- **D / Right Arrow** - Move Right

### Actions
- **Left Click (Hold)** - Cut trees (jungle) / Mine blocks (cave)
- **I** - Open/Close Inventory
- **C** - Open/Close Crafting Menu
- **E** - Eat food (if you have apples/meat)
- **ESC** - Pause game / Return to menu

### Menu
- **Space** - Start new game (from main menu)
- **R** - Respawn (when dead)

## Gameplay Tips

1. **Start in the Jungle** - You spawn in a grassy area
2. **Cut trees for wood** - Click and hold on dark green tree tiles
3. **Find the purple portal** - This leads to the cave (center of map around 75, 75)
4. **Survive the night** - Animals spawn when it gets dark in the jungle
5. **Explore the cave** - Mine stone, iron, and diamond ores
6. **Use portals** - Walk onto purple portal tiles to switch levels
7. **Craft better tools** - Better pickaxes mine faster
8. **Watch your hunger** - It depletes over time, eat food to restore it
9. **Fight animals** - Defeat them for meat drops

## Game Systems

### Level Switching
- **Jungle → Cave**: Walk onto the purple "Cave Entrance" portal
- **Cave → Jungle**: Walk onto the purple "Cave Exit" portal
- Your position is preserved when switching levels

### Resource Gathering
- **Jungle**: Cut trees and bushes for wood
- **Cave**: Mine stone walls for stone, search for iron and diamond ores
- Mining speed depends on your tool quality
- Progress bar shows mining status

### Health & Hunger
- Hunger depletes slowly over time
- When hunger reaches 0, you take damage
- Eat food (apples, meat) to restore hunger
- Health decreases from animal attacks

### Day/Night Cycle (Jungle Only)
- 100-second cycle (60s day + 40s night)
- Sky changes color based on time
- Animals spawn during nighttime
- Cave is always dark

### Enemy AI
- **Jungle Animals**:
  - **Tigers**: Tough and aggressive (40 HP, 8 damage)
  - **Snakes**: Fast and deadly (15 HP, 5 damage)
  - **Bears**: Slow but powerful (60 HP, 12 damage)
  - Spawn at night in the jungle
- **Cave Creatures**:
  - **Bats**: Quick flyers (20 HP, 6 damage)
  - Spawn anytime in caves
- Enemies detect and chase the player
- Drop meat when defeated (50% chance)

## Crafting Recipes

### Tools
- **Wooden Pickaxe**: 3x Wood
- **Stone Pickaxe**: 2x Wood + 3x Stone
- **Iron Pickaxe**: 2x Wood + 3x Iron
- **Diamond Pickaxe**: 2x Wood + 3x Diamond

### Weapons
- **Wooden Sword**: 2x Wood
- **Stone Sword**: 1x Wood + 2x Stone

### Structures
- **Workbench**: 4x Wood
- **Furnace**: 8x Stone
- **Chest**: 8x Wood
- **Wall**: 1x Stone
- **Door**: 2x Wood

## File Structure

```
experiment-hub/
├── game.py          # Main game loop and entry point
├── constants.py     # Game configuration and constants
├── player.py        # Player class with top-down movement
├── world.py         # Jungle and cave level generation
├── enemy.py         # Animal and creature AI
├── sprites.py       # Top-down sprite generation
├── ui.py            # User interface (HUD, menus, inventory)
├── README.md        # This file
└── requirements.txt # Python dependencies
```

## Technical Details

- **Resolution**: 1280x720 pixels
- **Target FPS**: 60
- **Tile Size**: 16x16 pixels
- **World Size**: 150x150 tiles per level (2400x2400 pixels)
- **Graphics**: Procedurally generated pixel art using colored shapes
- **Movement**: Top-down 4-directional with diagonal support

## Key Differences from Original

This game has been **converted from a platformer to a top-down explorer**:

### What Changed:
- ❌ **Removed**: Gravity, jumping, side-scrolling physics
- ✅ **Added**: 4-directional movement, multiple levels, portals
- 🔄 **Changed**: Side-view sprites → Top-down sprites
- 🔄 **Changed**: Single continuous world → Two separate levels (Jungle & Cave)
- 🔄 **Changed**: Zombies/skeletons → Jungle animals and cave creatures

### What Stayed:
- ✅ Mining and resource gathering
- ✅ Crafting system
- ✅ Inventory management
- ✅ Health and hunger survival
- ✅ Tool progression
- ✅ Enemy AI and combat
- ✅ Day/night cycle (jungle only)

## Credits

Built with Python and Pygame for educational purposes.

## License

This project is open source and available for educational use.
