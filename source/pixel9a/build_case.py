import os
ROOT_DEFAULT = os.environ.get("JUGG_ROOT",
    os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "work")))
import numpy as np, trimesh, os, sys, warnings
warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import manifold3d as m3
from mf import (to_mf, to_tm, clean, box, rrect, rrect_cs, rrect_taper, stats,
                extrude_x, extrude_negy, extrude_posy)
from params import *
from shapely.geometry.polygon import orient

ROOT = ROOT_DEFAULT
SRC  = os.path.join(ROOT, "jugg_case", "msenturk115", "juggernaut-tactical-molle-phone-case")
OUT  = os.path.join(ROOT, "pixel9a_case")
os.makedirs(OUT, exist_ok=True)

def load(n):
    m = trimesh.load(os.path.join(SRC, n + ".stl")); m.merge_vertices(); return m

# ============================================================ 1. STRETCH ======
def stretch_x(tm, x_split, dx):
    T = np.array([[0,1,0,0],[0,0,1,0],[1,0,0,-x_split],[0,0,0,1]], float)
    sec = tm.section(plane_origin=[x_split,0,0], plane_normal=[1,0,0])
    p2,_ = sec.to_planar(to_2D=T)
    rings = []
    for poly in p2.polygons_full:
        poly = orient(poly, 1.0)
        rings.append(np.asarray(poly.exterior.coords)[:-1])
        for it in poly.interiors:
            rings.append(np.asarray(it.coords)[:-1])
    cs = m3.CrossSection(rings, m3.FillRule.EvenOdd)
    print(f"   bridge: {len(rings)} ring(s), area {cs.area():.2f} mm2 -> inserting {2*dx:.1f} mm")
    bridge = extrude_x(cs, x_split-dx, x_split+dx)
    body = to_mf(tm); b = tm.bounds; pad = 25.0
    left  = (body ^ box(b[0][0]-pad, x_split,    b[0][1]-pad, b[1][1]+pad, b[0][2]-pad, b[1][2]+pad)).translate([-dx,0,0])
    right = (body ^ box(x_split,     b[1][0]+pad, b[0][1]-pad, b[1][1]+pad, b[0][2]-pad, b[1][2]+pad)).translate([ dx,0,0])
    return left + bridge + right

case = load("case")
print("original case bounds:", np.round(case.bounds,2).tolist())
C = stretch_x(case, X_SPLIT, DX);                    stats(C, "1 stretched")

# =============================== 2. RESTORE THE MOUNT GROOVE (trim the rib) ===
for y0, y1 in [(Y_RAIL_N, Y_GRV_N), (Y_GRV_P, Y_RAIL_P)]:
    yy0, yy1 = (y0-0.6, y1) if y0 < 0 else (y0, y1+0.6)
    C -= box(RIB_X0-DX-0.01, RIB_X0,        yy0, yy1, Z_GRV0, Z_GRV1)
    C -= box(RIB_X1,         RIB_X1+DX+0.01, yy0, yy1, Z_GRV0, Z_GRV1)
stats(C, "2 rib trimmed to mount gap")

# ============================================ 3. ERASE THE OLD S8 CAMERA ======
cf = (98.5, 128.5, -44.5, 5.5)
C -= box(cf[0], cf[1], cf[2], cf[3], -9.0, Z_BACK_WIN)
C += box(cf[0], cf[1], cf[2], cf[3], Z_BACK_WIN, POCK_Z0);   stats(C, "3 old camera erased")

# ======================================= 4. ERASE THE OLD S8 BUTTON HOLES =====
C += box(77.40,  94.20, Y_RAIL_N, POCK_Y1,  2.30, 8.70)
C += box(88.40, 115.20, POCK_Y0,  Y_RAIL_P, 2.30, 8.70)
C -= box(76.90,  94.70, Y_RAIL_N, Y_GRV_N,  Z_GRV0, Z_GRV1)
C -= box(87.90, 115.70, Y_GRV_P,  Y_RAIL_P, Z_GRV0, Z_GRV1); stats(C, "4 old buttons erased")

# ========================================= 5. ERASE THE OLD S8 PORT HOLES =====
C += box(WALL_X0, WALL_X1, -50.0, 6.0, 0.40, 9.60); stats(C, "5 old ports erased")

# ============================================== 6. NEW POCKET + LIP ==========
# the +X end of the pocket is squared off so the phone can be slid straight in
# once the top cap is removed; the -X end keeps the phone's own 12 mm corner radius.
pock_cs = rrect_cs(POCK_X0, POCK_X1, POCK_Y0, POCK_Y1, POCK_R) +           m3.CrossSection.square([POCK_R+1.0, POCK_Y1-POCK_Y0]).translate([POCK_X1-POCK_R-1.0, POCK_Y0])
# fill the whole pocket envelope solid first (removes the old S8 pocket's corner
# slivers, which sit outside the new, larger 12.5 mm corner radius) ...
C += box(POCK_X0, POCK_X1, POCK_Y0, POCK_Y1, POCK_Z0, LIP_FILL_Z)
# ... then cut the real pocket back out of it
C -= m3.Manifold.extrude(pock_cs, POCK_Z1-POCK_Z0).translate([0,0,POCK_Z0])
# carry the pocket profile straight out through the top-cap socket so the phone
# (camera bar included) can be slid in once the top cap is removed
C -= box(POCK_X1-0.01, ENTRY_X1, POCK_Y0, POCK_Y1, POCK_Z0, POCK_Z1)
# the pocket's rounded -X corners are now solid, so re-open the two blind detent
# pockets the bottom cap's snap bumps drop into, and relieve the top cap's rail tips
for y0, y1 in [(-59.20, -57.00), (14.97, 17.20)]:
    C -= box(POCK_X0-0.01, -13.10, y0, y1, 3.00, 7.00)
for y0, y1 in [(-58.60, -57.40), (15.40, 16.60)]:
    C -= box(136.90, POCK_X1+0.01, y0, y1, 1.05, 8.95)
stats(C, "6 pocket")

# ================================================= 7. SCREEN OPENING =========
op = (OPEN_X0, OPEN_X1, OPEN_Y0, OPEN_Y1, OPEN_R)
C -= rrect(*op, POCK_Z1-0.001, 20.0)
C -= rrect_taper(*op, LIP_FILL_Z-CHAMF, LIP_FILL_Z+3.0, CHAMF+3.0); stats(C, "7 screen opening")

# ================================================ 8. CAMERA + HOOD ===========
C += rrect_taper(CO_X0-HOOD_FOOT, CO_X1+HOOD_FOOT, CO_Y0-HOOD_FOOT, CO_Y1+HOOD_FOOT,
                 CO_R+HOOD_FOOT, Z_HOOD, Z_BACK_WIN, HOOD_W-HOOD_FOOT)
C += box(BOSS_X0, BOSS_X1, CO_Y0-BOSS_PAD, CO_Y1+BOSS_PAD, Z_BACK_RAIL, Z_BACK_WIN)
C -= box(CHAN_X0, ENTRY_X1, CO_Y0, CO_Y1, CHAN_Z, POCK_Z0+0.01)
C -= rrect(CO_X0, CO_X1, CO_Y0, CO_Y1, CO_R, -9.0, POCK_Z0+0.05)
C -= box(CO_X0-6.0, CO_X1+6.0, WIN_EXT[0], WIN_EXT[1], Z_BACK_RAIL-0.05, Z_BACK_WIN)
stats(C, "8 camera")

# ====================================================== 9. BUTTONS ===========
C -= box(VOL_X0-1.5, POCK_X1, Y_RELIEF, POCK_Y0+0.01, Z_RELIEF0, Z_RELIEF1)

VOL_GAP = 3.0
BUTTONS = {
 "volume": dict(rec=(VOL_X0-REC_MX, VOL_X1+REC_MX),
                win=[(VOL_X0-WIN_MX, VOL_MID-VOL_GAP/2), (VOL_MID+VOL_GAP/2, VOL_X1+WIN_MX)]),
 "power":  dict(rec=(PWR_X0-REC_MX, PWR_X1+REC_MX),
                win=[(PWR_X0-WIN_MX, PWR_X1+WIN_MX)]),
}
RZ0, RZ1 = BTN_Z0-REC_MZ, BTN_Z1+REC_MZ
WZ0, WZ1 = BTN_Z0-WIN_MZ, BTN_Z1+WIN_MZ
for name, b in BUTTONS.items():
    C -= extrude_negy(rrect_cs(b["rec"][0], b["rec"][1], RZ0, RZ1, 1.0), POCK_Y0+2.0, Y_RECESS)
    for wx0, wx1 in b["win"]:
        C -= extrude_negy(rrect_cs(wx0, wx1, WZ0, WZ1, 0.8), Y_RECESS+0.01, Y_RAIL_N-0.10)
stats(C, "9 buttons")

# ================================================ 10. BOTTOM-END PORTS =======
def port(y0, y1, h, r):
    return extrude_x(rrect_cs(y0, y1, PORT_Z_MID-h/2, PORT_Z_MID+h/2, r), WALL_X0-0.6, WALL_X1+0.6)
C -= port(SPK_Y0-0.50, SPK_Y1+0.50, 3.20, 1.40)
C -= port(USB_Y0-2.45, MIC_Y1+0.45, 6.00, 1.50)
C -= port(LFT_Y0-0.25, LFT_Y1+0.25, 4.00, 1.40);              stats(C, "10 ports")

# ========================================================= 11. EXPORT ========
C = clean(C)
out = to_tm(C)
tri=out.triangles
_a=np.linalg.norm(np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]),axis=1)/2
print('   zero-area tris:', int((_a<1e-12).sum()))
print("FINAL case:", np.round(out.bounds,2).tolist(),
      "| watertight", out.is_watertight, "| tris", len(out.faces), "| vol", round(out.volume,1))
out.export(os.path.join(OUT, "case_pixel9a.stl"))
np.save(os.path.join(OUT, "_case_ok.npy"), np.array([1]))
print("wrote", os.path.join(OUT, "case_pixel9a.stl"))
