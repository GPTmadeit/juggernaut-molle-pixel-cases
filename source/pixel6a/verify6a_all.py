import os
ROOT_DEFAULT = os.environ.get("JUGG_ROOT",
    os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "work")))
import numpy as np, trimesh, os, sys, warnings
warnings.filterwarnings("ignore"); sys.path.insert(0,'.')
from mf import to_mf, to_tm, box
from params6a import *
ROOT=ROOT_DEFAULT
SRC=os.path.join(ROOT,"jugg_case","msenturk115","juggernaut-tactical-molle-phone-case")
OUT=os.path.join(ROOT,"pixel6a_case")
def L(p):
    m=trimesh.load(p); m.merge_vertices(); return m
def P(n): return to_mf(L(os.path.join(OUT,n)))
CASE=P("case_pixel6a.stl"); PH=P("_phone6a_in_case.stl"); MT=to_mf(L(os.path.join(SRC,"mount.stl")))
parts={n:P(n+"_pixel6a.stl") for n in ["top_cap","bottom_cap","bottom_cap_for_usb_cable",
                                       "camera_protector_cap","volume_button","power_button"]}
def rep(a,b,lab,tol=0.5):
    v=(a^b).volume(); print(f"  {lab:44s}{v:9.4f} mm^3  {'OK' if v<tol else '<-- CLASH'}")
    if v>=tol:
        for c in sorted(to_tm(a^b).split(only_watertight=False),key=lambda k:-abs(k.volume))[:4]:
            print("       ",np.round(c.bounds,2).tolist(),round(abs(c.volume),3))
print("=== interference ===")
rep(CASE,MT,"case x mount (MOLLE adapter)")
rep(CASE,PH,"case x Pixel 6a")
for n,p in parts.items():
    q = p.translate([38.42,0,0]) if n=="bottom_cap_for_usb_cable" else p
    if n=="camera_protector_cap": rep(CASE,q,"case x camera_protector_cap (cap ON)"); continue
    rep(CASE,q,f"case x {n}"); rep(PH,q,f"phone x {n}")
print("\n=== button plunger ===")
for n in ["volume_button","power_button"]:
    t=to_tm(parts[n]); b=t.bounds
    print(f"  {n}: flange face Y={b[1][1]:.3f}  button face Y={Y_BTN_FACE:.3f}"
          f"  gap {abs(b[1][1]-Y_BTN_FACE):.3f} mm | pad face Y={b[0][1]:.2f} (tab tip -61.10)")
print("\n=== cap hole alignment (open fraction of each bottom feature) ===")
bc=parts["bottom_cap"]; uc=parts["bottom_cap_for_usb_cable"].translate([38.42,0,0]); tc=parts["top_cap"]
feat={"speaker":(SPK_Y0,SPK_Y1,SPK_Z0,SPK_Z1),"USB-C":(USB_Y0,USB_Y1,USB_Z0,USB_Z1),
      "left grille":(LFT_Y0,LFT_Y1,LFT_Z0,LFT_Z1)}
for capname,cap in [("bottom_cap",bc),("bottom_cap_for_usb_cable",uc)]:
    print(f" {capname}:")
    for nm,(y0,y1,z0,z1) in feat.items():
        pr=box(-26.0-DX, WALL_X0-0.05, y0,y1,z0,z1)
        print(f"    {nm:12s} open {100*(1-((CASE+cap)^pr).volume()/pr.volume()):5.1f}%")
pr=box(POCK_X1-0.05, 145.0, TOPMIC_Y0, TOPMIC_Y1, TOPMIC_Z0, TOPMIC_Z1)
print(f" top_cap over the 6a top mic: open {100*(1-((CASE+tc)^pr).volume()/pr.volume()):5.1f}%")
print("\n=== all STLs ===")
for f in sorted(os.listdir(OUT)):
    if not f.endswith('.stl') or f.startswith('_'): continue
    m=L(os.path.join(OUT,f)); b=m.bounds
    print(f"  {f:42s} tris={len(m.faces):7d} bodies={len(m.split(only_watertight=False)):2d} "
          f"watertight={str(m.is_watertight):5s} size={np.round(b[1]-b[0],2).tolist()}")
