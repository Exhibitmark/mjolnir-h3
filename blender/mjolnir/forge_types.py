import bpy, blf, enum
from bpy.props import *
from mathutils import *
from ctypes import *
from math import *

def inverseDict(dict):
    invDict = {}
    for key, val in dict.items():
        if val not in invDict: 
            invDict[val] = key
    return invDict

'''
*************************************

CORE CLASSES

*************************************
'''

class float3(Structure):
    _fields_ = [ 
        ('x', c_float), 
        ('y', c_float), 
        ('z', c_float) 
    ]
    def cross(self, other): 
        return float3(self.y * other.z - self.z * other.y, self.z * other.x - self.x * other.z, self.x * other.y - self.y * other.x)

    def fromVector(vec):
        return float3(vec.x,vec.y,vec.z)

    def toVector(self): 
        return Vector((self.x,self.y,self.z))

    def __str__(self): 
        return "(%.2f,%.2f,%.2f)"%(self.x,self.y,self.z)

class Transform(Structure):
    _fields_ = [
        ('position', float3),
        ('forward', float3),
        ('up', float3) 
    ]
    def __str__(self):
        return "%s %s %s"%(self.position, self.forward, self.up)

    def toMatrix(self):
        fwd = self.forward
        up = self.up
        right = fwd.cross(up)
        pos = self.position
        return Matrix(((right.x,fwd.x,up.x,pos.x),(right.y,fwd.y,up.y,pos.y),(right.z,fwd.z,up.z,pos.z),(0,0,0,1)))

class Range(Structure):
    _fields_ = [ 
        ('min', c_float),
        ('max', c_float) 
    ]
    def __str__(self): 
        return "(%.2f,%.2f)" % (self.min,self.max)


class Bounds(Structure):
    _fields_ = [
        ('x', Range),
        ('y', Range),
        ('z', Range)
    ]
    def __str__(self):
        return "(%s,%s,%s)" % (self.x,self.y,self.z)
'''
*************************************

CLASSES

*************************************
'''

class ShapeData(Structure):
    _fields_ = [
        ('width', c_float),
        ('length', c_float),
        ('top', c_float),
        ('bottom', c_float)
    ]

class ForgeObjectFlags(enum.IntFlag):
    PhysicsNormal = 0b00000000
    PhysicsFixed  = 0b01000000
    PhysicsPhased = 0b11000000
    PhysicsMask   = 0b11000000
    GameSpecific  = 0b00100000
    Asymmetric    = 0b00001000
    Symmetric     = 0b00000100
    SymmetryMask  = 0b00001100
    HideAtStart   = 0b00000010


class Quota(Structure):
    _fields_ = [
        ('object_definition_index', c_int),
        ('min_count', c_ubyte),
        ('max_count', c_ubyte),
        ('count', c_ubyte),
        ('max_allowed', c_ubyte),
        ('price', c_float),
    ]

class MCC_Game(enum.Enum):
    NoGame = 0
    HaloReach = 1
    Halo3 = 2

class PlacementFlags(enum.IntFlag):
    OCCUPIED_SLOT = 1
    OBJECT_EDITED = 2
    NEVER_CREATED_SCENARIO_OBJECT = 4
    SCENARIO_OBJECT_BIT = 8
    PLACEMENT_CREATE_AT_REST_BIT = 16
    SCENARIO_OBJECT_REMOVED = 32
    OBJECT_SUSPENDED = 64
    OBJECT_CANDY_MONITORED = 128
    SPAWNS_ATTACHED = 256
    HARD_ATTACHMENT = 512
'''
*************************************

ENUMS

*************************************
'''

colorNumberToEnum = { 
    0:'RED',
    1:'BLUE',
    2:'GREEN',
    3:'ORANGE',
    4:'PURPLE',
    5:'YELLOW',
    6:'BROWN',
    7:'PINK',
    8:'NEUTRAL',
    255:'TEAM_COLOR'
}

physicsFlags = {
    ForgeObjectFlags.PhysicsNormal: 'NORMAL',
    ForgeObjectFlags.PhysicsFixed: 'FIXED',
    ForgeObjectFlags.PhysicsPhased: 'PHASED'
}

symmetryFlags = {
    ForgeObjectFlags.Symmetric: 'SYMMETRIC',
    ForgeObjectFlags.Asymmetric: 'ASYMMETRIC',
    ForgeObjectFlags.Symmetric + ForgeObjectFlags.Asymmetric: 'BOTH'
}

shapeNumberToEnum = { 
    0:'NONE', 
    1:'SPHERE', 
    2:'CYLINDER', 
    3:'BOX'
}

teamEnum = [
    ('RED', "Red", "", 'SEQUENCE_COLOR_01', 0),
    ('BLUE', "Blue", "", 'SEQUENCE_COLOR_05', 1),
    ('GREEN', "Green", "", 'SEQUENCE_COLOR_04', 2),
    ('ORANGE', "Orange", "", 'SEQUENCE_COLOR_02', 3),
    ('PURPLE', "Purple", "", 'SEQUENCE_COLOR_06', 4),
    ('YELLOW', "Yellow", "", 'SEQUENCE_COLOR_03', 5),
    ('BROWN', "Brown", "", 'SEQUENCE_COLOR_08', 6),
    ('PINK', "Pink", "", 'SEQUENCE_COLOR_07', 7),
    ('NEUTRAL', "Neutral", "", 'SEQUENCE_COLOR_09', 9)
]

colorEnum = teamEnum + [ ('TEAM_COLOR', "Team", "", 'COMMUNITY', 10) ]

teleporterTypes = (12,13,14)

colorEnumToNumber = inverseDict(colorNumberToEnum)
physEnumToFlag = inverseDict(physicsFlags)
symmetryToFlag = inverseDict(symmetryFlags)
colorEnumToNumber = inverseDict(colorNumberToEnum)
shapeEnumToNumber = inverseDict(shapeNumberToEnum)
