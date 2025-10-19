# Aether - Python Game Development Framework

## Project Vision
**Aether is a Python-first, code-driven game development framework** built on pygame with a clean ECS architecture and modular platformer systems. The primary focus is creating excellent, reusable development tools that make 2D game development in Python intuitive and powerful.

Any games built with aether serve purely as showcases and testing grounds to validate and demonstrate the framework's capabilities.

## Framework Overview
- **ECS Architecture**: Clean Entity-Component-System design with World, Systems, and Components
- **Modular Systems**: Input handling, physics, rendering, and platformer mechanics as separate, reusable modules
- **Developer-Focused**: Clean APIs, comprehensive documentation, and excellent developer experience
- **Extensible Design**: Easy to add new systems, components, and game mechanics
- **Python-First**: Built specifically for Python developers with modern practices and clean code

## Core Framework Components

### ECS System
- **World**: Entity and component management with efficient querying
- **System**: Base class for game logic with priority-based execution order
- **Component**: Data-only classes for entity properties
- **EntityId**: Unique identifiers for entities

### Core Modules
- **App**: Minimal pygame application shell with frame management
- **Input**: Edge-press detection and configurable key mappings
- **Camera**: Smooth following camera system

### Physics & Rendering
- **Transform**: Position and rotation data
- **Kinematics**: Velocity and acceleration with ground detection
- **Collider**: Collision detection with configurable solidity
- **RenderSystem**: Sprite rendering and camera integration

### Platformer Layer
- **Components**: Controller, Params (tunable physics), JumpState, PlayerTag
- **Systems**: InputSystem, MovementSystem, TileCollisionSystem (axis-ordered)
- **Character**: Wrapper class for easy player entity creation

## Current Demo Controls
- **A/D**: Move left/right
- **Space**: Jump (with coyote time + buffer)
- **ESC**: Quit application

## Technical Overview
- **Engine**: Python 3.7+ + pygame 2.0+
- **Architecture**: ECS (Entity-Component-System) with modular design
- **Package**: `aether/` (local framework module)
- **Demo**: `test.py` (framework validation), `appv2.py` (platformer showcase)
- **Requirements**: See `requirements.txt`

## Getting Started
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run framework tests:
   ```bash
   python test.py          # Basic framework validation
   python appv2.py         # Platformer demo showcase
   ```

## Development Notes
This project is being built with the help of AI coding tools like Cursor and Warp, mostly on their free plans. My development cycle is a bit unusual: I usually get 1–2 intense days of coding each month, where I burn through all my free credits/tokens/limits. After that, I switch gears into a slower phase where I make use of ChatGPT and Perplexity to review, understand, and refine the code already generated.

The current MVP came together in about 6–8 hours of AI-assisted coding, with my role mainly being to guide prompts, debug, and catch obvious errors that sometimes loop the agents. Outside those bursts, I spend time reshaping and modeling the code in my own understanding—basically trying to make the AI’s output something I can truly follow and build on.

To keep track of progress (especially with the big gaps between active dev days), I’m also maintaining a devlog. It helps document changes, thought processes, and decisions so that the project doesn’t lose momentum across these cycles.

## License
MIT License

## Contributing
Aether is focused on creating the best possible Python game development framework. Contributions that improve developer experience, add useful systems, or enhance documentation are welcome.

## Roadmap
- **Short-term**: Variable jump, wall mechanics, dash system
- **Medium-term**: Tilemap service, combat systems, enemy framework
- **Long-term**: Advanced rendering, audio integration, level editor tools
