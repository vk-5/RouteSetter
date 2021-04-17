import bpy, math, mathutils, bpy_extras.view3d_utils, random
import os
from os import listdir


class MoveObjectWithSnapping(bpy.types.Operator):
    """Move selected objects. If this button is disabled, select any object to active it"""
    bl_idname = "object.move_object_with_snapping"
    bl_label = "Move"

    @classmethod
    def poll(self, context):
        return bpy.context.selected_objects and bpy.context.active_object and\
               bpy.context.active_object.mode == 'OBJECT'

    def execute(self, context):
        move_with_snapping(self, context, bpy.context.selected_objects[0])
        return {'FINISHED'}

class RotateModal(bpy.types.Operator):
    """Rotate selected objects. If this button is disabled, select any object to active it"""
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
    """Scale selected objects. If this button is disabled, select any object to active it"""
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
    """Delete selected objects. If this button is disabled, select any object to active it"""
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


class DrawPath(bpy.types.Operator):
    """Draw path on rock. If this button is disabled, select any object and switch to object mode to active it"""
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

        bpy.context.scene.tool_settings.use_keyframe_insert_auto = True
        return {'FINISHED'}


class DrawDone(bpy.types.Operator):
    """Finish path. If this button is disabled, press Draw route first or select object named GPencil and switch to draw mode to active it"""
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

        add_mesh(os.path.join("libraries", "circle.blend"), context, bpy.data.window_managers["WinMan"].path_collection)
        scale = bpy.data.window_managers["WinMan"].path_scale_prop / 5
        resize_object("circle", scale)
        bpy.data.objects.remove(bpy.data.objects["GPencil"], do_unlink=True)
        bpy.context.view_layer.objects.active = bpy.data.objects["circle"]

        bpy.ops.object.modifier_add(type='ARRAY')
        bpy.context.object.modifiers["Array"].fit_type = 'FIT_CURVE'
        bpy.context.object.modifiers["Array"].curve = bpy.data.objects["GP_Layer"]
        bpy.context.object.modifiers["Array"].relative_offset_displace[0] = 0
        bpy.context.object.modifiers["Array"].relative_offset_displace[1] = 0
        bpy.context.object.modifiers["Array"].relative_offset_displace[2] = 1
        bpy.context.object.modifiers["Array"].use_merge_vertices = True
        bpy.ops.object.modifier_add(type='CURVE')
        bpy.context.object.modifiers["Curve"].object = bpy.data.objects["GP_Layer"]
        bpy.context.object.modifiers["Curve"].deform_axis = 'POS_Z'

        bpy.ops.object.modifier_apply(modifier="Array")
        bpy.ops.object.modifier_apply(modifier="Curve")
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
        bpy.data.objects.remove(bpy.data.objects["GP_Layer"], do_unlink=True)
        bpy.data.objects["circle"].name = "Path"

        bpy.context.scene.tool_settings.use_keyframe_insert_auto = False
        bpy.ops.object.transform_apply(location=True, rotation=False, scale=False)
        return {'FINISHED'}


def resize_object(name, scale):
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects[name].select_set(True)
    bpy.ops.transform.resize(value=(scale, scale, scale))
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)


class AddRiggedHumanOperator(bpy.types.Operator):
    """Add real size character"""
    bl_idname = "object.human"
    bl_label = "Add human"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if "reference" not in bpy.data.collections.keys():
            self.report({'ERROR'}, "Corrupted collection hierarchy, press Pepare new scene to reset.") 
            return {'CANCELLED'}

        bpy.ops.object.select_all(action='DESELECT')
        add_mesh(os.path.join("libraries", "human.blend"), context, "human")
        scale = bpy.data.window_managers["WinMan"].scale_prop / 100
        resize_object(bpy.context.active_object.name, scale)
        return {'FINISHED'}


classes = (
    MoveObjectWithSnapping,
    RotateModal,
    ScaleObject,
    DeleteObject,
    DrawPath,
    DrawDone,
    AddRiggedHumanOperator
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
