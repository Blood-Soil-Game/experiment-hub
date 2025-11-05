# Vampire Cave Crawler

A pixel art survival game built with Pygame where you explore a procedurally generated world, gather resources, build your base, and survive the night!

## Features

### Core Gameplay
- **2D Side-scrolling Platformer** with smooth physics
- **Procedurally Generated World** with different biomes (Forest, Desert, Caves)
- **Day/Night Cycle** - Enemies spawn at night!
- **Resource Gathering** - Mine blocks to collect materials
- **Crafting System** - Create tools, weapons, and structures
- **Inventory Management** - Store and manage your items
- **Survival Mechanics** - Manage health and hunger
- **Enemy AI** - Zombies and Skeletons that hunt you down!

### World Features
- 200x100 tile procedurally generated world
- Multiple biomes with unique terrain
- Underground cave systems
- Ore deposits (Iron, Diamond)
- Trees and natural resources
- Smooth camera following system

### Player Mechanics
- WASD/Arrow keys for movement
- Jump physics with gravity
- Mining system with progress indicators
- Tool progression (Wooden → Stone → Iron → Diamond)
- Health and Hunger bars
- Animated walking sprites

### Crafting & Progression
- Workbenches for crafting
- Tool tiers that affect mining speed
- Weapons for combat
- Building blocks (walls, doors)
- Storage systems (chests)
- Smelting (furnaces)

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
- **W / Up Arrow / Space** - Jump
- **A / Left Arrow** - Move Left
- **D / Right Arrow** - Move Right

### Actions
- **Left Click (Hold)** - Mine blocks
- **I** - Open/Close Inventory
- **C** - Open/Close Crafting Menu
- **E** - Eat food (if you have apples/meat)
- **ESC** - Pause game / Return to menu

### Menu
- **Space** - Start new game (from main menu)
- **R** - Respawn (when dead)

## Gameplay Tips

1. **Start by gathering wood** - Punch/mine the brown tree blocks
2. **Craft a wooden pickaxe** - Press C to open crafting (requires 3 wood)
3. **Mine stone** - Use your pickaxe on gray stone blocks
4. **Upgrade your tools** - Better tools mine faster!
5. **Watch your hunger** - It depletes over time. Gather apples or meat!
6. **Survive the night** - Enemies spawn when the sky turns dark
7. **Explore caves** - Find rare ores deep underground
8. **Build a base** - Place blocks to create shelters

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

## Game Systems

### Mining
- Click and hold on blocks to mine them
- Mining speed depends on your tool
- Better tools = faster mining
- Progress bar shows mining status

### Health & Hunger
- Hunger depletes slowly over time
- When hunger reaches 0, you take damage
- Eat food to restore hunger
- Health regenerates when well-fed

### Day/Night Cycle
- Each cycle lasts 100 seconds (60 day + 40 night)
- Sky changes color based on time
- Enemies spawn during night
- Build shelter before nightfall!

### Enemy AI
- Enemies detect players within range
- They chase and attack when close
- Different enemy types have different stats
- Zombies: Slow but tough
- Skeletons: Fast but fragile

## File Structure

```
experiment-hub/
├── game.py          # Main game loop and entry point
├── constants.py     # Game configuration and constants
├── player.py        # Player class with physics and mechanics
├── world.py         # World generation and tile management
├── enemy.py         # Enemy AI and spawn system
├── sprites.py       # Sprite generation and management
├── ui.py            # User interface (HUD, menus, inventory)
├── README.md        # This file
└── requirements.txt # Python dependencies
```

## Technical Details

- **Resolution**: 1280x720 pixels
- **Target FPS**: 60
- **Tile Size**: 16x16 pixels
- **World Size**: 200x100 tiles (3200x1600 pixels)
- **Graphics**: Procedurally generated pixel art using colored rectangles

## Future Enhancements

Potential additions for future versions:
- More enemy types
- Boss battles
- Weather effects
- More biomes
- Advanced building system
- Multiplayer support
- Sound effects and music
- Save/Load system
- More crafting recipes
- Farming system
- NPCs and trading

## Credits

Built with Python and Pygame for educational purposes.

## License

This project is open source and available for educational use.
