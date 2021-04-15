import bpy, math, mathutils, random
import os
from os import listdir
from . render_operators import focus_camera, focus_light, assign_material, set_output_dimensions


class AddToWallLibrary(bpy.types.Operator):
    """Save selected to Wall library. If this button is disabled, select any object to active it"""
    bl_idname = "object.wall_library"
    bl_label = "Save"

    @classmethod
    def poll(self, context):
        return bpy.context.selected_objects

    def execute(self, context):
        bpy.ops.object.join()
        ob = set(bpy.context.selected_objects)
        for obj in bpy.context.selected_objects:
            obj.name = "wall.001"
        filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.join("libraries", "walls"))
        name = get_file_name(filepath, "wall")

        bpy.data.libraries.write(os.path.join(filepath, name + ".blend"), ob, fake_user=True)
        assign_material("Walls", (0.9, 0.9, 0.9, 1))
        focus_camera(rotation=(math.radians(85), math.radians(0), math.radians(20)))
        focus_light(rotation=(math.radians(45), math.radians(-45), math.radians(0)))
        set_output_dimensions(512, 512, 100)
        bpy.context.scene.render.filepath = os.path.join(filepath, name + ".png")
        bpy.ops.render.render(write_still=True)
        return {'FINISHED'}


class AddToStructureLibrary(bpy.types.Operator):
    """Save selected to Structure library. If this button is disabled, select any object to active it"""
    bl_idname = "object.structure_library"
    bl_label = "Save"

    @classmethod
    def poll(self, context):
        return bpy.context.selected_objects

    def execute(self, context):
        bpy.ops.object.join()
        ob = set(bpy.context.selected_objects)
        for obj in bpy.context.selected_objects:
            obj.name = "structure.001"
        filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                os.path.join("libraries", "structures"))
        name = get_file_name(filepath, "structure")

        bpy.data.libraries.write(os.path.join(filepath, name + ".blend"), ob, fake_user=True)
        assign_material("Structures", (0.5, 0.5, 0.5, 1))
        focus_camera(rotation=(math.radians(10), math.radians(10), math.radians(0)))
        focus_light(rotation=(math.radians(45), math.radians(-45), math.radians(0)))
        set_output_dimensions(512, 512, 100)
        bpy.context.scene.render.filepath = os.path.join(filepath, name + ".png")
        bpy.ops.render.render(write_still=True)
        return {'FINISHED'}


class AddToHoldLibrary(bpy.types.Operator):
    """Save selected to Hold library. If this button is disabled, select any object to active it"""
    bl_idname = "object.hold_library"
    bl_label = "Save"

    @classmethod
    def poll(self, context):
        return bpy.context.selected_objects

    def execute(self, context):
        bpy.ops.object.join()
        ob = set(bpy.context.selected_objects)
        for obj in bpy.context.selected_objects:
            obj.name = "hold.001"
        filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.join("libraries", "holds"))
        name = get_file_name(filepath, "hold")

        bpy.data.libraries.write(os.path.join(filepath, name + ".blend"), ob, fake_user=True)
        assign_material("Holds", (0.1, 0.1, 0.1, 1))
        focus_camera(rotation=(math.radians(60), math.radians(0), math.radians(30)))
        focus_light(rotation=(math.radians(45), math.radians(-45), math.radians(0)))
        set_output_dimensions(512, 512, 100)
        bpy.context.scene.render.filepath = os.path.join(filepath, name + ".png")
        bpy.ops.render.render(write_still=True)
        return {'FINISHED'}


class AddToRockLibrary(bpy.types.Operator):
    """Save selected to Rock library. If this button is disabled, select any object to active it"""
    bl_idname = "object.rock_library"
    bl_label = "Save"

    @classmethod
    def poll(self, context):
        return bpy.context.selected_objects

    def execute(self, context):
        bpy.ops.object.join()
        ob = set(bpy.context.selected_objects)
        for obj in bpy.context.selected_objects:
            obj.name = "rock.001"
        filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.join("libraries", "rocks"))
        name = get_file_name(filepath, "rock")

        bpy.data.libraries.write(os.path.join(filepath, name + ".blend"), ob, fake_user=True)
        assign_material("Rocks", (0.1, 0.1, 0.1, 1))
        focus_camera(rotation=(math.radians(85), math.radians(0), math.radians(20)))
        focus_light(rotation=(math.radians(45), math.radians(-45), math.radians(0)))
        set_output_dimensions(512, 512, 100)
        bpy.context.scene.render.filepath = os.path.join(filepath, name + ".png")
        bpy.ops.render.render(write_still=True)
        return {'FINISHED'}


def get_file_name(filepath, name):
    file_numbers = list(map(filenames_to_ints, listdir(filepath)))
    file_numbers.sort()
    number = 0

    while number in file_numbers:
        number += 1
    return name + "_" + str(number)


def filenames_to_ints(file_name):
    return int(file_name.split("_")[1].split(".")[0])


class RemoveFromWallLibrary(bpy.types.Operator):
    """Remove asset from Wall library. If this button is disabled, select any icon from collection to active it"""
    bl_idname = "object.wall_library_remove"
    bl_label = "Remove"

    @classmethod
    def poll(self,context):
        return bpy.data.window_managers["WinMan"].walls_previews

    def execute(self, context):
        icon = bpy.data.window_managers["WinMan"].walls_previews
        delete_asset_from_library(icon, os.path.join("libraries", "walls"))
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)


class RemoveFromStructureLibrary(bpy.types.Operator):
    """Remove asset from Structure library. If this button is disabled, select any icon from collection to active it"""
    bl_idname = "object.structure_library_remove"
    bl_label = "Remove"

    @classmethod
    def poll(self,context):
        return bpy.data.window_managers["WinMan"].structures_previews

    def execute(self, context):
        icon = bpy.data.window_managers["WinMan"].structures_previews
        delete_asset_from_library(icon, os.path.join("libraries", "structures"))
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)


class RemoveFromHoldLibrary(bpy.types.Operator):
    """Remove asset from Hold library. If this button is disabled, select any icon from collection to active it"""
    bl_idname = "object.hold_library_remove"
    bl_label = "Remove"

    @classmethod
    def poll(self,context):
        return bpy.data.window_managers["WinMan"].holds_previews

    def execute(self, context):
        icon = bpy.data.window_managers["WinMan"].holds_previews
        delete_asset_from_library(icon, os.path.join("libraries", "holds"))
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)


class RemoveFromRockLibrary(bpy.types.Operator):
    """Remove asset from Rock library. If this button is disabled, select any icon from collection to active it"""
    bl_idname = "object.rock_library_remove"
    bl_label = "Remove"

    @classmethod
    def poll(self,context):
        return bpy.data.window_managers["WinMan"].rocks_previews

    def execute(self, context):
        icon = bpy.data.window_managers["WinMan"].rocks_previews
        delete_asset_from_library(icon, os.path.join("libraries", "rocks"))
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

def delete_asset_from_library(icon, directory):
    asset = icon.split('.')[0] + ".blend"
    filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)),directory)
    icon = os.path.join(filepath, icon)
    asset = os.path.join(filepath, asset)
    os.remove(icon)
    os.remove(asset)

classes = (
    AddToWallLibrary,
    AddToStructureLibrary,
    AddToHoldLibrary,
    AddToRockLibrary,
    RemoveFromWallLibrary,
    RemoveFromStructureLibrary,
    RemoveFromHoldLibrary,
    RemoveFromRockLibrary
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
