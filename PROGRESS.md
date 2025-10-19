# Progress & Next Targets (Sprint 1 - Aether First)

## Whatâ€™s in place
- Aether scaffolding
  - ECS: World, System, Component, EntityId
  - Core: App (loop), Input (edge-press)
  - Render: Camera (smooth follow)
  - Physics: Transform, Kinematics, Collider
  - Platformer layer:
    - Components: Controller, Params, JumpState, PlayerTag
    - Systems: InputSystem, MovementSystem, TileCollisionSystem (axis-ordered)
    - Character wrapper (player.add/get)
- Demos
  - test.py â€“ sanity
  - appv2.py â€“ aether systems + ASCII tiles + camera
- Tuning
  - Coyote time + jump buffer; friction/air damping; speed clamp
  - Fixed horizontal collision climb-through

## Sprint 1 Goals
- Add VariableJumpSystem (hold-to-rise)
- Add WallSlideSystem + WallJumpSystem
- Add DashSystem (impulse + cooldown)
- Aether Tilemap service with flags (solid/lava/energy)
- HUD basics (health/energy, hints)

## Stretch (if time permits)
- Melee + Projectiles
- Enemy (patrol) and Boss placeholder

## Notes
- Keep appv2 thin; behavior lives in aether systems/components.
- Parameterize tunables via Params, avoid magic numbers.
