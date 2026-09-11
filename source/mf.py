"""Helpers: trimesh <-> manifold3d, and primitive builders."""
import numpy as np, trimesh, manifold3d as m3

m3.set_circular_segments(96)

def to_mf(mesh):
    mesh = mesh.copy(); mesh.merge_vertices()
    v = np.asarray(mesh.vertices, dtype=np.float64)
    f = np.asarray(mesh.faces, dtype=np.uint32)
    try:
        return m3.Manifold(m3.Mesh64(v, f))
    except Exception:
        return m3.Manifold(m3.Mesh(v.astype(np.float32), f))

def clean(man, tol=1e-4):
    """Rebuild through the Manifold constructor (collapses degenerate triangles), then
    drop redundant verts, so the exported STL survives a float32 round trip."""
    return to_mf(to_tm(man)).simplify(tol)

def to_tm(man):
    msh = man.to_mesh()
    v = np.asarray(msh.vert_properties)[:, :3].astype(np.float64)
    f = np.asarray(msh.tri_verts).astype(np.int64)
    return trimesh.Trimesh(vertices=v, faces=f, process=False)

def box(x0, x1, y0, y1, z0, z1):
    return m3.Manifold.cube([x1-x0, y1-y0, z1-z0]).translate([x0, y0, z0])

def rrect_cs(x0, x1, y0, y1, r):
    """Rounded-rectangle CrossSection."""
    r = max(0.0, min(r, (x1-x0)/2 - 1e-6, (y1-y0)/2 - 1e-6))
    cs = m3.CrossSection.square([x1-x0-2*r, y1-y0-2*r]).translate([x0+r, y0+r])
    if r > 1e-9:
        cs = cs.offset(r, m3.JoinType.Round, 2.0, 128)
    return cs

def rrect(x0, x1, y0, y1, r, z0, z1):
    return m3.Manifold.extrude(rrect_cs(x0, x1, y0, y1, r), z1-z0).translate([0, 0, z0])

def rrect_taper(x0, x1, y0, y1, r, z0, z1, grow_top):
    """Rounded rect prism whose top is `grow_top` mm larger on every side."""
    w, h = x1-x0, y1-y0
    sx, sy = (w+2*grow_top)/w, (h+2*grow_top)/h
    cs = rrect_cs(x0, x1, y0, y1, r)
    cx, cy = (x0+x1)/2, (y0+y1)/2
    cs = cs.translate([-cx, -cy])
    m = m3.Manifold.extrude(cs, z1-z0, 0, 0.0, (sx, sy))
    return m.translate([cx, cy, z0])

def cs_from_polygon(coords):
    return m3.CrossSection([np.asarray(coords, dtype=np.float64)], m3.FillRule.NonZero)

def prism_from_cs(cs, z0, z1):
    return m3.Manifold.extrude(cs, z1-z0).translate([0, 0, z0])

PROBE_X = None
def stats(man, name=""):
    extra = ""
    if PROBE_X is not None:
        import trimesh as _tm, numpy as _np
        t = to_tm(man)
        try:
            sec = t.section(plane_origin=[PROBE_X,0,0], plane_normal=[1,0,0])
            p2,_ = sec.to_planar(to_2D=_np.array([[0,1,0,0],[0,0,1,0],[1,0,0,0],[0,0,0,1]],float))
            extra = f"  area@x={PROBE_X}: {sum(p.area for p in p2.polygons_full):.1f}"
        except Exception as e:
            extra = f"  probe err {e}"
    print(f"   [{name}] tris={man.num_tri()} vol={man.volume():.1f} genus={man.genus()}{extra}")

def extrude_x(cs, x0, x1):
    """cs is drawn in (u,v)=(Y,Z); extrude it along +X from x0 to x1."""
    m = m3.Manifold.extrude(cs, x1-x0)
    return m.transform(np.array([[0.,0.,1., x0],
                                 [1.,0.,0., 0.],
                                 [0.,1.,0., 0.]]))

def extrude_negy(cs, y_start, y_end):
    """cs is drawn in (u,v)=(X,Z); extrude it along -Y from y_start down to y_end."""
    m = m3.Manifold.extrude(cs, y_start-y_end)
    return m.transform(np.array([[1.,0., 0., 0.],
                                 [0.,0.,-1., y_start],
                                 [0.,1., 0., 0.]]))

def extrude_posy(cs, y_start, y_end):
    """cs is drawn in (u,v)=(X,Z); extrude it along +Y from y_start up to y_end."""
    m = m3.Manifold.extrude(cs, y_end-y_start)
    return m.transform(np.array([[1.,0.,0., 0.],
                                 [0.,0.,1., y_start],
                                 [0.,1.,0., 0.]]))
