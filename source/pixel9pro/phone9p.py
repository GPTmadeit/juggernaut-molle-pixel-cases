import os
ROOT_DEFAULT = os.environ.get("JUGG_ROOT",
    os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "work")))
"""Pixel 9 Pro phone solid, repaired and placed in the case frame."""
import os, sys, numpy as np, trimesh, warnings
warnings.filterwarnings("ignore"); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from params9p import CX, CY, CZ
SRC = os.path.join(ROOT_DEFAULT, "p9pro_src", "files", "pixel_9_pro.stl")

def phone_native():
    m = trimesh.load(SRC)
    m.apply_scale(1000.0)                      # the file is in metres
    m.merge_vertices()
    m.apply_translation(-m.bounds[0])          # park at the origin
    m.update_faces(m.nondegenerate_faces())    # 96 zero-area tris from the Blender export
    m.remove_unreferenced_vertices(); m.merge_vertices()
    trimesh.repair.fix_normals(m); trimesh.repair.fix_winding(m)
    assert m.is_watertight, "9 Pro mesh did not close"
    return m

def phone_in_case():
    m = phone_native()
    M = np.array([[ 0.,-1., 0., CX],
                  [-1., 0., 0., CY],
                  [ 0., 0.,-1., CZ],
                  [ 0., 0., 0., 1.]])
    assert abs(np.linalg.det(M[:3,:3]) - 1.0) < 1e-9, "not a rotation"
    m.apply_transform(M); m.merge_vertices()
    return m
