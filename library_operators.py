import bpy, math, mathutils, random
import os
from os import listdir


class AddToWallLibrary(bpy.types.Operator):
    """Save selected to Wall library. If this button is disabled, select any object to active it."""
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
        filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "libraries\\walls\\")
        name = get_file_name(filepath, "wall")

        bpy.data.libraries.write(os.path.join(filepath, name + ".blend"), ob, fake_user=True)
        assign_material("Walls", (0.9, 0.9, 0.9, 0))
        focus_camera(rotation=(math.radians(85), math.radians(0), math.radians(20)))
        focus_light(rotation=(math.radians(45), math.radians(-45), math.radians(0)))
        set_output_dimensions(512, 512, 100)
        bpy.context.scene.render.filepath = os.path.join(filepath, name + ".png")
        bpy.ops.render.render(write_still=True)
        return {'FINISHED'}


class AddToStructureLibrary(bpy.types.Operator):
    """Save selected to Structure library. If this button is disabled, select any object to active it."""
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
                                "libraries\\structures\\")
        name = get_file_name(filepath, "structure")

        bpy.data.libraries.write(os.path.join(filepath, name + ".blend"), ob, fake_user=True)
        assign_material("Structures", (0.5, 0.5, 0.5, 0))
        focus_camera(rotation=(math.radians(10), math.radians(10), math.radians(0)))
        focus_light(rotation=(math.radians(45), math.radians(-45), math.radians(0)))
        set_output_dimensions(512, 512, 100)
        bpy.context.scene.render.filepath = os.path.join(filepath, name + ".png")
        bpy.ops.render.render(write_still=True)
        return {'FINISHED'}


class AddToHoldLibrary(bpy.types.Operator):
    """Save selected to Hold library. If this button is disabled, select any object to active it."""
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
        filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "libraries\\holds\\")
        name = get_file_name(filepath, "hold")

        bpy.data.libraries.write(os.path.join(filepath, name + ".blend"), ob, fake_user=True)
        assign_material("Holds", (0.1, 0.1, 0.1, 0))
        focus_camera(rotation=(math.radians(60), math.radians(0), math.radians(30)))
        focus_light(rotation=(math.radians(45), math.radians(-45), math.radians(0)))
        set_output_dimensions(512, 512, 100)
        bpy.context.scene.render.filepath = os.path.join(filepath, name + ".png")
        bpy.ops.render.render(write_still=True)
        return {'FINISHED'}


class AddToRockLibrary(bpy.types.Operator):
    """Save selected to Rock library. If this button is disabled, select any object to active it."""
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
        filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "libraries\\rocks\\")
        name = get_file_name(filepath, "rock")

        bpy.data.libraries.write(os.path.join(filepath, name + ".blend"), ob, fake_user=True)
        assign_material("Rocks", (0.1, 0.1, 0.1, 0))
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


def focus_camera(rotation, collection=None):
    if bpy.data.objects.get("Camera Asset") is None:
        camera_data = bpy.data.cameras.new(name="Camera Asset")
        cam_obj = bpy.data.objects.new("Camera Asset", camera_data)
        bpy.context.view_layer.active_layer_collection.collection.objects.link(cam_obj)
    else:
        cam_obj = bpy.data.objects.get("Camera Asset")

    bpy.data.cameras["Camera Asset"].lens = 50
    bpy.context.scene.camera = cam_obj
    cam_obj.rotation_euler = rotation
    if collection is not None:
        bpy.ops.object.select_all(action='DESELECT')
        for obj in bpy.data.collections[collection].objects:
            obj.select_set(True)
    bpy.ops.view3d.camera_to_view_selected()
    bpy.data.cameras["Camera Asset"].lens = 20


def set_output_dimensions(dimension_x, dimension_y, percentage):
    scene = bpy.data.scenes["Scene"]
    scene.render.resolution_x = dimension_x
    scene.render.resolution_y = dimension_y
    scene.render.resolution_percentage = percentage


def focus_light(rotation):
    if not bpy.data.objects.get("Light Asset"):
        light_data = bpy.data.lights.new(name="Light Asset", type='SUN')
        light_obj = bpy.data.objects.new("Light Asset", light_data)
        bpy.context.view_layer.active_layer_collection.collection.objects.link(light_obj)
    else:
        light_obj = bpy.data.objects.get("Light Asset")

    bpy.context.scene.render.engine = 'BLENDER_EEVEE'
    light_obj.rotation_euler = rotation
    light_obj.data.energy = 2


def assign_material(name, color, collection=None):
    material = bpy.data.materials.get(name)

    if not material:
        material = bpy.data.materials.new(name=name)
    material.diffuse_color = color

    if collection is None:
        for obj in bpy.context.selected_objects:
            if obj.data.materials:
                obj.data.materials[0] = material
            else:
                obj.data.materials.append(material)
    else:
        for obj in bpy.data.collections[collection].objects:
            if obj.data.materials:
                obj.data.materials[0] = material
            else:
                obj.data.materials.append(material)


class RemoveFromWallLibrary(bpy.types.Operator):
    """Remove asset from Wall library. If this button is disabled, select any icon from collection to active it."""
    bl_idname = "object.wall_library_remove"
    bl_label = "Remove"

    @classmethod
    def poll(self,context):
        return bpy.data.window_managers["WinMan"].walls_previews

    def execute(self, context):
        icon = bpy.data.window_managers["WinMan"].walls_previews
        delete_asset_from_library(icon, "libraries\\walls\\")
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)


class RemoveFromStructureLibrary(bpy.types.Operator):
    """Remove asset from Structure library. If this button is disabled, select any icon from collection to active it."""
    bl_idname = "object.structure_library_remove"
    bl_label = "Remove"

    @classmethod
    def poll(self,context):
        return bpy.data.window_managers["WinMan"].structures_previews

    def execute(self, context):
        icon = bpy.data.window_managers["WinMan"].structures_previews
        delete_asset_from_library(icon, "libraries\\structures\\")
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)


class RemoveFromHoldLibrary(bpy.types.Operator):
    """Remove asset from Hold library. If this button is disabled, select any icon from collection to active it."""
    bl_idname = "object.hold_library_remove"
    bl_label = "Remove"

    @classmethod
    def poll(self,context):
        return bpy.data.window_managers["WinMan"].holds_previews

    def execute(self, context):
        icon = bpy.data.window_managers["WinMan"].holds_previews
        delete_asset_from_library(icon, "libraries\\holds\\")
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)


class RemoveFromRockLibrary(bpy.types.Operator):
    """Remove asset from Rock library. If this button is disabled, select any icon from collection to active it."""
    bl_idname = "object.rock_library_remove"
    bl_label = "Remove"

    @classmethod
    def poll(self,context):
        return bpy.data.window_managers["WinMan"].rocks_previews

    def execute(self, context):
        icon = bpy.data.window_managers["WinMan"].rocks_previews
        delete_asset_from_library(icon, "libraries\\rocks\\")
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
