"""v1.1.1: notch the Pixel 9 Pro lens cap around the MOLLE adapter's arms.

The v1.0.0 cap's -X wall ran straight through the adapter's two arms (11.7 mm^3), so it could
not stay on while the case was clipped into the adapter. The 9 Pro build inputs are no longer
around, so this edits the committed STL in place with the same clear_mount() the Pixel 10
build uses (source/lenscap_mount.py). Re-running it changes nothing once the cap is clear.

    python source/pixel9pro/fix_lenscap_mount9p.py
"""
import os, sys, numpy as np, trimesh
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from mf import to_mf, to_tm, clean
from lenscap_mount import clear_mount, arm_bands
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
KIT = os.path.join(REPO, "pixel-9-pro")
CAP = os.path.join(KIT, "camera_protector_cap_pixel9pro.stl")

def L(p):
    m = trimesh.load(p); m.merge_vertices(); return to_mf(m)

cap, case = L(CAP), L(os.path.join(KIT, "case_pixel9pro.stl"))
mount = L(os.path.join(REPO, "shared-mount", "mount.stl"))
if not arm_bands(cap, mount):
    sys.exit("lens cap already clears the adapter, nothing to do")
before = (cap ^ mount).volume()
new = clear_mount(cap, case, mount)
snap = max((new.translate([0, 0, dz]) ^ mount).volume() for dz in np.arange(0, 12.01, 0.1))
t = to_tm(clean(new)); t.merge_vertices()
assert t.is_watertight and len(t.split(only_watertight=False)) == 1
assert (new ^ case).volume() < 0.01 and snap < 0.01
print(f"cap x mount {before:.3f} -> {(new ^ mount).volume():.3f} mm^3, snap-in worst {snap:.4f}, "
      f"cap x case {(new ^ case).volume():.4f}, volume {cap.volume():.1f} -> {new.volume():.1f} mm^3")
t.export(CAP)
