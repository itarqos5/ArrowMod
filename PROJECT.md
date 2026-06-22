# Arrow & Slots — Project Plan

## Overview

**Mod ID:** `arrowandslots`  
**Display name:** Arrow & Slots  
**Version:** `0.1.0`  
**License:** MIT

### Enhanced Description

> When you draw a bow, Arrow & Slots automatically consumes the arrow placed in the hotbar slot directly above that bow. This keeps your ammunition tied to your weapon layout and removes the need to manually select arrows before every shot.

The original wording was ambiguous, so it has been rewritten to describe the actual mechanic: **the bow uses the arrow in the slot immediately above it**.

## Goals

1. Implement the core behavior once in `common/` and share it across Fabric and NeoForge.
2. Provide a matching Paper plugin for Bukkit-based servers.
3. Keep the mod server-authoritative so it works on dedicated servers and in single-player worlds without requiring a client-side install.
4. Stay minimal: no new items, blocks, or entities unless needed for configuration.

## Architecture

### Modules

| Module | Responsibility |
|--------|----------------|
| `common` | Shared constants, helper logic, and the arrow-selection algorithm. |
| `fabric` | Fabric entry point, event hooks, and packaging. |
| `neoforge` | NeoForge entry point, event hooks, and packaging. |
| `paper` | Paper plugin entry point and event listeners. |

### Technology Stack

- **Minecraft:** 1.21.1 – 26.1.2 (targets 26.1.2)
- **Java:** 21
- **Build tool:** Gradle 8.11+ with the Gradle wrapper
- **Multi-loader plugin:** Architectury Loom
- **Mappings:** Official Mojang mappings
- **Loaders:**
  - Fabric Loader 0.19.3
  - Fabric API 0.152.1+26.1.2
  - NeoForge 26.1.2.76
- **Server platform:**
  - Paper API 26.1.2-R0.1-SNAPSHOT

## Roadmap

1. **Environment setup** (current step)
   - Gradle project with `common`, `fabric`, `neoforge`, and `paper` modules.
   - Skeleton entry-point classes and loader metadata.
   - Documentation and `.gitignore`.
2. **Core logic** (next step)
   - Detect bow draw events.
   - Locate the slot above the bow in the player's hotbar.
   - Consume and shoot the matching arrow.
3. **Loader integration**
   - Wire common logic into Fabric and NeoForge events.
   - Implement the equivalent behavior in the Paper plugin.
4. **Testing & polish**
   - Validate on dedicated server and single-player.
   - Crossbow support and edge cases (empty slot, non-arrow items).

## Suggested Initial Commit Message

```text
feat: implement slot-based arrow selection for Fabric, NeoForge and Paper

- Mixin Player.getProjectile on Fabric/NeoForge to use the arrow from the
  hotbar+9 slot directly above the held bow, falling through to vanilla
  when that slot is empty or doesn't contain an ArrowItem.
- Paper plugin cancels EntityShootBowEvent and launches a fresh
  AbstractArrow of the correct material (ARROW / TIPPED_ARROW /
  SPECTRAL_ARROW), copying potion data for tipped arrows, then decrements
  the upper slot for non-creative players.
- Target Minecraft 26.1.2; metadata declares support for [1.21.1,) so
  servers running anything from 1.21.1 onward can install the mod.
- Switch group id to gg.literal, author to Literal, and refresh docs.
```

## Notes

- The Paper module does not share code with `common/` because Bukkit's API is separate from the Minecraft codebase used by the mod loaders.
- Future iterations may add configuration files per platform.
