# Project Orion character sheet creator
## Version
0.1 - CLI

## Description
This command-line application creates ship character sheets for Project Orion ships. This includes stats, weapons, bays, and systems.

## First time setup
You will need a version of Python 3 installed before completing this setup. See https://www.python.org/downloads/ for the latest Python download links.

Clone the git repo into an empty directory. Then, navigate to the directory on the Windows `cmd` terminal, by doing one of:
- Open cmd.exe from the Start menu and `cd` to the target directory
- Right-click on the target directory in Windows Explorer and select "Open in Terminal"

Then, run the following command (paste into terminal): `setup.bat`.

## Usage

Navigate to this file's directory in the Terminal, as specified in the Setup section. Then, run the command `./venv/Scripts/activate.bat` in the Terminal. The tool is then ready to be used. This setup command must be run **every time** a new Terminal is opened for this tool.
Run `python cli.py -h` for help:
```
python cli.py -h  
usage: cli.py [-h] -s SHIP [-w [WEAPONS ...]] [-c [CRAFTS ...]] [-y [SYSTEMS ...]] -o OUTPUT

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
```

The tool is expected to produce an error if a weapon or craft cannot be equipped to its mount or bay, or if the maximum system slots are exceeded.

## Examples

```
python cli.py -s Emblem -w "Light Spinal Rail" "Coilgun" "Coilgun" "Guardian Laser" "Coilgun" "Coilgun" -y "Bulk Magazine" "Reactor Booster" -c "Chaff" "Scrambler Pods" "Tracking Beacon" -o test.pdf
```

The sheet created by this command is at `examples/test.pdf`.

## Compendium

Ship templates, systems, weapons, and crafts are defined in JSON files under the `resources` folder. These files can be modified to add new elements or modify them - following the same format as the existing elements should work. Use an editor such as Visual Studio Code or an online tool (such as https://jsonlint.com/) to validate the JSON before running the tool. The tool will fail if one or more of the resource files are incorrectly formatted.