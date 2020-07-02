# <pep8-80 compliant>

import bpy

env_name = "photo_studio_01"


def world_env():

    light_lib_path = bpy.path.abspath("//") + "env_light\\"
    source_file = "studio_ambience.blend"
    source = light_lib_path + source_file

    data_libs = bpy.data.libraries
    with data_libs.load(source, link=True) as (_data_from, data_to):
        data_to.worlds = [env_name]

    bpy.context.scene.world = bpy.data.worlds[env_name]
