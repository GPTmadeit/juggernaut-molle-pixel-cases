import os
ROOT_DEFAULT = os.environ.get("JUGG_ROOT",
    os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "work")))
"""Regression test for the charging port.

1. the USB cable window must stay ONE opening (a wide erase block once split it with a bar)
2. measure the actual clear aperture a plug can drive through -- cap + case together --
   all the way to the phone's USB-C port.
"""
import numpy as np, trimesh, os, sys, importlib, warnings
warnings.filterwarnings("ignore"); sys.path.insert(0,'.')
from mf import to_mf, box
ROOT=ROOT_DEFAULT
def L(p):
    m=trimesh.load(p); m.merge_vertices(); return m
Tyz=np.array([[0,1,0,0],[0,0,1,0],[1,0,0,0],[0,0,0,1]],float)
WIN_Y0, WIN_Y1 = -26.57, -15.47          # the stock cable window's Y span

def window_blocked(mesh, x0, x1):
    """Any material inside the intended cable window? A stray fill block once left a
    3.4 mm bar right across it, so check the volume directly rather than counting holes
    (the window is now open at the bottom, so it is no longer a closed interior loop)."""
    return (to_mf(mesh) ^ box(x0, x1, -26.5, -15.5, 1.05, 7.30)).volume()

def clear(solid, zc, w, h, x_from, x_to):
    """Can a w x h plug sweep from x_from to x_to without hitting anything?"""
    worst=0.0
    for dx in np.arange(0, x_to-x_from+0.01, 0.5):
        plug = box(x_from-16.0+dx, x_from+dx, -21.02-w/2, -21.02+w/2, zc-h/2, zc+h/2)
        worst=max(worst,(solid ^ plug).volume())
        if worst>0.01: break
    return worst<0.01

ok=True
for tag,d,pmod,DXv in [("9pro","pixel9pro_case","params9p",1.75),
                       ("9a","pixel9a_case","params",2.70),
                       ("6a","pixel6a_case","params6a",1.45)]:
    P=importlib.import_module(pmod); D=os.path.join(ROOT,d)
    uc=L(os.path.join(D,f"bottom_cap_for_usb_cable_pixel{tag}.stl"))
    blocked = window_blocked(uc, -63.0-DXv, -55.0-DXv)
    print(f"=== Pixel {tag} ===")
    print(f"   obstruction inside the cable window: {blocked:8.3f} mm^3   {'OK' if blocked<0.5 else '<-- BLOCKED'}")
    ok &= blocked<0.5
    solid = to_mf(uc).translate([38.42,0,0]) + to_mf(L(os.path.join(D,f"case_pixel{tag}.stl")))
    zc = getattr(P,"PORT_Z_MID", None)
    if zc is None: zc = (P.USB_Z0+P.USB_Z1)/2
    x_from, x_to = P.WALL_X0-3.0, P.WALL_X1+0.2
    best=None
    for hh in np.arange(7.5, 2.9, -0.25):
        for ww in np.arange(16.0, 7.9, -0.5):
            if clear(solid, zc, ww, hh, x_from, x_to):
                best=(ww,hh); break
        if best: break
    print(f"   clear aperture to the port (cap + case): {best[0]:.1f} x {best[1]:.2f} mm"
          f"   [USB-C plug shell is 8.3 x 2.6; typical overmould ~10-12 x 5-6.5]")
    ok &= best is not None and best[1] >= 3.5
print("\nPORTS ALL CLEAR" if ok else "\nSOMETHING IS BLOCKED")
