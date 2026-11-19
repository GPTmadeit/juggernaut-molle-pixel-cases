import os
ROOT_DEFAULT = os.environ.get("JUGG_ROOT",
    os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "work")))
"""Every fit check for the Pixel 10 kit, by boolean intersection.
Run against the build output (default) or the repo copy:  verify10_all.py [kit_dir]"""
import numpy as np, trimesh, sys, warnings
warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, ".."))
from mf import to_mf, to_tm, box
from params10 import *
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT  = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT_DEFAULT, "pixel10_case")
PHONE = os.path.join(ROOT_DEFAULT, "pixel10_case", "_phone10_in_case.stl")
def L(p):
    m = trimesh.load(p); m.merge_vertices(); return m
def P(n): return to_mf(L(os.path.join(OUT, n)))
CASE = P("case_pixel10.stl"); PH = to_mf(L(PHONE))
MT = to_mf(L(os.path.join(REPO, "shared-mount", "mount.stl")))
parts = {n: P(n+"_pixel10.stl") for n in ["top_cap","bottom_cap","bottom_cap_for_usb_cable",
                                         "camera_protector_cap","volume_button","power_button"]}
bad = []
def rep(a, b, lab, tol=0.5):
    v = (a ^ b).volume(); ok = v < tol
    print(f"  {lab:46s}{v:9.4f} mm^3  {'OK' if ok else '<-- CLASH'}")
    if not ok:
        bad.append(lab)
        for c in sorted(to_tm(a ^ b).split(only_watertight=False), key=lambda k: -abs(k.volume))[:4]:
            print("       ", np.round(c.bounds, 2).tolist(), round(abs(c.volume), 3))

print("=== interference ===")
rep(CASE, MT, "case x mount (MOLLE adapter)")
rep(CASE, PH, "case x Pixel 10 (seated)")
for n, p in parts.items():
    q = p.translate([USB_OFFSET,0,0]) if n == "bottom_cap_for_usb_cable" else p
    if n == "camera_protector_cap":
        rep(CASE, q, "case x camera_protector_cap (cap ON)"); continue
    rep(CASE, q, f"case x {n}"); rep(PH, q, f"phone x {n}")
for n in ["volume_button","power_button","camera_protector_cap"]:
    rep(MT, parts[n], f"mount x {n}")

# the case clips into the adapter along Z: with the lens cap on, the cap must clear the arms
# over the whole snap travel, not just when seated
lc = parts["camera_protector_cap"]
w = max(((lc.translate([0,0,float(dz)]) ^ MT).volume(), dz) for dz in np.arange(0, 12.01, 0.1))
ok = w[0] < 0.01; bad += [] if ok else ["lens cap snap-in"]
print(f"  {'mount x lens cap, case snapped in/out 0-12 mm':46s}{w[0]:9.4f} mm^3  {'OK' if ok else '<-- CLASH'}")

print("\n=== seated phone at the extremes of its clearance ===")
for dy, dz, lab in [(0.44,0,"+Y"),(-0.30,0,"-Y (relief limit)"),(0,0.29,"+Z lifted"),
                    (0.44,0.29,"+Y +Z"),(-0.30,0.29,"-Y +Z")]:
    rep(CASE, PH.translate([0,dy,dz]), f"seated, shifted {lab}")
for dx in (-0.55, 0.55):
    rep(CASE, PH.translate([dx,0,0]), f"seated, shifted X {dx:+.2f}")

print("\n=== insertion sweep (top cap off, phone slid in from the +X end, 2 mm steps) ===")
for dy, dz, lab in [(0,0,"centred"),(0.44,0,"+Y"),(-0.30,0,"-Y"),(0,0.29,"+Z"),(0.44,0.29,"+Y +Z")]:
    worst, wx = 0.0, 0
    for dx in np.arange(0, 170, 2.0):
        v = (CASE ^ PH.translate([float(dx), dy, dz])).volume()
        if v > worst: worst, wx = v, dx
    ok = worst < 0.5; bad += [] if ok else [f"sweep {lab}"]
    print(f"  {lab:12s} worst {worst:8.4f} mm^3 at +{wx:.0f} mm  {'OK' if ok else '<-- BLOCKED'}")

print("\n=== button plungers ===")
for n in ["volume_button","power_button"]:
    b = to_tm(parts[n]).bounds
    print(f"  {n:14s} flange face Y={b[1][1]:.3f}  button face Y={Y_BTN_FACE:.3f}  gap {abs(b[1][1]-Y_BTN_FACE):.3f}"
          f" | pad face Y={b[0][1]:.2f} (tab tip -61.10) | X {b[0][0]:.2f}..{b[1][0]:.2f}")

print("\n=== ports: open fraction looking in from outside, case + cap fitted ===")
bc = parts["bottom_cap"]; uc = parts["bottom_cap_for_usb_cable"].translate([USB_OFFSET,0,0])
feat = {"grille (-Y side)": (*GRL_A, *GRL_Z), "grille (+Y side)": (*GRL_B, *GRL_Z),
        "USB-C": (*USB_Y, *USB_Z)}
for capname, cap in [("case alone", None), ("bottom_cap", bc), ("bottom_cap_for_usb_cable", uc)]:
    print(f" {capname}:")
    for nm, (y0,y1,z0,z1) in feat.items():
        pr = box(-26.0-DX, WALL_X0-0.05 if cap is not None else WALL_X1+0.05, y0, y1, z0, z1)
        if cap is None: pr = box(WALL_X0-0.05, WALL_X1+0.05, y0, y1, z0, z1)
        solid = CASE if cap is None else CASE + cap
        fr = 1 - (solid ^ pr).volume()/pr.volume()
        need = 0.99 if (cap is None or nm == "USB-C" and capname.endswith("cable")) else 0.30
        if nm == "USB-C" and capname == "bottom_cap": need = 0.0       # the plain cap covers the port
        ok = fr >= need; bad += [] if ok else [f"{capname} {nm}"]
        print(f"    {nm:18s} open {100*fr:5.1f}%  {'OK' if ok else '<-- BLOCKED'}")
tc = parts["top_cap"]
pr = box(POCK_X1-0.05, 145.0, TOPMIC_Y[0], TOPMIC_Y[1], Zc(4.94), Zc(3.65))
print(f" top_cap over the top mic: open {100*(1-((CASE+tc)^pr).volume()/pr.volume()):5.1f}%")
# the camera: nothing may sit over the bar's footprint, case or lens cap off
# the bar's real outline (a pill), shrunk 0.3 mm, extruded straight out through the back
import manifold3d as m3
sec = to_tm(PH ^ box(-50, 200, -100, 100, -3.0, -1.5)).section(plane_origin=[0,0,-2.0], plane_normal=[0,0,1])
pg, _ = sec.to_2D(to_2D=np.eye(4))
rings = [np.asarray(p.exterior.coords)[:-1] for p in pg.polygons_full]
pr = m3.Manifold.extrude(m3.CrossSection(rings).offset(-0.3, m3.JoinType.Round), 12.0).translate([0,0,-12.0-0.95])
v = (CASE ^ pr).volume(); print(f" camera bar outline extruded through the back vs case: {v:.4f} mm^3  {'OK' if v<0.01 else '<-- BLOCKED'}")
if v >= 0.01: bad.append("camera")

print("\n=== all STLs ===")
for f in sorted(os.listdir(OUT)):
    if not f.endswith(".stl") or f.startswith("_"): continue
    m = L(os.path.join(OUT, f)); b = m.bounds
    nb = len(m.split(only_watertight=False))
    if not (m.is_watertight and nb == 1): bad.append(f)
    print(f"  {f:40s} tris={len(m.faces):6d} bodies={nb} watertight={m.is_watertight} "
          f"size={np.round(b[1]-b[0],2).tolist()}")
print("\nALL CHECKS PASS" if not bad else f"\nFAILED: {bad}")
sys.exit(1 if bad else 0)
