import bpy
import os

def rotation_store(context, boolSettings):
    boolSettings[0] = bpy.context.scene.tool_settings.use_snap
    boolSettings[1] = bpy.context.scene.tool_settings.use_snap_rotate
    boolSettings[2] = bpy.context.scene.tool_settings.use_snap_translate
    boolSettings[3] = bpy.context.scene.tool_settings.use_snap_project
    boolSettings[4] = bpy.context.scene.tool_settings.use_snap_align_rotation
    return bpy.context.scene.tool_settings.snap_elements

def rotation_set_up(context, boolSettings, snap_elements):
    bpy.context.scene.tool_settings.use_snap = boolSettings[0]
    bpy.context.scene.tool_settings.snap_elements = snap_elements
    bpy.context.scene.tool_settings.use_snap_rotate = boolSettings[1]
    bpy.context.scene.tool_settings.use_snap_translate = boolSettings[2]
    bpy.context.scene.tool_settings.use_snap_project = boolSettings[3]
    bpy.context.scene.tool_settings.use_snap_align_rotation = boolSettings[4]


class MoveObjectWithSnapping(bpy.types.Operator):
    """Create an Operator"""
    bl_idname = "object.move_object_with_snapping"
    bl_label = "Move"

    boolSettings = [True] * 5
    snap_elements = {'FACE'}

    @classmethod
    def poll(self, context):
        return bpy.context.selected_objects != [] and bpy.context.active_object.mode == 'OBJECT'

    def execute(self, context):
        boolSettings = [True] * 5
        snap_elements = {'FACE'}
        rotation_set_up(context, boolSettings, snap_elements)
        return {'FINISHED'}
    
    #def invoke(self, context):
    #    self.snap_elements = rotation_store(context, self.boolSettings)

class RotateObjectByNormal(bpy.types.Operator):
    """Create an Operator"""
    bl_idname = "object.rotate_object_by_normal"
    bl_label = "Rotate"

    boolSettings = [True] * 5
    snap_elements = {'FACE'}

    @classmethod
    def poll(self, context):
        return bpy.context.selected_objects != [] and bpy.context.active_object.mode == 'OBJECT'

    def execute(self, context):
        boolSettings = [True] * 5
        snap_elements = {'FACE'}
        rotation_set_up(context, boolSettings, snap_elements)
        return {'FINISHED'}

    '''orientation_type = bpy.context.scene.transform_orientation_slots[0].type

    def execute(self, context):
        return {'FINISHED'}'''
    

class DeleteObject(bpy.types.Operator):
    """Create an Operator"""
    bl_idname = "object.delete"
    bl_label = "Delete"


    @classmethod
    def poll(self, context):
        return bpy.context.selected_objects != [] and bpy.context.active_object.mode == 'OBJECT'


    def execute(self, context):
        '''if bpy.context.selected_objects == []:
            self.report({'WARNING'}, "No object selected".format())'''
        for obj in bpy.context.selected_objects:
            bpy.data.objects.remove(obj, do_unlink=True)
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
    RotateObjectByNormal,
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
