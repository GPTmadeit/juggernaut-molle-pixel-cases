import os
ROOT_DEFAULT = os.environ.get("JUGG_ROOT",
    os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "work")))
import numpy as np, trimesh, os, sys, warnings
warnings.filterwarnings("ignore"); sys.path.insert(0,'.')
import manifold3d as m3
from mf import to_mf, to_tm, box, rrect_cs, extrude_x
from params import *
ROOT=ROOT_DEFAULT
SRC=os.path.join(ROOT,"jugg_case","msenturk115","juggernaut-tactical-molle-phone-case")
OUT=os.path.join(ROOT,"pixel9a_case")
def L(p):
    m=trimesh.load(p); m.merge_vertices(); return m
def P(n): return to_mf(L(os.path.join(OUT,n)))
CASE=P("case_pixel9a.stl")
M=np.array([[0.,1.,0.,CX],[-1.,0.,0.,CY],[0.,0.,1.,CZ],[0.,0.,0.,1.]])
phm=L(os.path.join(ROOT,"pixel9a-phone.stl")); phm.apply_transform(M); PH=to_mf(phm)
MT=to_mf(L(os.path.join(SRC,"mount.stl")))
parts={n:P(n+"_pixel9a.stl") for n in ["top_cap","bottom_cap","bottom_cap_for_usb_cable",
                                       "camera_protector_cap","volume_button","power_button"]}
def chk(a,b,lab,tol=1e-2):
    v=(a^b).volume(); ok = v<tol
    print(f"  {lab:44s}{v:9.4f} mm^3  {'OK' if ok else '<-- CLASH'}")
    if not ok:
        for c in sorted(to_tm(a^b).split(only_watertight=False),key=lambda k:-abs(k.volume))[:4]:
            print("       ",np.round(c.bounds,2).tolist(),round(abs(c.volume),3))
print("=== interference (STL round-trip, so <0.5 mm^3 = float32 noise) ===")
chk(CASE,MT,"case x mount  (MOLLE adapter)")
chk(CASE,PH,"case x Pixel 9a")
for n,p in parts.items():
    if n=="bottom_cap_for_usb_cable":
        p=p.translate([38.42,0,0])   # this part is exported at a print offset
    if n=="camera_protector_cap": continue
    chk(CASE,p,f"case x {n}")
    chk(PH,p,f"phone x {n}")
chk(CASE,parts["camera_protector_cap"],"case x camera_protector_cap (cap ON)")
print("\n=== button plunger geometry ===")
for n,bx in [("volume_button",(VOL_X0,VOL_X1)),("power_button",(PWR_X0,PWR_X1))]:
    t=to_tm(parts[n]); b=t.bounds
    print(f"  {n}: flange face Y={b[1][1]:.2f}  (phone button face Y={CY-36.65-0.60:.2f}"
          f" -> gap {abs(b[1][1]-(CY-36.65-0.60)):.2f} mm), pad face Y={b[0][1]:.2f}"
          f" (outer surface {Y_RAIL_N:.2f}, groove floor {Y_GRV_N:.2f})")
print("\n=== port openings vs the phone's real features (case end wall) ===")
feat={"speaker grille":(SPK_Y0,SPK_Y1,2.65,4.45),"USB-C":(USB_Y0,USB_Y1,2.25,4.85),
      "bottom mic":(MIC_Y0,MIC_Y1,3.05,4.05),"left grille":(LFT_Y0,LFT_Y1,2.05,5.05)}
wall = box(WALL_X0-0.2, WALL_X1+0.2, -70, 30, -10, 20)
for nm,(y0,y1,z0,z1) in feat.items():
    probe = box(WALL_X0-0.1, WALL_X1+0.1, y0, y1, z0, z1)
    blocked=(CASE ^ probe).volume(); tot=probe.volume()
    print(f"  {nm:16s} feature {y0:7.2f}..{y1:6.2f} Y, {z0:.2f}..{z1:.2f} Z  -> blocked by case: {blocked:7.3f}/{tot:7.2f} mm^3 {'OK' if blocked<1e-2 else '<-- BLOCKED'}")
print("\n=== camera opening vs the Pixel camera bar ===")
bar = box(CAM_X0, CAM_X1, CAM_Y0, CAM_Y1, -1.55, POCK_Z0)
print(f"  bar blocked by case: {(CASE^bar).volume():.4f} mm^3")
