# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####
# <pep8 compliant>


bl_info = {
    "name": "Batch Import AMF",
    "author": "p2or",
    "version": (0, 1, 0),
    "blender": (2, 80, 0),
    "location": "File > Import-Export",
    "description": "Import multiple AMF files",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Import-Export"}


import bpy
import os

from bpy_extras.io_utils import ImportHelper

from bpy.props import (BoolProperty,
                       FloatProperty,
                       StringProperty,
                       EnumProperty,
                       CollectionProperty
                       )


class ImportMultipleObjs(bpy.types.Operator, ImportHelper):
    """Batch Import AMF"""
    bl_idname = "import_scene.multiple_objs"
    bl_label = "Import multiple AMF's"
    bl_options = {'PRESET', 'UNDO'}

    # ImportHelper mixin class uses this
    filename_ext = ".amf"

    filter_glob = StringProperty(
            default="*.amf",
            options={'HIDDEN'},
            )

    # Selected files
    files: CollectionProperty(type=bpy.types.PropertyGroup)


    def draw(self, context):
        layout = self.layout


    def execute(self, context):

        # get the folder
        folder = (os.path.dirname(self.filepath))

        # iterate through the selected files
        for i in self.files:

            # generate full path to file
            path_to_file = (os.path.join(folder, i.name))

            bpy.ops.import_scene.amf(filepath = path_to_file)

        return {'FINISHED'}


# Only needed if you want to add into a dynamic menu
def menu_func_import(self, context):
    self.layout.operator(ImportMultipleObjs.bl_idname, text="Bulk .amf Importer")


def register():
    bpy.utils.register_class(ImportMultipleObjs)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)


def .():
    bpy.utils.unregister_class(ImportMultipleObjs)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)


if __name__ == "__main__":
    register()

    # test call
    #bpy.ops.import_scene.multiple_objs('INVOKE_DEFAULT')
