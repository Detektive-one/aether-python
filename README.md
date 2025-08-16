# Elemental Metroidvania

## Project Vision
Elemental Metroidvania is a 2D platformer inspired by games like Hollow Knight and Momodora, with a focus on elemental abilities, tight controls, and puzzle-driven progression. The player explores five elemental regions (Earth, Fire, Water, Air, Space), each with unique mechanics, enemies, and bosses. The goal is to restore balance to the elemental realms by collecting fragments, solving puzzles, and defeating bosses.

## Gameplay Overview
- **Explore**: Traverse interconnected regions, each with 5 main levels and 2 hidden levels.
- **Abilities**: Unlock and master elemental powers unique to each region. Only one ability per region can be carried forward, but hidden bosses grant permanent cross-region abilities.
- **Puzzles**: Solve region-specific puzzles using your abilities to collect fragments and progress.
- **Combat**: Face off against enemies and challenging bosses using melee, ranged, and elemental attacks.
- **Progression**: Collect fragments to form elemental crystals and stabilize each region. Defeat all bosses to restore balance.

## Key Features
- **Elemental Regions**: Earth, Fire, Water, Air, Space, each with unique mechanics and puzzles.
- **Abilities**: 3 unlockable abilities per region, plus special permanent abilities from hidden bosses.
- **Tight Controls**: Responsive movement, coyote jump, wall jump, variable jump height, and air control.
- **Puzzle System**: Modular, reusable puzzle framework for elemental challenges.
- **Boss Fights**: 15+ unique bosses, including mixed-element hidden bosses.
- **Save/Load**: Persistent progression, ability unlocks, and region completion.
- **Debug & Dev Tools**: Visual debugging, test levels, and a planned level editor.

## Controls
- **WASD**: Move
- **Space**: Jump (hold for higher jump, tap for short hop)
- **Q/E/R**: Use abilities
- **Left Click**: Melee attack
- **Right Click**: Ranged attack
- **ESC**: Pause/Menu
- **Tab**: Inventory (planned)

## Technical Overview
- **Engine**: Python + Pygame
- **Modular Codebase**: Separated into player, level, settings, puzzle, and progression modules.
- **Level Format**: ASCII arrays for prototyping, with a planned visual level editor.
- **Debugging**: On-screen and console debug info for player state, collisions, and mechanics.
- **Requirements**: See `requirements.txt` (pygame>=2.0.0)

## Getting Started
1. Install Python 3.7+ and Pygame:
   ```
   pip install -r requirements.txt
   ```
2. Run the game:
   ```
   python app.py
   ```

## Development Notes
This project is being built with the help of AI coding tools like Cursor and Warp, mostly on their free plans. My development cycle is a bit unusual: I usually get 1–2 intense days of coding each month, where I burn through all my free credits/tokens/limits. After that, I switch gears into a slower phase where I make use of ChatGPT and Perplexity to review, understand, and refine the code already generated.

The current MVP came together in about 6–8 hours of AI-assisted coding, with my role mainly being to guide prompts, debug, and catch obvious errors that sometimes loop the agents. Outside those bursts, I spend time reshaping and modeling the code in my own understanding—basically trying to make the AI’s output something I can truly follow and build on.

To keep track of progress (especially with the big gaps between active dev days), I’m also maintaining a devlog. It helps document changes, thought processes, and decisions so that the project doesn’t lose momentum across these cycles.

## License
MIT (I don't know much about this)


## Working Snapshots: [16-08-2025]
Starting menu
<img width="1478" height="1007" alt="ss1" src="https://github.com/user-attachments/assets/f0adb934-395d-4851-9980-b011720ef9f9" />

Game as of now
<img width="1498" height="1015" alt="ss2" src="https://github.com/user-attachments/assets/c9596d72-513d-4785-88ee-396ddd66b833" />
