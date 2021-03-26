import bpy, os, bpy_extras.view3d_utils

def add_mesh(file_name, context, collection_name=None):
    filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)
    with bpy.data.libraries.load(filepath, link=False) as (data_from, data_to):
        data_to.objects = [name for name in data_from.objects]

    if collection_name is not None:
        collection = bpy.data.collections[collection_name]
        for obj in data_to.objects:
            collection.objects.link(obj)
    else:
        for obj in data_to.objects:
            bpy.context.collection.objects.link(obj)
    bpy.context.view_layer.objects.active = data_to.objects[0]

def move_with_snapping(self, context, obj):
    x, y, z = obj.location.x, obj.location.y, obj.location.z
    loc = bpy_extras.view3d_utils.location_3d_to_region_2d(bpy.context.region,
                                                           bpy.context.space_data.region_3d,
                                                           (x, y, z), (0, 0))

    context.window.cursor_warp(loc.x, loc.y)
    rotation_set_up(context, [True,True,True,False,True], {'FACE'})
    bpy.ops.transform.translate('INVOKE_DEFAULT')


def rotation_set_up(context, boolSettings, snap_elements):
    bpy.context.scene.tool_settings.snap_elements = snap_elements
    bpy.context.scene.tool_settings.use_snap = boolSettings[0]
    bpy.context.scene.tool_settings.use_snap_rotate = boolSettings[1]
    bpy.context.scene.tool_settings.use_snap_translate = boolSettings[2]
    bpy.context.scene.tool_settings.use_snap_project = boolSettings[3]
    bpy.context.scene.tool_settings.use_snap_align_rotation = boolSettings[4]
    bpy.context.scene.tool_settings.snap_target = 'ACTIVE'