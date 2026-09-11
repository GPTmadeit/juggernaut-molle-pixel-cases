import os
ROOT_DEFAULT = os.environ.get("JUGG_ROOT",
    os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "work")))
import numpy as np, trimesh, os, sys, warnings
warnings.filterwarnings("ignore"); sys.path.insert(0,'.')
import manifold3d as m3
from mf import to_mf, to_tm, box
from params6a import *
ROOT=ROOT_DEFAULT
SRC=os.path.join(ROOT,"jugg_case","msenturk115","juggernaut-tactical-molle-phone-case")
OUT=os.path.join(ROOT,"pixel6a_case")
def L(p):
    m=trimesh.load(p); m.merge_vertices(); return m
CASE=to_mf(L(os.path.join(OUT,"case_pixel6a.stl")))
PH  =to_mf(L(os.path.join(OUT,"_phone6a_in_case.stl")))
MT  =to_mf(L(os.path.join(SRC,"mount.stl")))
def rep(a,b,lab,tol=1e-2):
    v=(a^b).volume(); print(f"  {lab:40s}{v:10.4f} mm^3  {'OK' if v<tol else '<-- CLASH'}")
    if v>=tol:
        for c in sorted(to_tm(a^b).split(only_watertight=False),key=lambda k:-abs(k.volume))[:5]:
            print("       ",np.round(c.bounds,2).tolist(),round(abs(c.volume),3))
    return v
print("=== fits ===")
rep(CASE,MT,"case x mount (MOLLE adapter)")
rep(CASE,PH,"case x Pixel 6a (seated)")
for nm,dx in [("bottom_cap",-DX),("top_cap",DX)]:
    cap=L(os.path.join(SRC,nm+".stl")); cap.apply_translation([dx,0,0])
    rep(CASE,to_mf(cap),f"case x {nm}{dx:+.2f}")
    rep(PH,to_mf(cap),f"phone x {nm}{dx:+.2f}")
print("\n=== insertion sweep (top cap off, phone slid in from +X) ===")
for dy,dz,lab in [(0,0,"centred"),(0.44,0,"+Y"),(-0.29,0,"-Y (relief limit)"),(0,0.29,"+Z")]:
    worst=0.0; wx=None
    for dx in np.arange(0,166,2.0):
        v=(CASE ^ PH.translate([float(dx),dy,dz])).volume()
        if v>worst: worst,wx=v,dx
    print(f"  {lab:20s} worst {worst:9.4f} mm^3 at +{wx} mm  {'OK' if worst<0.5 else '<-- BLOCKED'}")
print("\n=== port / camera openings vs the phone's real features ===")
feat={"speaker grille":(SPK_Y0,SPK_Y1,SPK_Z0,SPK_Z1),"USB-C":(USB_Y0,USB_Y1,USB_Z0,USB_Z1),
      "left grille":(LFT_Y0,LFT_Y1,LFT_Z0,LFT_Z1)}
for nm,(y0,y1,z0,z1) in feat.items():
    pr=box(WALL_X0-0.1,WALL_X1+0.1,y0,y1,z0,z1)
    print(f"  {nm:16s} blocked {(CASE^pr).volume():8.3f} / {pr.volume():7.2f} mm^3")
vis=box(VIS_YN+CX, VIS_YP+CX, -VIS_XP+CY, -VIS_XN+CY, Z_VIS_OUT, POCK_Z0)
print(f"  camera visor    blocked {(CASE^vis).volume():8.3f} mm^3")
