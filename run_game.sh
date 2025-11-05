#!/bin/bash

# Vampire Cave Crawler - Game Launcher

echo "======================================"
echo "  Vampire Cave Crawler"
echo "  A Pixel Art Survival Game"
echo "======================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed."
    echo "Please install Python 3.7 or higher."
    exit 1
fi

# Check if pygame is installed
if ! python3 -c "import pygame" &> /dev/null; then
    echo "Pygame is not installed."
    echo "Installing pygame..."
    pip install -r requirements.txt
fi

echo "Starting game..."
echo ""

# Run the game
python3 game.py

echo ""
echo "Thanks for playing!"
