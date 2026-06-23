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

- **Minecraft:** 1.21.1 – 26.1.2 (builds against 1.21.1)
- **Java:** 21
- **Build tool:** Gradle 8.11+ with the Gradle wrapper
- **Multi-loader plugin:** Architectury Loom
- **Mappings:** Official Mojang mappings
- **Loaders:**
  - Fabric Loader 0.19.3
  - Fabric API 0.116.12+1.21.1
  - NeoForge 21.1.234
- **Server platform:**
  - Paper API 1.21.1-R0.1-SNAPSHOT

### Version Compatibility Strategy

The mod is compiled against **MC 1.21.1** (the lowest supported version) so
its bytecode uses intermediary / SRG names that are stable across the full
range. Official Mojang mappings guarantee that names like `Player#getProjectile`
and `ArrowItem` are identical from 1.21.1 through 26.1.2.

Defensive measures prevent crashes on any version in the range:

| Layer | Guard |
|-------|-------|
| `ArrowSlotHelper.findArrowAbove` | Full try-catch, returns `null` on any failure |
| `PlayerMixin` (Fabric / NeoForge) | `@Inject(require = 0)` — injection is silently skipped if the target method is absent or renamed |
| `BowShootListener` (Paper) | try-catch around the entire handler; `applyPotionData` has its own inner try-catch for API changes |

If a future MC version renames `Player#getProjectile` or changes its signature,
the Mixin will skip instead of crashing, and the mod simply won't override
ammo selection on that version. Rebuilding against the newer toolchain restores
the behavior.

### Metadata Version Ranges

| File | Dependency | Range | Covers |
|------|-----------|-------|--------|
| `fabric.mod.json` | `minecraft` | `>=1.21.1` | 1.21.1 – 26.1.2+ |
| `fabric.mod.json` | `fabricloader` | `>=0.16.0` | 0.19.3+ |
| `neoforge.mods.toml` | `minecraft` | `[1.21.1,)` | 1.21.1 – 26.1.2+ |
| `neoforge.mods.toml` | `neoforge` | `[21.1.0,)` | 21.1.x through 26.1.x |
| `plugin.yml` | `api-version` | `1.21` | Paper 1.21.1 through 26.1.2 |

## Roadmap

1. **Environment setup** ✔
   - Gradle project with `common`, `fabric`, `neoforge`, and `paper` modules.
   - Skeleton entry-point classes and loader metadata.
   - Documentation and `.gitignore`.
2. **Core logic** ✔
   - `ArrowSlotHelper` locates the arrow in hotbar slot +9.
   - Wrapped in try-catch for version safety.
3. **Loader integration** ✔
   - Fabric/NeoForge: Mixin on `Player#getProjectile` (`require = 0`).
   - Paper: `EntityShootBowEvent` listener with defensive arrow launch.
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
- Build against MC 1.21.1; metadata declares support for [1.21.1,) so
  the single jar works across the full 1.21.1–26.1.2 range.
- All injected code is wrapped in try-catch with require=0 on Mixin
  targets so the mod degrades gracefully instead of crashing if an API
  changes between MC versions.
- Switch group id to gg.literal, author to Literal, and refresh docs.
```

## Notes

- The Paper module does not share code with `common/` because Bukkit's API is separate from the Minecraft codebase used by the mod loaders.
- The single jar works across the 1.21.1 – 26.1.2 range because official Mojang mappings keep class and method names stable. The Mixin target `Player#getProjectile(ItemStack)` has the same name and signature in both versions.
- If a future MC version breaks the Mixin target, `require = 0` causes the injection to be silently skipped rather than crashing the game. The mod just stops overriding ammo selection on that version.
- Rebuilding against the newer MC toolchain (changing `minecraft_version` in `gradle.properties` and updating loader/API versions) restores full behavior.
- Future iterations may add configuration files per platform.
