import bpy
import os


def add_mesh(file_name, object_name, context):
    filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)
    with bpy.data.libraries.load(filepath, link=False) as (data_from, data_to):
        data_to.objects = [name for name in data_from.objects if name == object_name]

    if data_to.objects:
        for obj in data_to.objects:
            bpy.context.collection.objects.link(obj)
        return True
    return False


class AddFlatWallOperator(bpy.types.Operator):
    """Create an Operator"""
    bl_idname = "object.flat"
    bl_label = "Flat"

    def execute(self, context):
        if add_mesh("wall_library.blend", "FlatWall", context):
            return {'FINISHED'}
        self.report({'WARNING'}, "{} not found in {}".format("FlatWall", "wall_library.blend"))
        return {'CANCELLED'}


class AddNoseWallOperator(bpy.types.Operator):
    """Create an Operator"""
    bl_idname = "object.nose"
    bl_label = "Nose"

    def execute(self, context):
        if add_mesh("wall_library.blend", "NoseWall", context):
            return {'FINISHED'}
        self.report({'WARNING'}, "{} not found in {}".format("NoseWall", "wall_library.blend"))
        return {'CANCELLED'}


class AddOverHangWallOperator(bpy.types.Operator):
    """Create an Operator"""
    bl_idname = "object.overhang"
    bl_label = "Overhang"

    def execute(self, context):
        if add_mesh("wall_library.blend", "OverhangWall", context):
            return {'FINISHED'}
        self.report({'WARNING'}, "{} not found in {}".format("OverhangWall", "wall_library.blend"))
        return {'CANCELLED'}


class AddRiggedHumanOperator(bpy.types.Operator):
    """Create an Operator"""
    bl_idname = "object.human"
    bl_label = "Human"

    def execute(self, context):
        if add_mesh("wall_library.blend", "Human", context):
            return {'FINISHED'}
        self.report({'WARNING'}, "{} not found in {}".format("Human", "wall_library.blend"))
        return {'CANCELLED'}


classes = (
    AddNoseWallOperator,
    AddFlatWallOperator,
    AddOverHangWallOperator,
    AddRiggedHumanOperator
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
