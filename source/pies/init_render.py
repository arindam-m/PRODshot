# <pep8-80 compliant>

import bpy


def trig_renderer(file_path, skp_file):

    scene = bpy.context.scene

    render_fpath = file_path + "\\Render Outputs\\"
    scene.render.image_settings.file_format = 'PNG'
    file_name = skp_file.replace(".skp", "")
    scene.render.filepath = render_fpath + file_name

    bpy.ops.render.render(write_still=True)
