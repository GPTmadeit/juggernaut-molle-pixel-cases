import os
ROOT_DEFAULT = os.environ.get("JUGG_ROOT",
    os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "work")))
"""Build the Pixel 6a phone solid and its pocket cross-section from the 3MF."""
import sys, os, numpy as np, trimesh, warnings
warnings.filterwarnings("ignore"); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import manifold3d as m3
from read3mf import load_3mf
from mf import to_mf, to_tm
from params6a import *
from shapely.geometry.polygon import orient

SRC3MF = os.path.join(ROOT_DEFAULT, "pixel6a_src", "Pixel6AModel.3mf")
_objs, _items = load_3mf(SRC3MF)
def part(oid):
    V, F = _objs[oid]
    m = trimesh.Trimesh(vertices=V, faces=F, process=False); m.merge_vertices(); return m

def phone_native():
    """Full outer solid: body + screen + visor + lenses + flash + buttons."""
    KEEP = ['21','19','7','25','23','5','15','13','1','3']
    U = to_mf(part(KEEP[0]))
    for k in KEEP[1:]: U = U + to_mf(part(k))
    return U

def phone_in_case():
    M = np.array([[0.,1.,0.,CX],[-1.,0.,0.,CY],[0.,0.,1.,CZ],[0.,0.,0.,1.]])
    t = to_tm(phone_native()); t.apply_transform(M); t.merge_vertices(); return t

def pocket_cs():
    """Pocket outline = body silhouette (port notches filled) offset by the clearances."""
    body = part('21')
    s = body.section(plane_origin=[0,0,4.3], plane_normal=[0,0,1])
    p2,_ = s.to_planar(to_2D=np.eye(4))
    poly = orient(max(p2.polygons_full, key=lambda p: p.area), 1.0)
    cs = m3.CrossSection([np.asarray(poly.exterior.coords)[:-1]], m3.FillRule.Positive)
    cs = cs + m3.CrossSection.square([60.0, 7.7]).translate([-20.0, PH_YN])   # fill the port notches
    cs = cs.offset(CLR_SIDE, m3.JoinType.Round, 2.0, 128)
    e = CLR_END - CLR_SIDE
    cs = cs + cs.translate([0.0, e]) + cs.translate([0.0, -e])                # extra end clearance
    return cs.rotate(-90.0).translate([CX, CY])                               # phone frame -> case frame

def visor_cs():
    """Visor footprint where it meets the phone's back, in the case frame, + clearance."""
    vis = part('7')
    s = vis.section(plane_origin=[0,0,-0.001], plane_normal=[0,0,1])
    p2,_ = s.to_planar(to_2D=np.eye(4))
    poly = orient(max(p2.polygons_full, key=lambda p: p.area), 1.0)
    cs = m3.CrossSection([np.asarray(poly.exterior.coords)[:-1]], m3.FillRule.Positive)
    cs = cs.offset(CAM_CLR, m3.JoinType.Round, 2.0, 64)
    return cs.rotate(-90.0).translate([CX, CY])
