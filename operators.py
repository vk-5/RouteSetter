import bpy
import os

class MoveObjectWithSnapping(bpy.types.Operator):
    """Create an Operator"""
    bl_idname = "object.move_object_with_snapping"
    bl_label = "Move"

    def execute(self, context):
        bpy.context.scene.tool_settings.use_snap = True
        bpy.context.scene.tool_settings.snap_elements = {'FACE'}
        bpy.context.scene.tool_settings.use_snap_rotate = True
        bpy.context.scene.tool_settings.use_snap_translate = True
        bpy.context.scene.tool_settings.use_snap_project = True
        bpy.context.scene.tool_settings.use_snap_align_rotation = True
        return {'FINISHED'}

class DeleteObject(bpy.types.Operator):
    """Create an Operator"""
    bl_idname = "object.delete"
    bl_label = "Delete"

    def execute(self, context):
        for obj in bpy.context.selected_objects:
            bpy.data.objects.remove(obj, do_unlink=True)
        return {'FINISHED'} 

class DeleteObjectOperator(bpy.types.Operator):
    """Create an Operator"""
    bl_idname = "object.move_object_with_snapping"
    bl_label = "Move"

    def execute(self, context):
        bpy.context.scene.tool_settings.use_snap = True
        bpy.context.scene.tool_settings.snap_elements = {'FACE'}
        bpy.context.scene.tool_settings.use_snap_rotate = True
        bpy.context.scene.tool_settings.use_snap_translate = True
        bpy.context.scene.tool_settings.use_snap_project = True
        bpy.context.scene.tool_settings.use_snap_align_rotation = True
        return {'FINISHED'}



def add_mesh(file_name, context):
    filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)
    with bpy.data.libraries.load(filepath, link=False) as (data_from, data_to):
        data_to.objects = [name for name in data_from.objects]

    for obj in data_to.objects:
        bpy.context.collection.objects.link(obj)


class AddWallOperator(bpy.types.Operator):
    """Create an Operator"""
    bl_idname = "object.wall"
    bl_label = "Wall"

    def execute(self, context):
        add_mesh('libraries\\wall_library\\1.blend', context )
        #self.report({'WARNING'}, "{} not found in {}".format("FlatWall", "wall_library.blend"))
        return {'FINISHED'}


class AddRiggedHumanOperator(bpy.types.Operator):
    """Create an Operator"""
    bl_idname = "object.human"
    bl_label = "Human"

    def execute(self, context):
        if add_mesh("wall_library.blend", context):
            return {'FINISHED'}
        self.report({'WARNING'}, "{} not found in {}".format("Human", "wall_library.blend"))
        return {'CANCELLED'}


classes = (
    MoveObjectWithSnapping,
    DeleteObject,
    AddWallOperator,
    AddRiggedHumanOperator
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
