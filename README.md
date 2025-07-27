# Raycasting

A simple **2D raycasting engine** built with **Python** and **Pygame**, simulating basic first-person vision and player movement in a 2D grid-based map.

This project serves as an educational experiment in rendering, geometry, and basic collision detection.

---

## 🧠 Project Overview

This simulation recreates a **pseudo-3D environment** using 2D raycasting.  
The player can move around a grid-based level, and the engine casts rays to detect nearby walls, projecting them as vertical lines — mimicking a 3D perspective.

Key features:
- Custom **raycasting system** with horizontal and vertical collision checks
- Player movement with **rotation and strafing**
- Basic **shading and perspective projection**
- Modular design with `Player`, `Tile`, and map logic separated
- Designed for performance and clarity

---

## 🕹️ Controls

| Key         | Action                    |
|-------------|---------------------------|
| `W`         | Move forward              |
| `S`         | Move backward             |
| `A` / `D`   | Strafe left / right       |
| `←` / `→`   | Rotate view left / right  |
| `ESC` / `X` | Exit (via close button)   |

---

## 🚀 Getting Started

1. Make sure you have **Python 3.8+** installed.
2. Install Pygame:
   ```bash
   pip install pygame
   ```
3. Run the simulation:
   ```bash
   python raycaster.py
   ```

---

## 🧱 Technologies Used

- **Python**
- **Pygame**
- Basic math and trigonometry (`math` module)

---

## 📜 License

This project is made for learning purposes and is released without any warranty.  
Feel free to use, modify, and share it for non-commercial or educational use.

