# <pep8-80 compliant>

import io
from contextlib import redirect_stderr, redirect_stdout

import bpy

stdout_err = io.StringIO()


def fetch_geo(skp_file):

    with redirect_stdout(stdout_err), redirect_stderr(stdout_err):

        bpy.ops.import_scene.skp(filepath=skp_file,
                                 # scenes_as_camera=False,
                                 #  import_camera=True, # SU Active View
                                 reuse_material=True,
                                 max_instance=1000
                                 )

    # Moving camera objects to another collection

    scene_master_collection = bpy.context.view_layer.layer_collection

    # cam_collection = bpy.data.collections.new(name="cameras")
    # bpy.context.scene.collection.children.link(cam_collection)

    bpy.ops.object.select_all(action='DESELECT')
    for obj in bpy.data.objects:
        if obj.type == 'CAMERA':
            if obj != bpy.data.collections["cameras"].objects['Default_Camera']:
                obj.select_set(True)

                bpy.data.collections["cameras"].objects.link(obj)
                bpy.data.collections["main_product"].objects.unlink(obj)

    bpy.ops.object.select_all(action='DESELECT')

    scene_master_collection.children['cameras'].hide_viewport = True
