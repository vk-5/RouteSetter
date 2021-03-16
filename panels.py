import bpy
import os
import bpy.utils.previews
from bpy.props import (
    StringProperty,
    EnumProperty,
)

class EditPanel(bpy.types.Panel):
    """Creates Edit panel."""
    bl_label = "Edit"
    bl_idname = "OBJECT_PT_edit"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'RouteSetter'

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.operator("object.empty_scene")
        row = layout.row()
        row.operator("object.move_object_with_snapping")
        row.operator("object.rotate_modal")
        row = layout.row()
        row.operator("object.scale")
        row.operator("object.delete")
        row = layout.row()
        row.operator("wm.url_open", text="Documentation").url = "https://github.com/vk-5/RouteSetter"


def enum_previews_from_directory_walls(self, context):
    """EnumProperty callback"""
    enum_items = []

    if context is None:
        return enum_items

    wm = context.window_manager
    directory = wm.walls_previews_dir

    pcoll = preview_collections["walls"]
    enum_previews_from_directory(directory, pcoll, enum_items)
    pcoll.walls_previews = enum_items
    pcoll.walls_previews_dir = directory
    return pcoll.walls_previews


def enum_previews_from_directory_structures(self, context):
    """EnumProperty callback"""
    enum_items = []

    if context is None:
        return enum_items

    wm = context.window_manager
    directory = wm.structures_previews_dir

    pcoll = preview_collections["structures"]
    enum_previews_from_directory(directory, pcoll, enum_items)
    pcoll.structures_previews = enum_items
    pcoll.structures_previews_dir = directory
    return pcoll.structures_previews


def enum_previews_from_directory_holds(self, context):
    """EnumProperty callback"""
    enum_items = []

    if context is None:
        return enum_items

    wm = context.window_manager
    directory = wm.holds_previews_dir

    pcoll = preview_collections["holds"]
    enum_previews_from_directory(directory, pcoll, enum_items)
    pcoll.holds_previews = enum_items
    pcoll.holds_previews_dir = directory
    return pcoll.holds_previews


def enum_previews_from_directory_rocks(self, context):
    """EnumProperty callback"""
    enum_items = []

    if context is None:
        return enum_items

    wm = context.window_manager
    directory = wm.rocks_previews_dir

    pcoll = preview_collections["rocks"]
    enum_previews_from_directory(directory, pcoll, enum_items)
    pcoll.rocks_previews = enum_items
    pcoll.rocks_previews_dir = directory
    return pcoll.rocks_previews


def enum_previews_collections(self, context):
    """EnumProperty callback"""
    enum_items = []

    if context is None:
        return enum_items

    pcoll = preview_collections["collections"]
    for key in bpy.data.collections.keys():
        enum_items.append((key, key, ""))
    for obj in bpy.data.objects.keys():
        if bpy.data.objects[obj].name.split(".")[0] == "path":
            enum_items.append((obj, obj, ""))
    pcoll.collections_previews = enum_items
    return pcoll.collections_previews

def enum_route_previews_collections(self, context):
    """EnumProperty callback"""
    enum_items = []

    if context is None:
        return enum_items

    pcoll = preview_collections["route_collections"]
    for key in bpy.data.collections.keys():
        if key.split(".")[0] == "route":
            enum_items.append((key, key, ""))
    pcoll.route_collection = enum_items
    return pcoll.route_collection

def enum_path_previews_collections(self, context):
    """EnumProperty callback"""
    enum_items = []

    if context is None:
        return enum_items

    pcoll = preview_collections["path_collections"]
    for key in bpy.data.collections.keys():
        if key.split(".")[0] == "path":
            enum_items.append((key, key, ""))
    pcoll.path_collection = enum_items
    return pcoll.path_collection


def enum_previews_from_directory(directory, pcoll, enum_items):
    if directory and os.path.exists(directory):
        VALID_EXTENSIONS = (".png", ".jpg", ".jpeg")
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


def update_walls_collection(self, context):
    enum_previews_from_directory_walls(self, context)
    return None


def update_structures_collection(self, context):
    enum_previews_from_directory_structures(self, context)
    return None


def update_holds_collection(self, context):
    enum_previews_from_directory_holds(self, context)
    return None


def update_rocks_collection(self, context):
    enum_previews_from_directory_rocks(self, context)
    return None


def update_collections_collection(self, context):
    enum_previews_collections(self, context)
    return None

def update_route_collections(self, context):
    enum_route_previews_collections(self, context)
    return None

def update_path_collections(self, context):
    enum_path_previews_collections(self, context)
    return None

class BoulderPreviewsPanel(bpy.types.Panel):
    """Creates Boulder panel."""
    bl_label = "Boulder"
    bl_idname = "OBJECT_PT_preview_boulder"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'RouteSetter'

    def draw(self, context):
        layout = self.layout
        wm = context.window_manager

        row = layout.row()
        row.label(text="Walls")
        add_preview_with_add_button(layout, wm, "walls_previews", "wall")
        add_manage_library_buttons(layout, "wall_library", "wall_library_remove")

        row = layout.row()
        row.label(text="Structures")
        add_preview_with_add_button(layout, wm, "structures_previews", "structure")
        add_manage_library_buttons(layout, "structure_library", "structure_library_remove")

        row = layout.row()
        row.label(text="Holds")
        row = layout.row()
        row.operator("object.add_route_collection")
        row.prop(wm, "route_collection", text="")
        add_preview_with_add_button(layout, wm, "holds_previews", "hold")
        add_manage_library_buttons(layout, "hold_library", "hold_library_remove")


def add_preview_with_add_button(layout, wm, preview_name, operator_name):
    row = layout.row()
    row.template_icon_view(wm, preview_name)
    row = layout.row()
    row.operator("object." + operator_name)

def add_manage_library_buttons(layout, add_operator_name, remove_operator_name):
    row = layout.row()
    row.label(text="Manage library")
    row = layout.row()
    row.operator("object." + add_operator_name)
    row.operator("object." + remove_operator_name)


class RockPreviewsPanel(bpy.types.Panel):
    """Creates Rock panel."""
    bl_label = "Rock"
    bl_idname = "OBJECT_PT_preview_rock"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'RouteSetter'

    def draw(self, context):
        layout = self.layout
        wm = context.window_manager

        add_preview_with_add_button(layout, wm, "rocks_previews", "rock")
        add_manage_library_buttons(layout, "rock_library", "rock_library_remove")

        row = layout.row()
        row.label(text="Paths")
        row = layout.row()
        row.operator("object.add_path_collection")
        row.prop(wm, "path_collection", text="")
        row = layout.row()
        row.operator("object.draw")
        row.operator("object.done")


preview_collections = {}


class RenderPanel(bpy.types.Panel):
    """Creates a Render panel."""
    bl_label = "Render"
    bl_idname = "OBJECT_PT_collection_preview"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'RouteSetter'

    def draw(self, context):
        layout = self.layout
        wm = context.window_manager

        row = layout.row()
        row.label(text="Choose collection to render")
        row = layout.row()
        row.prop(wm, "collections_previews", text="")
        row = layout.row()
        row.prop(wm, "rotation_prop", slider=True, text="Rotation")
        row = layout.row()
        row.operator("object.render")


class ReferencePanel(bpy.types.Panel):
    """Creates a reference panel."""
    bl_label = "References"
    bl_idname = "OBJECT_PT_human"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'RouteSetter'

    def draw(self, context):
        layout = self.layout
        wm = context.window_manager

        row = layout.row()
        row.label(text="Rope stretching check")
        row = layout.row()
        row.operator("object.carabiner")
        row.operator("object.helper_points")
        row = layout.row()
        row.operator("object.chain")
        row = layout.row()
        row.operator("object.play_simulation")
        row = layout.row()
        row.label(text="Add real size human reference")
        row = layout.row()
        row.prop(wm, "scale_prop", slider=True, text="Centimeters")
        row = layout.row()
        row.operator("object.human")


classes = (
    EditPanel,
    BoulderPreviewsPanel,
    RockPreviewsPanel,
    ReferencePanel,
    RenderPanel
)


def register():
    from bpy.types import WindowManager
    from bpy.props import (
        StringProperty,
        EnumProperty,
        IntProperty,
    )

    WindowManager.walls_previews_dir = StringProperty(
        name="Folder Path",
        subtype='DIR_PATH',
        default=os.path.join(os.path.dirname(
            os.path.abspath(__file__)), "libraries\\walls")
    )

    WindowManager.walls_previews = EnumProperty(
        items=enum_previews_from_directory_walls,
        default=None,
        update=update_walls_collection,
    )

    WindowManager.structures_previews_dir = StringProperty(
        name="Folder Path",
        subtype='DIR_PATH',
        default=os.path.join(os.path.dirname(
            os.path.abspath(__file__)), "libraries\\structures")
    )

    WindowManager.structures_previews = EnumProperty(
        items=enum_previews_from_directory_structures,
        default=None,
        update=update_structures_collection,
    )

    WindowManager.holds_previews_dir = StringProperty(
        name="Folder Path",
        subtype='DIR_PATH',
        default=os.path.join(os.path.dirname(
            os.path.abspath(__file__)), "libraries\\holds")
    )

    WindowManager.holds_previews = EnumProperty(
        items=enum_previews_from_directory_holds,
        default=None,
        update=update_holds_collection,
    )

    WindowManager.rocks_previews_dir = StringProperty(
        name="Folder Path",
        subtype='DIR_PATH',
        default=os.path.join(os.path.dirname(
            os.path.abspath(__file__)), "libraries\\rocks")
    )

    WindowManager.rocks_previews = EnumProperty(
        items=enum_previews_from_directory_rocks,
        default=None,
        update=update_rocks_collection,
    )

    WindowManager.collections_previews = EnumProperty(
        items=enum_previews_collections,
        default=None,
        update=update_collections_collection,
    )

    WindowManager.route_collection = EnumProperty(
        items=enum_route_previews_collections,
        default=None,
        update=update_route_collections,
    )

    WindowManager.path_collection = EnumProperty(
        items=enum_path_previews_collections,
        default=None,
        update=update_path_collections,
    )

    WindowManager.rotation_prop = IntProperty(default=0, soft_min=-180, soft_max=180)
    WindowManager.scale_prop = IntProperty(default=180, soft_min=100, soft_max=230)

    pcoll_walls = bpy.utils.previews.new()
    pcoll_walls.walls_previews_dir = ""
    pcoll_walls.walls_previews = ()

    pcoll_structures = bpy.utils.previews.new()
    pcoll_structures.structures_previews_dir = ""
    pcoll_structures.structures_previews = ()

    pcoll_holds = bpy.utils.previews.new()
    pcoll_holds.holds_previews_dir = ""
    pcoll_holds.holds_previews = ()

    pcoll_rocks = bpy.utils.previews.new()
    pcoll_rocks.rocks_previews_dir = ""
    pcoll_rocks.rocks_previews = ()

    pcoll_collections = bpy.utils.previews.new()
    pcoll_collections.collections_previews = ()

    pcoll_route_collections = bpy.utils.previews.new()
    pcoll_route_collections.route_collection = ()

    pcoll_path_collections = bpy.utils.previews.new()
    pcoll_path_collections.path_collection = ()

    preview_collections["walls"] = pcoll_walls
    preview_collections["structures"] = pcoll_structures
    preview_collections["holds"] = pcoll_holds
    preview_collections["rocks"] = pcoll_rocks
    preview_collections["collections"] = pcoll_collections
    preview_collections["route_collections"] = pcoll_route_collections
    preview_collections["path_collections"] = pcoll_path_collections

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    from bpy.types import WindowManager

    del WindowManager.walls_previews
    del WindowManager.structures_previews
    del WindowManager.holds_previews
    del WindowManager.rocks_previews
    del WindowManager.collections_previews
    del WindowManager.route_collection
    del WindowManager.path_collection
    del WindowManager.walls_previews_dir
    del WindowManager.structures_previews_dir
    del WindowManager.holds_previews_dir
    del WindowManager.rocks_previews_dir
    del WindowManager.rotation_prop
    del WindowManager.scale_prop

    for pcoll in preview_collections.values():
        bpy.utils.previews.remove(pcoll)
    preview_collections.clear()

    for cls in classes:
        bpy.utils.unregister_class(cls)
