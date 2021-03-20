import bpy

from . import properties, operators, library_operators, panels

bl_info = {
    "name": "Route setter Add-on",
    "blender": (2, 92, 0),
    "category": "Object",
    "author": "Vojtech Kovarik"
}


files = (
    properties,
    operators,
    library_operators,
    panels
)


def register():
    for f in files:
        f.register()


def unregister():
    for f in reversed(files):
        f.unregister()
