import os
ROOT_DEFAULT = os.environ.get("JUGG_ROOT",
    os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "work")))
"""Pixel 10 kit, derived from the finished Pixel 9 Pro kit in ../../pixel-9-pro/.

The Pixel 10 has the 9 Pro's 152.8 x 72.0 footprint, so everything the MOLLE adapter and
the end caps touch is inherited untouched.  What differs is refilled, then recut:
  * pocket 0.1 mm taller (8.6 mm phone) and cut with a tighter corner radius
  * camera bar 1.4 mm longer and 0.5 mm wider -> wider shelf, opening and slide channel
  * buttons ~1 mm lower down the side
  * bottom edge: two speaker grilles either side of the USB-C (9 Pro: grille / mic / hole)
"""
import numpy as np, trimesh, sys, warnings
warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, ".."))
import manifold3d as m3
from mf import to_mf, to_tm, clean, box, rrect, rrect_cs, rrect_taper, extrude_x, extrude_negy
from params10 import *
from phone10 import phone_in_case

REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
BASE = os.path.join(REPO, "pixel-9-pro")
OUT  = os.path.join(ROOT_DEFAULT, "pixel10_case"); os.makedirs(OUT, exist_ok=True)
def load(n):
    m = trimesh.load(os.path.join(BASE, n + ".stl")); m.merge_vertices(); return to_mf(m)
def save(man, name):
    t = to_tm(clean(man))
    assert t.is_watertight and len(t.split(only_watertight=False)) == 1, name
    t.export(os.path.join(OUT, name))
    print(f"  wrote {name:36s} tris={len(t.faces):6d} bbox={np.round(t.bounds,2).tolist()}")
    return t
def grow(man, d):
    g = man
    for v in [(d,0,0),(-d,0,0),(0,d,0),(0,-d,0),(0,0,d),(0,0,-d)]:
        g = g + man.translate(list(v))
    return g

phone = phone_in_case()
phone.export(os.path.join(OUT, "_phone10_in_case.stl"))
PH = to_mf(phone)
print("phone in case:", np.round(phone.bounds, 2).tolist())

# ================================================================== CASE ======
C = load("case_pixel9pro")

# ---- fills (restore solid wherever the 9 Pro features no longer line up) ----
# camera shelf, grown for the longer/wider bar.  Filling over the old opening is fine:
# the new opening and channel below are supersets of the old ones.
# The MOLLE adapter's arms sit just below x 97.4 under the back, which is why the 9 Pro's
# shelf stops at 97.49.  Keep that limit: grow the taper toward the bar, then clip it there,
# so the -X end goes vertical above z -5.2 and the outer rim stays 1.0 mm like the 9 Pro's.
C += rrect_taper(SHELF_X0+SHELF_TAPER, CASE_X1-SHELF_TAPER,
                 SHELF_Y0+SHELF_TAPER, SHELF_Y1-SHELF_TAPER, 6.0,
                 SHELF_Z, Z_BACK_WIN, SHELF_TAPER) ^ box(SHELF_X_LIMIT, 500, -500, 500, -50, 50)
# button wall between the mount groove and the pocket
C += box(52.0, 97.2, Y_GRV_N, POCK_Y0, 0.30, 6.60)
# bottom wall (plus the 0.6 mm the 9 Pro port cutters bit into the pocket side)
C += box(WALL_X0, WALL_X1+0.6, -53.0, 8.0, 0.05, 9.60)

# ---- pocket: 0.1 mm taller, tighter corners, squared entry through the top-cap socket
pock = rrect_cs(POCK_X0, POCK_X1, POCK_Y0, POCK_Y1, POCK_R) + \
       m3.CrossSection.square([POCK_R+1.0, POCK_Y1-POCK_Y0]).translate([POCK_X1-POCK_R-1.0, POCK_Y0])
C -= m3.Manifold.extrude(pock, POCK_Z1-POCK_Z0).translate([0,0,POCK_Z0])
C -= box(POCK_X1-0.01, ENTRY_X1, POCK_Y0, POCK_Y1, POCK_Z0, POCK_Z1)

# ---- camera: slide channel + opening
C -= box(CHAN_X0, ENTRY_X1, CO_Y0, CO_Y1, CHAN_Z, POCK_Z0+0.01)
C -= rrect(CO_X0, CO_X1, CO_Y0, CO_Y1, CO_R, -12.0, POCK_Z0+0.05)

# ---- buttons
C -= box(VOL_X0-1.5, POCK_X1, Y_RELIEF, POCK_Y0+0.01, Z_RELIEF0, Z_RELIEF1)
VOL_GAP = 3.0
BUTTONS = {
 "volume": dict(rec=(VOL_X0-REC_MX, VOL_X1+REC_MX),
                win=[(VOL_X0-WIN_MX, VOL_MID-VOL_GAP/2), (VOL_MID+VOL_GAP/2, VOL_X1+WIN_MX)]),
 "power":  dict(rec=(PWR_X0-REC_MX, PWR_X1+REC_MX), win=[(PWR_X0-WIN_MX, PWR_X1+WIN_MX)]),
}
RZ0, RZ1 = BTN_Z0-REC_MZ, BTN_Z1+REC_MZ
WZ0, WZ1 = BTN_Z0-WIN_MZ, BTN_Z1+WIN_MZ
for b in BUTTONS.values():
    C -= extrude_negy(rrect_cs(b["rec"][0], b["rec"][1], RZ0, RZ1, 1.0), POCK_Y0+2.0, Y_RECESS)
    for wx0, wx1 in b["win"]:
        C -= extrude_negy(rrect_cs(wx0, wx1, WZ0, WZ1, 0.8), Y_RECESS+0.01, Y_RAIL_N-0.10)

# ---- bottom-end ports (cut oversize, like the 9 Pro)
def port(y0, y1, z0, z1, r):
    return extrude_x(rrect_cs(y0, y1, z0, z1, r), WALL_X0-0.6, WALL_X1+0.6)
for g in (GRL_A, GRL_B):
    C -= port(g[0]-1.50, g[1]+1.50, GRL_Z[0]-0.80, GRL_Z[1]+0.80, 1.30)   # speaker grilles
C -= port(-21.02-7.50, -21.02+7.50, 0.05, 6.10, 1.50)                   # USB-C (generous)
case_t = save(C, "case_pixel10.stl")
CASE = to_mf(case_t)

# ================================================================ TOP CAP =====
tc = load("top_cap_pixel9pro")            # already carries the 9 Pro trench tongue
trench_h = POCK_Z0 - CHAN_Z
reach = float(np.clip(4.0*trench_h, 5.0, 16.0))
x0 = max(CO_X1 + 0.6, CASE_X1 - (CASE_X1 - POCK_X1) - reach)
blank = box(x0, CASE_X1, CO_Y0, CO_Y1, CHAN_Z, POCK_Z0 + 0.20)
tongue = blank - grow(CASE, 0.20) - grow(PH, 0.20)
old_tc = tc
tc = (tc + tongue) - grow(PH, 0.15)       # widen it for the wider channel; never touch the phone
worst_add = 0.0
for dx in np.arange(0, 26, 0.5):
    a = (old_tc.translate([float(dx),0,0]) ^ CASE).volume()
    b = (tc.translate([float(dx),0,0])     ^ CASE).volume()
    worst_add = max(worst_add, b - a)
print(f"  top-cap tongue: extra interference over a 26 mm withdrawal {worst_add:+.4f} mm^3")
save(tc, "top_cap_pixel10.stl")

# ============================================================ BOTTOM CAPS =====
def slot_row(y0, y1, n, z0, z1, gap=1.0):
    w = ((y1-y0)-(n-1)*gap)/n
    return [(y0+i*(w+gap), y0+i*(w+gap)+w, z0, z1, min(0.8, w/2-0.01, (z1-z0)/2-0.01)) for i in range(n)]
CAP_HOLES = []
for g in (GRL_A, GRL_B):
    CAP_HOLES += slot_row(g[0]-0.6, g[1]+0.6, 4, GRL_Z[0]-0.55, GRL_Z[1]+0.55)
def recap(man, x0, x1):
    man += box(x0, x1, -53.0, 7.0, 1.30, 8.70)          # close the 9 Pro's holes
    for (y0,y1,z0,z1,r) in CAP_HOLES:
        man -= extrude_x(rrect_cs(y0, y1, z0, z1, r), x0-0.5, x1+0.5)
    return man
bc = recap(load("bottom_cap_pixel9pro"), CAP_P0, CAP_P1)
save(bc, "bottom_cap_pixel10.stl")

U0, U1 = CAP_P0-USB_OFFSET, CAP_P1-USB_OFFSET           # cable cap is exported 38.42 mm off
uc = recap(load("bottom_cap_for_usb_cable_pixel9pro"), U0, U1)
uc -= extrude_x(rrect_cs(-27.60, -14.40, 0.80, 7.55, 0.5), -61.95-DX-0.5, U1+0.5)   # cable window
save(uc, "bottom_cap_for_usb_cable_pixel10.stl")

# ==================================================== CAMERA PROTECTOR CAP ====
def shelf(g):                             # the case's shelf (clipped at the adapter limit), grown by g
    return rrect_taper(SHELF_X0+SHELF_TAPER-g, CASE_X1-SHELF_TAPER+g,
                       SHELF_Y0+SHELF_TAPER-g, SHELF_Y1-SHELF_TAPER+g, 4.0+g,
                       SHELF_Z, Z_BACK_WIN, SHELF_TAPER) ^ box(SHELF_X_LIMIT-g, 500, -500, 500, -50, 50)
WALL, FLOOR, CLR = 1.30, 1.40, 0.12
def skirt(g, z0):
    return rrect(SHELF_X0+SHELF_TAPER-g, CASE_X1-SHELF_TAPER+g,
                 SHELF_Y0+SHELF_TAPER-g, SHELF_Y1-SHELF_TAPER+g, 4.0+g, z0, SHELF_Z+0.001)
cavity = shelf(CLR) + skirt(CLR, SHELF_Z-25.0)
outer  = shelf(CLR+WALL) + skirt(CLR+WALL, SHELF_Z-FLOOR)
# trimmed flush with the case's +X end face, like the 9 Pro's
cap = (outer - cavity) ^ box(-500, CASE_X1, -500, 500, SHELF_Z-FLOOR, Z_BACK_WIN)
cap -= grow(CASE, 0.15)                   # let the rim sit on the real back profile
# the cap must also stay on while the case is clipped into the MOLLE adapter: the adapter's
# arms pass right beside the shelf's -X end (the 9 Pro cap overlaps them by 11.7 mm^3)
MOUNT = to_mf(trimesh.load(os.path.join(REPO, "shared-mount", "mount.stl")))
cap -= grow(MOUNT, 0.20)
for i in range(-5, 6):                    # grip ribs
    cap -= box(-500, 500, (SHELF_Y0+SHELF_Y1)/2 + i*4.2-0.6, (SHELF_Y0+SHELF_Y1)/2 + i*4.2+0.6,
               SHELF_Z-FLOOR-0.01, SHELF_Z-FLOOR+0.45)
save(cap, "camera_protector_cap_pixel10.stl")

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
b = BUTTONS["volume"]; save(insert(b["rec"], b["win"], thin=(VOL_MID-1.1, VOL_MID+1.1)), "volume_button_pixel10.stl")
b = BUTTONS["power"];  save(insert(b["rec"], b["win"]), "power_button_pixel10.stl")
print("done ->", OUT)
