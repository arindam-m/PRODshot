# <pep8-80 compliant>

import bpy
import sketchup


def zoom_io(file_path, skp_file):

    source_fpath = file_path + "\\" + skp_file
    skp_data = sketchup.Model.from_file(source_fpath)
    scenes_to_render = [scene.name for scene in skp_data.scenes]

    if len(scenes_to_render) > 0:
        bpy.context.scene.camera = bpy.data.objects[scenes_to_render[0]]
        bpy.ops.view3d.camera_to_view_selected()

    else:
        bpy.context.scene.camera = bpy.data.objects['Default_Camera']
        bpy.ops.view3d.camera_to_view_selected()

    bpy.ops.object.select_all(action='DESELECT')

    obj = bpy.data.objects.get('Bound_SU_Import')
    obj.select_set(True)
    bpy.data.objects.remove(obj, do_unlink=True)
