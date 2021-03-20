import bpy
import os
import bpy.utils.previews
from bpy.props import (
    StringProperty,
    EnumProperty,
)



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
    for collection in bpy.data.collections:
        if collection.name.split(".")[0] in ["path", "route", "carabiners"]:
            enum_items.append((collection.name, collection.name, ""))
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

preview_collections = {}


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

    WindowManager.scale_prop = IntProperty(default=180, soft_min=100, soft_max=210)

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
    del WindowManager.scale_prop

    for pcoll in preview_collections.values():
        bpy.utils.previews.remove(pcoll)
    preview_collections.clear()
