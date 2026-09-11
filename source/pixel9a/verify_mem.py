import os
ROOT_DEFAULT = os.environ.get("JUGG_ROOT",
    os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "work")))
"""Rebuild the case in memory and run every fit check on the exact manifold."""
import sys, os, numpy as np, warnings, trimesh
warnings.filterwarnings("ignore"); sys.path.insert(0,'.')
import manifold3d as m3
from mf import *
from params import *
ROOT=ROOT_DEFAULT
SRC=os.path.join(ROOT,"jugg_case","msenturk115","juggernaut-tactical-molle-phone-case")
OUT=os.path.join(ROOT,"pixel9a_case")
src=open('build_case.py').read().split("# ========================================================= 11. EXPORT")[0]
src=src.replace("stats(C,","_ig(C,").replace(
  "from mf import (to_mf, to_tm, clean, box, rrect, rrect_cs, rrect_taper, stats,\n                extrude_x, extrude_negy, extrude_posy)",
  "from mf import *\n_ig=lambda *a,**k: None")
exec(src)
CASE = C
print("in-memory case: vol %.2f genus %d tris %d" % (CASE.volume(), CASE.genus(), CASE.num_tri()))
def L(p):
    m=trimesh.load(p); m.merge_vertices(); return m
M = np.array([[0.,1.,0.,CX],[-1.,0.,0.,CY],[0.,0.,1.,CZ],[0.,0.,0.,1.]])
phone=L(os.path.join(ROOT,"pixel9a-phone.stl")); phone.apply_transform(M)
PH=to_mf(phone)
MT=to_mf(L(os.path.join(SRC,"mount.stl")))
def rep(a,b,lab):
    v=(a^b).volume()
    print(f"  {lab:36s} {v:10.4f} mm^3  {'OK' if v<1e-2 else '<-- CLASH'}")
    if v>=1e-2:
        for c in sorted(to_tm(a^b).split(only_watertight=False),key=lambda k:-abs(k.volume))[:6]:
            print("      ", np.round(c.bounds,2).tolist(), round(abs(c.volume),3))
    return v
print("\n== fits ==")
rep(CASE,MT,"case x mount")
rep(CASE,PH,"case x phone (seated)")
for nm,dx in [("bottom_cap",-DX),("top_cap",DX)]:
    cap=L(os.path.join(SRC,nm+".stl")); cap.apply_translation([dx,0,0])
    rep(CASE,to_mf(cap),f"case x {nm}")
    rep(PH,to_mf(cap),f"phone x {nm}")
print("\n== insertion sweep ==")
bad=[]
for dx in np.arange(0,168,3.0):
    v=(CASE ^ PH.translate([float(dx),0,0])).volume()
    if v>1e-2: bad.append((dx,v))
print("   clear" if not bad else "   blocked at "+", ".join(f"{d:.0f}mm({v:.1f})" for d,v in bad[:12]))
