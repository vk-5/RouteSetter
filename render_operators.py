import bpy, math, mathutils, bpy_extras.view3d_utils, random
import os
from os import listdir

class RenderOperator(bpy.types.Operator):
    """Render selected collection. If this button is disabled, you are trying to render empty collection, select different collection or add some object to active it."""
    bl_idname = "object.render"
    bl_label = "Render"

    @classmethod
    def poll(self, context):
        return len(bpy.data.collections) > 1 and len(bpy.data.collections[bpy.data.window_managers["WinMan"].collections_previews].objects) != 0

    def execute(self, context):
        assign_material_for_render()
        focus_camera(rotation=(math.radians(85), math.radians(0),
                               get_angle_for_render() + math.radians(90)), collection=bpy.data.window_managers["WinMan"].collections_previews)
        focus_light(rotation=(math.radians(45), math.radians(-45),
                              get_angle_for_render() + math.radians(45)))

        set_output_dimensions(1080, 1920, 100)
        bpy.ops.render.render('INVOKE_DEFAULT')
        return {'FINISHED'}

def assign_material_for_render():
    walls_color = (0.7, 0.7, 0.7, 0)
    rocks_color = (0.7, 0.7, 0.7, 0)
    structures_color = (0.1, 0.1, 0.1, 0)
    carabiners_color = (0.1, 0.1, 0.1, 0)
    bpy.ops.object.select_all(action='DESELECT')
    assign_material("walls", walls_color, collection="walls")
    assign_material("rocks", rocks_color, collection="rocks")
    assign_material("structures", structures_color, collection="structures")
    assign_material("carabiners", carabiners_color, collection="carabiners")
    for col in bpy.data.collections.keys():
        if col.split(".")[0] in ["path", "route"]:
            collection_color_tag = bpy.data.collections[col].color_tag
            assign_material(collection_color_tag, get_color_from_color_tag(collection_color_tag), col)


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


def get_angle_for_render():
    angles = []
    bpy.ops.object.select_all(action='DESELECT')
    for obj in bpy.data.collections[bpy.data.window_managers["WinMan"].collections_previews].objects:
        angles.append(math.atan2(obj.location.y, obj.location.x))
        print()
    return sum(angles) / len(angles)

class RecalculateMaterial(bpy.types.Operator):
    """Delete selected objects. If this button is disabled, select any object to active it."""
    bl_idname = "object.materials"
    bl_label = "Assign materials"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if "walls" not in bpy.data.collections.keys():
            self.report({'ERROR'}, "Corrupted collection hierarchy, press Pepare new scene to reset.") 
            return {'CANCELLED'}
        assign_material_for_render()
        return {'FINISHED'}


classes = (
    RenderOperator,
    RecalculateMaterial,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
