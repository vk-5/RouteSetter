import bpy, math, mathutils, bpy_extras
from bpy_extras.view3d_utils import region_2d_to_location_3d
import os

def rotation_store(context, boolSettings):
    boolSettings[0] = bpy.context.scene.tool_settings.use_snap
    boolSettings[1] = bpy.context.scene.tool_settings.use_snap_rotate
    boolSettings[2] = bpy.context.scene.tool_settings.use_snap_translate
    boolSettings[3] = bpy.context.scene.tool_settings.use_snap_project
    boolSettings[4] = bpy.context.scene.tool_settings.use_snap_align_rotation
    return bpy.context.scene.tool_settings.snap_elements


def rotation_set_up(context, boolSettings, snap_elements):
    bpy.context.scene.tool_settings.snap_elements = snap_elements
    bpy.context.scene.tool_settings.use_snap = boolSettings[0]
    bpy.context.scene.tool_settings.use_snap_rotate = boolSettings[1]
    bpy.context.scene.tool_settings.use_snap_translate = boolSettings[2]
    bpy.context.scene.tool_settings.use_snap_project = boolSettings[3]
    bpy.context.scene.tool_settings.use_snap_align_rotation = boolSettings[4]


class MoveObjectWithSnapping(bpy.types.Operator):
    """Move selected object"""
    bl_idname = "object.move_object_with_snapping"
    bl_label = "Move"


    @classmethod
    def poll(self, context):
        return bpy.context.selected_objects and bpy.context.active_object and bpy.context.active_object.mode == 'OBJECT'
        
    
    def execute(self, context):
        obj = bpy.context.object
        x,y,z = obj.location.x, obj.location.y, obj.location.z
        loc = bpy_extras.view3d_utils.location_3d_to_region_2d(bpy.context.region, bpy.context.space_data.region_3d, (x, y, z), (0, 0))
        context.window.cursor_warp(loc.x, loc.y)

        rotation_set_up(context, [True] * 5, {'FACE'})
        bpy.ops.transform.translate('INVOKE_DEFAULT')
        return {'FINISHED'}
    
    
class RotateModal(bpy.types.Operator):
    """Rotate selected object"""
    bl_idname = "object.rotate_modal"
    bl_label = "Rotate"
    x = 0
    init_rotation = [0,0,0]


    @classmethod
    def poll(self, context):
        return bpy.context.selected_objects and bpy.context.active_object and bpy.context.active_object.mode == 'OBJECT'
    
    
    def modal(self, context, event):
        obj = bpy.context.object

        if event.type == 'MOUSEMOVE':
            change_x = event.mouse_region_x
            obj.rotation_euler.rotate_axis("Z", math.radians(change_x-self.x))
            self.x = change_x

        if event.type in ['LEFTMOUSE','ENTER']:
            return{'FINISHED'}

        if event.type in ['ESC','RIGHTMOUSE']:
            obj.rotation_euler = self.init_rotation
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}


    def invoke(self, context, event):
        self.init_rotation = bpy.context.object.rotation_euler.copy()
        self.x = event.mouse_x
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}
    

class ScaleObject(bpy.types.Operator):
    """Scale selected object"""
    bl_idname = "object.scale"
    bl_label = "Scale"


    @classmethod
    def poll(self, context):
        return bpy.context.selected_objects and bpy.context.active_object and bpy.context.active_object.mode == 'OBJECT'


    def execute(self, context):
        bpy.ops.transform.resize('INVOKE_DEFAULT') 
        return {'FINISHED'} 


class DeleteObject(bpy.types.Operator):
    """Delete selected objects"""
    bl_idname = "object.delete"
    bl_label = "Delete"


    @classmethod
    def poll(self, context):
        return bpy.context.selected_objects #and bpy.context.active_object.mode == 'OBJECT'


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


class AddObject(bpy.types.Operator):
    """Add Operator"""
    bl_idname = "object.obj"
    bl_label = "Add"

    def execute(self, context):
        add_mesh('libraries\\walls\\wall_1.blend', context )
        #self.report({'WARNING'}, "{} not found in {}".format("FlatWall", "props.blend"))
        return {'FINISHED'}


class AddRiggedHumanOperator(bpy.types.Operator):
    """Create an Operator"""
    bl_idname = "object.human"
    bl_label = "Human"

    def execute(self, context):
        if add_mesh("props.blend", context):
            return {'FINISHED'}
        self.report({'WARNING'}, "{} not found in {}".format("Human", "props.blend"))
        return {'CANCELLED'}


classes = (
    MoveObjectWithSnapping,
    RotateModal,
    ScaleObject,
    DeleteObject,
    AddObject,
    AddRiggedHumanOperator
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
