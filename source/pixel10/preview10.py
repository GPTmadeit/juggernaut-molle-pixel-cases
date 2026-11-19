import os
ROOT_DEFAULT = os.environ.get("JUGG_ROOT",
    os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "work")))
"""Preview images for the Pixel 10 kit: a sectioned drawing and shaded 3D views."""
import numpy as np, trimesh, sys, warnings
warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, ".."))
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch
from matplotlib.path import Path
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from params10 import *
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT  = os.path.join(ROOT_DEFAULT, "pixel10_case")
PREV = os.path.join(REPO, "pixel-10", "preview"); os.makedirs(PREV, exist_ok=True)
def L(n):
    p = n if os.path.isabs(n) else os.path.join(OUT, n)
    m = trimesh.load(p); m.merge_vertices(); return m
case = L("case_pixel10.stl"); mount = L(os.path.join(REPO, "shared-mount", "mount.stl"))
FILL, EDGE, CUT = "#8fb2dc", "#1d2a3a", "#c0392b"

def section(mesh, origin, normal, T):
    s = mesh.section(plane_origin=origin, plane_normal=normal)
    p, _ = s.to_2D(to_2D=T); return p.polygons_full
def draw(ax, polys, fill=FILL, edge=EDGE, holes_red=True, lw=0.8):
    for pg in polys:
        verts, codes = [], []
        for ring in [pg.exterior] + list(pg.interiors):
            c = np.asarray(ring.coords); verts += c.tolist()
            codes += [Path.MOVETO] + [Path.LINETO]*(len(c)-2) + [Path.CLOSEPOLY]
        ax.add_patch(PathPatch(Path(verts, codes), fc=fill, ec=edge, lw=lw))
        if holes_red:
            for ring in pg.interiors:
                c = np.asarray(ring.coords); ax.plot(c[:,0], c[:,1], color=CUT, lw=0.8)
    ax.set_aspect("equal"); ax.autoscale_view(); ax.grid(alpha=0.25); ax.tick_params(labelsize=8)

TXY = np.eye(4)
TXZ = np.array([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]], float)
TYZ = np.array([[0,1,0,0],[0,0,1,0],[1,0,0,0],[0,0,0,1]], float)
fig = plt.figure(figsize=(18, 12.5))
gs = fig.add_gridspec(3, 2, height_ratios=[2.1, 1.0, 1.0])
ax = fig.add_subplot(gs[0, :])
draw(ax, section(case, [0,0,-1.6], [0,0,1], TXY))
ax.set_title("BACK of the Pixel 10 case, slice at z = -1.6 mm (through the back plate)")
ax.text(-20, -21, "port\nwall", ha="center", va="center", fontsize=9)
ax.text(45, -21, f"pocket {POCK_X1-POCK_X0:.1f} x {POCK_Y1-POCK_Y0:.1f} x {POCK_Z1-POCK_Z0:.1f} mm\n"
        f"for Pixel 10 152.8 x 72.0 x 8.6", ha="center", va="center", fontsize=9)
ax.text((CO_X0+CO_X1)/2, -21, f"camera opening {CO_X1-CO_X0:.1f} x {CO_Y1-CO_Y0:.1f} mm\n"
        f"(bar 22.9 x 65.0 + 0.7 clr)\nbar stands {BAR_PROUD:.2f} mm proud", ha="center", va="center", fontsize=9)
ax.set_xlim(-30, 150)

ax = fig.add_subplot(gs[1, :])
draw(ax, section(case, [0,-59.0,0], [0,1,0], TXZ))
ax.set_title("BUTTON WALL at y = -59.0 mm  (volume + power on the Pixel 10's right edge)")
ax.text((VOL_X0+VOL_X1)/2, 10.5, f"volume rocker\n{VOL_X0:.1f} - {VOL_X1:.1f}", ha="center", fontsize=9)
ax.text((PWR_X0+PWR_X1)/2, 10.5, f"power\n{PWR_X0:.1f} - {PWR_X1:.1f}", ha="center", fontsize=9)

ax = fig.add_subplot(gs[2, 0])
draw(ax, section(case, [-17.3,0,0], [1,0,0], TYZ))
ax.set_title("BOTTOM EDGE at x = -17.3 mm (ports)")
for (y0, y1), lab in [(GRL_A, "speaker"), (USB_Y, "USB-C"), (GRL_B, "speaker")]:
    ax.text((y0+y1)/2, 8.5, lab, ha="center", fontsize=9)

ax = fig.add_subplot(gs[2, 1])
draw(ax, section(case, [45,0,0], [1,0,0], TYZ))
for pg in section(mount, [45,0,0], [1,0,0], TYZ):
    c = np.asarray(pg.exterior.coords); ax.plot(c[:,0], c[:,1], color=CUT, lw=1.0)
ax.set_xlim(-68, 24); ax.set_ylim(-7, 14)
ax.set_title("MOUNT INTERFACE at x = 45 mm  (red = original mount.stl, untouched)")
ax.text(-35, 7, "rail + z=1.00 snap ledge\nidentical to the original", fontsize=9)
fig.tight_layout(); fig.savefig(os.path.join(PREV, "P10_drawing.png"), dpi=100); plt.close(fig)

# ---------------------------------------------------------------- 3D views ----
def render(parts, fname, title, elev, azim, W=1500, H=1000):
    """Orthographic z-buffer rasteriser (no depth-sort artefacts), flat-shaded, headless."""
    e, a = np.radians(elev), np.radians(azim)
    view = np.array([np.cos(e)*np.cos(a), np.cos(e)*np.sin(a), np.sin(e)])   # toward the camera
    up0 = np.array([0, 0, 1.0]) if abs(view[2]) < 0.95 else np.array([0, 1.0, 0])
    right = np.cross(up0, view); right /= np.linalg.norm(right); up = np.cross(view, right)
    R = np.stack([right, up, view])
    allv = np.vstack([m.vertices for m, _, _ in parts]) @ R.T
    lo, hi = allv.min(0), allv.max(0)
    s = 0.88*min(W/(hi[0]-lo[0]), H/(hi[1]-lo[1])); off = np.array([W/2, H/2]) - s*(lo[:2]+hi[:2])/2
    zbuf = np.full((H, W), -np.inf); img = np.ones((H, W, 3))
    light = R.T @ np.array([-0.35, 0.55, 0.75]); light /= np.linalg.norm(light)
    for m, col, alpha in parts:
        v = m.vertices @ R.T; p = v[:, :2]*s + off; z = v[:, 2]
        n = m.face_normals; ndv = n @ view
        sh = 0.30 + 0.70*np.abs(n @ light)
        for f, k, ff in zip(m.faces, sh, ndv):
            P = p[f]; Z = z[f]
            x0, y0 = np.floor(P.min(0)).astype(int); x1, y1 = np.ceil(P.max(0)).astype(int)
            x0, y0 = max(x0, 0), max(y0, 0); x1, y1 = min(x1, W-1), min(y1, H-1)
            if x1 < x0 or y1 < y0: continue
            xs, ys = np.meshgrid(np.arange(x0, x1+1)+0.5, np.arange(y0, y1+1)+0.5)
            (ax_, ay), (bx, by), (cx, cy) = P
            d = (by-cy)*(ax_-cx) + (cx-bx)*(ay-cy)
            if abs(d) < 1e-12: continue
            w0 = ((by-cy)*(xs-cx) + (cx-bx)*(ys-cy))/d
            w1 = ((cy-ay)*(xs-cx) + (ax_-cx)*(ys-cy))/d; w2 = 1-w0-w1
            inside = (w0 >= -1e-6) & (w1 >= -1e-6) & (w2 >= -1e-6)
            if not inside.any(): continue
            zz = w0*Z[0] + w1*Z[1] + w2*Z[2]
            sub = zbuf[y0:y1+1, x0:x1+1]; upd = inside & (zz > sub)
            sub[upd] = zz[upd]
            img[y0:y1+1, x0:x1+1][upd] = np.clip(np.array(col)*k*(1.0 if ff > 0 else 0.8), 0, 1)
    fig = plt.figure(figsize=(W/100, H/100+0.4), dpi=100)
    ax = fig.add_axes([0, 0, 1, H/(H+40)]); ax.imshow(img[::-1]); ax.set_axis_off()
    fig.suptitle(title, y=0.995, fontsize=12)
    fig.savefig(os.path.join(PREV, fname), dpi=100); plt.close(fig)
    print("  rendered", fname)

DARK, ORANGE, RED, GREEN, BLUE, GREY = (0.16,0.18,0.20),(0.85,0.45,0.10),(0.80,0.15,0.15),(0.20,0.60,0.35),(0.20,0.40,0.75),(0.72,0.74,0.78)
phone = L("_phone10_in_case.stl")
render([(case, (0.35,0.38,0.42), 1)], "P10_case_front.png", "Pixel 10 case - front (screen side)", 55, -60)
render([(case, (0.35,0.38,0.42), 1)], "P10_case_back.png", "Pixel 10 case - back, camera shelf", -50, -60)
render([(case, (0.35,0.38,0.42), 1), (phone, GREY, 1)], "P10_case_phone.png", "Pixel 10 seated in the case", 55, -60)
render([(case, (0.35,0.38,0.42), 1), (mount, BLUE, 1)], "P10_case_mount.png", "Pixel 10 case on the unmodified MOLLE adapter", -40, -50)
parts = [(case, DARK, 1), (L("top_cap_pixel10.stl"), ORANGE, 1), (L("bottom_cap_pixel10.stl"), ORANGE, 1),
         (L("volume_button_pixel10.stl"), RED, 1), (L("power_button_pixel10.stl"), RED, 1),
         (L("camera_protector_cap_pixel10.stl"), GREEN, 1), (mount, BLUE, 1), (phone, GREY, 1)]
render(parts, "P10_assembly.png", "Pixel 10 - fully assembled, 8 coloured parts", -35, -55)
print("previews ->", PREV)
