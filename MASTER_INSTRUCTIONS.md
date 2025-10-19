# MASTER INSTRUCTIONS (Aether-first Development)

## Philosophy
- Aether (framework) first; game acts as a showcase.
- Build in small, testable increments. Prefer minimal working slices over big refactors.
- Keep original `app.py` intact; all migration happens via `appv2.py` and aether.

## Directory Structure
- `aether/` framework package
  - ecs/, core/, physics/, render/, platformer/, scene/, assets/
- `appv2.py` showcase entrypoint using aether systems
- `test.py` framework sanity runner
- `README.md` aether-first overview
- `devlog.md` session logs and milestones

## Workflow
1) Define the next small goal (feature or fix).
2) Implement in aether as components/systems; expose clean APIs.
3) Integrate in `appv2.py` (keep it thin).
4) Test via `test.py`/`appv2.py`. Tweak Params.
5) Commit with clear message; update `devlog.md` if significant.

## Coding Guidelines
- ECS: data-only Components; logic lives in Systems.
- Systems: deterministic order by `priority`.
- Physics: axis-separated resolution (vertical then horizontal).
- Avoid game-specific code inside framework layers; use params/components to customize.

## Current Milestones
- [x] ECS/core/render/physics scaffolding
- [x] Platformer basic: input, move, coyote/buffer, collisions
- [x] Character wrapper
- [ ] Variable jump height system
- [ ] Wall slide/jump
- [ ] Dash
- [ ] Tilemap service + tile flags (solid/lava/energy)
- [ ] Melee and projectiles
- [ ] Enemies and boss placeholders
- [ ] HUD basics

## Next Targets (Short-term)
1) VariableJumpSystem
2) WallSlideSystem + WallJumpSystem
3) DashSystem

## Medium-term
- Aether Tilemap service with flags and queries
- Melee/Projectile systems; Enemy/Boss scaffolds
- HUDSystem (health/energy)

## Long-term
- Level editor (headless scripts first)
- Save/progression service
- Swappable input backends (gamepad)

## Conventions
- Use `Params` for tunables; no magic numbers in systems.
- Keep `appv2.py` as an integration demo, not a logic dump.
- Prefer small PR-sized commits with clear messages.


