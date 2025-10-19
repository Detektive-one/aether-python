# Aether (Python Game Framework) + Showcase Game

## Project Vision
I’m building a Python-first, code-driven game framework (aether) with a clean ECS and platformer layer on top of pygame. The game will be a showcase/byproduct: I’ll use aether to build something fun, but the primary focus now is the framework itself, polishing its modules and dev ergonomics.

## Gameplay Overview
- **Explore**: Traverse interconnected regions, each with 5 main levels and 2 hidden levels.
- **Abilities**: Unlock and master elemental powers unique to each region. Only one ability per region can be carried forward, but hidden bosses grant permanent cross-region abilities.
- **Puzzles**: Solve region-specific puzzles using your abilities to collect fragments and progress.
- **Combat**: Face off against enemies and challenging bosses using melee, ranged, and elemental attacks.
- **Progression**: Collect fragments to form elemental crystals and stabilize each region. Defeat all bosses to restore balance.

## Aether Highlights (work-in-progress)
- **ECS core**: World, Systems, Components
- **Core**: App shell, Input abstraction (edge-press), dt clamp
- **Render**: Camera (smooth follow)
- **Physics**: Transform, Kinematics, Collider
- **Platformer layer**:
  - Components: Controller, Params (tunable physics), JumpState
  - Systems: InputSystem, MovementSystem, TileCollisionSystem (axis-ordered)
  - Character wrapper (player.add/get)

## Controls (current test/demo)
- **A/D**: Move
- **Space**: Jump (with coyote time + buffer)
- **ESC**: Quit

## Technical Overview
- **Engine**: Python + pygame
- **Package**: `aether/` (install-less local module for now)
- **Level Format**: ASCII prototypes → future aether Tilemap
- **Demo**: `test.py` (framework sanity), `appv2.py` (framework + level tiles)
- **Requirements**: See `requirements.txt` (pygame>=2.0.0)

## Getting Started
1. Install Python 3.7+ and Pygame:
   ```
   pip install -r requirements.txt
   ```
2. Run the demo tests:
   ```
   python test.py
   python appv2.py
   ```

## Development Notes
This project is being built with the help of AI coding tools like Cursor and Warp, mostly on their free plans. My development cycle is a bit unusual: I usually get 1–2 intense days of coding each month, where I burn through all my free credits/tokens/limits. After that, I switch gears into a slower phase where I make use of ChatGPT and Perplexity to review, understand, and refine the code already generated.

The current MVP came together in about 6–8 hours of AI-assisted coding, with my role mainly being to guide prompts, debug, and catch obvious errors that sometimes loop the agents. Outside those bursts, I spend time reshaping and modeling the code in my own understanding—basically trying to make the AI’s output something I can truly follow and build on.

To keep track of progress (especially with the big gaps between active dev days), I’m also maintaining a devlog. It helps document changes, thought processes, and decisions so that the project doesn’t lose momentum across these cycles.

## License
MIT (I don't know much about this)


## Working Snapshots
Keeping screenshots light until aether stabilizes; the showcase game will follow.
