import os
ROOT_DEFAULT = os.environ.get("JUGG_ROOT",
    os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "work")))
"""Accessory parts for the Pixel 9a conversion (same coordinate frame as the case)."""
import numpy as np, trimesh, os, sys, warnings
warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import manifold3d as m3
from mf import to_mf, to_tm, clean, box, rrect, rrect_cs, rrect_taper, stats, extrude_x, extrude_negy
from params import *

ROOT = ROOT_DEFAULT
SRC  = os.path.join(ROOT, "jugg_case", "msenturk115", "juggernaut-tactical-molle-phone-case")
OUT  = os.path.join(ROOT, "pixel9a_case")
os.makedirs(OUT, exist_ok=True)
def load(n):
    m = trimesh.load(os.path.join(SRC, n + ".stl")); m.merge_vertices(); return m
def save(man, name):
    t = to_tm(clean(man))
    t.export(os.path.join(OUT, name))
    print(f"  wrote {name:34s} tris={len(t.faces):6d} watertight={t.is_watertight} bbox={np.round(t.bounds,2).tolist()}")
    return t

# ----------------------------------------------------------------- port pattern
# Pixel 9a bottom-edge features, as (y0, y1, z-height, corner r) slot groups
def slot_row(y0, y1, n, h, gap=1.0, r=0.8):
    """n evenly spaced slots filling y0..y1."""
    w = ((y1 - y0) - (n - 1) * gap) / n
    out = []
    for i in range(n):
        a = y0 + i * (w + gap)
        out.append((a, a + w, h, min(r, w / 2 - 0.01, h / 2 - 0.01)))
    return out
SPK_SLOTS = slot_row(SPK_Y0 + 0.1, SPK_Y1 - 0.1, 4, 1.8)
LFT_SLOTS = slot_row(LFT_Y0 + 0.1, LFT_Y1 - 0.1, 4, 2.4)
MIC_SLOT  = [(MIC_Y0 - 0.6, MIC_Y1 + 0.6, 2.0, 0.9)]
CAP_HOLES = SPK_SLOTS + LFT_SLOTS + MIC_SLOT

def cut_cap_holes(man, x0, x1, dy=0.0):
    for (y0, y1, h, r) in CAP_HOLES:
        cs = rrect_cs(y0 + dy, y1 + dy, PORT_Z_MID - h/2, PORT_Z_MID + h/2, r)
        man -= extrude_x(cs, x0, x1)
    return man

# The stock cap's four S8 speaker slots sit at Y -44.22..-32.82.  Keep the erase
# block to exactly that band: anything wider also plugs the USB cable window.
SLOT_FILL_Y0, SLOT_FILL_Y1 = -45.5, -31.5

# =============================================================== 1. TOP CAP ====
tc = to_mf(load("top_cap")).translate([DX, 0, 0])
save(tc, "top_cap_pixel9a.stl")     # its existing vent already lines up with the Pixel's top mic

# ============================================================ 2. BOTTOM CAP ====
bc = to_mf(load("bottom_cap")).translate([-DX, 0, 0])
PLATE0, PLATE1 = -21.03 - DX, -17.40 - DX               # -23.73 .. -20.10
bc += box(PLATE0, PLATE1, SLOT_FILL_Y0, SLOT_FILL_Y1, 3.30, 6.70)   # erase the S8 speaker slots
bc = cut_cap_holes(bc, PLATE0 - 0.5, PLATE1 + 0.5)
save(bc, "bottom_cap_pixel9a.stl")

# ================================================ 3. BOTTOM CAP (USB CABLE) ====
UOFF = -40.92                                            # this part's own print offset
uc = to_mf(load("bottom_cap_for_usb_cable")).translate([-DX, 0, 0])
UP0, UP1 = -59.45 - DX, -55.82 - DX
uc += box(UP0, UP1, SLOT_FILL_Y0, SLOT_FILL_Y1, 3.30, 6.70)
uc = cut_cap_holes(uc, UP0 - 0.5, UP1 + 0.5)
# drop the cable window's lower edge so a plug clears the Pixel's USB-C port
# The stock cable window (Z 2.45..7.55) was aligned to the S8's USB-C, which sits
# ~1.5-1.9 mm higher in the pocket than these phones'.  Recut it as one clean
# window that spans the phone's actual port height, so the cap stops being the
# narrowest point of the plug corridor.
uc -= extrude_x(rrect_cs(-27.60, -14.40, 0.80, 7.55, 0.5), -61.95 - DX - 0.5, UP1 + 0.5)
save(uc, "bottom_cap_for_usb_cable_pixel9a.stl")

# =================================================== 4. CAMERA PROTECTOR CAP ===
def hood(g):
    """The case's camera hood, grown by g on every side (45 deg taper preserved)."""
    return rrect_taper(CO_X0 - HOOD_FOOT - g, CO_X1 + HOOD_FOOT + g,
                       CO_Y0 - HOOD_FOOT - g, CO_Y1 + HOOD_FOOT + g,
                       CO_R + HOOD_FOOT + g, Z_HOOD, Z_BACK_WIN, HOOD_W - HOOD_FOOT)
WALL, FLOOR, CLR = 1.20, 1.40, 0.12
cavity = hood(CLR)
cavity += rrect(CO_X0 - HOOD_FOOT - CLR, CO_X1 + HOOD_FOOT + CLR,
                CO_Y0 - HOOD_FOOT - CLR, CO_Y1 + HOOD_FOOT + CLR,
                CO_R + HOOD_FOOT + CLR, Z_HOOD - 20.0, Z_HOOD + 0.001)
shell = hood(CLR + WALL)
shell += rrect(CO_X0 - HOOD_FOOT - CLR - WALL, CO_X1 + HOOD_FOOT + CLR + WALL,
               CO_Y0 - HOOD_FOOT - CLR - WALL, CO_Y1 + HOOD_FOOT + CLR + WALL,
               CO_R + HOOD_FOOT + CLR + WALL, Z_HOOD - FLOOR, Z_HOOD + 0.001)
cap = (shell - cavity) ^ box(-500, CASE_X1, -500, 500, Z_HOOD - FLOOR, Z_BACK_WIN)
# grip ribs on the outside of the cap floor
for i in range(-4, 5):
    cap -= box(CO_X0 - 40, CO_X1 + 40, CO_Y0 + i * 3.6 - 0.6, CO_Y0 + i * 3.6 + 0.6,
               Z_HOOD - FLOOR - 0.01, Z_HOOD - FLOOR + 0.45)
save(cap, "camera_protector_cap_pixel9a.stl")

# ========================================================= 5. BUTTON INSERTS ===
Y_FLANGE_OUT = Y_RECESS + 0.05           # rests against the recess shoulder
Y_FLANGE_IN  = Y_FLANGE_OUT + 0.80       # 0.80 mm flange -> 0.20 mm gap to the phone button,
                                         # so the phone can bias 0.25 mm toward the wall (the depth
                                         # of the button relief groove) without pressing anything
def insert(rec_x, wins, thin=None):
    fl = extrude_negy(rrect_cs(rec_x[0] + 0.15, rec_x[1] - 0.15,
                               BTN_Z0 - REC_MZ + 0.15, BTN_Z1 + REC_MZ - 0.15, 1.0),
                      Y_FLANGE_IN, Y_FLANGE_OUT)
    for wx0, wx1 in wins:
        fl += extrude_negy(rrect_cs(wx0 + 0.20, wx1 - 0.20,
                                    BTN_Z0 - WIN_MZ + 0.20, BTN_Z1 + WIN_MZ - 0.20, 0.7),
                           Y_FLANGE_OUT, Y_PAD_FACE)
    if thin:
        fl -= box(thin[0], thin[1], Y_FLANGE_OUT, Y_FLANGE_IN - 0.45, BTN_Z0 - 4, BTN_Z1 + 4)
    return fl
VOL_GAP = 3.0
vol = insert((VOL_X0 - REC_MX, VOL_X1 + REC_MX),
             [(VOL_X0 - WIN_MX, VOL_MID - VOL_GAP/2), (VOL_MID + VOL_GAP/2, VOL_X1 + WIN_MX)],
             thin=(VOL_MID - 1.1, VOL_MID + 1.1))
pwr = insert((PWR_X0 - REC_MX, PWR_X1 + REC_MX), [(PWR_X0 - WIN_MX, PWR_X1 + WIN_MX)])
save(vol, "volume_button_pixel9a.stl")
save(pwr, "power_button_pixel9a.stl")
print("done")
