# Arrow & Slots

A lightweight Minecraft archery helper that lets you focus on aiming, not inventory management.

## Description

When you draw a bow, **Arrow & Slots** automatically picks the arrow from the hotbar slot directly **above** the bow. No more swapping items mid-fight—your ammunition always matches the weapon you are holding.

- Works on dedicated servers (the logic runs server-side).
- Works in single-player because the integrated server handles it.
- Also available as a **Paper** plugin for Bukkit-based servers.

## Supported Platforms

| Platform | Type | Status |
|----------|------|--------|
| Fabric | Mod | implemented |
| NeoForge | Mod | implemented |
| Paper | Plugin | implemented |

## Project Layout

```text
ArrowMod/
├── common/        Shared code used by Fabric and NeoForge
├── fabric/        Fabric loader entry point
├── neoforge/      NeoForge loader entry point
├── paper/         Paper plugin entry point
├── build.gradle   Root build configuration
└── settings.gradle
```

## Supported Versions

| Platform | Supported MC versions | Notes |
|----------|----------------------|-------|
| Fabric | 1.21.1 – 26.1.2 | Built against 1.21.1; metadata declares `>=1.21.1` |
| NeoForge | 1.21.1 – 26.1.2 | NeoForge 21.1+ through 26.1+ |
| Paper | 1.21.1 – 26.1.2 | `api-version: '1.21'` |

The jar is compiled against MC 1.21.1 with official Mojang mappings.
All injected code is wrapped in try-catch with `require = 0` on Mixin targets
so it degrades gracefully instead of crashing if an API changes between versions.

If you hit issues on a newer MC version, rebuild the mod against that version's
toolchain — the Mixin target (`Player#getProjectile`) and class names are
stable across all supported versions under official mappings.

## Requirements

- Java 21 or newer
- Gradle 8.11+ (wrapper included)

## Building

```bash
./gradlew build
```

Built artifacts will be in each subproject's `build/libs/` directory.

## Development Run Configurations

Generate run configs for your IDE with:

```bash
./gradlew genIntelliJRuns
# or
./gradlew genEclipseRuns
```

You can also run a client/server directly from the command line:

```bash
./gradlew :fabric:runClient
./gradlew :fabric:runServer
./gradlew :neoforge:runClient
./gradlew :neoforge:runServer
```

## License

MIT
