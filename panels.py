import bpy

class EditPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Edit"
    bl_idname = "OBJECT_PT_edit"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'RouteSetter'

    def draw(self, context):
        layout = self.layout

        obj = context.object

        row = layout.row()
        row.operator("object.move_object_with_snapping")
        row.operator("object.rotate_modal")
        row = layout.row()
        row.operator("object.scale")
        row.operator("object.delete")


class ClimbingWallPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Climbing Wall"
    bl_idname = "OBJECT_PT_climbing_wall"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'RouteSetter'

    def draw(self, context):
        layout = self.layout

        obj = context.object

        row = layout.row()
        row.label(text="Add Wall")

        row = layout.row()
        row.operator("object.wall")



class RouteSetterPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Route Setter"
    bl_idname = "OBJECT_PT_route_setter"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'RouteSetter'

    def draw(self, context):
        layout = self.layout

        obj = context.object

        row = layout.row()
        row.label(text="Add hold")

        row = layout.row()
        row.operator("mesh.primitive_cube_add")
        row.operator("mesh.primitive_cube_add")
        row.operator("mesh.primitive_cube_add")


class ClimbingHoldsPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Climbing Holds"
    bl_idname = "OBJECT_PT_climbing_holds"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'RouteSetter'

    def draw(self, context):
        layout = self.layout

        obj = context.object

        row = layout.row()
        row.label(text="Create Hold")

        row = layout.row()
        row.operator("mesh.primitive_cube_add")
        row.operator("mesh.primitive_cube_add")
        row.operator("mesh.primitive_cube_add")


class RiggedHumanPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Add human"
    bl_idname = "OBJECT_PT_human"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'RouteSetter'

    def draw(self, context):
        layout = self.layout

        obj = context.object

        row = layout.row()
        row.operator("object.human")


classes = (
    EditPanel,
    ClimbingWallPanel,
    RouteSetterPanel,
    ClimbingHoldsPanel,
    RiggedHumanPanel
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
