import bpy, math, mathutils, bpy_extras, random
from bpy_extras.view3d_utils import region_2d_to_location_3d
import os
from os import listdir


class MoveObjectWithSnapping(bpy.types.Operator):
    """Move selected objects."""
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
    rotation_set_up(context, [True] * 5, {'FACE'})
    bpy.ops.transform.translate('INVOKE_DEFAULT')


def rotation_set_up(context, boolSettings, snap_elements):
    bpy.context.scene.tool_settings.snap_elements = snap_elements
    bpy.context.scene.tool_settings.use_snap = boolSettings[0]
    bpy.context.scene.tool_settings.use_snap_rotate = boolSettings[1]
    bpy.context.scene.tool_settings.use_snap_translate = boolSettings[2]
    bpy.context.scene.tool_settings.use_snap_project = boolSettings[3]
    bpy.context.scene.tool_settings.use_snap_align_rotation = boolSettings[4]


class RotateModal(bpy.types.Operator):
    """Rotate selected objects."""
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
    """Scale selected objects."""
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
    """Delete selected objects."""
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
    """Add Wall asset from collection."""
    bl_idname = "object.wall"
    bl_label = "Add"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(self, context):
        return len(os.listdir(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "libraries\\walls\\"))) > 0

    def execute(self, context):
        icon = bpy.data.window_managers["WinMan"].walls_previews
        asset = icon.split('.')[0] + ".blend"
        bpy.ops.object.select_all(action='DESELECT')
        add_mesh("libraries\\walls\\" + asset, context, "wall")
        return {'FINISHED'}


class AddStructuresFromCollection(bpy.types.Operator):
    """Add Structure asset from collection."""
    bl_idname = "object.structure"
    bl_label = "Add"

    @classmethod
    def poll(self, context):
        return context.active_object and len(os.listdir(
            os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "libraries\\structures\\"))) > 0 and \
               bpy.context.object.users_collection[0].name.split(".")[0] == "wall"

    def execute(self, context):
        icon = bpy.data.window_managers["WinMan"].structures_previews
        asset = icon.split(".")[0] + ".blend"
        parent_collection = find_obj_collection(self, context)
        bpy.ops.object.select_all(action='DESELECT')
        add_mesh("libraries\\structures\\" + asset, context, "structure", parent_collection)
        move_with_snapping(self, context, context.active_object)
        return {'FINISHED'}


class AddHoldsFromCollection(bpy.types.Operator):
    """Add Hold asset from collection."""
    bl_idname = "object.hold"
    bl_label = "Add"

    @classmethod
    def poll(self, context):
        return bpy.context.active_object and len(os.listdir(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "libraries\\holds\\"))) > 0 and \
               bpy.context.object.users_collection[0].name.split(".")[0] == "wall"

    def execute(self, context):
        icon = bpy.data.window_managers["WinMan"].holds_previews
        asset = icon.split('.')[0] + ".blend"
        parent_collection = find_obj_collection(self, context)
        bpy.ops.object.select_all(action='DESELECT')
        add_mesh("libraries\\holds\\" + asset, context, "hold", parent_collection)
        move_with_snapping(self, context, context.active_object)
        return {'FINISHED'}


class AddRocksFromCollection(bpy.types.Operator):
    """Add Rock asset from collection."""
    bl_idname = "object.rock"
    bl_label = "Add"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(self, context):
        return len(os.listdir(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "libraries\\rocks\\"))) > 0

    def execute(self, context):
        icon = bpy.data.window_managers["WinMan"].rocks_previews
        asset = icon.split('.')[0] + ".blend"
        bpy.ops.object.select_all(action='DESELECT')
        add_mesh("libraries\\rocks\\" + asset, context)
        return {'FINISHED'}


def add_mesh(file_name, context, collection_name=None, parent_collection=None):
    filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)
    with bpy.data.libraries.load(filepath, link=False) as (data_from, data_to):
        data_to.objects = [name for name in data_from.objects]

    if collection_name is not None:
        collection = create_collection(context, collection_name, parent_collection)
        for obj in data_to.objects:
            collection.objects.link(obj)
    else:
        for obj in data_to.objects:
            bpy.context.collection.objects.link(obj)
    bpy.context.view_layer.objects.active = data_to.objects[0]


def create_collection(context, name, parent_collection):
    collection = None
    if name == "wall":
        collection = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(collection)
    elif parent_collection is not None:
        if parent_collection.split(".")[0] == "wall":
            for col in bpy.data.collections[parent_collection].children:
                if col.name.split(".")[0] == name:
                    collection = col
                    break
            if collection is None:
                collection = bpy.data.collections.new(name)
                bpy.data.collections[parent_collection].children.link(collection)
    else:
        collection = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(collection)
    return collection


def find_obj_collection(self, context):
    parent_collection = None
    for collection_name in bpy.data.collections.keys():
        if context.active_object.name in bpy.data.collections[collection_name].objects:
            parent_collection = collection_name
            break
    return parent_collection


class AddToWallLibrary(bpy.types.Operator):
    """Export selected to Wall library."""
    bl_idname = "object.wall_library"
    bl_label = "Export"

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
    """Export selected to Structure library."""
    bl_idname = "object.structure_library"
    bl_label = "Export"

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
    """Export selected to Hold library."""
    bl_idname = "object.hold_library"
    bl_label = "Export"

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
    """Export selected to Rock library."""
    bl_idname = "object.rock_library"
    bl_label = "Export"

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
    if not bpy.data.objects.get("Camera Asset"):
        camera_data = bpy.data.cameras.new(name="Camera Asset")
        cam_obj = bpy.data.objects.new("Camera Asset", camera_data)
        bpy.context.view_layer.active_layer_collection.collection.objects.link(cam_obj)
    else:
        cam_obj = bpy.data.objects.get("Camera Asset")

    bpy.context.scene.camera = cam_obj
    cam_obj.rotation_euler = rotation
    bpy.ops.view3d.camera_to_view_selected()


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


class RemoveFromWallLibrary(bpy.types.Operator):
    """Remove asset from Wall library."""
    bl_idname = "object.wall_library_remove"
    bl_label = "Remove from asset library"

    @classmethod
    def poll(self, context):
        return bpy.context.selected_objects

    def execute(self, context):
        icon = bpy.data.window_managers["WinMan"].walls_previews
        asset = icon.split('.')[0] + ".blend"
        filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "libraries\\walls\\")
        icon = os.path.join(filepath, icon)
        asset = os.path.join(filepath, asset)
        os.remove(icon)
        os.remove(asset)
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)


class RemoveFromStructureLibrary(bpy.types.Operator):
    """Remove asset from Structure library."""
    bl_idname = "object.structure_library_remove"
    bl_label = "Remove from asset library"

    @classmethod
    def poll(self, context):
        return bpy.context.selected_objects

    def execute(self, context):
        icon = bpy.data.window_managers["WinMan"].structures_previews
        asset = icon.split('.')[0] + ".blend"
        filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "libraries\\structures\\")
        icon = os.path.join(filepath, icon)
        asset = os.path.join(filepath, asset)
        os.remove(icon)
        os.remove(asset)
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)


class RemoveFromHoldLibrary(bpy.types.Operator):
    """Remove asset from Hold library."""
    bl_idname = "object.hold_library_remove"
    bl_label = "Remove from asset library"

    @classmethod
    def poll(self, context):
        return bpy.context.selected_objects

    def execute(self, context):
        icon = bpy.data.window_managers["WinMan"].holds_previews
        asset = icon.split('.')[0] + ".blend"
        filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "libraries\\holds\\")
        icon = os.path.join(filepath, icon)
        asset = os.path.join(filepath, asset)
        os.remove(icon)
        os.remove(asset)
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)


class RemoveFromRockLibrary(bpy.types.Operator):
    """Remove asset from Rock library."""
    bl_idname = "object.rock_library_remove"
    bl_label = "Remove from asset library"

    @classmethod
    def poll(self, context):
        return bpy.context.selected_objects

    def execute(self, context):
        icon = bpy.data.window_managers["WinMan"].rocks_previews
        asset = icon.split('.')[0] + ".blend"
        filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "libraries\\rocks\\")
        icon = os.path.join(filepath, icon)
        asset = os.path.join(filepath, asset)
        os.remove(icon)
        os.remove(asset)
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)


class DrawPath(bpy.types.Operator):
    """Draw route on rock."""
    bl_idname = "object.draw"
    bl_label = "Draw route"

    @classmethod
    def poll(self, context):
        return context.selected_objects and len(
            bpy.context.selected_objects) > 0 and context.active_object.type == 'MESH' and \
               context.active_object.mode == 'OBJECT'

    def execute(self, context):
        bpy.ops.object.gpencil_add(align='WORLD', location=(0, 0, 0), scale=(1, 1, 1), type='EMPTY')
        bpy.ops.gpencil.paintmode_toggle()
        bpy.context.scene.tool_settings.gpencil_stroke_placement_view3d = 'SURFACE'
        bpy.context.object.data.zdepth_offset = 0
        bpy.context.scene.tool_settings.gpencil_sculpt.lock_axis = 'VIEW'
        return {'FINISHED'}


class DrawDone(bpy.types.Operator):
    """Finish route."""
    bl_idname = "object.done"
    bl_label = "Done"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(self, context):
        return context.selected_objects and len(
            bpy.context.selected_objects) > 0 and context.active_object.type == 'GPENCIL' and \
               context.active_object.mode == 'PAINT_GPENCIL'

    def execute(self, context):
        bpy.ops.gpencil.paintmode_toggle(back=True)
        bpy.ops.gpencil.convert(type='POLY', use_timing_data=False)
        add_mesh("libraries\\circle.blend", context)
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
        bpy.ops.object.select_all(action='DESELECT')
        collection = bpy.data.collections[bpy.data.window_managers["WinMan"].collections_previews]
        objs = collection.all_objects
        for ob in objs:
            ob.select_set(True)
        assign_material("Walls", (0.7, 0.7, 0.7, 0), collection="wall")
        assign_material("Rocks", (0.7, 0.7, 0.7, 0), collection="rock")
        assign_material("Structures", (0.1, 0.1, 0.1, 0), collection="structure")

        color = get_random_color()
        assign_material("Holds", color, object_name="hold")
        color = get_random_color()
        assign_material("Paths", color, object_name="Path")

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
    bl_label = "Add human reference"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        add_mesh("libraries\\human.blend", context)
        scale = bpy.data.window_managers["WinMan"].scale_prop / 100
        bpy.ops.transform.resize(value=(scale, scale, scale))
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        return {'FINISHED'}


classes = (
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
    AddRiggedHumanOperator
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
