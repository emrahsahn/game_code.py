# Lords of the Polywarphism

## Project Overview
This project, titled **"Lords of the Polywarphism"**, is a multiplayer war game developed in a 2-dimensional matrix world. The game emphasizes strategic gameplay with different warrior types, each having unique abilities, and supports up to 4 players, where each player takes turns to deploy and control warriors to defeat opponents and dominate the game world.

---

## Game Description

- **World Size:** Players can choose the world size at the start, selecting from 16x16, 24x24, or 32x32 grids. The grid size is restricted between 8x8 (minimum) and 32x32 (maximum).
- **Player Count:** The game requires at least 1 real player and can support up to 4 players.
- **Turn-Based Strategy:** Players take turns to produce up to 2 warriors per turn, given they have enough resources.
- **Warrior Placement:** Players specify the coordinates for each warrior’s placement. Warriors must be placed adjacent to an existing unit.
- **Resources:** Players gain resources each turn and must manage them strategically.
- **Game Winning Condition:** The last player remaining or the player controlling 60% of the world wins.

---

## Warrior Types

| Warrior   | Resource Cost | Health | Attack Target                   | Damage            | Horizontal Range | Vertical Range | Diagonal Range |
|-----------|---------------|--------|---------------------------------|-------------------|------------------|----------------|----------------|
| Guardian  | 10            | 80     | All enemies in range           | -20 health        | 1                | 1              | 1              |
| Archer    | 20            | 30     | 3 enemies with highest health  | -60% health       | 2                | 2              | 2              |
| Artillery | 50            | 30     | 1 enemy with highest health    | -100% health      | 2                | 2              | 0              |
| Cavalry   | 30            | 40     | 2 most expensive enemies       | -30 health        | 0                | 0              | 3              |
| Healer    | 10            | 100    | 3 allied units with lowest health | +50% health   | 2                | 2              | 2              |

---

## Technical Requirements

- **Class Structure:** All warrior types inherit from a single base class to ensure modular design.
- **Polymorphism:** Implement polymorphism to allow players to select different warriors dynamically.
- **World Creation:** The game world is created as a standard 2D vector.
- **Object-Oriented Design:** The entire project follows object-oriented programming (OOP) principles and best practices.

---

## How to Play

1. Set the game world size and player count.
2. Players take turns, manage resources, and deploy warriors strategically.
3. When all players have completed their turns, warriors on the field perform actions.
4. The game continues until a player dominates 60% of the world or is the last one remaining.

---

## Installation and Setup

1. Clone this repository:
    ```bash
    git clone https://github.com/yourusername/LordsOfThePolywarphism.git
    ```
2. Compile and run the project following standard compilation steps (ensure your compiler supports C++ polymorphism if applicable).



## VISUALIZATION 
![Ekran görüntüsü 2024-11-05 122448](https://github.com/user-attachments/assets/8b58cefa-991f-4e2e-9b01-5ffaf87d139a)

![Ekran görüntüsü 2024-11-05 122826](https://github.com/user-attachments/assets/3081bff6-e0b6-4e65-81c2-4b49c22f5b49)
![Ekran görüntüsü 2024-11-05 122854](https://github.com/user-attachments/assets/129dc630-a1af-4edd-b07b-fa46af3d4f19)
![Ekran görüntüsü 2024-11-05 122906](https://github.com/user-attachments/assets/c0fc6839-c0f0-4ab1-94e9-5898996f05b1)
