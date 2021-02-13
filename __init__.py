import bpy

from . import panels, operators

bl_info = {
    "name": "Route setter Add-on",
    "blender": (2, 90, 0),
    "category": "Object",
    "author": "Vojtech Kovarik"
}


files = (
    operators,
    panels
)


def register():
    for f in files:
        f.register()


def unregister():
    for f in reversed(files):
        f.unregister()
