# Devlog: Elemental Metroidvania

---

## 05-07-25 — Project Kickoff
So this is where it all began. I had just downloaded Warp to test out its capabilities, and I pointed it at one of my older Pygame projects — just a simple one with basic movement and platforming. My task for it: rebuild the same thing, but cleaner, tighter, and ready to expand.

In just a short burst, it managed to:
- Replicate the entire movement/collision system with way less code.
- Add in basic melee and ranged attacks.
- Set up placeholder elemental abilities (like a fire dash).
- Build a working framework with placeholder functions for future features.
- Generate tutorial levels using my ASCII-array method (letters mapped to tiles/objects).
- Implement a simple camera system.
- Put together a normal game loop and a basic UI that explains the controls.

This was enough to kickstart the actual idea: a full elemental metroidvania with proper structure and room to grow.

---

## 16-08-25 — Core Systems & Control Polish
Today was a heavy dev day, and I managed to refine a lot of the foundation into something much more playable and “Hollow Knight–ish” in feel.

### Progress Made
- **Refactored collision system** for cleaner platforming and better edge cases (no more sticking to walls).
- Built a **simplified camera system** (world surface + camera offset).
- Removed duplicate collision logic, tidied up code.
- **Player controls overhaul:**
  - Coyote jump (8 frames).
  - Wall jump & wall slide with proper cooldowns.
  - Variable jump height (tap/hold).
  - Air control + tuned movement physics (accel, friction, max speed, fall cap).
  - Jump buffer (5 frames).
- **Debugging tools:**
  - On-screen info (player state, timers, wall slide state, etc.).
  - Visual overlays for collision boxes and edge detection.
  - Dedicated test levels for coyote jump, wall jump, edge detection.
- **Systems work:**
  - Modularized codebase (player, level, settings, puzzle, progression).
  - Puzzle system framework (switches, crystals, gates).
  - Progression system for saving/loading + region/ability tracking.
  - Early plans for a level editor.

### Technical Challenges
- **Coyote Jump:** Needed precise edge detection + correct order of updates after collision.
- **Wall Jump/Slide:** Cooldowns & state tracking were tricky to stabilize.
- **Variable Jump Height:** Simplified into a responsive, tunable system.
- **Debugging:** Console + visual overlays together made iteration much faster.

### Where We Stand
- Controls feel tight and responsive.
- Collision & camera are solid.
- Codebase is modular and maintainable.
- Puzzle/progression frameworks are set up.
- Debugging tools make testing way smoother.
- Clear roadmap going forward.

---

## Roadmap Ahead
1. Build a proper **level editor**.
2. Expand puzzles with elemental mechanics tied to regions.
3. Enemy & boss AI (different types + mixed-element hidden bosses).
4. Polish menus/HUD and add inventory + map.
5. Replace placeholders with real **art & audio**.
6. Improve save/load system (slots, achievements).
7. Playtesting + balancing loop.

---



## 2025-09-29 — Aether scaffolding + appv2 migration start
Today we began extracting a reusable Python-first engine package (aether) and started migrating the game to it while keeping the original app intact.

What we built
- Aether core
  - ECS: `World`, `System`, `Component`, `EntityId`
  - Core app shell and input: `App`, `Input` (edge-press detection), dt clamp
  - Render: `Camera`
  - Physics components: `Transform`, `Kinematics`, `Collider`
  - Platformer layer:
    - Components: `Controller`, `Params` (tunable physics), `JumpState`, `PlayerTag`
    - Systems: `InputSystem`, `MovementSystem` (no position integration), `TileCollisionSystem` (axis-ordered resolution)
    - Wrapper: `Character(world, x, y, w, h, params)` with `add/get` helpers

- Test harness
  - `test.py` to validate aether loop, input abstraction, and basic physics

- appv2 migration
  - Built tiles from ASCII level, spawned player via `Character`
  - Registered aether systems to drive input, movement, collisions
  - Added coyote time + jump buffering in systems; tuned params (speed=460, jump=-800)
  - Camera follows player; simple rect rendering retained

Bug fixes and polish
- Removed double integration; unified axis-wise collision (vertical then horizontal)
- Fixed horizontal collision to prevent “climbing” through walls
- Added friction/air damping and max speed clamp to stop idle drift

Notes / next steps
- Add VariableJumpSystem (hold-to-rise), WallSlide/WallJump, Dash
- Introduce aether Tilemap service (tile flags for lava/energy), then combat (melee/projectiles), pickups/abilities, enemies/boss, and HUD
- Continue incremental migration; original app remains untouched for reference

