import tkinter as tk
from typing import *
from utils import *
import re

class Craft():
    DEFAULT_CRAFT_STATS = {
        ShipStat.POWER: 0,
        ShipStat.AMMO: 0,
        ShipStat.RESTORES: 0,
        ShipStat.SHIELDS: 0,
        ShipStat.SENSORS: 0,
        ShipStat.SIGNATURE: 0
    }
    def __init__(self, name: str, stats: Dict[str, int], size: int, ammo: int, power: int, description: str="", tags: List[str]=[]):
        self._name = name
        self._description = description
        self._stats = stats.copy()
        self._stats.update(Craft.DEFAULT_CRAFT_STATS)
        self._tags = tags
        self._size = size
        self._ammo = ammo
        self._power = power
    
    def get_tags(self) -> List[str]:
        return self._tags
    
    def get_size(self) -> int:
        return self._size
    
    def get_ammo(self) -> int:
        return self._ammo
    
    def get_power(self) -> int:
        return self._power

    def get_stat(self, stat: ShipStat):
        return self._stats.get(stat)
    
    def get_swarm(self) -> str:
        for tag in self._tags:
            if "Swarm" in tag:
                match = re.match(pattern=r"Swarm (\d+(?:d\d+(?:\+\d+)?)?)", string=tag)
                return match.group(1)
        return "1"
    
    def get_damage(self) -> str:
        return "-"
    
    def get_ap(self) -> int:
        return 0
    
    @staticmethod
    def from_json(json_obj: dict):
        raise NotImplementedError()

class Weapon():
    def __init__(self, name: str, size: int, range: int, damage: str, ammo_cost: int=0, power_cost: int=0, ap: int=0, description: str="", tags: List[str]=[]):
        self._name = name
        self._size = size
        self._range = range
        self._description = description
        self._power_cost = power_cost
        self._ammo_cost = ammo_cost
        self._ap = ap
        self._damage = damage
        self._tags = tags
    
    def get_shots(self) -> str:
        if "EWAR" in self._tags:
            return "1"
        for tag in self._tags:
            if "Shots" in tag:
                match = re.match(pattern=r"Shots (\d+(?:d\d+(?:\+\d+)?)?)", string=tag)
                return match.group(1)
        return "1"
    
    def is_spinal(self) -> bool:
        return "Spinal" in self._tags
    
    @staticmethod
    def from_json(json_obj: dict):
        if not json_obj["__type__"] or json_obj["__type__"] != "Weapon":
            raise ValueError("Dict does not represent a Weapon")
        return Weapon(
            json_obj["name"], json_obj["size"], json_obj["range"], json_obj["damage"],
            json_obj["ammo"], json_obj["power"], json_obj["ap"], tags=json_obj["tags"]
        )

class Payload(Craft):
    def __init__(self, name: str, stats: Dict[str, int], weapon: Weapon, description: str="", tags: List[str]=[]):
        super().__init__(name, stats, weapon._size, weapon._ammo_cost, weapon._power_cost, description, tags)
        self._weapon = weapon

    @staticmethod
    def from_json(json_obj: dict):
        if not json_obj["__type__"] or json_obj["__type__"] != "Payload":
            raise ValueError("Dict does not represent a Payload")
        weapon = Weapon(
            json_obj["name"], json_obj["size"], 0, json_obj["damage"],
            json_obj["ammo"], json_obj["power"], json_obj["ap"], tags=json_obj["tags"]
        )
        stats = json_obj["stats"]
        stats = {ShipStat[key.upper()]: value for key, value in stats.items() if key.upper() in [stat.name for stat in ShipStat]}
        return Payload(json_obj["name"], stats, weapon, tags=json_obj["tags"])
    
    def get_damage(self) -> str:
        return self._weapon._damage
    
    def get_ap(self) -> int:
        return self._weapon._ap

class Deployable(Craft):
    @staticmethod
    def from_json(json_obj: dict):
        if not json_obj["__type__"] or json_obj["__type__"] != "Deployable":
            raise ValueError("Dict does not represent a Deployable")
        stats = json_obj["stats"]
        stats = {ShipStat[key.upper()]: value for key, value in stats.items() if key.upper() in [stat.name for stat in ShipStat]}
        return Deployable(json_obj["name"], stats, json_obj["size"], json_obj["ammo"], json_obj["power"], tags=json_obj["tags"])

class Mount():
    def __init__(self, size: int, count: int, mount_type: MountType | str, position: MountPosition | str, is_spinal_only: bool=False, equip_restrictions: Callable[[Weapon], bool]=lambda w : True):
        self._size = size
        self._count = count
        self._type = MountType[mount_type] if type(mount_type) is str else mount_type
        self._position = MountPosition[position] if type(position) is str else position
        self._weapon = None
        self._is_spinal_only = is_spinal_only
        self._equip_predicate = equip_restrictions
        if self._is_spinal_only:
            self._equip_predicate = lambda w : equip_restrictions(w) and w.is_spinal()

    def equip(self, weapon: Weapon) -> bool:
        if self.can_equip(weapon):
            self._weapon = weapon
        else:
            raise ValueError(f"Weapon {weapon} cannot be equipped on this mount {self}")
        
    def can_equip(self, weapon: Weapon) -> bool:
        return self._size >= weapon._size and self._equip_predicate(weapon)
    
    @staticmethod
    def from_json(json_obj: dict):
        if not json_obj["__type__"] or json_obj["__type__"] != "Mount":
            raise ValueError("Dict does not represent a Mount")
        mount = Mount(
            json_obj["size"], json_obj["count"], json_obj["type"], json_obj["position"], json_obj["spinal"])
        if json_obj.get("weapon"):
            mount.equip(Weapon.from_json(json_obj["weapon"]))
        return mount

class Bay():
    def __init__(self, size: int, count: int, positions: List[MountPosition | str], equip_restrictions: Callable[[Craft], bool]=lambda w : True):
        self._size = size
        self._count = count
        self._positions = [MountPosition[position] if type(position) is str else position for position in positions]
        self._craft = None
        self._equip_predicate = equip_restrictions

    def equip(self, craft: Craft) -> bool:
        if self.can_equip(craft):
            self._craft = craft
        else:
            raise ValueError(f"Payload {craft._name} cannot be equipped on this mount")
        
    def can_equip(self, craft: Craft) -> bool:
        return self._size >= craft.get_size() and self._equip_predicate(craft)

    def get_count(self) -> int:
        if "Highlander" in self._craft.get_tags():
            return 1
        else:
            return self._count

    @staticmethod
    def from_json(json_obj: dict):
        if not json_obj["__type__"] or json_obj["__type__"] != "Bay":
            raise ValueError("Dict does not represent a Bay")
        bay = Bay(
            json_obj["size"], json_obj["count"], json_obj["positions"])
        if json_obj.get("payload"):
            bay.equip(Payload.from_json(json_obj["payload"]))
        if json_obj.get("deployable"):
            bay.equip(Deployable.from_json(json_obj["deployable"]))
        return bay


class ShipSystem():
    def __init__(self, name: str, description: str, slots: int, hp: int, bubble_text: List[str]=None, ship_classes: List[str]=None):
        self._name = name
        self._description = description
        self._slots = slots
        self._hp = hp
        self._bubble_text = bubble_text
        if self._bubble_text is not None and len(self._bubble_text) != self._hp:
            raise ValueError(f"`bubble_text` has {len(self._bubble_text)} elements, must be the same as system HP ({self._hp}).")
        if not ship_classes:
            self._ship_classes = []
        else:
            self._ship_classes = [ShipClass[ship_class] for ship_class in ship_classes]
    
    @staticmethod
    def from_json(json_obj: dict):
        if not json_obj["__type__"] or json_obj["__type__"] != "ShipSystem":
            raise ValueError("Dict does not represent a ShipSystem")
        return ShipSystem(
            json_obj["name"], json_obj["description"], json_obj["slots"], json_obj["hp"], json_obj["bubble_text"], json_obj["ship_classes"])

class Ship():
    def __init__(self, name: str, stats: Dict[str, int], system_slots: int, points: int, traits: Dict[str, str], ship_class: ShipClass, mounts: List[Mount], bays: List[Bay], systems: List[ShipSystem], id: str=""):
        self._name = name
        self._stats = stats
        self._class = ship_class
        self._mounts = mounts
        self._bays = bays
        self._systems = systems
        self._system_slots = system_slots
        self._point_cost = points
        self._traits = traits
        self._traits.update(self._class.get_traits())
        self._id = id
    
    def get_free_system_slots(self):
        return self._system_slots - sum(system._slots for system in self._systems)
    
    def get_stat(self, stat: ShipStat):
        return self._stats.get(stat)
    
    def can_equip(self, system: ShipSystem):
        return (not system._ship_classes or self._class in system._ship_classes) and system._slots <= self.get_free_system_slots()
    
    def equip(self, system: ShipSystem):
        if system in self._systems:
            return
        if self.can_equip(system):
            self._systems.append(system)
        else:
            raise ValueError(f"System {system._name} cannot be equipped on this ship")

    @staticmethod
    def from_json(json_obj: dict):
        if not json_obj["__type__"] or json_obj["__type__"] != "Ship":
            raise ValueError("Dict does not represent a Ship")
        mounts = [Mount.from_json(mount) for mount in json_obj["mounts"]]
        bays = [Bay.from_json(bay) for bay in json_obj["bays"]]
        systems = []
        if json_obj.get("systems"):
            systems = [ShipSystem.from_json(system) for system in json_obj["systems"]]
        stats = json_obj["stats"]
        stats.update({"Power": stats["Reactor"]})
        stats = {ShipStat[key.upper()]: value for key, value in stats.items() if key.upper() in [stat.name for stat in ShipStat]}
        return Ship(json_obj["name"], stats, json_obj["system_slots"], json_obj["point_cost"], json_obj["traits"],
            ShipClass[json_obj["ship_class"]], mounts, bays, systems
        )
    

class Army():
    def __init__(self, max_points: int, ships: List[Ship]=[]):
        self._max_points = max_points
        self._ships = ships
    
    def get_point_cost(self):
        return sum(ship._point_cost for ship in self._ships)
    
    def get_free_points(self):
        return self._max_points - self.get_point_cost()
    
    def add_ship(self, ship: Ship):
        self._ships.append(ship)
    
    def remove_ship(self, ship: Ship):
        self._ships.remove(ship)