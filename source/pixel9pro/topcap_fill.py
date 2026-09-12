import os
ROOT_DEFAULT = os.environ.get("JUGG_ROOT",
    os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "work")))
"""Close the slide-channel trench that sits under the top cap.

The camera-bump channel has to run out through the top-cap socket so the phone can be
slid in with the cap off.  Once the cap is back on, that leaves an open slot between the
cap's underside and the channel floor, open at the case's end face.  Fix it on the CAP,
not the case: give the cap a tongue that plugs the trench.

The tongue is shaped by boolean, not by hand: take the trench box, then subtract the case
and the phone each grown by CLR, so the tongue can never foul either one.
"""
import numpy as np, trimesh, os, sys, importlib, warnings
warnings.filterwarnings("ignore"); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import manifold3d as m3
from mf import to_mf, to_tm, clean, box

ROOT = ROOT_DEFAULT
CLR  = 0.20                       # sliding clearance around the tongue
KITS = [("9pro","pixel9pro_case","params9p","_phone9pro_in_case.stl"),
        ("9a",  "pixel9a_case",  "params",  "_phone9a_in_case.stl"),
        ("6a",  "pixel6a_case",  "params6a","_phone6a_in_case.stl")]

def L(p):
    m = trimesh.load(p); m.merge_vertices(); return m
def grow(man, d):
    g = man
    for v in [(d,0,0),(-d,0,0),(0,d,0),(0,-d,0),(0,0,d),(0,0,-d)]:
        g = g + man.translate(list(v))
    return g

for tag, d, pmod, phname in KITS:
    P = importlib.import_module(pmod)
    D = os.path.join(ROOT, d)
    case  = to_mf(L(os.path.join(D, f"case_pixel{tag}.stl")))
    phone = to_mf(L(os.path.join(D, phname)))
    capf  = os.path.join(D, f"top_cap_pixel{tag}.stl")
    cap   = to_mf(L(capf))

    trench_h = P.POCK_Z0 - P.CHAN_Z                     # how deep the channel is cut
    reach    = float(np.clip(4.0*trench_h, 5.0, 16.0))  # keep the tongue's aspect ratio sane
    x0 = max(P.CO_X1 + 0.6, P.CASE_X1 - (P.CASE_X1 - P.POCK_X1) - reach)
    blank = box(x0, P.CASE_X1, P.CO_Y0, P.CO_Y1, P.CHAN_Z, P.POCK_Z0 + 0.20)
    tongue = blank - grow(case, CLR) - grow(phone, CLR)
    newcap = clean(cap + tongue)

    t = to_tm(newcap)
    assert t.is_watertight and len(t.split(only_watertight=False)) == 1, f"{tag} cap not a single solid"
    # The stock cap snaps past a detent on the way in, so absolute interference during
    # withdrawal is expected.  What matters is that the tongue adds none of its own:
    # compare the new cap against the untouched one at every step.
    worst_add = 0.0
    for dx in np.arange(0, 26, 0.5):
        a = (cap.translate([float(dx),0,0])    ^ case).volume()
        b = (newcap.translate([float(dx),0,0]) ^ case).volume()
        worst_add = max(worst_add, b - a)
    seated  = (newcap ^ case).volume()
    wphone  = max((newcap.translate([float(dx),0,0]) ^ phone).volume() for dx in np.arange(0, 26, 0.5))
    print(f"Pixel {tag:5s} trench {trench_h:4.2f} mm  tongue {P.CASE_X1-x0:5.2f} mm long  "
          f"+{newcap.volume()-cap.volume():7.1f} mm^3")
    print(f"              seated {seated:7.4f}  extra interference from the tongue {worst_add:+7.4f}  "
          f"x phone {wphone:7.4f}  {'OK' if max(seated, worst_add, wphone) < 0.5 else '<-- PROBLEM'}")
    t.export(capf)
