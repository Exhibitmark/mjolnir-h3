from ast import If
import bpy
import time
from os.path import exists
from ctypes import *
from importlib import reload
import binascii
import struct
import mjolnir.utils

import mjolnir.halo3
import mjolnir.forge_types
import mjolnir.forge_props
reload(mjolnir.halo3)
reload(mjolnir.forge_types)
reload(mjolnir.forge_props)
reload(mjolnir.utils)

from mjolnir.forge_types import *
from mjolnir.forge_props import *
from mjolnir.halo3 import *
from mjolnir.utils import *

dllPath = bpy.path.abspath("//") + "ForgeBridge.dll"
mapPalette = 'Sandbox Palette'
maxObjectCount = 640
quotas = None

def tryReload():
    forge.ReadMemory()

def ShowMessageBox(message = "", title = "Message Box", icon = 'INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

def tryGetForgeObjectFromInstance(instance):
    object = instance.object
    if instance.is_instance and object.is_instancer:
        return object
    elif object.get('isForgeObject',False):
        p = object.parent
        if p is None or p.instance_type == 'NONE' or p.instance_type == 'COLLECTION': 
            return object
    else:
        return None

def checkRemove(val):
    return bool((val >> 5) & 1)

def importForgeObjects(context, self=None, createCollections=False):
    bpy.types.Object.protected = BoolProperty(name = 'protected', default = False)
    if context.scene.name == 'Props': 
        return False
    if not forge.TrySetConnect(True):
        return False

    t0 = time.time()

    forge.ReadMemory()
    forge.FindPointer()
    mvar = None
    mvar = forge.GetH3_MVAR_Ptr().contents
    print("Name: %s (by %s)" % (mvar.data.display_name, mvar.data.author.decode()))
    print("Description: " + mvar.data.description.decode())
    print("Scenario Objects: "+ str(mvar.data.scenario_objects))
    quotas = mvar.quotas

    for i in range(mvar.data.variant_objects):
        forgeObject = mvar.objects[i]
        itemName = "%s (%d, %d, %d)" % (getItemName(forgeObject.definition_index),forgeObject.definition_index, forgeObject.object_index, forgeObject.helper_index)

        if getItemName(forgeObject.definition_index) != 'Unknown' and checkRemove(forgeObject.placement) == False:
            itemName = getItemName(forgeObject.definition_index)
        else:
            collection = bpy.data.collections.new(itemName)
            #bpy.data.scenes['Scene'].collection.children.link(collection)
            blenderObject = bpy.data.objects.new(itemName, None)
            collection.objects.link(blenderObject)
            blenderObject.empty_display_type = 'ARROWS'
            blenderObject.empty_display_size = 0.5
        #if (i > mvar.data.scenario_objects and forgeObject.definition_index != -1) or (i < mvar.data.scenario_objects):
        blenderObject = createForgeObject(context, itemName, i)
        if i <= mvar.data.scenario_objects:
            blenderObject.protected = True

        for x in range(len(blenderObject.forge.placementFlags)):
            blenderObject.forge.placementFlags[x] = setFlags(forgeObject.placement, x)

        for x in range(len(blenderObject.forge.variantPlacementFlags)):
            blenderObject.forge.variantPlacementFlags[x] = setFlags(forgeObject.mp_placement, x)
        blenderObject.forge.sharedStorage = forgeObject.shared_storage
        blenderObject.forge.spawnTime = forgeObject.spawn_time_seconds
        blenderObject.name = blenderObject.name
        blenderObject['placement'] = forgeObject.placement
        blenderObject['reuse_timeout'] = forgeObject.reuse_timeout
        blenderObject['object_index'] = forgeObject.object_index
        blenderObject['helper_index'] = forgeObject.helper_index
        blenderObject['definition_index'] = forgeObject.definition_index
        blenderObject.matrix_world = forgeObject.transform.toMatrix()
        blenderObject['attached_id'] = forgeObject.attached_id
        blenderObject['attached_bsp_index'] = forgeObject.attached_bsp_index
        blenderObject['attached_type'] = forgeObject.attached_type
        blenderObject['attached_source'] = forgeObject.attached_source

        blenderObject['game_engine_flags'] = forgeObject.game_engine_flags
        blenderObject['mp_placement'] = forgeObject.mp_placement
        blenderObject['team'] = forgeObject.team
        blenderObject['shared_storage'] = forgeObject.shared_storage
        blenderObject['spawn_time_seconds'] = forgeObject.spawn_time_seconds
        blenderObject['object_type'] = forgeObject.object_type
        blenderObject['shape'] = forgeObject.shape
        blenderObject['width'] = forgeObject.shape_data.width
        blenderObject['length'] = forgeObject.shape_data.length
        blenderObject['top'] = forgeObject.shape_data.top
        blenderObject['bottom'] = forgeObject.shape_data.bottom

    print("Imported %d objects in %.3fs" % (mvar.data.variant_objects ,time.time() - t0))
    forge.ClearObjectList()
    return {'FINISHED'}

def setFlags(value, bit):
    return (value>>bit) & 1

def getStringEnum(options, val):
    return options.index(val)

def toStruct(obj, m):
    if obj['definition_index'] != -1:
        fields = [
            getFlagsVal(obj.forge.placementFlags),
            0,
            -1,
            -1,
            obj['definition_index'],
            round(m.col[3][0],4),
            round(m.col[3][1],4),
            round(m.col[3][2],4),
            round(m.col[1][0],4),
            round(m.col[1][1],4),
            round(m.col[1][2],4),
            round(m.col[2][0],4),
            round(m.col[2][1],4),
            round(m.col[2][2],4),
            -1,
            -1,
            255,
            255,
            1023, # e_scenario_game_engine just makes it valid for everything
            getFlagsVal(obj.forge.variantPlacementFlags),
            obj['team'],
            obj.forge.sharedStorage,
            obj.forge.spawnTime,
            obj['object_type'],
            obj['shape'],
            obj['width'],
            obj['length'],
            obj['top'],
            obj['bottom']
        ]
        try:
            return struct.Struct('<hhiiifffffffffihBBhBBBBBBffff').pack(*fields)
        except struct.error as e:
            print("Error: " + e)

    else:
        return None

def checkQuota(obj):
    index = obj['definition_index']
    quota = quotas[index]

def exportForgeObjects(self=None):
    #if not forge.TrySetConnect(True):
       # return False

    hitLimit = False
    t0 = time.time()
    i = 0
    for instance in bpy.context.evaluated_depsgraph_get().object_instances:
        if instance.object.name in bpy.context.scene.collection.all_objects and instance.object.name != 'Sandbox':
            blenderObject = tryGetForgeObjectFromInstance(instance)
            if blenderObject != None:
                if i >= maxObjectCount: 
                    hitLimit = True
                    continue
                if not hitLimit:
                    forgeObject = forge.GetObjectPtr(i).contents
                    blenderObject.forge.ToForgeObject(forgeObject, blenderObject, instance)
                    b = toStruct(blenderObject, instance.matrix_world)
                    if i in range(2,640):
                        if b != None:
                            if 'Grid' not in instance.object.name and 'Invisible' not in instance.object.name:
                                #'porter' not in instance.object.name and 
                                #print(binascii.hexlify(b))
                                forge.WriteMemory(binascii.hexlify(b), i-2)

            i += 1
    forge.WriteCount(i)
    ShowMessageBox("Exported %d objects in %.3fs" % (i, time.time() - t0))
    print("Exported %d objects in %.3fs" % (i, time.time() - t0), "Export Success")
    return {'FINISHED'} 

def modPhysics():
    forge.TogglePhysics()

def bridgeMain():
    global forge
    forge = cdll.LoadLibrary(dllPath)
    print("ForgeBridge.dll Version is: %d" % forge.GetDllVersion())
    forge.TrySetConnect.restype = c_bool
    forge.GetObjectPtr.restype = POINTER(H3_ForgeObject)
    forge.GetH3_MVAR_Ptr.restype = POINTER(H3_MVAR)
    forge.GetH3_MVAR.restype = H3_MVAR
    if forge.TrySetConnect(True):
        forge.ReadMemory()