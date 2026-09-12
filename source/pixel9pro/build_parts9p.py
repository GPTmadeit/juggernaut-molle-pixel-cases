import os
ROOT_DEFAULT = os.environ.get("JUGG_ROOT",
    os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "work")))
"""Accessory parts for the Pixel 6a conversion (same frame as the case)."""
import numpy as np, trimesh, os, sys, warnings
warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import manifold3d as m3
from mf import to_mf, to_tm, clean, box, rrect, rrect_cs, rrect_taper, extrude_x, extrude_negy
from params9p import *

ROOT = ROOT_DEFAULT
SRC  = os.path.join(ROOT, "jugg_case", "msenturk115", "juggernaut-tactical-molle-phone-case")
OUT  = os.path.join(ROOT, "pixel9pro_case")
def load(n):
    m = trimesh.load(os.path.join(SRC, n + ".stl")); m.merge_vertices(); return m
def save(man, name):
    t = to_tm(clean(man)); t.export(os.path.join(OUT, name))
    print(f"  wrote {name:36s} tris={len(t.faces):6d} watertight={t.is_watertight} bbox={np.round(t.bounds,2).tolist()}")
    return t

def slot_row(y0, y1, n, z0, z1, gap=1.0):
    w = ((y1-y0)-(n-1)*gap)/n
    return [(y0+i*(w+gap), y0+i*(w+gap)+w, z0, z1, min(0.8, w/2-0.01, (z1-z0)/2-0.01)) for i in range(n)]
CAP_HOLES = (slot_row(SPK_Y0-0.6, SPK_Y1+0.6, 4, SPK_Z0-0.55, SPK_Z1+0.55) +
             [(MIC_Y0-1.0, MIC_Y1+1.0, MIC_Z0-0.9, MIC_Z1+0.9, 0.8),
              (AUX_Y0-1.0, AUX_Y1+1.0, AUX_Z0-0.9, AUX_Z1+0.9, 0.8)])
def cut_cap_holes(man, x0, x1):
    for (y0,y1,z0,z1,r) in CAP_HOLES:
        man -= extrude_x(rrect_cs(y0, y1, z0, z1, r), x0, x1)
    return man

# =============================================================== TOP CAP ======
tc = to_mf(load("top_cap")).translate([DX, 0, 0])
# the 9 Pro's top mic (Y -45.22..-44.02) already falls inside the stock cap's vent at Y -46.54..-43.54
save(tc, "top_cap_pixel9pro.stl")

# ============================================================ BOTTOM CAP ======
bc = to_mf(load("bottom_cap")).translate([-DX, 0, 0])
P0, P1 = -21.03-DX, -17.40-DX
bc += box(P0, P1, -50.0, 6.0, 3.30, 6.70)
bc = cut_cap_holes(bc, P0-0.5, P1+0.5)
save(bc, "bottom_cap_pixel9pro.stl")

# ================================================ BOTTOM CAP (USB CABLE) ======
uc = to_mf(load("bottom_cap_for_usb_cable")).translate([-DX, 0, 0])
U0, U1 = -59.45-DX, -55.82-DX
uc += box(U0, U1, -50.0, 6.0, 3.30, 6.70)
uc = cut_cap_holes(uc, U0-0.5, U1+0.5)
uc -= extrude_x(rrect_cs(-27.60, -14.40, 1.40, 2.60, 0.3), -61.95-DX-0.5, U1+0.5)
save(uc, "bottom_cap_for_usb_cable_pixel9pro.stl")

# ==================================================== CAMERA PROTECTOR CAP ====
def shelf(g):
    return rrect_taper(SHELF_X0+SHELF_TAPER-g, CASE_X1-SHELF_TAPER+g,
                       SHELF_Y0+SHELF_TAPER-g, SHELF_Y1-SHELF_TAPER+g, 4.0+g,
                       SHELF_Z, Z_BACK_WIN, SHELF_TAPER)
WALL, FLOOR, CLR = 1.30, 1.40, 0.12
def skirt(g, z0):
    return rrect(SHELF_X0+SHELF_TAPER-g, CASE_X1-SHELF_TAPER+g,
                 SHELF_Y0+SHELF_TAPER-g, SHELF_Y1-SHELF_TAPER+g, 4.0+g, z0, SHELF_Z+0.001)
cavity = shelf(CLR) + skirt(CLR, SHELF_Z-25.0)
outer  = shelf(CLR+WALL) + skirt(CLR+WALL, SHELF_Z-FLOOR)
cap = (outer - cavity) ^ box(-500,500,-500,500, SHELF_Z-FLOOR, Z_BACK_WIN)
case = to_mf(trimesh.load(os.path.join(OUT,"case_pixel9pro.stl")))
grown = case
for d in [(0.15,0,0),(-0.15,0,0),(0,0.15,0),(0,-0.15,0),(0,0,-0.15)]:
    grown = grown + case.translate(list(d))
cap -= grown                                   # let the rim sit on the real back profile
for i in range(-5, 6):                         # grip ribs
    cap -= box(-500, 500, (SHELF_Y0+SHELF_Y1)/2 + i*4.2-0.6, (SHELF_Y0+SHELF_Y1)/2 + i*4.2+0.6,
               SHELF_Z-FLOOR-0.01, SHELF_Z-FLOOR+0.45)
save(cap, "camera_protector_cap_pixel9pro.stl")

# ========================================================= BUTTON INSERTS =====
Y_FLANGE_OUT = Y_RECESS + 0.05
Y_FLANGE_IN  = Y_FLANGE_OUT + FLANGE_T
def insert(rec_x, wins, thin=None):
    fl = extrude_negy(rrect_cs(rec_x[0]+0.15, rec_x[1]-0.15,
                               BTN_Z0-REC_MZ+0.15, BTN_Z1+REC_MZ-0.15, 1.0), Y_FLANGE_IN, Y_FLANGE_OUT)
    for wx0, wx1 in wins:
        fl += extrude_negy(rrect_cs(wx0+0.20, wx1-0.20, BTN_Z0-WIN_MZ+0.20, BTN_Z1+WIN_MZ-0.20, 0.7),
                           Y_FLANGE_OUT, Y_PAD_FACE)
    if thin:
        fl -= box(thin[0], thin[1], Y_FLANGE_OUT, Y_FLANGE_IN-0.45, BTN_Z0-4, BTN_Z1+4)
    return fl
VOL_GAP = 3.0
save(insert((VOL_X0-REC_MX, VOL_X1+REC_MX),
            [(VOL_X0-WIN_MX, VOL_MID-VOL_GAP/2), (VOL_MID+VOL_GAP/2, VOL_X1+WIN_MX)],
            thin=(VOL_MID-1.1, VOL_MID+1.1)), "volume_button_pixel9pro.stl")
save(insert((PWR_X0-REC_MX, PWR_X1+REC_MX), [(PWR_X0-WIN_MX, PWR_X1+WIN_MX)]), "power_button_pixel9pro.stl")
print("done")
