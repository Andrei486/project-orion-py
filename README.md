# Project Orion character sheet creator
## Version
0.1 - CLI

## Description
This command-line application creates ship character sheets for Project Orion ships. This includes stats, weapons, bays, and systems.

## Python Usage

Follow the steps below if one or more of the following applies:
- you want to modify the Compendium files locally and use those updated versions
- you want to use better-looking fonts on your sheets

Otherwise, follow the much simpler [Executable Usage](#-Executable-Usage) instructions.

### First time setup
You will need a version of Python 3 installed before completing this setup. See https://www.python.org/downloads/ for the latest Python download links.

Clone the git repo into an empty directory. Then, navigate to the directory on the Windows `cmd` terminal. To do so, open the Command Prompt from the Start menu and `cd` to the target directory (you may want to copy the full directory path from the Windows Explorer to do this, then `cd "<absolute directory path here>"`).

Then, run the following command (paste into terminal): `.\setup.bat`.

### Running the tool

Navigate to this file's directory in the Terminal, as specified in the Setup section. Then, run the command `.\venv\Scripts\activate.bat` in the Terminal. If you see `(venv)` at the start of your command prompt, the tool is ready to be used. This setup command must be run **every time** a new Terminal is opened for this tool.
Run `python cli.py -h` for help:
```
python cli.py [-h] -s SHIP [-w [WEAPONS ...]] [-c [CRAFTS ...]] [-y [SYSTEMS ...]] -o OUTPUT [-f]

options:
  -h, --help            show this help message and exit
  -s SHIP, --ship SHIP  The name of the ship to use as a template. Ex: Emblem
  -w [WEAPONS ...], --weapons [WEAPONS ...]
                        The names of weapons to assign to mounts, double-quoted and in order. Ex: "Light Cannon" "Guardian Laser"
  -c [CRAFTS ...], --crafts [CRAFTS ...]
                        The names of crafts to assign to bays, double-quoted and in order. Ex: "Light Missile" "Standard Torpedo" "Chaff"
  -y [SYSTEMS ...], --systems [SYSTEMS ...]
                        The names of all non-default systems to equip, double-quoted. Ex: "Reinforced Magazine" "Radar Booster"
  -o OUTPUT, --output OUTPUT
                        Output file path for the character sheet PDF.
  -f, --fancy           Provide this option to use fancy fonts. Requires the font files to be correctly set up - DO NOT USE with the packaged executable!
```

The tool is expected to produce an error if a weapon or craft cannot be equipped to its mount or bay, or if the maximum system slots are exceeded.

For the `-w` and `-c` options, if fewer weapons/crafts are specified than there are mounts/bays, the remaining mounts/bays will be considered empty and filler rows will be generated for them. Empty mounts can be manually specified by providing `""` as the weapon name.

For the `-y` option, if the ship has system slots remaining after equipping all specified systems, a filler row will be generated for each system point remaining.

### Examples

```
python cli.py -s Emblem -w "Light Spinal Rail" "" "Coilgun" "Guardian Laser" "" "Coilgun" -y "Reactor Booster" -c "Chaff" "" "Tracking Beacon" -o test.pdf

python cli.py -s Elena -w -c -y -o empty_sheet.pdf
```

The sheets created by these commands are under the `examples` directory.

### Compendium

Ship templates, systems, weapons, and crafts are defined in JSON files under the `resources` folder. These files can be modified to add new elements or modify them - following the same format as the existing elements should work. Use an editor such as Visual Studio Code or an online tool (such as https://jsonlint.com/) to validate the JSON before running the tool. The tool will fail if one or more of the resource files are incorrectly formatted.

## Executable Usage

### First time setup
Download the `ship_creator.zip` folder from the GitHub repository. Extract its files into a known location on your computer.

### Running the program
Navigate to the `cli.exe` file's directory in the Terminal. This file is contained at `dist\cli` in the extracted files - navigate there via te File Explorer, and copy the directory path. Then, open a Command Prompt via the Start Menu (typing "cmd" should show it) and paste `cd <your path>` into the directory, replacing the path with the directory path copied earlier. If the file is on a different drive than your command prompt indicates, type in the name of the drive (ex: `D:`) then hit Enter before running the command.

You can then run the tool via the Terminal. You can also obtain the absolute path to the `cli.exe` file and skip the preceding step.
Run `cli.exe -h` for help:
```
cli.exe [-h] -s SHIP [-w [WEAPONS ...]] [-c [CRAFTS ...]] [-y [SYSTEMS ...]] -o OUTPUT [-f]

options:
  -h, --help            show this help message and exit
  -s SHIP, --ship SHIP  The name of the ship to use as a template. Ex: Emblem
  -w [WEAPONS ...], --weapons [WEAPONS ...]
                        The names of weapons to assign to mounts, double-quoted and in order. Ex: "Light Cannon" "Guardian Laser"
  -c [CRAFTS ...], --crafts [CRAFTS ...]
                        The names of crafts to assign to bays, double-quoted and in order. Ex: "Light Missile" "Standard Torpedo" "Chaff"
  -y [SYSTEMS ...], --systems [SYSTEMS ...]
                        The names of all non-default systems to equip, double-quoted. Ex: "Reinforced Magazine" "Radar Booster"
  -o OUTPUT, --output OUTPUT
                        Output file path for the character sheet PDF.
  -f, --fancy           Provide this option to use fancy fonts. Requires the font files to be correctly set up - DO NOT USE with the packaged executable!
```

DO NOT USE the `-f` or `--fancy` option unless you know what you are doing and have manually set up the required fonts!

The tool is expected to produce an error if a weapon or craft cannot be equipped to its mount or bay, or if the maximum system slots are exceeded.

For the `-w` and `-c` options, if fewer weapons/crafts are specified than there are mounts/bays, the remaining mounts/bays will be considered empty and filler rows will be generated for them. Empty mounts can be manually specified by providing `""` as the weapon name.

For the `-y` option, if the ship has system slots remaining after equipping all specified systems, a filler row will be generated for each system point remaining.

### Examples

```
cli.exe -s Emblem -w "Light Spinal Rail" "" "Coilgun" "Guardian Laser" "" "Coilgun" -y "Reactor Booster" -c "Chaff" "" "Tracking Beacon" -o test.pdf

cli.exe -s Elena -w -c -y -o empty_sheet.pdf
```

These sheets will be very similar to the ones under the `examples` directory, minus font differences.
