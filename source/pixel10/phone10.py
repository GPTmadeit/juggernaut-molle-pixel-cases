import os
ROOT_DEFAULT = os.environ.get("JUGG_ROOT",
    os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "work")))
"""Pixel 10 phone solid, placed in the case frame."""
import sys, numpy as np, trimesh, warnings
warnings.filterwarnings("ignore"); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from params10 import CX, CY, CZ, NAT_W, NAT_L
from mf import to_mf, to_tm
SRC = os.path.join(ROOT_DEFAULT, "p10_src", "Pixel10.stl")

def phone_native():
    m = trimesh.load(SRC); m.merge_vertices()
    m.apply_translation(-m.bounds[0])                 # park at the origin
    assert np.allclose(m.extents[:2], [NAT_W, NAT_L], atol=0.02), m.extents
    # four closed shells (body, lens glass, two buttons) -> one solid
    u = None
    for p in m.split(only_watertight=False):
        assert p.is_watertight
        q = to_mf(p); u = q if u is None else u + q
    return to_tm(u)

def phone_in_case():
    m = phone_native()
    R = np.array([[-1.,0.,0.,NAT_W],[0.,-1.,0.,NAT_L],[0.,0.,1.,0.],[0.,0.,0.,1.]])  # 180 deg about Z
    M = np.array([[ 0.,-1., 0., CX],
                  [-1., 0., 0., CY],
                  [ 0., 0.,-1., CZ],
                  [ 0., 0., 0., 1.]])
    T = M @ R
    assert abs(np.linalg.det(T[:3,:3]) - 1.0) < 1e-9, "not a rotation"
    m.apply_transform(T); m.merge_vertices()
    return m
