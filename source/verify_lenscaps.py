"""Every kit's lens cap against the MOLLE adapter and its own case, straight from the repo.

  * seated: cap x mount and cap x case
  * snap-in: the case clips into the adapter along Z, so the cap (fitted to the case) is
    swept 0-12 mm away from the adapter in 0.1 mm steps and must never touch it
  * one watertight body

    python source/verify_lenscaps.py
"""
import os, sys, numpy as np, trimesh, warnings
warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from mf import to_mf
REPO = os.path.abspath(os.path.join(HERE, ".."))
def L(p):
    m = trimesh.load(p); m.merge_vertices(); return m
MT = to_mf(L(os.path.join(REPO, "shared-mount", "mount.stl")))
bad = []
for folder, tag in [("pixel-10", "pixel10"), ("pixel-9-pro", "pixel9pro"),
                    ("pixel-9a", "pixel9a"), ("pixel-6a", "pixel6a")]:
    d = os.path.join(REPO, folder)
    t = L(os.path.join(d, f"camera_protector_cap_{tag}.stl")); cap = to_mf(t)
    case = to_mf(L(os.path.join(d, f"case_{tag}.stl")))
    seat, cc = (cap ^ MT).volume(), (cap ^ case).volume()
    snap = max((cap.translate([0, 0, float(z)]) ^ MT).volume() for z in np.arange(0, 12.01, 0.1))
    one = t.is_watertight and len(t.split(only_watertight=False)) == 1
    ok = seat < 0.01 and cc < 0.01 and snap < 0.01 and one
    bad += [] if ok else [folder]
    print(f"  {folder:12s} cap x mount {seat:7.3f}  snap-in worst {snap:7.3f}  cap x case {cc:7.3f}"
          f"  one body {one}  {'OK' if ok else '<-- FAIL'}")
print("\nALL LENS CAPS PASS" if not bad else f"\nFAILED: {bad}")
sys.exit(1 if bad else 0)
