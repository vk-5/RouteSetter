import bpy, os, bpy.utils.previews
from bpy.types import WindowManager,StringProperty, EnumProperty,Scene
from bpy.props import (
    StringProperty,
    EnumProperty,
    )


class EditPanel(bpy.types.Panel):
    """Creates Edit Panel in the Object properties window"""
    bl_label = "Edit"
    bl_idname = "OBJECT_PT_edit"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'RouteSetter'

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.operator("object.move_object_with_snapping")
        row.operator("object.rotate_modal")
        row = layout.row()
        row.operator("object.scale")
        row.operator("object.delete")


def enum_previews_from_directory_items(self, context): # edited blender ui template jak mam citovat?
    """EnumProperty callback"""
    enum_items = []

    if context is None:
        return enum_items

    wm = context.window_manager
    directory = wm.my_previews_dir

    pcoll = preview_collections["main"]

    if directory == pcoll.my_previews_dir:
        return pcoll.my_previews


    if directory and os.path.exists(directory):
        VALID_EXTENSIONS = ('.png', '.jpg', '.jpeg')
        image_paths = []
        for fn in os.listdir(directory):
            if fn.lower().endswith(VALID_EXTENSIONS):
                image_paths.append(fn)
        

        for i, name in enumerate(image_paths):
            filepath = os.path.join(directory, name)
            icon = pcoll.get(name)
            if not icon:
                thumb = pcoll.load(name, filepath, 'IMAGE')
            else:
                thumb = pcoll[name]
            enum_items.append((name, name, "", thumb.icon_id, i))

    pcoll.my_previews = enum_items
    pcoll.my_previews_dir = directory
    return pcoll.my_previews


class WallPreviewsPanel(bpy.types.Panel): # edited blender ui template jak mam citovat?
    bl_label = "Walls"
    bl_idname = "OBJECT_PT_preview_walls"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'RouteSetter'

    def draw(self, context):
        layout = self.layout
        wm = context.window_manager

        row = layout.row()
        row.template_icon_view(wm, "my_previews")

        row = layout.row()
        row.operator("object.obj")


preview_collections = {}


class RiggedHumanPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Add human"
    bl_idname = "OBJECT_PT_human"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'RouteSetter'

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.operator("object.obj")


classes = (
    EditPanel,
    WallPreviewsPanel,
    RiggedHumanPanel
)


def register():
    from bpy.props import (
            StringProperty,
            EnumProperty,
            )

    WindowManager.my_previews_dir = os.path.join(os.path.dirname(__file__), "libraries\\walls")

    WindowManager.my_previews = EnumProperty(
        items=enum_previews_from_directory_items,
    )

    pcoll = bpy.utils.previews.new()
    pcoll.my_previews_dir = ""
    pcoll.my_previews = ()

    preview_collections["main"] = pcoll

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
 
    del WindowManager.my_previews

    for pcoll in preview_collections.values():
        bpy.utils.previews.remove(pcoll)
    preview_collections.clear()

    for cls in classes:
        bpy.utils.unregister_class(cls)


