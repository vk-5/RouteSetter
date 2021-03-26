import bpy, math, mathutils, bpy_extras.view3d_utils, random
import os
from os import listdir
from . functions import move_with_snapping, add_mesh


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
