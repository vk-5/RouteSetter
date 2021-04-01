import bpy, math, mathutils, bpy_extras.view3d_utils, random
import os
from os import listdir
from . asset_import_functions import add_mesh, move_with_snapping

    
class AddCarabinerOperator(bpy.types.Operator):
    """Add carabiner to the scene."""
    bl_idname = "object.carabiner"
    bl_label = "Add carabiner"

    def execute(self, context):

        bpy.context.scene.frame_set(0)
        bpy.ops.object.select_all(action='DESELECT')
        add_mesh("libraries\\carabiner.blend", context, "carabiners")
        for obj in bpy.context.selected_objects:
            if "carabiner_1" in obj.name:
                bpy.context.view_layer.objects.active = obj

        carabiners = bpy.data.window_managers["WinMan"].carabiners
        obj = carabiners.add()
        obj.name = context.object.name
        obj.obj_type = context.object.type
        obj.obj_id = len(carabiners)
        bpy.data.window_managers["WinMan"].carabiners_index = len(carabiners)-1

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
            if "helperParent" in obj.name:
                bpy.context.view_layer.objects.active = obj
        
        carabiners = bpy.data.window_managers["WinMan"].carabiners
        obj = carabiners.add()
        obj.name = context.object.name
        obj.obj_type = context.object.type
        obj.obj_id = len(carabiners)
        bpy.data.window_managers["WinMan"].carabiners_index = len(carabiners) - 1

        move_with_snapping(self, context, context.active_object)
        return {'FINISHED'}

class GenerateChainOperator(bpy.types.Operator):
    """Generates chain through all carabiners and points. If this button is disabled, add carabiner or point to active it."""
    bl_idname = "object.chain"
    bl_label = "Generate rope"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(self, context):
        return "chain_big.001" not in bpy.data.objects.keys() and ("carabiner_1.001" in bpy.data.objects.keys() or "helperParent.001" in bpy.data.objects.keys())

    def execute(self, context):
        bpy.context.scene.frame_set(0)
        helper_meshes = []
        for obj in bpy.data.collections["carabiners"].objects:
            if "helperParent" in obj.name or "carabiner_1." in obj.name:
                helper_meshes.append(obj.name)
        prepare_carabiners()
        prepare_points()
        coordinates = prepare_coordinates(helper_meshes)     
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
        if "carabiner_1." in carabiner.name:
            carabiner.select_set(True)
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
            for obj in carabiner.children:
                if "carabiner_1." in obj.name:
                    obj.select_set(True)
                else:
                    obj.select_set(False)
            bpy.ops.object.parent_clear(type='CLEAR')
            carabiner.select_set(False)


def prepare_points():
    bpy.ops.object.select_all(action='DESELECT')
    for helper_parent in bpy.data.collections["carabiners"].objects:
        if helper_parent.name.split(".")[0] == "helperParent":
            helper_parent.select_set(True)
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
            for obj in helper_parent.children:
                obj.select_set(True)
            bpy.ops.object.parent_clear(type='CLEAR')
            helper_parent.select_set(False)


def prepare_coordinates(helper_meshes):
    # TODO refactor
    coordinates = []
    
    bpy.ops.object.select_all(action='DESELECT')
    i = 0
    for carabiner in bpy.data.window_managers["WinMan"].carabiners.keys():
        helper_a = str(helper_meshes.index(carabiner) * 2 + 1)
        while len(helper_a) < 3:
            helper_a = "0" + helper_a
        helper_b = str(helper_meshes.index(carabiner) * 2 + 2)
        while len(helper_b) < 3:
            helper_b = "0" + helper_b
        helper_a = "helper_chain." + helper_a
        helper_b = "helper_chain." + helper_b
        helper_a = bpy.data.objects[helper_a]
        helper_b = bpy.data.objects[helper_b]
        vertex_a = [helper_a.location.x, helper_a.location.y, helper_a.location.z]
        vertex_b = [helper_b.location.x, helper_b.location.y, helper_b.location.z]
        coordinates.append([vertex_a, vertex_b])
        i += 1
   
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
        if "chain_" in obj.name:
            obj.select_set(True)
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')


def chain_set_parent():
    for obj_small in bpy.data.collections["carabiners"].objects:
        if "chain_" in obj_small.name and "_small." in obj_small.name:
            for obj_big in bpy.data.collections["carabiners"].objects:
                if "chain_" in obj_big.name and "_big." in obj_big.name and obj_small.name.split(".")[1] == obj_big.name.split(".")[1]:
                    obj_small.parent = obj_big
                    obj_small.matrix_parent_inverse = obj_big.matrix_world.inverted()


def prepare_chain_children():
    bpy.ops.object.select_all(action='DESELECT')
    for obj_small in bpy.data.collections["carabiners"].objects:
        if  "chain_" in obj_small.name and "_small." in obj_small.name:
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
        if "curve" in obj.name or "helper" in obj.name:
            bpy.data.objects.remove(obj, do_unlink=True)

def stop_animation_handler(scene):
    if scene.frame_current >= 50:
        bpy.ops.screen.animation_cancel()
            

class PlaySimulationOperator(bpy.types.Operator):
    """Play physics simulation. If this button is disabled, generate rope to active it."""
    bl_idname = "object.play_simulation"
    bl_label = "Play Simulation"
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
        if "carabiner_" not in obj.name and "chain_" not in obj.name:
            bpy.context.view_layer.objects.active = obj
            bpy.ops.rigidbody.object_add()
            bpy.context.object.rigid_body.enabled = False
            bpy.context.object.rigid_body.collision_shape = 'MESH'


class MoveUpUIlist(bpy.types.Operator):
    """Moves selected carabiner up. If this button is disabled, carabiner is first."""
    bl_idname = "object.move_up"
    bl_label = "UP"

    @classmethod
    def poll(self, context):
        return bpy.data.window_managers["WinMan"].carabiners_index >= 1

    def execute(self, context):
        bpy.data.window_managers["WinMan"].carabiners.move(bpy.data.window_managers["WinMan"].carabiners_index - 1, bpy.data.window_managers["WinMan"].carabiners_index)
        bpy.data.window_managers["WinMan"].carabiners_index -= 1
        return {'FINISHED'}


class MoveDownUIlist(bpy.types.Operator):
    """Moves selected carabiner down. If this button is disabled, carabiner is last."""
    bl_idname = "object.move_down"
    bl_label = "DOWN"

    @classmethod
    def poll(self, context):
        return bpy.data.window_managers["WinMan"].carabiners_index < len(bpy.data.window_managers["WinMan"].carabiners) - 1

    def execute(self, context):
        bpy.data.window_managers["WinMan"].carabiners.move(bpy.data.window_managers["WinMan"].carabiners_index, bpy.data.window_managers["WinMan"].carabiners_index + 1)
        bpy.data.window_managers["WinMan"].carabiners_index += 1
        return {'FINISHED'}


class RemoveFromUIlist(bpy.types.Operator):
    """Remove selected carabiner. If this button is disabled, no carabiner is choosen."""
    bl_idname = "object.remove_carabiner"
    bl_label = "Remove"

    @classmethod
    def poll(self, context):
        return bpy.data.window_managers["WinMan"].carabiners_index != -1

    def execute(self, context):
        if bpy.data.window_managers["WinMan"].carabiners[bpy.data.window_managers["WinMan"].carabiners_index].name in bpy.data.objects.keys():    
            select_whole_carabiner(bpy.data.window_managers["WinMan"].carabiners[bpy.data.window_managers["WinMan"].carabiners_index].name)
            for obj in bpy.context.selected_objects:
                bpy.data.objects.remove(obj, do_unlink=True)
        bpy.data.window_managers["WinMan"].carabiners.remove(bpy.data.window_managers["WinMan"].carabiners_index)
        bpy.data.window_managers["WinMan"].carabiners_index -= 1
        return {'FINISHED'}


class SelectCarabinerFromUIlist(bpy.types.Operator):
    """Select carabiner in scene. If this button is disabled, no carabiner is choosen or rope has been already generated, in that case roll back by ctrl + z."""
    bl_idname = "object.select_carabiner"
    bl_label = "Select"

    @classmethod
    def poll(self, context):
        return bpy.data.window_managers["WinMan"].carabiners_index != -1

    def execute(self, context):
        if bpy.data.window_managers["WinMan"].carabiners[bpy.data.window_managers["WinMan"].carabiners_index].name not in bpy.data.objects.keys():
            self.report({'ERROR'}, "Rope has been already generated, in that case roll back by ctrl + z.") 
            return {'CANCELLED'}
        select_whole_carabiner(bpy.data.window_managers["WinMan"].carabiners[bpy.data.window_managers["WinMan"].carabiners_index].name)
        return {'FINISHED'}

def select_whole_carabiner(name):
    # TODO refactor
    bpy.ops.object.select_all(action='DESELECT')
    if "chain_big.001" in  bpy.data.objects:
        number = name.split(".")[1]
        bpy.context.view_layer.objects.active = bpy.data.objects[name]
        bpy.ops.object.select_hierarchy(direction='CHILD', extend=True)
        bpy.data.objects[name].select_set(True)
        name = "carabiner_2." + number
        bpy.context.view_layer.objects.active = bpy.data.objects[name]
        bpy.ops.object.select_hierarchy(direction='CHILD', extend=True)
        bpy.data.objects[name].select_set(True)
        name = "carabiner_3." + number
        bpy.context.view_layer.objects.active = bpy.data.objects[name]
        bpy.ops.object.select_hierarchy(direction='CHILD', extend=True)
        bpy.data.objects[name].select_set(True)
        name = "carabiner_4." + number
        bpy.context.view_layer.objects.active = bpy.data.objects[name]
        bpy.ops.object.select_hierarchy(direction='CHILD', extend=True)
        bpy.data.objects[name].select_set(True)
        bpy.context.view_layer.objects.active = bpy.data.objects["carabiner_1." + number]
    else:
        bpy.context.view_layer.objects.active = bpy.data.objects[name]
        bpy.ops.object.select_grouped(type='CHILDREN_RECURSIVE')
        bpy.data.objects[name].select_set(True)

class MarkRope(bpy.types.Operator):
    """Mark rope intersecting with object. If this button is disabled, rope has not been generated yet."""
    bl_idname = "object.mark_rope"
    bl_label = "Intersection"

    @classmethod
    def poll(self, context):
        return "chain_big.001" in bpy.data.objects.keys()

    def execute(self, context):
        for obj in bpy.data.objects:
            if "chain_big" in obj.name:
                obj.select_set(True)
        return {'FINISHED'}
        

classes = (
    AddCarabinerOperator,
    AddHelperPointsOperator,
    GenerateChainOperator,
    PlaySimulationOperator,
    MoveUpUIlist,
    MoveDownUIlist,
    RemoveFromUIlist,
    SelectCarabinerFromUIlist,
    MarkRope
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    bpy.app.handlers.frame_change_pre.append(stop_animation_handler)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
