import bpy, math, mathutils, bpy_extras.view3d_utils, random
import os
from os import listdir
from . operators import add_mesh, move_with_snapping

class CreateEmptyScene(bpy.types.Operator):
    """Delete all objects and create new empty scene."""
    bl_idname = "object.empty_scene"
    bl_label = "Prepare new scene"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.object.select_all(action='SELECT')
        if bpy.context.selected_objects:
            bpy.ops.object.delete()
        for c in bpy.data.collections:
            bpy.data.collections.remove(c)
        for m in bpy.data.materials:
            bpy.data.materials.remove(m)
        for c in bpy.data.curves:
            bpy.data.curves.remove(c)
        for m in bpy.data.meshes:
            bpy.data.meshes.remove(m)
        for l in bpy.data.lights:
            bpy.data.lights.remove(l)
        for c in bpy.data.cameras:
            bpy.data.cameras.remove(c)

        wall_collection = create_collection("walls")
        create_collection("structures", wall_collection)
        create_collection("route", wall_collection, get_random_color_tag())
        rock_collection = create_collection("rocks")
        create_collection("path", rock_collection, get_random_color_tag())
        ref_collection = create_collection("reference")
        create_collection("carabiners", ref_collection)
        create_collection("human", ref_collection)
        bpy.context.scene.frame_set(0)

        bpy.data.window_managers["WinMan"].carabiners.clear()
        bpy.data.window_managers["WinMan"].carabiners_index = -1
        bpy.data.window_managers["WinMan"].route_collection = "route"
        bpy.data.window_managers["WinMan"].path_collection = "path"
        bpy.data.window_managers["WinMan"].collections_previews = "carabiners"
        return {'FINISHED'}


def create_collection(name, parent=None, color=None):
    collection = bpy.data.collections.new(name)
    if parent is None:
        bpy.context.scene.collection.children.link(collection)
    else:
        parent.children.link(collection)
    if color is not None:
        collection.color_tag = color
    return collection


def get_random_color_tag():
    index = random.randint(0, 8)
    colors = ['NONE', 'COLOR_01', 'COLOR_02', 'COLOR_03', 'COLOR_04', 'COLOR_05', 'COLOR_06', 'COLOR_07', 'COLOR_08']
    return colors[index]


class AddWallFromCollection(bpy.types.Operator):
    """Add Wall asset from collection. If this button is disabled, select any icon from collection to active it"""
    bl_idname = "object.wall"
    bl_label = "Add"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(self, context):
        return bpy.data.window_managers["WinMan"].walls_previews

    def execute(self, context):
        if "walls" not in bpy.data.collections.keys():
            self.report({'ERROR'}, "Corrupted collection hierarchy, press Pepare new scene to reset.") 
            return {'CANCELLED'}

        icon = bpy.data.window_managers["WinMan"].walls_previews
        asset = icon.split('.')[0] + ".blend"

        bpy.ops.object.select_all(action='DESELECT')
        add_mesh("libraries\\walls\\" + asset, context, "walls")
        return {'FINISHED'}


class AddStructuresFromCollection(bpy.types.Operator):
    """Add Structure asset from collection. If this button is disabled, select any icon from collection to active it"""
    bl_idname = "object.structure"
    bl_label = "Add"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(self, context):
        return bpy.data.window_managers["WinMan"].structures_previews

    def execute(self, context):
        if "structures" not in bpy.data.collections.keys():
            self.report({'ERROR'}, "Corrupted collection hierarchy, press Pepare new scene to reset.") 
            return {'CANCELLED'}

        icon = bpy.data.window_managers["WinMan"].structures_previews
        asset = icon.split(".")[0] + ".blend"

        bpy.ops.object.select_all(action='DESELECT')
        add_mesh("libraries\\structures\\" + asset, context, "structures")
        move_with_snapping(self, context, context.active_object)
        return {'FINISHED'}


class AddHoldsFromCollection(bpy.types.Operator):
    """Add Hold asset from collection. If this button is disabled, select any icon from collection to active it"""
    bl_idname = "object.hold"
    bl_label = "Add"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(self, context):
        return bpy.data.window_managers["WinMan"].holds_previews

    def execute(self, context):
        number_of_routes = 0
        for key in bpy.data.collections.keys():
            if key.split(".")[0] == "route":
                number_of_routes += 1
        if number_of_routes == 0:
            self.report({'ERROR'}, "Corrupted collection hierarchy, press Pepare new scene to reset.") 
            return {'CANCELLED'}

        icon = bpy.data.window_managers["WinMan"].holds_previews
        asset = icon.split('.')[0] + ".blend"

        bpy.ops.object.select_all(action='DESELECT')
        add_mesh("libraries\\holds\\" + asset, context, bpy.data.window_managers["WinMan"].route_collection)
        move_with_snapping(self, context, context.active_object)
        return {'FINISHED'}


class AddRocksFromCollection(bpy.types.Operator):
    """Add Rock asset from collection. If this button is disabled, select any icon from collection to active it"""
    bl_idname = "object.rock"
    bl_label = "Add"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(self, context):
        return bpy.data.window_managers["WinMan"].rocks_previews

    def execute(self, context):
        if "rocks" not in bpy.data.collections.keys():
            self.report({'ERROR'}, "Corrupted collection hierarchy, press Pepare new scene to reset.") 
            return {'CANCELLED'}

        icon = bpy.data.window_managers["WinMan"].rocks_previews
        asset = icon.split('.')[0] + ".blend"

        bpy.ops.object.select_all(action='DESELECT')
        add_mesh("libraries\\rocks\\" + asset, context, "rocks")
        return {'FINISHED'}


class AddRouteCollection(bpy.types.Operator):
    """Adds new route collection"""
    bl_idname = "object.add_route_collection"
    bl_label = "Add new route"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if "walls" not in bpy.data.collections.keys():
            self.report({'ERROR'}, "Corrupted collection hierarchy, press Pepare new scene to reset.") 
            return {'CANCELLED'}

        wall_collection = bpy.data.collections["walls"]
        collection = create_collection("route", wall_collection, get_random_color_tag())
        bpy.data.window_managers["WinMan"].route_collection = collection.name
        return {'FINISHED'}

class AddPathCollection(bpy.types.Operator):
    """Adds new path collection"""
    bl_idname = "object.add_path_collection"
    bl_label = "Add new path"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if "rocks" not in bpy.data.collections.keys():
            self.report({'ERROR'}, "Corrupted collection hierarchy, press Pepare new scene to reset.") 
            return {'CANCELLED'}

        rock_collection = bpy.data.collections["rocks"]
        collection = create_collection("path", rock_collection, get_random_color_tag())
        bpy.data.window_managers["WinMan"].path_collection = collection.name
        return {'FINISHED'}


classes = (
    CreateEmptyScene,
    AddWallFromCollection,
    AddStructuresFromCollection,
    AddHoldsFromCollection,
    AddRocksFromCollection,
    AddRouteCollection,
    AddPathCollection
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
