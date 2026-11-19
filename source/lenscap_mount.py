"""Notch a lens cap around the MOLLE adapter's arms.

The adapter (shared-mount/mount.stl) has two flat arms, x < 97.34, z -5.55 .. -3.10, that lie
along the -X end of the case's camera shelf. A lens cap that wraps that end needs a gap there,
or it clashes with the arms when the case is clipped in.

clear_mount() does that with clean, full-depth cuts, never a thin offset skim:
  1. Over each arm, everything above the arm's underside (less CLR) is removed, from the
     rim down. The cap keeps its full-thickness wall below the arm.
  2. Anything still under the arm (x < arm end + CLR) is cut away all the way to the outer
     face. This keeps the cap clear while the case snaps in along Z with the cap on.
  3. If step 2 cut into the cap's outer ring, the ring segment is rebuilt just past the arm
     at full ring width. That segment is flat, under the shelf face, and clear of the case.
"""
import manifold3d as m3
from mf import to_mf, to_tm, box

CLR = 0.20          # clearance to the adapter, all round
MARGIN = 0.30       # extra length on each side of the arm (y)
RING_W = 1.30       # lens cap ring / wall width
EPS = 0.05

def _grow(man, d):
    g = man
    for v in [(d,0,0),(-d,0,0),(0,d,0),(0,-d,0),(0,0,d),(0,0,-d)]:
        g = g + man.translate(list(v))
    return g

def arm_bands(cap, mount):
    """[(y0, y1, x_end, z_under)] for each adapter arm the cap runs into, seated or while the
    case snaps in along Z. The y extent comes from the real contact with the arm, whose inner
    end is chamfered and whose outer end runs under the cap's rounded corners."""
    arms = mount ^ box(90, 99.0, -80, 40, -6.5, -2.9)
    g = _grow(arms, CLR)
    swept = g
    for dz in [0.25 * i for i in range(1, 49)]:           # the cap rises past the arm by 12 mm
        swept = swept + g.translate([0, 0, -dz])
    hit = to_tm(cap ^ swept)
    out = []
    for p in hit.split(only_watertight=False):
        if abs(p.volume) < 1e-3:
            continue
        a = to_tm(arms ^ box(90, 99, p.bounds[0][1] - 1, p.bounds[1][1] + 1, -50, 50)).bounds
        out.append((p.bounds[0][1] - MARGIN, p.bounds[1][1] + MARGIN, a[1][0] + CLR, a[0][2] - CLR))
    return sorted(out)

def clear_mount(cap, case, mount):
    zmin = to_tm(cap).bounds[0][2]
    for y0, y1, xe, zu in arm_bands(cap, mount):
        cap -= box(80, 100.5, y0, y1, zu, 5)              # 1. notch from the rim down
        under = cap ^ box(80, xe, y0, y1, -50, zu)
        if under.volume() > 1e-3:                         # 2. + 3.
            zt = to_tm(under).bounds[1][2]
            # overlap the cuts by EPS: cuts that only touch leave zero-thickness faces,
            # which merge back into stray material once the mesh is cleaned
            cap -= box(80, xe, y0, y1, -50, zu + EPS)
            cap += box(xe - EPS, xe + RING_W, y0, y1, zmin, zt) - case
    return cap
