import bpy
import os
from bpy.types import UIList, WindowManager


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
        row.operator("object.materials", icon='MATERIAL')
        row = layout.row()
        row.operator("wm.url_open", text="Documentation", icon='URL').url = "https://github.com/vk-5/RouteSetter"


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
        row.operator("object.add_route_collection", icon='OUTLINER_OB_GROUP_INSTANCE')
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
        row.operator("object.add_path_collection", icon='OUTLINER_OB_GROUP_INSTANCE')
        row.prop(wm, "path_collection", text="")
        row = layout.row()
        row.operator("object.draw")
        row.operator("object.done")


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
        row.operator("object.render", icon='OUTLINER_DATA_CAMERA')


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
        row.template_list("REFERENCE_UL_carabiners", "", wm, "carabiners", wm, "carabiners_index")
        col = row.column(align=True)
        col.operator("object.move_up", icon='TRIA_UP', text="")
        col.operator("object.move_down", icon='TRIA_DOWN', text="")
        col.separator()
        col.operator("object.select_carabiner", icon='VIS_SEL_11', text="")
        col.operator("object.remove_carabiner", icon='X', text="")

        row = layout.row()
        row.operator("object.chain")
        row.operator("object.mark_rope")
        row = layout.row()
        row.operator("object.play_simulation", icon='PLAY')
        row = layout.row()
        row.label(text="Add real size human reference")
        row = layout.row()
        row.prop(wm, "scale_prop", slider=True, text="Centimeters")
        row = layout.row()
        row.operator("object.human")
        row = layout.row()


class REFERENCE_UL_carabiners(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        split = layout.split(factor=0.3)
        split.label(text=item.name, icon="MESH_CUBE")

    def invoke(self, context, event):
        pass   


classes = (
    EditPanel,
    BoulderPreviewsPanel,
    RockPreviewsPanel,
    REFERENCE_UL_carabiners,
    ReferencePanel,
    RenderPanel
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    