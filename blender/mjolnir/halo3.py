import bpy
from ctypes import *
import sys
import os
from importlib import reload

dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
   sys.path.append(dir)

import mjolnir.forge_types
reload(mjolnir.forge_types)
from mjolnir.forge_types import *


'''
*************************************

CLASSES

*************************************
'''

class H3_SaveGame(Structure):
    _pack_ = 1
    _fields_ = [
        ('unique_id', c_ulonglong),
        ('display_name', c_wchar * 16),
        ('description', c_char * 128),
        ('author', c_char * 16),
        ('e_saved_game_file_type', c_uint),
        ('author_is_xuid_online', c_ubyte),
        ('pad0', c_ubyte * 3),
        ('author_xuid', c_ubyte * 8),# hex
        ('byte_size', c_ulonglong),
        ('date', c_ulonglong),
        ('length_seconds', c_int),
        ('e_campaign_id', c_int),
        ('e_map_id', c_int),
        ('e_game_engine_type', c_int),
        ('e_campaign_difficulty_level', c_int),
        ('hopper_id', c_short),
        ('pad', c_short),
        ('game_id', c_ulonglong),
        ('map_variant_version', c_short),
        ('scenario_objects', c_short),
        ('variant_objects', c_short),
        ('quotas', c_short),
        ('e_map_id_2', c_int),
        ('bounds', Bounds),
        ('e_scenario_game_engine', c_int),
        ('max_budget', c_float),
        ('spent_budget', c_float),
        ('showing_helpers', c_short),
        ('built_in', c_short),
        ('original_map_signature_hash', c_uint),
    ]

class H3_ForgeObject(Structure):
    _fields_ = [
        ('placement', c_ushort),
        ('reuse_timeout', c_ushort),
        ('object_index', c_int),
        ('helper_index', c_int),
        ('definition_index', c_int),
        ('transform', Transform),
        ('attached_id', c_int),
        ('attached_bsp_index', c_ushort),
        ('attached_type', c_ubyte),
        ('attached_source', c_ubyte),
        ('game_engine_flags', c_ubyte),
        ('scenario', c_ubyte),
        ('mp_placement', c_ubyte),
        ('team', c_ubyte),
        ('shared_storage', c_ubyte),
        ('spawn_time_seconds', c_ubyte),
        ('object_type', c_ubyte),
        ('shape', c_ubyte),
        ('shape_data', ShapeData)
    ]
    def __str__(self): 
        return "%d %s" % (self.definition_index, self.transform)


class H3_MVAR(Structure):
    _pack_ = 1
    _fields_ = [
        ('data', H3_SaveGame),
        ('objects', H3_ForgeObject * 640),
        ('object_type_start_index', c_short * 14),
        ('quotas', Quota * 256),
        ('gamestate_indices', c_int * 80)
    ]

sandboxItems = {
    0: "Banshee",
    1: "Chopper",
    2: "Hornet",
    3: "Ghost",
    4: "Prowler",
    5: "Mongoose",
    6: "Scorpion",
    7: "Warthog",
    8: "Warthog, Gauss",
    9: "Wraith",

    16: "Assault Rifle",
    17: "Battle Rifle",
    18: "Shotgun",
    19: "Sniper Rifle",
    20: "SMG",
    21: "Spiker",
    22: "Magnum",
    23: "Plasma Pistol",
    24: "Plasma Rifle",
    25: "Needler",
    26: "Brute Shot",
    27: "Rocket Launcher",
    28: "Spartan Laser",
    29: "Energy Sword",
    30: "Plasma Cannon",
    31: "Gravity Hammer",
    32: "Covenant Carbine",
    33: "Mauler",
    34: "Fuel Rod Gun",
    35: "Beam Rifle",
    36: "Sentinel Beam",
    37: "Machine Gun Turret",
    38: "Flamethrower",
    39: "Missile Pod",

    43: "Frag Grenade",
    44: "Plasma Grenade",
    45: "Spike Grenade",
    46: "Firebomb Grenade",
    47: "Bubble Shield",
    48: "Power Drain",
    49: "Trip Mine",
    50: "Grav Lift",
    51: "Regenerator",
    52: "Radar Jammer",
    53: "Flare",
    54: "Deployable Cover",
    55: "Overshield",
    56: "Active Camo",
    57: "Custom Powerup",
    58: "Auto-Turret",
    59: "SPNKR Ammo",

    # MAP VARIANT SCENERY STARTS
    60: "Wall",
    61: "Wall, Half",
    62: "Wall, Quarter",
    63: "Wall, Corner",
    64: "Wall, Slit",
    65: "Wall, T",
    66: "Wall, Double",
    67: "Wedge, Small",
    68: "Wedge, Long",
    69: "Block, Large",
    70: "Block, Double",
    71: "Block, Tall",
    72: "Block, Huge",
    73: "Wedge, Huge",
    74: "Ramp, Long",
    75: "Wedge, Large",
    76: "Wedge, Corner",
    77: "Tube Piece",
    78: "Tube Y-Intersection",
    79: "Tube, Corner",
    80: "Tube Ramp",
    81: "Column, Stone Small",
    82: "Column, Damaged Small",
    83: "Column, Blue Small",
    84: "Column, Red Small",
    85: "Column, Large",
    86: "Column, Stone Large",
    87: "Block, Tiny",
    88: "Block, Small",
    89: "Block, Flat",
    90: "Block, Angled",
    91: "Corner, Small",
    92: "Corner, Large",
    93: "Stone Bridge",
    94: "Obelisk",
    95: "Fin",
    96: "Ramp, Short",
    97: "Ramp, Wide",
    98: "Ramp, Thick",
    99: "Stone Platform",
    100: "Arch",
    101: "Scaffolding",
    102: "Wood Bridge, Large",
    103: "Wood Bridge, Thin",
    104: "Barricade",
    155: "Radio Antennae",
    106: "Fusion Coil",
    107: "Pallet",
    108: "Frav Lift",
    109: "Mancannon",
    101: "Weapon Holder",
    110: "Shield Door",
    112: "FX, Nova",
    113: "FX, Pen And Ink",
    114: "FX, Old Timey",
    115: "FX, Gloomy",
    116: "FX, Colorblind",
    117: "FX, Juicy",
    118: "Light, Blue",
    119: "Light, Red",
    120: "Killball",
    121: "7-Wood",
    122: "Tin Cup",
    123: "Golf Ball",
    124: "Wall, Corner, Short",
    125: "Steel Ramp",
    126: "Steel Wall",
    127: "Steel Barrier",
    128: "Stell Wall, Corner",
    129: "Watchtower Base",
    130: "Forerunner Crate, Blue",
    131: "Forerunner Crate, Red",
    132: "Comm Node",
    133: "Supply Case",
    134: "Supply Case, Open",
    135: "Barricade, Covenant",
    136: "Tube Shield",
    137: "Forklift",
    138: "Dinghy",
    139: "Soccer Ball",
    140: "Ramp, Covenant",
    141: "Door, Small",
    142: "Door, Medium",
    143: "Door, Large",
    144: "Door",
    # MAP VARIANT SCENERY ENDS

    # MAP VARIANT TELEPORTERS START
    145: "Teleporter Sender",
    146: "Teleporter Receiver",
    147: "Teleporter 2-way",
    # MAP VARIANT TELEPORTERS END

    # MAP VARIANT SPAWNERS START
    148: "Respawn Point",
    149: "Assault Initial Spawn Point",
    150: "CTF Initial Spawn Point",
    151: "KOTH Initial Spawn Point",
    152: "Oddball Initial Spawn Point",
    153: "Slayer Initial Spawn Point",
    154: "Territories Initial Spawn Point",
    155: "VIP Initial Spawn Point",
    156: "Assault Respawn Zone",
    157: "CTF Respawn Zone",
    158: "CTF Flag at Home Respawn Zone",
    159: "CTF Flag Away Respawn Zone",
    160: "KOTH Respawn Zone",
    161: "Oddball Respawn Zone",
    162: "Slayer Respawn Zone",
    163: "Territories Respawn Zone",
    164: "VIP Respawn Zone",
    165: "Infection Respawn Zone",
    166: "Spawn Point",
    167: "Spawn Point Invisible",
    # MAP VARIANT SPAWNERS END

    # MAP VARIANT GOALS START
    168: "Flag Spawn Point",
    169: "Flag Return Point",
    170: "Assault Bomb Spawn Point",
    171: "Assault Bomb Goal Area",
    172: "Hill Marker",
    173: "Ball Spawn Point",
    174: "Territory Static",
    175: "VIP Destination Static",
    # MAP VARIANT GOALS END

    # SCENERY START
    174: "Obelisk Eyeball",
    176: "Skull",
    177: "Grid Hidden",
    178: "Spawn Point Invisible",
    179: "Teleporter 2-way Sandbox",
    180: "box_l",
    181: "box_m",
    182: "box_xl",
    183: "box_xxl",
    184: "box_xxxl",
    185: "wall_l",
    186: "wall_m",
    187: "wall_xl",
    188: "wall_xxl",
    189: "wall_xxxl"
}

e_variant_object_placement_flags = [
    'Occupied Slot' ,
    'Object Edited' ,
    'Never Created Scenario Object' ,
    'Scenario Object Bit' ,
    'Placement Create At Rest Bit' ,
    'Scenario Object Removed' ,
    'Object Suspended' ,
    'Object Candy Monitored' ,
    'Spawns Attached' ,
    'Hard Attachment'
]

e_variant_placement_flags = [
    'Unique Spawn Bit',
    'Not Initially Placed Bit',
    'Symmetric Placement',
    'Asymmetric Placement',
    'Timer Starts On Death',
    'Timer Starts On Disturbance',
    'Object Fixed',
    'Object Phased'
]

mp_object_types = [
    ('ORDINARY', 'Ordinary ',''),
    ('WEAPON', 'Weapon',''),
    ('GRENADE', 'Grenade',''),
    ('PROJECTILE', 'Projectile',''),
    ('POWERUP', 'Powerup',''),
    ('EQUIPMENT', 'Equipment',''),
    ('LIGHTVEHICLE', 'Light Land Vehicle',''),
    ('HEAVYVEHICLE', 'Heavy Land Vehicle',''),
    ('FLYINGVEHICLE', 'Flying Vehicle',''),
    ('2WAY', 'Teleporter 2Way',''),
    ('SENDER', 'Teleporter Sender',''),
    ('RECEIVER', 'Teleporter Receiver',''),
    ('SPAWNLOCATION', 'Player Spawn Location',''),
    ('RESPAWNZONE', 'Player Respawn Zone',''),
    ('ODDBALLSPAWN', 'Oddball Spawn Location',''),
    ('FLAGSPAWN', 'Ctf Flag Spawn Location',''),
    ('TARGETSPAWN', 'Target Spawn Location',''),
    ('FLAGRETURN', 'Ctf Flag Return Area',''),
    ('KOTHHILL', 'Koth Hill Area',''),
    ('INFECTIONSAFEAREA', 'Infection Safe Area',''),
    ('TERRITORY', 'Territory Area',''),
    ('VIPAREA', 'Vip Influence Area',''),
    ('VIPDESTINATION', 'Vip Destination Zone',''),
    ('JUGGERNAUTDESTINATION', 'Juggernaut Destination Zone','')
]

'''
*************************************

FUNCTIONS

*************************************
'''

def createForgeObject(context, itemName, i=None, data=None):
    blenderObject = bpy.data.objects.new(itemName if i is None else "%d - %s"%(i,itemName), data)
    context.collection.objects.link(blenderObject)
    blenderObject['isForgeObject'] = True
    blenderObject.forge.object = blenderObject.name
    if itemName in bpy.data.collections:
        blenderObject.instance_collection = bpy.data.collections[itemName]
        blenderObject.instance_type = 'COLLECTION'
        blenderObject.empty_display_size = 0.0001
    else:
        blenderObject.empty_display_type = 'ARROWS'
        blenderObject.empty_display_size = 0.5
    return blenderObject

def getItemName(index):
    try:
        return sandboxItems[index]
    except:
        return 'Unknown'