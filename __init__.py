import bpy

from . import panels, operators, properties

bl_info = {
    "name": "Route setter Add-on",
    "blender": (2, 92, 0),
    "category": "Object",
    "author": "Vojtech Kovarik"
}


files = (
    operators,
    panels,
    properties
)


def register():
    for f in files:
        f.register()


def unregister():
    for f in reversed(files):
        f.unregister()
