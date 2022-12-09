
import bpy
import sys
import os
from bpy.props import *
from bpy.types import Scene
from importlib import reload

dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
   sys.path.append(dir)

import mjolnir.forge_types
reload(mjolnir.forge_types)

import mjolnir.halo3
reload(mjolnir.halo3)

from mjolnir.halo3 import *
from mjolnir.forge_types import *

'''
*************************************

CLASSES

*************************************
'''

class ForgeCollectionProperties(bpy.types.PropertyGroup):
    def iconsEnum(self, context):
        icons = bpy.types.UILayout.bl_rna.functions['prop'].parameters['icon'].enum_items.keys()
        icoEnum = []
        for i in range(0,len(icons)):
            ico = icons[i]
            icoEnum.append((ico,"",ico,ico,i))
        return icoEnum
        
    icon: EnumProperty(name="Icon",description="Icon used in menus", items=iconsEnum, default=0)

class ForgeCollectionPanel(bpy.types.Panel):
    bl_label = "Forge Collection"
    bl_idname = 'SCENE_PT_forge_collection'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'collection'
    
    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        collectionProps = context.collection.forge
        layout.prop(collectionProps, 'icon')
    
class ForgeObjectProperties(bpy.types.PropertyGroup):
    def UpdateColor(self, context):
        color = self.color
        if color == 'TEAM_COLOR': 
            color = self.team
        self.colorIndex = colorEnumToNumber[color]

    def UpdateShape(self, context):
        shapeObject = bpy.data.objects.get(self.shapeObject, None)
        if self.shape == 'NONE':
            if shapeObject != None: 
                bpy.data.objects.remove(shapeObject, do_unlink=True)
            return
        
        if shapeObject is None:
            shapeObject = bpy.data.objects.new("%s Shape" % self.object, None)
            self.shapeObject = shapeObject.name
            collection = context.collection
            collection.objects.link(shapeObject)
            shapeObject.rotation_euler = Euler((0,0,radians(90)))
            shapeObject.show_instancer_for_viewport = shapeObject.show_instancer_for_render = False
            shapeObject.instance_type = 'COLLECTION'
            blenderObject = bpy.data.objects[self.object]
            shapeObject.parent = blenderObject
        
        collection = None
        if self.shape == 'BOX':
            collection = bpy.data.collections['Shape Box']
            shapeObject.scale = (self.width, self.length, self.top + self.bottom)
        elif self.shape == 'CYLINDER':
            collection = bpy.data.collections['Shape Cylinder']
            diameter = self.width * 2
            shapeObject.scale = (diameter, diameter, self.top + self.bottom)

        if shapeObject.instance_collection != collection: 
            shapeObject.instance_collection = collection
        
        shapeObject.location = (0, 0, (self.top - self.bottom) / 2)

    def UpdatePhysics(self, context):
        mode = self.physics
        if mode == 'NORMAL':
            self.variantPlacementFlags[6] = False
            self.variantPlacementFlags[7] = False
        elif mode == 'FIXED':
            self.variantPlacementFlags[6] = True
            self.variantPlacementFlags[7] = False
        elif mode == 'PHASED':
            self.variantPlacementFlags[6] = False
            self.variantPlacementFlags[7] = True

    def UpdateObjectType(self, context):
        current = self.mpObjectType
        for i, value in enumerate(mp_object_types):
            if current == value[0]:
                bpy.context.selected_objects[0]['object_type'] = i

    def UpdateDefinitionIndex(self, context):
        current = self.mpObjectType
        for i, value in enumerate(mp_object_types):
            if current == value[0]:
                bpy.context.selected_objects[0]['object_type'] = i

    shapeObject: StringProperty()
    objectPlacementFlags: EnumProperty(name="Physics", description="Physics mode", default='PHASED',
        items= [
            ('NORMAL', "Normal", "Affected by gravity and movable"),
            ('FIXED', "Fixed", "Unaffected by gravity"),
            ('PHASED', "Phased", "Unaffected by gravity and collisionless"),
        ]
    )
    
    physics: EnumProperty(name="Physics", description="Physics mode", default='PHASED',
        items= [
            ('NORMAL', "Normal", "Affected by gravity and movable"),
            ('FIXED', "Fixed", "Unaffected by gravity"),
            ('PHASED', "Phased", "Unaffected by gravity and collisionless"),
        ],
        update=UpdatePhysics
    )
    team: EnumProperty(name="Team", description="Object team", items=teamEnum, default='NEUTRAL', update=UpdateColor)
    color: EnumProperty(name="Color", description="Object color", items=colorEnum, default='TEAM_COLOR', update=UpdateColor)
    colorIndex: IntProperty(default=8)
    spawnTime: IntProperty(name="Spawn Time", description="Time in seconds before the object spawns or respawns", min=0, max=255)# 0 is never
    sharedStorage: IntProperty(name="Channel", description="Shared Storage(Channels,Ammo)", default=0)
    gameSpecific: BoolProperty(name="Game Specific", description="Should object exclusively spawn for current gamemode")
    placeAtStart: BoolProperty(name="Place At Start", description="Should object spawn at start", default=True)

    Scene.placementFlagsStatus = BoolProperty(
        default=False
    )

    placementFlags: BoolVectorProperty( name="Prop name", description="Object Placement Flags", size = 10, default = (False,) * 10)

    Scene.variantPlacementFlagStatus = BoolProperty(
        default=False
    )
    variantPlacementFlags: BoolVectorProperty( name="Prop name", description="Variant Placement Flags", size = 8, default = (False,) * 8)

    mpObjectType: EnumProperty(name="Multiplayer Object Type", description="Shows different forge menu options", items= mp_object_types, default='ORDINARY', update=UpdateObjectType)

    symmetry: EnumProperty(name="Symmetry", description="Gamemode symmetry",
        items=[
            ('BOTH', "Both", "Present in symmetric and asymmetric gamemodes (default)"),
            ('SYMMETRIC', "Symmetric", "Present only in symmetric gamemodes"),
            ('ASYMMETRIC', "Asymmetric", "Present only in asymmetric gamemodes"),
        ],
        default='BOTH'
    )
    
    shape: EnumProperty(name="Shape", description="Area shape", default='NONE', update=UpdateShape,
        items= [
            ('NONE', "None", ""), 
            ('CYLINDER', "Cylinder", ""), 
            ('BOX', "Box", "")
        ]
    )

    width: FloatProperty(name="Width", description="", unit='LENGTH', min=0, max=60.0, update=UpdateShape)
    length: FloatProperty(name="Length", description="", unit='LENGTH', min=0, max=60.0, update=UpdateShape)
    top: FloatProperty(name="Top", description="Distance to top from center", unit='LENGTH', min=0, max=60.0, update=UpdateShape)
    bottom: FloatProperty(name="Bottom", description="Distance to bottom from center", unit='LENGTH', min=0, max=60.0, update=UpdateShape)


    def ToForgeObject(self, forgeObject, blobj, inst=None):
        forgeObject.team = colorEnumToNumber[self.team]
        forgeObject.color = colorEnumToNumber[self.color]
        forgeObject.flags = ForgeObjectFlags.HideAtStart*(not self.placeAtStart) + ForgeObjectFlags.GameSpecific*self.gameSpecific + physEnumToFlag[self.physics] + symmetryToFlag[self.symmetry]
        forgeObject.spawnTime = self.spawnTime
        forgeObject.sharedStorage = self.sharedStorage
        forgeObject.shape = shapeEnumToNumber[self.shape]
        '''forgeObject.shape_data.width = self.width
        forgeObject.shape_data.length = self.length
        forgeObject.shape_data.top = self.top
        forgeObject.shape_data.bottom = self.bottom'''
        m = inst.matrix_world
        forgeObject.forward = float3.fromVector(m.col[1])
        forgeObject.up = float3.fromVector(m.col[2])
        forgeObject.position = float3.fromVector(m.col[3])
        #print(forgeObject.position)