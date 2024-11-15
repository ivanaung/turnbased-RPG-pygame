Turn-Based Python RPG Battle Game
![image](https://github.com/user-attachments/assets/a2944342-7caf-461a-a1c5-4bed5dc5939c)

This project is a Turn-Based RPG Battle Game created using Python and the Pygame library. The game simulates a battle between two players (or a player and an AI) in which each participant takes turns to perform actions such as attacking, defending, or using special abilities. This game is designed as a school project to demonstrate programming knowledge in Python, game logic, and Pygame development.

Features
* Turn-Based Gameplay: Players alternate turns to take actions.
* Simple Battle Mechanics: Basic actions such as attack, defend, and special moves.
* Interactive Visuals: Game board and player animations created using Pygame.
* Score Tracking: Keeps track of health and status to determine the winner.

![image](https://github.com/user-attachments/assets/011da118-2036-46d5-b029-c4de6747283b)

  
Installation
1. Ensure Python 3.x is installed on your computer.
2. Install visual code and open folder in VS Code
3. Install Pygame by running in visual code terminal:
4.   pip install pygame
5.   pip install pygame-menu
6. Clone this repository or download the project files.

![image](https://github.com/user-attachments/assets/b9abcaf6-a84b-49cb-9b89-8840d4740ec5)

   
How to Play
1. Start the Game: Run the main.py script to start the game:
2.    python main.py
     
4. Game Controls:
    * Usse Mouse to control attack or defence      
      
5. Objective: Reduce your opponent's health to zero before yours runs out to win the match.
Game Structure
* Initialization: The game initializes by setting up the game window and basic parameters such as player health, turn indicators, and game states.
* Turn Logic: The main game loop handles events, updating the screen, and switching between players when an action is completed.
* Actions: Players can perform different actions such as:
    * Attack: Reduces the opponent's health by a set amount.
    * Defend: Reduces incoming damage for the next opponent's turn.
    * Special Move: Powerful action with cooldown or heal
      




