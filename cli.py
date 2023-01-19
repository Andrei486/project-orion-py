import argparse
from ship_configuration import *
from pdf_convert import ShipSheet
import compendium

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--ship", required=True, help="The name of the ship to use as a template. Ex: Emblem")
    parser.add_argument("-w", "--weapons", nargs="*", help="The names of weapons to assign to mounts, double-quoted and in order. Ex: \"Light Cannon\" \"Guardian Laser\"")
    parser.add_argument("-c", "--crafts", nargs="*", help="The names of crafts to assign to bays, double-quoted and in order. Ex: \"Light Missile\" \"Standard Torpedo\" \"Chaff\"")
    parser.add_argument("-y", "--systems", nargs="*", help="The names of all non-default systems to equip, double-quoted. Ex: \"Reinforced Magazine\" \"Radar Booster\"")
    parser.add_argument("-o", "--output", required=True, help="Output file path for the character sheet PDF.")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    comp = compendium.get_compendium()
    ship = comp.get_ship(args.ship)
    comp.equip_default_systems(ship)
    weapons = [comp.get_weapon(weapon) if weapon else None for weapon in args.weapons] if args.weapons else []
    systems = [comp.get_system(system) for system in args.systems] if args.systems else []
    crafts = [comp.get_craft(craft) if craft else None for craft in args.crafts] if args.crafts else []
    for system in systems:
        ship.equip(system)
    for weapon, mount in zip(weapons, ship._mounts):
        if weapon:
            mount.equip(weapon)
    for craft, bay in zip(crafts, ship._bays):
        if craft:
            bay.equip(craft)
    sheet = ShipSheet()
    sheet.create_sheet(ship, args.output)