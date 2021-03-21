import bpy, math, mathutils, bpy_extras.view3d_utils, random
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
        create_collection("route", wall_collection, get_random_color_tag())
        return {'FINISHED'}

class AddPathCollection(bpy.types.Operator):
    """Adds new path collection."""
    bl_idname = "object.add_path_collection"
    bl_label = "Add new path"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if "rocks" not in bpy.data.collections.keys():
            self.report({'ERROR'}, "Corrupted collection hierarchy, press Pepare new scene to reset.") 
            return {'CANCELLED'}

        rock_collection = bpy.data.collections["rocks"]
        create_collection("path", rock_collection, get_random_color_tag())
        return {'FINISHED'}


class DrawPath(bpy.types.Operator):
    """Draw path on rock. If this button is disabled, select any object and switch to object mode to active it."""
    bl_idname = "object.draw"
    bl_label = "Draw path"

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
    """Finish path. If this button is disabled, press Draw route first or select object named GPencil and switch to draw mode to active it."""
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

        add_mesh("libraries\\circle.blend", context, bpy.data.window_managers["WinMan"].path_collection)
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

        bpy.ops.object.modifier_apply(modifier="Array")
        bpy.ops.object.modifier_apply(modifier="Curve")
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
        bpy.data.objects.remove(bpy.data.objects["GP_Layer"], do_unlink=True)
        return {'FINISHED'}


class RenderOperator(bpy.types.Operator):
    """Render selected collection. If this button is disabled, you are trying to render empty collection, select different collection or add some object to active it."""
    bl_idname = "object.render"
    bl_label = "Render"

    @classmethod
    def poll(self, context):
        return len(bpy.data.collections) > 1 and len(bpy.data.collections[bpy.data.window_managers["WinMan"].collections_previews].objects) != 0

    def execute(self, context):
        walls_color = (0.7, 0.7, 0.7, 0)
        rocks_color = (0.7, 0.7, 0.7, 0)
        structures_color = (0.1, 0.1, 0.1, 0)
        carabiners_color = (0.1, 0.1, 0.1, 0)
        render_collection = bpy.data.window_managers["WinMan"].collections_previews
        collection_color_tag = bpy.data.collections[render_collection].color_tag

        bpy.ops.object.select_all(action='DESELECT')
        assign_material("walls", walls_color, collection="walls")
        assign_material("rocks", rocks_color, collection="rocks")
        assign_material("structures", structures_color, collection="structures")
        assign_material("carabiners", carabiners_color, collection="carabiners")
        assign_material(collection_color_tag, get_color_from_color_tag(collection_color_tag), render_collection)

        focus_camera(rotation=(math.radians(85), math.radians(0),
                               get_angle_for_render() + math.radians(90)), collection=render_collection)
        focus_light(rotation=(math.radians(45), math.radians(-45),
                              get_angle_for_render() + math.radians(45)))

        set_output_dimensions(1080, 1920, 100)
        bpy.ops.render.render('INVOKE_DEFAULT')
        return {'FINISHED'}

def get_angle_for_render():
    angles = []
    bpy.ops.object.select_all(action='DESELECT')
    for obj in bpy.data.collections[bpy.data.window_managers["WinMan"].collections_previews].objects:
        angles.append(math.atan2(obj.location.y, obj.location.x))
        print()
    return sum(angles) / len(angles)

def get_color_from_color_tag(tag):
    if tag == 'COLOR_01':
        color = (1, 0, 0, 0)
    elif tag == 'COLOR_02':
        color = (1, 0.25, 0, 0)
    elif tag == 'COLOR_03':
        color = (1, 1, 0, 0)
    elif tag == 'COLOR_04':
        color = (0, 1, 0, 0)
    elif tag == 'COLOR_05':
        color = (0, 0, 1, 0)
    elif tag == 'COLOR_06':
        color = (0.3, 0, 1, 0)
    elif tag == 'COLOR_07':
        color = (1, 0, 0.5, 0)
    elif tag == 'COLOR_08':
        color = (0.15, 0.05, 0, 0)
    else:
        color = (1, 1, 1, 0)
    return color

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
    """Add carabiner to the scene."""
    bl_idname = "object.carabiner"
    bl_label = "Add carabiner"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.object.select_all(action='DESELECT')
        add_mesh("libraries\\carabiner.blend", context, "carabiners")
        for obj in bpy.context.selected_objects:
            if obj.name.split(".")[0] == "carabiner_1":
                bpy.context.view_layer.objects.active = obj
        move_with_snapping(self, context, context.active_object)
        return {'FINISHED'}

class AddHelperPointsOperator(bpy.types.Operator):
    """Add points so chain will not go through any other object."""
    bl_idname = "object.helper_points"
    bl_label = "Add point"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.object.select_all(action='DESELECT')
        add_mesh("libraries\\points.blend", context, "carabiners")
        for obj in bpy.context.selected_objects:
            if obj.name.split(".")[0] == "helperParent":
                bpy.context.view_layer.objects.active = obj
        move_with_snapping(self, context, context.active_object)
        return {'FINISHED'}

class GenerateChainOperator(bpy.types.Operator):
    """Generates chain through all carabiners and points. If this button is disabled, add carabiner or point to active it."""
    bl_idname = "object.chain"
    bl_label = "Generate rope"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(self, context):
        return "carabiner_1" in bpy.data.objects.keys() or "helperParent" in bpy.data.objects.keys()

    def execute(self, context):
        prepare_carabiners()
        prepare_points()
        coordinates = prepare_coordinates()     
        prepare_curve_and_empty(coordinates)
        prepare_modifiers(context)
        apply_modifiers("chain_big.001", ['Array', 'Curve'])
        apply_modifiers("chain_small.001", ['Array', 'Curve'])
        prepare_chain_rigid()
        chain_set_parent()
        prepare_chain_children()
        chain_clean_up()
        return {'FINISHED'}


def prepare_carabiners():
    bpy.ops.object.select_all(action='DESELECT')
    for carabiner in bpy.data.collections["carabiners"].objects:
        if carabiner.name.split("_")[0] == "carabiner" and len(carabiner.name.split("_")) == 2 and carabiner.name.split("_")[1].split(".")[0] == "1":
            carabiner.select_set(True)
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
            for obj in carabiner.children:
                if obj.name.split("_")[1] != "1":
                    obj.select_set(True)
                else:
                    obj.select_set(False)
            bpy.ops.object.parent_clear(type='CLEAR')
            carabiner.select_set(False)


def prepare_points():
    bpy.ops.object.select_all(action='DESELECT')
    for helper_parent in bpy.data.collections["carabiners"].objects:
        if helper_parent.name.split("_")[0] == "helperParent":
            helper_parent.select_set(True)
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
            for obj in helper_parent.children:
                obj.select_set(True)
            bpy.ops.object.parent_clear(type='CLEAR')
            helper_parent.select_set(False)


def prepare_coordinates():
    coordinates = []
    edges = []
    
    bpy.ops.object.select_all(action='DESELECT')
    for helper in bpy.data.collections["carabiners"].objects:
        if helper.name.split("_")[0] == "helper":
            if len(edges) == 2:
                coordinates.append(edges)
                edges = [[helper.location.x, helper.location.y, helper.location.z]]
            else:
                edges.append([helper.location.x, helper.location.y, helper.location.z])
    coordinates.append(edges)      
    coordinates = merge_coordinates(coordinates)
    return coordinates


def merge_coordinates(coordinates):
    while len(coordinates) > 1:
        new_coordinates = merge_edges(coordinates[0], coordinates[1])
        coordinates.pop(0)
        coordinates[0] = new_coordinates
    return coordinates[0]


def merge_edges( coordinates_a, coordinates_b):
    first_a_first_b = vertices_distance(coordinates_a[0],coordinates_b[0])
    first_a_last_b = vertices_distance(coordinates_a[0],coordinates_b[-1])
    last_a_first_b = vertices_distance(coordinates_a[-1],coordinates_b[0])
    last_a_last_b = vertices_distance(coordinates_a[-1],coordinates_b[-1])

    lowest_distance = min(first_a_first_b,first_a_last_b,last_a_first_b,last_a_last_b)

    if lowest_distance == first_a_first_b:
        coordinates_a.reverse()
    elif lowest_distance == first_a_last_b:
        coordinates_a.reverse()
        coordinates_b.reverse()
    elif lowest_distance == last_a_last_b:
        coordinates_b.reverse()

    return coordinates_a + coordinates_b


def vertices_distance( vertex_a, vertex_b):
    return math.sqrt((vertex_b[0] - vertex_a[0])**2 + (vertex_b[1] - vertex_a[1])**2 + (vertex_a[2] - vertex_b[2])**2) 


def prepare_curve_and_empty(coordinates):
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


def prepare_modifiers(context):
    bpy.ops.object.select_all(action='DESELECT')
    add_mesh("libraries\\chain.blend", context, "carabiners")
    bpy.context.view_layer.objects.active = bpy.data.objects["chain_big.001"]
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


def apply_modifiers( obj_name, modifiers):
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = bpy.data.objects[obj_name]
    for mod in modifiers:
        bpy.ops.object.modifier_apply(modifier=mod)


def prepare_chain_rigid():
    bpy.context.view_layer.objects.active = bpy.data.objects["chain_big.001"]
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.separate(type='LOOSE')
    bpy.ops.object.editmode_toggle()
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = bpy.data.objects["chain_small.001"]
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.separate(type='LOOSE')
    bpy.ops.object.editmode_toggle()
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')


def chain_set_parent():
    for obj_small in bpy.data.collections["carabiners"].objects:
        if obj_small.name.split("_")[0] == "chain" and obj_small.name.split("_")[1].split(".")[0] == "small":
            for obj_big in bpy.data.collections["carabiners"].objects:
                if obj_big.name.split("_")[0] == "chain" and obj_big.name.split("_")[1].split(".")[0] == "big" and obj_small.name.split(".")[1] == obj_big.name.split(".")[1]:
                    obj_small.parent = obj_big
                    obj_small.matrix_parent_inverse = obj_big.matrix_world.inverted()


def prepare_chain_children():
    bpy.ops.object.select_all(action='DESELECT')
    for obj_small in bpy.data.collections["carabiners"].objects:
        if obj_small.name.split("_")[0] == "chain" and obj_small.name.split("_")[1].split(".")[0] == "small":
            obj_small.select_set(True)
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.edge_split(type='VERT')
    bpy.ops.mesh.separate(type='LOOSE')
    bpy.ops.object.editmode_toggle()

def chain_clean_up():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    for obj in bpy.context.selected_objects:
        if obj.name.split("_")[0] == "helper" or obj.name.split("_")[0] == "curve" or obj.name.split("_")[0] == "helperParent":
            bpy.data.objects.remove(obj, do_unlink=True)
            

class PlaySimulationOperator(bpy.types.Operator):
    """Play physics simulation. If this button is disabled, generate rope to active it."""
    bl_idname = "object.play_simulation"
    bl_label = "Play / Stop Simulation"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(self, context):
        return "chain_big.001" in bpy.data.objects.keys()

    def execute(self, context):
        prepare_rigid_world()    
        prepare_collisions()
        bpy.context.scene.frame_end = 51
        bpy.ops.screen.animation_play()
        return {'FINISHED'}

def prepare_rigid_world():
    if bpy.context.scene.rigidbody_world is None:
        bpy.ops.rigidbody.world_add()
    bpy.context.scene.rigidbody_world.collection = bpy.data.collections["carabiners"]
    bpy.context.scene.rigidbody_world.effector_weights.collection = bpy.data.collections["carabiners"]
    bpy.context.scene.rigidbody_world.substeps_per_frame = 30
    bpy.context.scene.rigidbody_world.solver_iterations = 30

def prepare_collisions():
    bpy.ops.object.select_all(action='SELECT')
    for obj in bpy.context.selected_objects:
        if obj.name.split("_")[0] != "carabiner" and obj.name.split("_")[0] != "chain":
            bpy.context.view_layer.objects.active = obj
            bpy.ops.rigidbody.object_add()
            bpy.context.object.rigid_body.enabled = False
            bpy.context.object.rigid_body.collision_shape = 'MESH'

classes = (
    CreateEmptyScene,
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
    AddRouteCollection,
    AddPathCollection,
    RenderOperator,
    AddRiggedHumanOperator,
    AddCarabinerOperator,
    AddHelperPointsOperator,
    GenerateChainOperator,
    PlaySimulationOperator
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
