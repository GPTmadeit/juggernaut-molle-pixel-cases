import os
ROOT_DEFAULT = os.environ.get("JUGG_ROOT",
    os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "work")))
import numpy as np, trimesh, os, sys, warnings
warnings.filterwarnings("ignore"); sys.path.insert(0,'.')
from mf import to_mf, to_tm, box
from params import *
ROOT=ROOT_DEFAULT; OUT=os.path.join(ROOT,"pixel9a_case")
print(f"{'file':44s} {'tris':>7s} {'bodies':>7s} {'watertight':>11s} {'vol cm3':>9s}  bbox size (mm)")
for f in sorted(os.listdir(OUT)):
    if not f.endswith(".stl"): continue
    m=trimesh.load(os.path.join(OUT,f)); m.merge_vertices()
    b=m.bounds; sz=np.round(b[1]-b[0],2)
    print(f"{f:44s} {len(m.faces):7d} {len(m.split(only_watertight=False)):7d} {str(m.is_watertight):>11s} {m.volume/1000:9.2f}  {sz.tolist()}")
# screen opening vs display
DISP_W, DISP_H = 65.1, 146.1
print(f"\nscreen opening {OPEN_X1-OPEN_X0:.2f} x {OPEN_Y1-OPEN_Y0:.2f} mm  (Pixel 9a display ~{DISP_H:.1f} x {DISP_W:.1f})")
print(f"   clear of the display by {((OPEN_X1-OPEN_X0)-DISP_H)/2:.2f} mm (length) / {((OPEN_Y1-OPEN_Y0)-DISP_W)/2:.2f} mm (width)")
print(f"   lip overlap onto the phone's front face: {(15.63-1.71)-OPEN_Y1+1.71:.2f} mm each side")
CASE=to_mf(trimesh.load(os.path.join(OUT,"case_pixel9a.stl")))
disp = box(CX-DISP_H/2, CX+DISP_H/2, CY-DISP_W/2, CY+DISP_W/2, POCK_Z0+PH_T-0.01, 30)
print(f"   display area obstructed by the case: {(CASE^disp).volume():.3f} mm^3")
