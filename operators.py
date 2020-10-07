import bpy
import os


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
    AddWallOperator,
    AddRiggedHumanOperator
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
