from enum import Enum
import re

class MountType(Enum):
    FIXED = 0
    TURRET = 1
    OMNI = 2

    def __str__(self):
        return str(self.name)[0]

class MountPosition(Enum):
    FORWARD = 0
    PORT = 1
    REAR = 2
    STARBOARD = 3
    
    def __str__(self):
        return str(self.name)[0]

class ShipClass(Enum):
    ESCORT = 0
    LINE = 1
    CAPITAL = 2

    def get_traits(self):
        return SHIP_CLASS_TRAITS[self]


SHIP_CLASS_TRAITS = {
    ShipClass.ESCORT: {
        "Maneuverable": "This ship may make two heading adjustments instead of one during the Movement Phase."
    },
    ShipClass.LINE: {
        "Superior Shielding": "When using Charge Shields, this ship generates +1 Shields per Power spent."
    },
    ShipClass.CAPITAL: {
        "Supreme Shielding": "When using Charge Shields, this ship generates +2 Shields per Power spent.",
        "Well Defended": "When this ship takes system damage to reduce damage, reduce the damage taken by 2d6 instead of 1d6.",
        "Like a Cow": "This ship can only adjust its heading at the end of its Movement Phase."
    }
}

class ShipStat(Enum):
    HP = 0
    SHIELDS = 1
    POWER = 2
    AMMO = 3
    RESTORES = 4
    EVASION = 5
    ARMOUR = 6
    SPEED = 7
    SENSORS = 8
    SIGNATURE = 9

    def __str__(self):
        return str(self.name)
    
    def is_gauge(self) -> bool:
        return self.value < 5

def multiply_dice(dice: str, constant: int) -> str:
    if dice.isdigit():
        return str(int(dice) * constant)
    else:
        match = re.match(pattern=r"(\d+)d(\d+)(?:\+(\d+))?", string=dice)
        dice_count = int(match.group(1)) * constant
        dice_size = int(match.group(2))
        calculated_string = f"{dice_count}d{dice_size}"
        if len(match.groups()) > 2 and match.group(3):
            added_value = int(match.group(3))
            calculated_string += f"+{added_value * constant}"
        return calculated_string