import bpy, os, bpy.utils.previews
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



def enum_previews_from_directory_items(self, context):
    """EnumProperty callback"""
    enum_items = []

    if context is None:
        return enum_items

    wm = context.window_manager
    directory = wm.walls_previews_dir

    pcoll_walls = preview_collections["walls"]

    if directory == pcoll_walls.walls_previews_dir:
        return pcoll_walls.walls_previews

    if directory and os.path.exists(directory):
        VALID_EXTENSIONS = ('.png', '.jpg', '.jpeg')
        image_paths = []
        for fn in os.listdir(directory):
            if fn.lower().endswith(VALID_EXTENSIONS):
                image_paths.append(fn)
        

        for i, name in enumerate(image_paths):
            filepath = os.path.join(directory, name)
            icon = pcoll_walls.get(name)
            if not icon:
                thumb = pcoll_walls.load(name, filepath, 'IMAGE')
            else:
                thumb = pcoll_walls[name]
            enum_items.append((name, name, "", thumb.icon_id, i))

    pcoll_walls.walls_previews = enum_items
    pcoll_walls.walls_previews_dir = directory
    return pcoll_walls.walls_previews

def enum_previews_from_directory_items2(self, context):
    """EnumProperty callback"""
    enum_items = []

    if context is None:
        return enum_items

    wm = context.window_manager
    directory = wm.holds_previews_dir

    pcoll_walls = preview_collections["holds"]

    if directory == pcoll_walls.holds_previews_dir:
        return pcoll_walls.holds_previews

    if directory and os.path.exists(directory):
        VALID_EXTENSIONS = ('.png', '.jpg', '.jpeg')
        image_paths = []
        for fn in os.listdir(directory):
            if fn.lower().endswith(VALID_EXTENSIONS):
                image_paths.append(fn)
        

        for i, name in enumerate(image_paths):
            filepath = os.path.join(directory, name)
            icon = pcoll_walls.get(name)
            if not icon:
                thumb = pcoll_walls.load(name, filepath, 'IMAGE')
            else:
                thumb = pcoll_walls[name]
            enum_items.append((name, name, "", thumb.icon_id, i))

    pcoll_walls.holds_previews = enum_items
    pcoll_walls.holds_previews_dir = directory
    return pcoll_walls.holds_previews


class WallPreviewsPanel(bpy.types.Panel):
    bl_label = "Walls"
    bl_idname = "OBJECT_PT_preview_walls"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'RouteSetter'

    def draw(self, context):
        layout = self.layout
        wm = context.window_manager

        row = layout.row()
        row.template_icon_view(wm, "walls_previews")

        row = layout.row()
        row.operator("object.obj")


class HoldsPreviewPanel(bpy.types.Panel):
    bl_label = "Holds"
    bl_idname = "OBJECT_PT_preview_holds"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'RouteSetter'

    def draw(self, context):
        layout = self.layout
        wm = context.window_manager

        row = layout.row()
        row.template_icon_view(wm, "holds_previews")

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
    HoldsPreviewPanel,
    RiggedHumanPanel
)


def register():
    from bpy.types import WindowManager
    from bpy.props import (
            StringProperty,
            EnumProperty,
            )

    WindowManager.walls_previews_dir = StringProperty(
            name="Folder Path",
            subtype='DIR_PATH',
            default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "libraries\\walls")
            )

    WindowManager.walls_previews = EnumProperty(
            items=enum_previews_from_directory_items,
            )

    WindowManager.holds_previews_dir = StringProperty(
            name="Folder Path",
            subtype='DIR_PATH',
            default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "libraries\\holds")
            )

    WindowManager.holds_previews = EnumProperty(
            items=enum_previews_from_directory_items2,
            )


    pcoll_walls = bpy.utils.previews.new()
    pcoll_walls.walls_previews_dir = ""
    pcoll_walls.walls_previews = ()
    pcoll_holds = bpy.utils.previews.new()
    pcoll_holds.holds_previews_dir = ""
    pcoll_holds.holds_previews = ()

    preview_collections["walls"] = pcoll_walls
    preview_collections["holds"] = pcoll_holds

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    from bpy.types import WindowManager
 
    del WindowManager.walls_previews

    for pcoll_walls in preview_collections.values():
        bpy.utils.previews.remove(pcoll_walls)
    preview_collections.clear()

    for cls in classes:
        bpy.utils.unregister_class(cls)


