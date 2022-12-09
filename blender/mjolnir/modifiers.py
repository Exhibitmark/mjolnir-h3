import bpy, blf, enum, time
from bpy.types import Operator
from bpy.props import *
from mathutils import *
from ctypes import *
from math import *


def arrayModifier(context, type, count=3, offset=(1,0,0), rotation=(0,0,0), curveLen=5):
    sourceObject = context.active_object
    loc = sourceObject.location
    size = 1

    collection = sourceObject.instance_collection
    if collection != None:
        name = collection.name

        for instanced_object in collection.objects:
            s = instanced_object.dimensions.y
            if s > size: size = s
    else: 
        name = sourceObject.name

    bpy.ops.mesh.primitive_plane_add(enter_editmode=False, align='WORLD', location=loc, size=1)
    arrayObject = masterParent = context.object
    arrayObject.name = "%s Array" % name
    arrayObject.instance_type = 'FACES'
    arrayObject.show_instancer_for_viewport = arrayObject.show_instancer_for_render = False
    arrayObject.select_set(True)
    
    bpy.ops.object.modifier_add(type='ARRAY')
    modifier = arrayObject.modifiers["Array"]
    modifier.show_on_cage = True
    modifier.use_relative_offset = False

    if type != 'CONST':
        parentObject = masterParent = bpy.data.objects.new("%s Array Holder" % name, None)
        context.collection.objects.link(parentObject)
        parentObject.location = loc
        parentObject.empty_display_size = 2
        arrayObject.parent = parentObject
        arrayObject.location = (0,0,0)


    if type == 'OBJECT':
        offsetObj = bpy.data.objects.new("%s Array Offset" % name, None)
        context.collection.objects.link(offsetObj)
        offsetObj.empty_display_size = size
        offsetObj.location = offset
        offsetObj.rotation_euler = rotation
        offsetObj.parent = parentObject
        offsetObj.select_set(True)

        modifier.use_constant_offset = False
        modifier.use_object_offset = True
        modifier.offset_object = offsetObj

    else:
        modifier.use_constant_offset = True
        modifier.constant_offset_displace = offset
    if type == 'CURVE':
        bpy.ops.object.modifier_add(type='CURVE')
        curveModifier = arrayObject.modifiers["Curve"]
        curveModifier.show_on_cage = curveModifier.show_in_editmode = True
        
        bpy.ops.curve.primitive_bezier_curve_add(enter_editmode=False, align='WORLD', location=(0,0,0), radius=curveLen)
        curve = bpy.context.object
        curve.name = "%s Curve" % name
        curve.parent = parentObject
        curve.select_set(True)
        curveData = curve.data
        curveData.twist_mode = 'Z_UP'
        curveData.use_deform_bounds = curve.show_in_front = True

        modifier.fit_type = 'FIT_CURVE'
        modifier.curve = curve
        curveModifier.object = curve

        arrayObject.select_set(True)
    else:
        modifier.count = count

    masterParent.rotation_euler = sourceObject.rotation_euler

    sourceObject.parent = arrayObject
    sourceObject.location = (0,0,0)
    sourceObject.rotation_euler = (0,0,0)
    sourceObject.display_type = 'BOUNDS'
    sourceObject.select_set(True)
        
    
    if type != 'CONST': 
        parentObject.select_set(True)
