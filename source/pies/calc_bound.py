# <pep8-80 compliant>

import bmesh
import bpy
import mathutils
from bpy_extras import object_utils


def add_box(width, height, depth):

    verts = [(+1.0, +1.0, -1.0),
             (+1.0, -1.0, -1.0),
             (-1.0, -1.0, -1.0),
             (-1.0, +1.0, -1.0),
             (+1.0, +1.0, +1.0),
             (+1.0, -1.0, +1.0),
             (-1.0, -1.0, +1.0),
             (-1.0, +1.0, +1.0),
             ]

    faces = [(0, 1, 2, 3),
             (4, 7, 6, 5),
             (0, 4, 5, 1),
             (1, 5, 6, 2),
             (2, 6, 7, 3),
             (4, 0, 3, 7),
             ]

    for i, v in enumerate(verts):
        verts[i] = v[0] * width, v[1] * depth, v[2] * height

    return verts, faces


def create_bb():

    context = bpy.context

    if len(context.selected_objects) != 0:

        minx, miny, minz = (999999.0,) * 3
        maxx, maxy, maxz = (-999999.0,) * 3
        for obj in context.selected_objects:
            for v in obj.bound_box:
                v_world = obj.matrix_world @ \
                    mathutils.Vector((v[0], v[1], v[2]))

                if v_world[0] < minx:
                    minx = v_world[0]
                if v_world[0] > maxx:
                    maxx = v_world[0]

                if v_world[1] < miny:
                    miny = v_world[1]
                if v_world[1] > maxy:
                    maxy = v_world[1]

                if v_world[2] < minz:
                    minz = v_world[2]
                if v_world[2] > maxz:
                    maxz = v_world[2]

        verts_loc, faces = add_box(
            (maxx - minx) / 2, (maxz - minz) / 2, (maxy - miny) / 2)
        mesh = bpy.data.meshes.new("Bound_SU_Import")
        bm = bmesh.new()
        for v_co in verts_loc:
            bm.verts.new(v_co)

        bm.verts.ensure_lookup_table()

        for f_idx in faces:
            bm.faces.new([bm.verts[i] for i in f_idx])

        bm.to_mesh(mesh)
        mesh.update()

        bbox = object_utils.object_data_add(context, mesh)

        bbox.location[0] = minx + ((maxx - minx) / 2)
        bbox.location[1] = miny + ((maxy - miny) / 2)
        bbox.location[2] = minz + ((maxz - minz) / 2)

        bbox.display_type = 'BOUNDS'
        bbox.hide_render = True
