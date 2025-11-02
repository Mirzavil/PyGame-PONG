# 🏓 Pong (Pygame Edition)

A simple **Pong clone** built with [Pygame](https://www.pygame.org/).  
This project started as me experimenting with Pygame, but it now includes a menu, single-player mode with AI, two-player mode, scoring, and pause/resume functionality.

---

## 🎮 Features
- **Main Menu**: Choose between Single Player or Two Players (via mouse or keyboard).  
- **Single Player**: Play against a basic AI paddle.  
- **Two Players**: Local multiplayer (W/S for Player 1, Arrow Keys for Player 2).  
- **Pause/Resume**: After each point, press `SPACE` to continue.  
- **Score Tracking**: Displays current score at the top of the screen.  
- **Smooth Gameplay**: Delta-time based movement for consistent speed.  

---

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/Mirzavil/PyGame-PONG.git
cd pong-pygame
```
### 2. Install dependencies
Make sure you have Python 3 installed, then install Pygame:
```bash
pip install pygame
```
### 3. Run the game
```bash
python game.py
```
---

## 🎹 Controls

| Action             | Player 1 | Player 2 (Multiplayer) |
|---------------------|----------|-------------------------|
| Move Up            | W        | ↑ (Up Arrow)           |
| Move Down          | S        | ↓ (Down Arrow)         |
| Select Menu Option | 1 / 2 or Mouse Click | 1 / 2 or Mouse Click |
| Resume After Score | SPACE    | SPACE                  |
| Quit Game          | Close window | Close window        |

---

## 📝 Notes
- This is a learning project to get familiar with Pygame.  
- The AI is intentionally simple - it just follows the ball’s vertical position.  
- Feel free to fork and extend it (e.g., add sound effects, menus, difficulty levels, or power-ups).  
