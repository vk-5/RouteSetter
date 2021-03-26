import bpy, math, mathutils, bpy_extras.view3d_utils, random
import os
from os import listdir
from . functions import move_with_snapping, add_mesh
    
class AddCarabinerOperator(bpy.types.Operator):
    """Add carabiner to the scene."""
    bl_idname = "object.carabiner"
    bl_label = "Add carabiner"

    def execute(self, context):
        bpy.context.scene.frame_set(0)
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

    def execute(self, context):
        bpy.context.scene.frame_set(0)
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
        bpy.context.scene.frame_set(0)
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
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = bpy.data.objects["chain_small.001"]
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.separate(type='LOOSE')
    bpy.ops.object.editmode_toggle()
    for obj in bpy.data.collections["carabiners"].objects:
        if obj.name.split("_")[0] == "chain":
            obj.select_set(True)
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
        bpy.context.scene.frame_set(0)
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
