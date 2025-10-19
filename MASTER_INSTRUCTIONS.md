# MASTER INSTRUCTIONS (Framework-First Development)

## Philosophy
- **Aether framework is the primary product**; any game serves purely as a showcase and testing ground.
- **Tool quality over game completion**: Focus on creating excellent, reusable development tools.
- **Small, testable increments**: Build features incrementally with clear APIs and comprehensive testing.
- **Developer experience priority**: Make the framework intuitive, well-documented, and easy to extend.

## Directory Structure
- `aether/` framework package
  - ecs/, core/, physics/, render/, platformer/, scene/, assets/
- `appv2.py` showcase entrypoint using aether systems
- `test.py` framework sanity runner
- `README.md` aether-first overview
- `devlog.md` session logs and milestones

## Development Workflow
1) **Define framework goal**: Identify the next small improvement to aether's capabilities.
2) **Implement cleanly**: Build as reusable components/systems with clear APIs.
3) **Test thoroughly**: Validate through framework tests and showcase demos.
4) **Document changes**: Update documentation and devlog with clear explanations.
5) **Iterate and refine**: Use showcase feedback to improve framework design.

## Framework Design Guidelines
- **ECS Architecture**: Data-only Components; all logic lives in Systems.
- **System Priority**: Deterministic execution order via `priority` attribute.
- **Physics Stability**: Axis-separated resolution (vertical then horizontal).
- **Framework Purity**: Avoid game-specific code in framework layers; use parameters/components for customization.
- **API Clarity**: Design clean, intuitive interfaces that make common tasks easy.
- **Extensibility**: Build systems that can be easily extended and composed.

## Framework Development Milestones

### ✅ Completed Foundation
- [x] ECS/core/render/physics scaffolding
- [x] Platformer basic: input, move, coyote/buffer, collisions
- [x] Character wrapper and entity management
- [x] Framework validation and showcase demos

### 🔄 Next Framework Targets (Short-term)
1) **VariableJumpSystem**: Hold-to-rise jump mechanics
2) **WallSlideSystem + WallJumpSystem**: Wall interaction systems
3) **DashSystem**: Impulse movement with cooldown

### 📋 Medium-term Framework Goals
- **Aether Tilemap Service**: Tile-based level system with flags and queries
- **Combat Systems**: Melee and projectile mechanics framework
- **Enemy Framework**: Basic AI systems and behavior patterns
- **HUD System**: UI components for health/energy display

### 🎯 Long-term Framework Vision
- **Advanced Rendering**: Sprite batching, effects, lighting systems
- **Audio Integration**: Sound and music management framework
- **Level Editor Tools**: Framework for creating development tools
- **Save System**: Game state persistence and loading
- **Asset Management**: Texture and resource loading systems
- **Input Backends**: Gamepad and other input device support

## Framework Development Conventions
- **Parameterization**: Use `Params` components for all tunables; eliminate magic numbers in systems.
- **Showcase Clarity**: Keep `appv2.py` as a clean integration demo, not a logic dump.
- **Clean Commits**: Prefer small, focused commits with clear, descriptive messages.
- **Documentation**: Update devlog and documentation for significant framework changes.
- **Testing**: Validate all framework changes through both unit tests and showcase demos.
- **API Design**: Prioritize developer experience and intuitive interfaces over implementation convenience.


