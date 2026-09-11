import os
ROOT_DEFAULT = os.environ.get("JUGG_ROOT",
    os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "work")))
"""Release pass: decimate every STL to a 5 micron tolerance, then re-verify every fit."""
import numpy as np, trimesh, os, sys, warnings
warnings.filterwarnings("ignore"); sys.path.insert(0,'.')
from mf import to_mf, to_tm
TOL = 0.005
ROOT=ROOT_DEFAULT
SRC=os.path.join(ROOT,"jugg_case","msenturk115","juggernaut-tactical-molle-phone-case")
for d in ["pixel9a_case","pixel6a_case"]:
    P=os.path.join(ROOT,d)
    for f in sorted(os.listdir(P)):
        if not f.endswith(".stl") or "UNCHANGED" in f or f.startswith("_"): continue
        m=trimesh.load(os.path.join(P,f)); m.merge_vertices()
        n0=len(m.faces); M=to_mf(m); v0=M.volume()
        S=M.simplify(TOL); t=to_tm(S); t.merge_vertices()
        assert t.is_watertight and len(t.split(only_watertight=False))==1, f
        t.export(os.path.join(P,f))
        print(f"  {f:42s} {n0:7d} -> {len(t.faces):6d} tris   dVol {abs(S.volume()-v0):7.3f} mm^3")
print("\n=== re-verify after decimation ===")
def L(p):
    m=trimesh.load(p); m.merge_vertices(); return m
MT=to_mf(L(os.path.join(SRC,"mount.stl")))
# regenerate the full-fidelity phone references used for the fit checks
import importlib
sys.path.insert(0,'.')
import params as P9
M9=np.array([[0.,1.,0.,P9.CX],[-1.,0.,0.,P9.CY],[0.,0.,1.,P9.CZ],[0.,0.,0.,1.]])
_p9=L(os.path.join(ROOT,"pixel9a-phone.stl")); _p9.apply_transform(M9)
_p9.export(os.path.join(ROOT,"pixel9a_case","_phone9a_in_case.stl"))
from phone6a import phone_in_case as _pic6
_pic6().export(os.path.join(ROOT,"pixel6a_case","_phone6a_in_case.stl"))
for tag,d,dxp in [("9a","pixel9a_case",2.70),("6a","pixel6a_case",1.45)]:
    P=os.path.join(ROOT,d)
    case=to_mf(L(os.path.join(P,f"case_pixel{tag}.stl")))
    ph  =to_mf(L(os.path.join(P,[x for x in os.listdir(P) if x.startswith('_phone')][0])))
    print(f" {tag}:  case x mount {(case^MT).volume():8.4f}   case x phone {(case^ph).volume():8.4f}")
    for n in ["top_cap","bottom_cap","bottom_cap_for_usb_cable","camera_protector_cap","volume_button","power_button"]:
        p=to_mf(L(os.path.join(P,f"{n}_pixel{tag}.stl")))
        q=p.translate([38.42,0,0]) if n=="bottom_cap_for_usb_cable" else p
        a=(case^q).volume(); b=(ph^q).volume() if n!="camera_protector_cap" else 0.0
        flag = "" if max(a,b)<0.5 else "   <-- CLASH"
        print(f"      {n:26s} case {a:7.4f}  phone {b:7.4f}{flag}")
    worst=0.0
    for dx in np.arange(0,170,2.0):
        worst=max(worst,(case ^ ph.translate([float(dx),0,0])).volume())
    print(f"      insertion sweep worst {worst:.4f} mm^3  {'OK' if worst<0.5 else '<-- BLOCKED'}")
