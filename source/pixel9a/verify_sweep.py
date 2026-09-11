import os
ROOT_DEFAULT = os.environ.get("JUGG_ROOT",
    os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "work")))
import numpy as np, trimesh, os, sys, warnings
warnings.filterwarnings("ignore"); sys.path.insert(0,'.')
from mf import to_mf, to_tm, box
from params import *
ROOT=ROOT_DEFAULT; OUT=os.path.join(ROOT,"pixel9a_case")
def L(p):
    m=trimesh.load(p); m.merge_vertices(); return m
CASE=to_mf(L(os.path.join(OUT,"case_pixel9a.stl")))
M=np.array([[0.,1.,0.,CX],[-1.,0.,0.,CY],[0.,0.,1.,CZ],[0.,0.,0.,1.]])
ph=L(os.path.join(ROOT,"pixel9a-phone.stl")); ph.apply_transform(M); PH=to_mf(ph)
print("insertion sweep, phone pushed to each corner of its clearance envelope")
for dy,dz,lab in [(0,0,"centred"),(0.44,0,"+Y"),(-0.25,0,"-Y (button relief limits travel to 0.25)"),(0,0.29,"+Z lifted"),
                  (0.44,0.29,"+Y +Z"),(-0.25,0.29,"-Y +Z")]:
    worst=0.0; wx=None
    for dx in np.arange(0,167,2.0):
        v=(CASE ^ PH.translate([float(dx),dy,dz])).volume()
        if v>worst: worst,wx=v,dx
    print(f"  {lab:10s} worst clash {worst:8.4f} mm^3 at insertion offset {wx} mm  {'OK' if worst<0.5 else '<-- BLOCKED'}")
print("\nseated clearances (gap between case and phone at the extremes):")
print(f"  width : pocket {POCK_Y1-POCK_Y0:.2f} vs phone {PH_W:.2f}  -> {POCK_Y1-POCK_Y0-PH_W:.2f} mm total")
print(f"  length: pocket {POCK_X1-POCK_X0:.2f} vs phone {PH_L:.2f}  -> {POCK_X1-POCK_X0-PH_L:.2f} mm total")
print(f"  depth : pocket {POCK_Z1-POCK_Z0:.2f} vs phone {PH_T:.2f}  -> {POCK_Z1-POCK_Z0-PH_T:.2f} mm")
