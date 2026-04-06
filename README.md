*Fork of [MCAutoModUpdater](https://github.com/lom3e/MCAutoModUpdater)*

# Mod Updater
Update your server/client mods with a simple python script

## Installation

### Windows
Go to [releases](https://github.com/Paddsladd/mod-updater/releases/latest) and download `update.exe`.
Place `update.exe` in the root of your server/minecraft instance.
Run `update.exe` and modify the generated json file.

### Linux and MacOS
Download `update.py` and `requirements.txt` from [releases](https://github.com/Paddsladd/mod-updater/releases/latest).
Move `update.py` to the root of your server/minecraft instance.
Install the dependencies with:
```
pip install -r requirements.txt
```
Run `update.py` and configure the json file.

## Config
Defaults for `update.json`:
```
{
  "hashAlgorithm": "sha512",
  "mcVersion": "26.1.1",
  "modLoader": "fabric",
  "modsFolder": "mods"
}
```
- hashAlgorithm: The algorithm used for hashing the mods.
    - "sha512" or "sha1"
- mcVersion: The Minecraft version used for downloading mods.
    - The current Minecraft version
- modLoader: The mod loader used.
    - "fabric", "quilt", "forge" or "neoforge"
- modsFolder: The folder for storing mods.
    - "mods"
