from fpdf import FPDF
from ship_configuration import *
from utils import multiply_dice
from compendium import *

class ShipSheet(FPDF):

    MOUNT_TABLE_HEADINGS = [
        "WEAPON NAME", "POS", "RANGE", "AMMO", "PW",
        "SHOTS", "AP", "DMG", "TAGS"
    ]
    TABLE_COLUMN_SPACING = 4
    BAY_TABLE_HEADINGS = [
        "PAYLOAD NAME", "POS", "SPEED", "AMMO", "PW",
        "SWARM", "AP", "DMG", "TAGS"
    ]
    TRAIT_TABLE_HEADINGS = [
        "NAME", "DESCRIPTION"
    ]
    DAMAGE_BUBBLE = "[_]"
    FANCY_FONT_PRESETS = {
        "Heading 2": {
            "font": ('DejaVu', 'B', 14),
            "color": (40, 40, 100)
        },
        "Heading 3": {
            "font": ('DejaVu', 'B', 10),
            "color": (40, 40, 100)
        },
        "Mono Heading 3": {
            "font": ('DejaVu Mono', 'B', 10),
            "color": (0, 0, 0)
        },
        "Paragraph": {
            "font": ('DejaVu', '', 10),
            "color": (0, 0, 0)
        },
        "Mono": {
            "font": ("DejaVu Mono", '', 8),
            "color": (0, 0, 0)
        },
        "Stat Box": {
            "font": ("DejaVu Condensed", '', 12),
            "color": (0, 0, 0)
        },
    }

    BASE_FONT_PRESETS = {
        "Heading 2": {
            "font": ('Arial', 'B', 14),
            "color": (40, 40, 100)
        },
        "Heading 3": {
            "font": ('Arial', 'B', 10),
            "color": (40, 40, 100)
        },
        "Mono Heading 3": {
            "font": ('Courier', 'B', 10),
            "color": (0, 0, 0)
        },
        "Paragraph": {
            "font": ('Courier', '', 10),
            "color": (0, 0, 0)
        },
        "Mono": {
            "font": ("Courier", '', 8),
            "color": (0, 0, 0)
        },
        "Stat Box": {
            "font": ("Arial", '', 12),
            "color": (0, 0, 0)
        },
    }

    def __init__(self, orientation = 'P', unit = 'mm', format='A4', use_base_fonts: bool=True):
        super().__init__(orientation, unit, format)
        self._font_presets = self.BASE_FONT_PRESETS if use_base_fonts else self.FANCY_FONT_PRESETS
        if not use_base_fonts:
            self.import_fonts()

    def import_fonts(self):
        self.add_font("DejaVu", "", "DejaVuSansCondensed.ttf", uni=True)
        self.add_font("DejaVu", "B", "DejaVuSansCondensed-Bold.ttf", uni=True)
        self.add_font("DejaVu Mono", "", "DejaVuSansMono.ttf", uni=True)
        self.add_font("DejaVu Mono", "B", "DejaVuSansMono-Bold.ttf", uni=True)
        self.add_font("DejaVu Condensed", "", "DejaVuSansCondensed.ttf", uni=True)
        self.add_font("DejaVu Condensed", "B", "DejaVuSansCondensed-Bold.ttf", uni=True)

    def set_font_from_preset(self, preset_name: str):
        self.set_font(*self._font_presets.get(preset_name).get("font"))
        self.set_text_color(*self._font_presets.get(preset_name).get("color"))

    def create_mount_table(self, mounts: List[Mount]):
        self.set_font_from_preset("Mono Heading 3")
        cell_widths = [self.get_string_width(heading) + ShipSheet.TABLE_COLUMN_SPACING for heading in ShipSheet.MOUNT_TABLE_HEADINGS]
        self.set_font_from_preset("Mono")
        weapon_name_widths = [(self.get_string_width(f"{self.DAMAGE_BUBBLE} {mount._weapon._name}") + ShipSheet.TABLE_COLUMN_SPACING) if mount._weapon else 0 for mount in mounts]
        cell_widths[0] = max(cell_widths[0], *weapon_name_widths)
        cell_widths[-1] = 0 # last cell takes all the remaining space
        
        self.set_font_from_preset("Mono Heading 3")
        self.create_row(ShipSheet.MOUNT_TABLE_HEADINGS, cell_widths)
        self.set_font_from_preset("Mono")
        for mount in mounts:
            mount_data = self.get_mount_display_data(mount)
            self.create_row(mount_data, cell_widths)
    
    def create_bay_table(self, bays: List[Bay]):
        self.set_font_from_preset("Mono Heading 3")
        cell_widths = [self.get_string_width(heading) + ShipSheet.TABLE_COLUMN_SPACING for heading in ShipSheet.BAY_TABLE_HEADINGS]
        self.set_font_from_preset("Mono")
        weapon_name_widths = [(self.get_string_width(f"{self.DAMAGE_BUBBLE} {bay._craft._name}") + ShipSheet.TABLE_COLUMN_SPACING) if bay._craft else 0 for bay in bays]
        cell_widths[0] = max(cell_widths[0], *weapon_name_widths)
        cell_widths[-1] = 0 # last cell takes all the remaining space

        self.set_font_from_preset("Mono Heading 3")
        self.create_row(ShipSheet.BAY_TABLE_HEADINGS, cell_widths)
        self.set_font_from_preset("Mono")
        for bay in bays:
            bay_data = self.get_bay_display_data(bay)
            self.create_row(bay_data, cell_widths)

    def create_row(self, data: List[str], cell_widths: List[int], row_height: int=6):
        for datum, width in zip(data, cell_widths):
            self.cell(width, row_height, datum, border='T', ln=0, align='L')
        self.ln()
    
    def create_multicell_row(self, data: List[str], cell_widths: List[int], row_height: int=6):
        for datum, width in zip(data, cell_widths):
            if width == 0:
                self.multi_cell(width, row_height, datum, border='T', align='L')
            else:
                self.cell(width, row_height, datum, border='T', ln=0, align='L')
    
    def get_mount_display_data(self, mount: Mount) -> List[str]:
        mount_position_data = f"{mount._position}{mount._type}" if not mount._is_spinal_only else f"{mount._position}S"
        if not mount._weapon:
            return [f"{self.DAMAGE_BUBBLE}", mount_position_data, "", "", "", f" (x{mount._count})", "", "", ""]
        weapon = mount._weapon
        mount_data = [str(datum) for datum in [
            f"{self.DAMAGE_BUBBLE} {weapon._name}", mount_position_data, weapon._range, weapon._ammo_cost, weapon._power_cost,
            multiply_dice(weapon.get_shots(), mount._count), weapon._ap, weapon._damage, ', '.join(weapon._tags)
        ]]
        return mount_data
    
    def get_bay_display_data(self, bay: Bay) -> List[str]:
        if not bay._craft:
            return [f"{self.DAMAGE_BUBBLE}", "".join(str(pos) for pos in bay._positions), "", "", "", f" (x{bay._count})", "", "", ""]
        craft = bay._craft
        bay_data = [str(datum) for datum in [
            f"{self.DAMAGE_BUBBLE} {craft._name}", "".join(str(pos) for pos in bay._positions), craft.get_stat(ShipStat.SPEED), craft.get_ammo(), craft.get_power(),
            f"{craft.get_swarm()}(x{bay.get_count()})", craft.get_ap(), craft.get_damage(), ', '.join(craft.get_tags())
        ]]
        return bay_data

    def create_system_row(self, system: ShipSystem, start_x: float, end_x: float) -> int:
        HEIGHT = 5
        self.set_x(start_x)
        self.set_font_from_preset("Mono")
        if system:
            damage_bubble_text = ""
            if system._bubble_text is None:
                damage_bubble_text = self.DAMAGE_BUBBLE * system._hp
            else:
                damage_bubble_text = "".join(f"[{text}]" for text in system._bubble_text)
            data = [system._name, damage_bubble_text, system._description]
        else:
            data = [""] * 3
        max_width = end_x - start_x
        cell_widths = [max_width * 0.35, max_width * 0.2, max_width * 0.45]
        for datum, width in zip(data, cell_widths):
            self.cell(int(width), HEIGHT, datum, border='T' if system else 'TB', ln=0, align='L')
        return HEIGHT
    
    def create_system_table(self, systems: List[ShipSystem], heading: str, start_x: float, end_x: float):
        self.set_font_from_preset("Heading 2")
        self.set_x(start_x)
        self.cell(end_x - start_x, 8, heading, border=0, ln=2, align='L')
        for system in systems:
            height = self.create_system_row(system, start_x, end_x)
            self.set_y(self.get_y() + height)
    
    def show_stat(self, ship: Ship, stat: ShipStat, width: int, height: int, is_gauge: bool=False):
        stat_box_width = height * 1.5
        stat_value = ship.get_stat(stat)
        self.set_font_from_preset("Heading 3")
        self.cell(width-stat_box_width, height, str(stat), border=0, ln=0, align='L')
        self.set_font_from_preset("Stat Box")
        if is_gauge:
            stat_box_text = f"/{stat_value}"
            stat_box_align = 'R'
        else:
            stat_box_text = f"{str(stat_value)} (+  )"
            stat_box_align = 'C'
        self.cell(stat_box_width, height, stat_box_text, border=1, ln=1, align=stat_box_align)

    def show_stats(self, ship: Ship, start_x: int, end_x: int):
        STAT_COLUMNS = [
            [ShipStat.HP, ShipStat.SHIELDS, ShipStat.POWER, ShipStat.AMMO, ShipStat.RESTORES],
            [ShipStat.EVASION, ShipStat.ARMOUR, ShipStat.SPEED, ShipStat.SENSORS, ShipStat.SIGNATURE]
        ]
        COLUMN_SPACING = 4
        middle = end_x / 2
        bounds = [
            [start_x, middle],
            [middle + COLUMN_SPACING, end_x]
        ]
        top_y = self.get_y()
        for stats, bound in zip(STAT_COLUMNS, bounds):
            self.set_y(top_y)
            self.show_stats_column(ship, stats, bound[0], bound[1])

    def show_stats_column(self, ship: Ship, stats: List[ShipStat], start_x: int, end_x: int):
        STAT_HEIGHT=10
        for stat in stats:
            self.set_x(start_x)
            self.show_stat(ship, stat, end_x - start_x, STAT_HEIGHT, stat.is_gauge())
        
    def show_traits(self, ship: Ship):
        traits = ship._traits
        if not traits:
            return
        self.set_font_from_preset("Heading 2")
        self.cell(0, 8, "TRAITS", border=0, ln=1, align="L")
        self.set_font_from_preset("Mono Heading 3")
        trait_name_widths = [(self.get_string_width(trait_name) + ShipSheet.TABLE_COLUMN_SPACING) for trait_name in traits.keys()]
        cell_widths = [max(self.get_string_width(ShipSheet.TRAIT_TABLE_HEADINGS[0]) + ShipSheet.TABLE_COLUMN_SPACING, *trait_name_widths), 0]
        self.create_row(ShipSheet.TRAIT_TABLE_HEADINGS, cell_widths)
        self.set_font_from_preset("Mono")
        for trait_name, trait_description in traits.items():
            self.create_multicell_row([trait_name, trait_description], cell_widths)
    
    def create_status_trackers(self):
        pass
    
    def create_sheet(self, ship: Ship, output_path: str):
        self.alias_nb_pages()
        self.add_page()
        self.set_font_from_preset("Heading 2")
        self.cell(0, 8, f"{ship._name}", border=0, ln=1, align='C')
        self.set_font_from_preset("Paragraph")
        self.show_stats(ship, self.l_margin, int((self.w - self.r_margin - self.l_margin) * 2/3))
        self.show_traits(ship)
        systems_y = self.get_y()
        self.create_system_table([system for system in ship._systems if system._slots == 0], "SYSTEMS - CORE", self.l_margin, (self.w / 2) - 5)
        core_systems_end_y = self.get_y()
        self.set_y(systems_y)
        self.create_system_table([system for system in ship._systems if system._slots > 0] + [None] * ship.get_free_system_slots(), "SYSTEMS - SLOTS", (self.w / 2), self.w - self.r_margin)
        slot_systems_end_y = self.get_y()
        self.set_y(max(core_systems_end_y, slot_systems_end_y))
        self.set_font_from_preset("Heading 2")
        self.cell(0, 8, "WEAPONS", border=0, ln=1, align='L')
        self.set_font_from_preset("Paragraph")
        self.create_mount_table(ship._mounts)
        self.set_font_from_preset("Heading 2")
        self.cell(0, 8, "BAYS", border=0, ln=1, align='L')
        self.set_font_from_preset("Paragraph")
        self.create_bay_table(ship._bays)
        self.output(output_path, 'F')


# VERY_LONG_STRING = "A test weapon. This is about as long as a description will ever be, but I need to make sure that text wraps around correctly, just in case. "

# if __name__ == "__main__":
#     # Instantiation of inherited class
#     pdf = ShipSheet()
#     test_mount = Mount(2, 2, MountType.TURRET, MountPosition.FORWARD)
#     test_weapon = Weapon("Test Weapon", 2, 12, "2d6+3", 1, 0, 2, VERY_LONG_STRING, ["Accurate", "Tag 1", "Tag 2"])
#     test_mount.equip(test_weapon)
#     test_weapon_2 = Weapon("Multi-Shot Weapon", 1, 8, "3", 1, 0, 1, VERY_LONG_STRING, ["Inaccurate", "Shots 1d6+2"])
#     test_mount_2 = Mount(3, 5, MountType.FIXED, MountPosition.STARBOARD)
#     test_mount_2.equip(test_weapon_2)
#     test_weapon_2 = Weapon("Multi-Shot Weapon 2", 1, 8, "3", 1, 0, 1, VERY_LONG_STRING, ["Inaccurate", "Shots 1d8"])
#     test_mount_3 = Mount(1, 2, MountType.OMNI, MountPosition.REAR)
#     test_mount_3.equip(test_weapon_2)
#     test_missile_weapon = Weapon("Light Missile Ram", 2, 0, "2d6+2", 1, 0, 6, "Auto-hits.", [])
#     test_payload = Payload("Light Missile", {ShipStat.HP: 3, ShipStat.SPEED: 8, ShipStat.EVASION: 8, ShipStat.ARMOUR: 0}, test_missile_weapon)
#     test_bay = Bay(2, 2, [MountPosition.FORWARD])
#     test_bay.equip(test_payload)
#     test_missile_weapon_2 = Weapon("2x2 Swarm Missile Cell Ram", 2, 0, "1d3", 1, 0, 5, "Auto-hits.", [])
#     test_payload_2 = Payload("2x2 Swarm Missile Cell", {ShipStat.HP: 1, ShipStat.SPEED: 7, ShipStat.EVASION: 7, ShipStat.ARMOUR: 0}, test_missile_weapon_2, tags=["Swarm 4"])
#     test_bay_2 = Bay(2, 4, [MountPosition.REAR])
#     test_bay_2.equip(test_payload_2)
#     test_missile_weapon_3 = Weapon("Standard Sprint Missile Ram", 3, 0, "5d6+4", 2, 0, 10, "Auto-hits.", ["Reload 1"])
#     test_payload_3 = Payload("Standard Sprint Missile", {ShipStat.HP: 3, ShipStat.SPEED: 8, ShipStat.EVASION: 8, ShipStat.ARMOUR: 0}, test_missile_weapon_3, tags=["Sprints"])
#     test_bay_3 = Bay(3, 1, [MountPosition.FORWARD, MountPosition.PORT, MountPosition.STARBOARD])
#     test_bay_3.equip(test_payload_3)
#     ship = Ship("Test Ship", {
#         ShipStat.HP: 100, ShipStat.SPEED: 7, ShipStat.EVASION: 7, ShipStat.ARMOUR: 0, ShipStat.AMMO: 36,
#         ShipStat.RESTORES: 5, ShipStat.POWER: 10, ShipStat.SENSORS: 6, ShipStat.SIGNATURE: 4, ShipStat.SHIELDS: 10},
#         5, 2, {"test trait 1": "does nothing", "test trait 2": "also does nothing"}, ShipClass.ESCORT,
#         [test_mount, test_mount_2, test_mount_3], [test_bay, test_bay_2, test_bay_3], [])
    
#     from compendium import *
#     compendium = Compendium()
#     compendium.equip_default_systems(ship)
#     pdf.create_sheet(ship, "test_sheet.pdf")