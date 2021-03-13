import bpy, math, mathutils, bpy_extras, random
from bpy_extras.view3d_utils import region_2d_to_location_3d
import os
from os import listdir

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

        wall_collection = bpy.data.collections.new("walls")
        bpy.context.scene.collection.children.link(wall_collection)
        structure_collection = bpy.data.collections.new("structures")
        wall_collection.children.link(structure_collection)
        path_collection = bpy.data.collections.new("route")
        wall_collection.children.link(path_collection)
        rock_collection = bpy.data.collections.new("rocks")
        bpy.context.scene.collection.children.link(rock_collection)
        ref_collection = bpy.data.collections.new("reference")
        bpy.context.scene.collection.children.link(ref_collection)
        human_collection = bpy.data.collections.new("human")
        ref_collection.children.link(human_collection)
        carabiners_collection = bpy.data.collections.new("carabiners")
        ref_collection.children.link(carabiners_collection)
        return {'FINISHED'}


class AddRouteCollection(bpy.types.Operator):
    """Adds new route collection."""
    bl_idname = "object.add_route_collection"
    bl_label = "Add new route"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if "walls" not in bpy.data.collections.keys():
            self.report({'ERROR'}, "Corrupted collection hierarchy, press Pepare new scene to reset.") 
            return {'CANCELLED'}

        wall_collection = bpy.data.collections["walls"]
        path_collection = bpy.data.collections.new("route")
        wall_collection.children.link(path_collection)
        return {'FINISHED'}


class MoveObjectWithSnapping(bpy.types.Operator):
    """Move selected objects. If this button is disabled, select any object to active it."""
    bl_idname = "object.move_object_with_snapping"
    bl_label = "Move"

    @classmethod
    def poll(self, context):
        return bpy.context.selected_objects and bpy.context.active_object and\
               bpy.context.active_object.mode == 'OBJECT'

    def execute(self, context):
        move_with_snapping(self, context, bpy.context.selected_objects[0])
        return {'FINISHED'}


def move_with_snapping(self, context, obj):
    x, y, z = obj.location.x, obj.location.y, obj.location.z
    loc = bpy_extras.view3d_utils.location_3d_to_region_2d(bpy.context.region,
                                                           bpy.context.space_data.region_3d,
                                                           (x, y, z), (0, 0))

    context.window.cursor_warp(loc.x, loc.y)
    rotation_set_up(context, [True,True,True,False,True], {'FACE'})
    bpy.ops.transform.translate('INVOKE_DEFAULT')


def rotation_set_up(context, boolSettings, snap_elements):
    bpy.context.scene.tool_settings.snap_elements = snap_elements
    bpy.context.scene.tool_settings.use_snap = boolSettings[0]
    bpy.context.scene.tool_settings.use_snap_rotate = boolSettings[1]
    bpy.context.scene.tool_settings.use_snap_translate = boolSettings[2]
    bpy.context.scene.tool_settings.use_snap_project = boolSettings[3]
    bpy.context.scene.tool_settings.use_snap_align_rotation = boolSettings[4]
    bpy.context.scene.tool_settings.snap_target = 'ACTIVE'


class RotateModal(bpy.types.Operator):
    """Rotate selected objects. If this button is disabled, select any object to active it."""
    bl_idname = "object.rotate_modal"
    bl_label = "Rotate"
    bl_options = {'REGISTER', 'UNDO'}
    x = 0
    init_rotation = [0, 0, 0]

    @classmethod
    def poll(self, context):
        return bpy.context.selected_objects and bpy.context.active_object and\
               bpy.context.active_object.mode == 'OBJECT'

    def modal(self, context, event):
        obj = bpy.context.object
        if event.type == 'MOUSEMOVE':
            change_x = event.mouse_region_x
            obj.rotation_euler.rotate_axis("Z", math.radians(change_x - self.x))
            self.x = change_x

        if event.type in ['LEFTMOUSE', 'ENTER']:
            return {'FINISHED'}

        if event.type in ['ESC', 'RIGHTMOUSE']:
            obj.rotation_euler = self.init_rotation
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        self.init_rotation = bpy.context.object.rotation_euler.copy()
        self.x = event.mouse_x
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


class ScaleObject(bpy.types.Operator):
    """Scale selected objects. If this button is disabled, select any object to active it."""
    bl_idname = "object.scale"
    bl_label = "Scale"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(self, context):
        return bpy.context.selected_objects and bpy.context.active_object \
               and bpy.context.active_object.mode == 'OBJECT'

    def execute(self, context):
        bpy.ops.transform.resize('INVOKE_DEFAULT')
        return {'FINISHED'}


class DeleteObject(bpy.types.Operator):
    """Delete selected objects. If this button is disabled, select any object to active it."""
    bl_idname = "object.delete"
    bl_label = "Delete"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(self, context):
        return bpy.context.selected_objects and bpy.context.active_object.mode == 'OBJECT'

    def execute(self, context):
        for obj in bpy.context.selected_objects:
            bpy.data.objects.remove(obj, do_unlink=True)
        return {'FINISHED'}


class AddWallFromCollection(bpy.types.Operator):
    """Add Wall asset from collection. If this button is disabled, select any icon from collection to active it."""
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
    """Add Structure asset from collection. If this button is disabled, select any icon from collection to active it."""
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
    """Add Hold asset from collection. If this button is disabled, select any icon from collection to active it."""
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
    """Add Rock asset from collection. If this button is disabled, select any icon from collection to active it."""
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


def add_mesh(file_name, context, collection_name=None):
    filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)
    with bpy.data.libraries.load(filepath, link=False) as (data_from, data_to):
        data_to.objects = [name for name in data_from.objects]

    if collection_name is not None:
        collection = bpy.data.collections[collection_name]
        for obj in data_to.objects:
            collection.objects.link(obj)
    else:
        for obj in data_to.objects:
            bpy.context.collection.objects.link(obj)
    bpy.context.view_layer.objects.active = data_to.objects[0]


def find_obj_collection(self, context):
    parent_collection = None

    for collection_name in bpy.data.collections.keys():
        if context.active_object.name in bpy.data.collections[collection_name].objects:
            parent_collection = collection_name
            break
    return parent_collection


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


def focus_camera(rotation):
    if bpy.data.objects.get("Camera Asset") is None:
        camera_data = bpy.data.cameras.new(name="Camera Asset")
        cam_obj = bpy.data.objects.new("Camera Asset", camera_data)
        bpy.context.view_layer.active_layer_collection.collection.objects.link(cam_obj)
    else:
        cam_obj = bpy.data.objects.get("Camera Asset")

    bpy.data.cameras["Camera Asset"].lens = 50
    bpy.context.scene.camera = cam_obj
    cam_obj.rotation_euler = rotation
    bpy.ops.view3d.camera_to_view_selected()
    bpy.data.cameras["Camera Asset"].lens = 30


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


def assign_material(name, color, collection=None, object_name=None):
    material = bpy.data.materials.get(name)

    if not material:
        material = bpy.data.materials.new(name=name)

    material.diffuse_color = color

    for obj in bpy.context.selected_objects:
        if (collection is None and object_name is None) or obj.users_collection[0].name.split('.')[
                0] == collection or obj.name.split('.')[0] == object_name:
            if obj.data.materials:
                obj.data.materials[0] = material
            else:
                obj.data.materials.append(material)


def delete_asset_from_library(icon, directory):
    asset = icon.split('.')[0] + ".blend"
    filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)),directory)
    icon = os.path.join(filepath, icon)
    asset = os.path.join(filepath, asset)
    os.remove(icon)
    os.remove(asset)


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


class DrawPath(bpy.types.Operator):
    """Draw route on rock. If this button is disabled, select any object and switch to object mode to active it."""
    bl_idname = "object.draw"
    bl_label = "Draw route"

    @classmethod
    def poll(self, context):
        return len(
            bpy.context.selected_objects) > 0 and context.active_object.type == 'MESH' and \
               bpy.context.active_object.mode == 'OBJECT'

    def execute(self, context):
        if "rocks" not in bpy.data.collections.keys():
            self.report({'ERROR'}, "Corrupted collection hierarchy, press Pepare new scene to reset.") 
            return {'CANCELLED'}

        bpy.ops.object.gpencil_add(align='WORLD', location=(0, 0, 0), scale=(1, 1, 1), type='EMPTY')
        bpy.ops.gpencil.paintmode_toggle()
        bpy.context.scene.tool_settings.gpencil_stroke_placement_view3d = 'SURFACE'
        bpy.context.object.data.zdepth_offset = 0
        bpy.context.scene.tool_settings.gpencil_sculpt.lock_axis = 'VIEW'
        return {'FINISHED'}


class DrawDone(bpy.types.Operator):
    """Finish route. If this button is disabled, select object named GPencil and switch to draw mode to active it."""
    bl_idname = "object.done"
    bl_label = "Done"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(self, context):
        return context.selected_objects and len(
            bpy.context.selected_objects) > 0 and context.active_object.type == 'GPENCIL' and \
               bpy.context.active_object.mode == 'PAINT_GPENCIL'

    def execute(self, context):
        bpy.ops.gpencil.paintmode_toggle(back=True)
        bpy.ops.gpencil.convert(type='POLY', use_timing_data=False)

        add_mesh("libraries\\circle.blend", context, "rocks")
        bpy.data.objects.remove(bpy.data.objects["GPencil"], do_unlink=True)
        new_name = bpy.context.active_object.name
        bpy.context.view_layer.objects.active = bpy.data.objects[new_name]

        bpy.ops.object.modifier_add(type='ARRAY')
        bpy.context.object.modifiers["Array"].fit_type = 'FIT_CURVE'
        bpy.context.object.modifiers["Array"].curve = bpy.data.objects["GP_Layer"]
        bpy.context.object.modifiers["Array"].relative_offset_displace[0] = 0
        bpy.context.object.modifiers["Array"].relative_offset_displace[1] = 0
        bpy.context.object.modifiers["Array"].relative_offset_displace[2] = 1

        bpy.ops.object.modifier_add(type='CURVE')
        bpy.context.object.modifiers["Curve"].object = bpy.data.objects["GP_Layer"]
        bpy.context.object.modifiers["Curve"].deform_axis = 'POS_Z'

        bpy.ops.object.apply_all_modifiers()
        bpy.data.objects.remove(bpy.data.objects["GP_Layer"], do_unlink=True)
        return {'FINISHED'}


class RenderOperator(bpy.types.Operator):
    """Render selected collection hierachy"""
    bl_idname = "object.render"
    bl_label = "Render"

    @classmethod
    def poll(self, context):
        return bpy.data.collections

    def execute(self, context):
        walls_color = (0.7, 0.7, 0.7, 0)
        rocks_color = (0.7, 0.7, 0.7, 0)
        structures_color = (0.1, 0.1, 0.1, 0)
        route_color = get_random_color()
        path_color = get_random_color()

        bpy.ops.object.select_all(action='DESELECT')
        if bpy.data.window_managers["WinMan"].collections_previews.split(".")[0] == "path":
            ob = bpy.data.objects[bpy.data.window_managers["WinMan"].collections_previews]
            ob.select_set(True)
        else:
            collection = bpy.data.collections[bpy.data.window_managers["WinMan"].collections_previews]
            objs = collection.all_objects
            for ob in objs:
                ob.select_set(True)

        assign_material("Walls", walls_color, collection="wall")
        assign_material("Rocks", rocks_color, collection="rock")
        assign_material("Structures", structures_color, collection="structure")
        assign_material("Holds", route_color, object_name="hold")
        assign_material("Paths", path_color, object_name="path")

        focus_camera(rotation=(math.radians(85), math.radians(0),
                               math.radians(bpy.data.window_managers["WinMan"].rotation_prop)))
        focus_light(rotation=(math.radians(45), math.radians(-45),
                              math.radians(bpy.data.window_managers["WinMan"].rotation_prop + 45)))
        set_output_dimensions(1920, 1080, 100)
        bpy.ops.render.render('INVOKE_DEFAULT')
        return {'FINISHED'}


def get_random_color():
    index = random.randint(0, 5)
    colors = [(0.5, 0, 0, 0), (0.5, 0.5, 0, 0), (0.5, 0, 0.5, 0), (0, 0.5, 0, 0), (0, 0.5, 0.5, 0),
              (0, 0, 0.5, 0)]
    return colors[index]


class AddRiggedHumanOperator(bpy.types.Operator):
    """Add real size character"""
    bl_idname = "object.human"
    bl_label = "Add human"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.object.select_all(action='DESELECT')
        add_mesh("libraries\\human.blend", context, "human")
        scale = bpy.data.window_managers["WinMan"].scale_prop / 100
        bpy.ops.transform.resize(value=(scale, scale, scale))
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        return {'FINISHED'}
    
class AddCarabinerOperator(bpy.types.Operator):
    """Add real size character"""
    bl_idname = "object.carabiner"
    bl_label = "Add carabiner"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.object.select_all(action='DESELECT')
        add_mesh("libraries\\carabiner.blend", context, "carabiners")
        for obj in bpy.context.selected_objects:
            if obj.name.split(".")[0] == "carabiner_1":
                bpy.context.view_layer.objects.active = obj
        if bpy.context.scene.rigidbody_world is None:
            bpy.ops.rigidbody.world_add()
        bpy.context.scene.rigidbody_world.collection = bpy.data.collections["carabiners"]
        bpy.context.scene.rigidbody_world.effector_weights.collection = bpy.data.collections["carabiners"]
        bpy.context.scene.rigidbody_world.substeps_per_frame = 30
        bpy.context.scene.rigidbody_world.solver_iterations = 30
        move_with_snapping(self, context, context.active_object)
        return {'FINISHED'}

class PlaySimulationOperator(bpy.types.Operator):
    """Play physics simulation."""
    bl_idname = "object.play_simulation"
    bl_label = "Play"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if bpy.context.scene.rigidbody_world is None:
            bpy.ops.rigidbody.world_add()
        bpy.context.scene.rigidbody_world.collection = bpy.data.collections["carabiners"]
        bpy.context.scene.rigidbody_world.effector_weights.collection = bpy.data.collections["carabiners"]
        bpy.context.scene.rigidbody_world.substeps_per_frame = 30
        bpy.context.scene.rigidbody_world.solver_iterations = 30    

        bpy.ops.object.select_all(action='SELECT')
        for obj in bpy.context.selected_objects:
            if obj.name.split("_")[0] != "carabiner":
                bpy.context.view_layer.objects.active = obj
                bpy.ops.rigidbody.object_add()
                bpy.context.object.rigid_body.enabled = False 

        bpy.ops.object.select_all(action='DESELECT')
        for carabiner in bpy.data.collections["carabiners"].objects:
            if carabiner.name.split("_")[0] == "carabiner" and len(carabiner.name.split("_"))  == 2 and carabiner.name.split("_")[1].split(".")[0] == "1":
                bpy.ops.object.select_all(action='DESELECT')
                carabiner.select_set(True)
                bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
                for obj in carabiner.children:
                    if obj.name.split("_")[1] != "1":
                        obj.select_set(True)
                    else:
                        obj.select_set(False)
                bpy.ops.object.parent_clear(type='CLEAR')

        bpy.ops.object.select_all(action='DESELECT')
        coordinates = []
        edges = []
        for helper in bpy.data.collections["carabiners"].objects:
            if helper.name.split("_")[0] == "helper":
                if len(edges) == 2:
                    coordinates.append(edges)
                    edges = [[helper.location.x, helper.location.y, helper.location.z]]
                else:
                    edges.append([helper.location.x, helper.location.y, helper.location.z])
        coordinates.append(edges)
        
        coordinates = merge_edges(coordinates)
        curve_data = bpy.data.curves.new('curve_chain', 'CURVE')
        curve_data.dimensions = '3D'
        spline = curve_data.splines.new(type='POLY')
        spline.points.add(len(coordinates)-1)
        for i in range(len(coordinates)):
            x,y,z = coordinates[i]
            spline.points[i].co = (x, y, z, 1)
        curve_obj = bpy.data.objects.new('curve_chain', curve_data)
        bpy.data.collections["carabiners"].objects.link(curve_obj)

        bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        bpy.context.active_object.rotation_euler.rotate_axis("X", math.radians(90))
        bpy.context.active_object.name = "curve_rotate"

        bpy.ops.object.select_all(action='DESELECT')
        add_mesh("libraries\\chain.blend", context, "carabiners")

        bpy.context.view_layer.objects.active = bpy.data.objects["chain_big"]
        bpy.ops.object.modifier_add(type='ARRAY')
        bpy.context.object.modifiers["Array"].fit_type = 'FIT_CURVE'
        bpy.context.object.modifiers["Array"].curve = bpy.data.objects["curve_chain"]
        bpy.context.object.modifiers["Array"].use_constant_offset = True
        bpy.context.object.modifiers["Array"].use_relative_offset = False
        bpy.context.object.modifiers["Array"].constant_offset_displace[0] = 0.07
        bpy.context.object.modifiers["Array"].use_object_offset = True
        bpy.context.object.modifiers["Array"].offset_object = bpy.data.objects["curve_rotate"]

        bpy.ops.object.modifier_add(type='CURVE')
        bpy.context.object.modifiers["Curve"].object = bpy.data.objects["curve_chain"]
        bpy.context.object.modifiers["Curve"].deform_axis = 'POS_X'
        bpy.ops.object.make_links_data(type='MODIFIERS')
        bpy.ops.object.apply_all_modifiers()

        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.separate(type='LOOSE')
        bpy.ops.object.editmode_toggle()

        bpy.context.view_layer.objects.active = bpy.data.objects["chain_small"]
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.separate(type='LOOSE')
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')

        for obj_small in bpy.data.collections["carabiners"].objects:
            if obj_small.name.split("_")[0] == "chain" and obj_small.name.split("_")[1].split(".")[0] == "small":
                for obj_big in bpy.data.collections["carabiners"].objects:
                    if obj_big.name.split("_")[0] == "chain" and obj_big.name.split("_")[1].split(".")[0] == "big" and len(obj_small.name.split(".")) == len(obj_big.name.split(".")):
                        if len(obj_small.name.split(".")) == 1 or obj_small.name.split(".")[1] == obj_big.name.split(".")[1]:
                            obj_small.parent = obj_big
                            obj_small.matrix_parent_inverse = obj_big.matrix_world.inverted()

        bpy.ops.object.select_all(action='DESELECT')
        for obj_small in bpy.data.collections["carabiners"].objects:
            if obj_small.name.split("_")[0] == "chain" and obj_small.name.split("_")[1].split(".")[0] == "small":
                obj_small.select_set(True)
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.edge_split(type='VERT')
        bpy.ops.mesh.separate(type='LOOSE')
        bpy.ops.object.editmode_toggle()

        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        return {'FINISHED'}

def merge_edges(coordinates):
    while len(coordinates) > 1:
        new_coordinates = merge(coordinates[0], coordinates[1])
        coordinates.pop(0)
        coordinates[0] = new_coordinates
    return coordinates[0]

def merge( coordinates_a, coordinates_b):
    first_a_first_b = distance(coordinates_a[0],coordinates_b[0])
    first_a_last_b = distance(coordinates_a[0],coordinates_b[-1])
    last_a_first_b = distance(coordinates_a[-1],coordinates_b[0])
    last_a_last_b = distance(coordinates_a[-1],coordinates_b[-1])

    lowest_distance = min(first_a_first_b,first_a_last_b,last_a_first_b,last_a_last_b)

    if lowest_distance == first_a_first_b:
        coordinates_a.reverse()
    elif lowest_distance == first_a_last_b:
        coordinates_a.reverse()
        coordinates_b.reverse()
    elif lowest_distance == last_a_last_b:
        coordinates_b.reverse()

    return coordinates_a + coordinates_b

def distance( vertex_a, vertex_b):
    return math.sqrt((vertex_b[0] - vertex_a[0])**2 + (vertex_b[1] - vertex_a[1])**2 + (vertex_a[2] - vertex_b[2])**2) 



        
"""                            helper.select_set(True)
                    coordinates.append([helper.location.x, helper.location.y, helper.location.z])
                    helper.select_set(False)"""

"""                bpy.context.scene.frame_end = 51
        bpy.ops.ptcache.bake_all(bake=True)
        bpy.context.scene.frame_current = 50"""


classes = (
    CreateEmptyScene,
    AddRouteCollection,
    MoveObjectWithSnapping,
    RotateModal,
    ScaleObject,
    DeleteObject,
    AddWallFromCollection,
    AddStructuresFromCollection,
    AddHoldsFromCollection,
    AddRocksFromCollection,
    DrawPath,
    DrawDone,
    AddToWallLibrary,
    AddToStructureLibrary,
    AddToHoldLibrary,
    AddToRockLibrary,
    RemoveFromWallLibrary,
    RemoveFromStructureLibrary,
    RemoveFromHoldLibrary,
    RemoveFromRockLibrary,
    RenderOperator,
    AddRiggedHumanOperator,
    AddCarabinerOperator,
    PlaySimulationOperator
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
