*Fork of [MCAutoModUpdater](https://github.com/lom3e/MCAutoModUpdater)*

# Mod Updater
Update your server/client mods with a simple python script

# Installation

### Windows
Go to [releases](https://github.com/Paddsladd/mod-updater/releases/latest) and download `update.exe`.
Place `update.exe` in the root of your server/minecraft instance.
Run `update.exe` and modify the generated json file.

### Linux and MacOS
Download `update.py` from [releases](https://github.com/Paddsladd/mod-updater/releases/latest).
Move `update.py` to the root of your server/minecraft instance and run it.
Configure the json file with the right info.

# Config example for Fabric 26.1.1
```
{
  "hashAlgorithm": "sha512", // "sha512" or "sha1"
  "mcVersion": "26.1.1", // Minecraft version
  "modLoader": "fabric", // Your mod loader
  "modsFolder": "mods" // The mods folder
}
```
