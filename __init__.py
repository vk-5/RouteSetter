import bpy

from . import properties, functions, operators, collection_operators, library_operators, rope_operators, render_operators, panels

bl_info = {
    "name": "Route setter Add-on",
    "blender": (2, 92, 0),
    "category": "Object",
    "author": "Vojtech Kovarik"
}


files = (
    properties,
    operators,
    collection_operators,
    library_operators,
    rope_operators,
    render_operators,
    panels
)


def register():
    for f in files:
        f.register()


def unregister():
    for f in reversed(files):
        f.unregister()
