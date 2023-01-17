from utils import *
from ship_configuration import *
import json
from typing import *

class Compendium():

    WEAPON_LIST = "./resources/weapon_list.json"
    CRAFT_LIST = "./resources/craft_list.json"
    SYSTEM_LIST = "./resources/system_list.json"
    SHIP_LIST = "./resources/ship_list.json"

    def __init__(self):
        self._weapons = []
        self._ships = []
        self._slot_systems = []
        self._default_systems = []
        self._ship_templates = []
        self._crafts = []
        self.load_systems()
        self.load_weapons()
        self.load_ships()
        self.load_crafts()

    def load_weapons(self):
        with open(Compendium.WEAPON_LIST, "r") as weapons_file:
            weapon_list_obj = json.load(weapons_file)
        weapon_list = weapon_list_obj["weapons"]
        self._weapons = [Weapon.from_json(weapon) for weapon in weapon_list]
    
    def get_weapons(self, predicate: Callable[[Weapon], bool]=lambda w : True) -> List[Weapon]:
        return [weapon for weapon in self._weapons if predicate(weapon)]

    def get_weapon(self, name: str) -> Weapon:
        for weapon in self._weapons:
            if weapon._name == name:
                return weapon
        return None
    
    def load_systems(self):
        with open(Compendium.SYSTEM_LIST, "r") as systems_file:
            system_list_obj = json.load(systems_file)
        slot_system_list = system_list_obj["slots"]
        self._slot_systems = [ShipSystem.from_json(system) for system in slot_system_list]
        default_system_list = system_list_obj["default"]
        self._default_systems = [ShipSystem.from_json(system) for system in default_system_list]
    
    def get_systems(self, predicate: Callable[[ShipSystem], bool]=lambda w : True) -> List[ShipSystem]:
        return [system for system in self._default_systems + self._slot_systems if predicate(system)]
    
    def get_default_systems(self, predicate: Callable[[ShipSystem], bool]=lambda w : True) -> List[ShipSystem]:
        return [system for system in self._default_systems if predicate(system)]

    def get_slot_systems(self, predicate: Callable[[ShipSystem], bool]=lambda w : True) -> List[ShipSystem]:
        return [system for system in self._slot_systems if predicate(system)]

    def get_system(self, name: str) -> ShipSystem:
        for system in self.get_systems():
            if system._name == name:
                return system
        return None
    
    def equip_default_systems(self, ship: Ship):
        for system in self.get_default_systems():
            ship.equip(system)
    
    def load_ships(self):
        with open(Compendium.SHIP_LIST, "r") as ship_file:
            ship_list_obj = json.load(ship_file)
        ship_list = ship_list_obj["ships"]
        self._ship_templates = [Ship.from_json(ship) for ship in ship_list]
    
    def get_ships(self, predicate: Callable[[Ship], bool]=lambda w : True) -> List[Ship]:
        return [ship for ship in self._ship_templates if predicate(ship)]

    def get_ship(self, name: str) -> Ship:
        for ship in self.get_ships():
            if name in ship._name:
                return ship
        return None
    
    def load_crafts(self):
        with open(Compendium.CRAFT_LIST, "r") as ship_file:
            craft_list_obj = json.load(ship_file)
        deployable_list = craft_list_obj["deployables"]
        payload_list = craft_list_obj["payloads"]
        self._crafts.extend(Deployable.from_json(deployable) for deployable in deployable_list)
        self._crafts.extend(Payload.from_json(payload) for payload in payload_list)
    
    def get_crafts(self, predicate: Callable[[Ship], bool]=lambda w : True) -> List[Ship]:
        return [craft for craft in self._crafts if predicate(craft)]

    def get_craft(self, name: str) -> Craft:
        for craft in self.get_crafts():
            if name == craft._name:
                return craft
        return None

compendium = None

def get_compendium() -> Compendium:
    global compendium
    if not compendium:
        compendium = Compendium()
    return compendium

if __name__ == "__main__":
    compendium = Compendium()
    print(compendium.get_weapon("Class B Spinal Beam"))
    print(compendium.get_system("Engine"))