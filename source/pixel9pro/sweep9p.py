import os
ROOT_DEFAULT = os.environ.get("JUGG_ROOT",
    os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "work")))
import numpy as np, trimesh, os, sys, warnings
warnings.filterwarnings("ignore"); sys.path.insert(0,'.')
from mf import to_mf
from params9p import *
ROOT=ROOT_DEFAULT; OUT=os.path.join(ROOT,"pixel9pro_case")
def L(p):
    m=trimesh.load(p); m.merge_vertices(); return m
CASE=to_mf(L(os.path.join(OUT,"case_pixel9pro.stl"))); PH=to_mf(L(os.path.join(OUT,"_phone9pro_in_case.stl")))
print("insertion sweep (top cap off, phone slid in from the +X end):")
for dy,dz,lab in [(0,0,"centred"),(0.44,0,"+Y"),(-0.30,0,"-Y (relief limit)"),(0,0.29,"+Z lifted"),(0.44,0.29,"+Y +Z")]:
    worst=0.0; wx=None
    for dx in np.arange(0,170,2.0):
        v=(CASE ^ PH.translate([float(dx),dy,dz])).volume()
        if v>worst: worst,wx=v,dx
    print(f"  {lab:20s} worst {worst:9.4f} mm^3 at +{wx} mm  {'OK' if worst<0.5 else '<-- BLOCKED'}")
print("\nclearances: width %.2f  length %.2f  depth %.2f mm total"%(POCK_Y1-POCK_Y0-PH_W, POCK_X1-POCK_X0-PH_L, POCK_Z1-POCK_Z0-PH_T))
