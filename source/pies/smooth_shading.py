# <pep8-80 compliant>

from math import pi

import bmesh
import bpy


def auto_bsmooth():

    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.shade_smooth()

    target_objects = bpy.context.scene.objects

    target_unique_meshes = set(
        obj.data
        for obj in target_objects
        if obj.type == 'MESH'
    )

    bm = bmesh.new()

    for u_mesh in target_unique_meshes:

        u_mesh.use_auto_smooth = True

        bm.from_mesh(u_mesh)

        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)

        for bm_edge in bm.edges:
            if bm_edge.is_manifold:
                if bm_edge.calc_face_angle() > 89 * pi / 180:
                    bm_edge.smooth = False

        bmesh.ops.join_triangles(bm,
                                 faces=bm.faces,
                                 cmp_seam=True,
                                 cmp_sharp=True,
                                 cmp_uvs=True,
                                 cmp_vcols=True,
                                 cmp_materials=True,
                                 angle_face_threshold=0.01,
                                 angle_shape_threshold=0.01
                                 )

        bm.to_mesh(u_mesh)
        u_mesh.update()
        bm.clear()

    bm.free()
