# <pep8-80 compliant>
# coding=UTF-8

import os
import sys
import time

import bpy

time_start = time.time()
DONE = "✔"

sys.stderr.write("\n\nStarting Product Shot Renders Automation...\n\n")


def con_time(time_in_secs):

    if int(time_in_secs) <= 60:
        converted_time = '%.2f' % time_in_secs + ' Seconds'

    elif int(time_in_secs) <= 3600:
        converted_time = (str(int(time_in_secs / 60)) + ' Min  ' +
                          '%.2f' % (time_in_secs % 60) + ' Sec')

    elif int(time_in_secs) > 3600:
        converted_time = (str(int(time_in_secs / 3600)) + ' Hr  ' +
                          str(int((time_in_secs % 3600) / 60)) + ' Min  ' +
                          '%.2f' % (time_in_secs % 60) + ' Sec')

    return converted_time


cwd = bpy.path.abspath("//")
sys.path.append(cwd + "\\pies\\")

if "bpy" in locals():
    import importlib
    import import_skp
    importlib.reload(import_skp)
    import smooth_shading
    importlib.reload(smooth_shading)
    import calc_bound
    importlib.reload(calc_bound)
    import cam_retarget
    importlib.reload(cam_retarget)
    import assign_shaders
    importlib.reload(assign_shaders)
    import ext_light
    importlib.reload(ext_light)
    import init_render
    importlib.reload(init_render)


arguments = sys.argv[sys.argv.index("--") + 1:]
io_files_path = arguments[0]


bpy.ops.object.select_all(action='DESELECT')

source_files = os.listdir(io_files_path)

PROCESS_COUNT = 1

for file in source_files:

    if file.endswith(".skp") or file.endswith(".SKP"):

        print(f"\nRunning: Process # {PROCESS_COUNT}")
        print("----------------------")
        print(f"File:  {file} \n")

        ## --- Pre Sanitize --- ##

        for block in bpy.data.meshes:
            if block.users == 0:
                bpy.data.meshes.remove(block)

        for block in bpy.data.materials:
            if block.users == 0:
                bpy.data.materials.remove(block)

        for block in bpy.data.textures:
            if block.users == 0:
                bpy.data.textures.remove(block)

        for block in bpy.data.images:
            if block.users == 0:
                bpy.data.images.remove(block)

        # --------------------------------------------- #
        source_fpath = io_files_path + "\\" + file
        # --------------------------------------------- #

        # --------------------------------------------- #
        print("Importing Process Has Started...\r", end='')
        import_skp.fetch_geo(source_fpath)
        print("Importing Of SketchUp Data      (Done)")
        # --------------------------------------------- #

        # breakpoint()

        # --------------------------------------------- #
        smooth_shading.auto_bsmooth()
        print("Smoothing Of Geo-Mesh           (Done)")
        # --------------------------------------------- #

        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')

        # --------------------------------------------- #
        calc_bound.create_bb()
        # --------------------------------------------- #

        bb_obj = bpy.context.object

        bb_loc_x = bb_obj.location[0]
        bb_loc_y = bb_obj.location[1]

        bpy.ops.object.mode_set(mode='EDIT')

        # Minimum z-value of all verts after converting to global transform

        bb_bottom_most_z = min([(bb_obj.matrix_world @ v.co).z
                                for v in bb_obj.data.vertices]
                               )

        bpy.ops.object.mode_set()

        cursor_loc_x = bpy.context.scene.cursor.location[0]
        cursor_loc_y = bpy.context.scene.cursor.location[1]
        cursor_loc_z = bpy.context.scene.cursor.location[2]

        bpy.context.scene.cursor.location[0] = bb_loc_x
        bpy.context.scene.cursor.location[1] = bb_loc_y
        bpy.context.scene.cursor.location[2] = bb_bottom_most_z

        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')

        bpy.context.scene.cursor.location[0] = cursor_loc_x
        bpy.context.scene.cursor.location[1] = cursor_loc_y
        bpy.context.scene.cursor.location[2] = cursor_loc_z

        for obj in bpy.data.collections["main_product"].objects:
            obj.select_set(True)

        # --------------------------------------------- #

        bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)

        bpy.ops.object.select_all(action='DESELECT')
        bb_obj.select_set(True)
        bpy.ops.object.location_clear(clear_delta=False)

        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')

        bpy.ops.object.select_all(action='DESELECT')
        bb_obj.select_set(True)
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')

        # --------------------------------------------- #

        bpy.data.scenes[0].tool_settings.transform_pivot_point = 'MEDIAN_POINT'

        base_x = bpy.context.object.dimensions[0]
        base_y = bpy.context.object.dimensions[1]

        base_max = max(base_x, base_y)

        # Giving some room for margin space
        bpy.ops.transform.resize(value=(1.105, 1.105, 1.105))

        # --------------------------------------------- #
        cam_retarget.zoom_io(io_files_path, file)
        print("Camera Focused To The Subject   (Done)")
        # --------------------------------------------- #

        # --------------------------------------------- #
        assign_shaders.update_proper_mat(io_files_path, file)
        print("Material Shaders Linked         (Done)")
        # --------------------------------------------- #

#         scale = 2.5 * base_max
#         bpy.ops.transform.resize(value=(scale, scale, 1))

        # --------------------------------------------- #
        ext_light.world_env()
        print("Environment Light Linked        (Done)")
        # --------------------------------------------- #

        # --------------------------------------------- #
        print("\n\nRendering Process Has Started...\r", end='')
        ren_start_time = time.time()
        init_render.trig_renderer(io_files_path, file)
        ren_time = time.time() - ren_start_time
        print(f"Rendering Process (#{PROCESS_COUNT}) Has Completed.   \n")
        print(f"Render Time: {con_time(ren_time)} \n\n")
        # --------------------------------------------- #

        # --- Post Sanitize --- ##

        for c_obj in bpy.data.collections["cameras"].objects:
            if c_obj.type == 'CAMERA' and c_obj.name != 'Default_Camera':
                bpy.data.objects.remove(c_obj, do_unlink=True)

        bpy.context.scene.camera = bpy.data.objects['Default_Camera']

        bpy.ops.object.select_all(action='DESELECT')

        for obj in bpy.data.collections["main_product"].objects:
            bpy.data.objects.remove(obj, do_unlink=True)

        # print(f"Process # {PROCESS_COUNT} Has Been Successfully Completed.\n")
        PROCESS_COUNT += 1

print("\nEntire Automation Has Completed Now!")
print(f"Total Execution Time: {con_time(time.time() - time_start)} \n")
