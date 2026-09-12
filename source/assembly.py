import os
ROOT_DEFAULT = os.environ.get("JUGG_ROOT",
    os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "work")))
"""Export a fully-assembled, per-part coloured model of each case kit.

Every part is written in the SAME (case/mount) coordinate frame, so:
  * separate STLs   -> import into Tinkercad, one shape per part, colour each
  * one OBJ + MTL   -> single import, named groups with distinct materials
  * one 3MF         -> per-object colours for slicers (Bambu/Prusa/Cura)
  * one merged STL  -> quick visual check
"""
import numpy as np, trimesh, os, sys, zipfile, warnings
warnings.filterwarnings("ignore"); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = ROOT_DEFAULT
SRC  = os.path.join(ROOT, "jugg_case", "msenturk115", "juggernaut-tactical-molle-phone-case")
USB_OFFSET = 38.42
INCLUDE_PHONE = os.environ.get("INCLUDE_PHONE","1") != "0"
OUTNAME = os.environ.get("ASSEMBLY_DIR","assembly")                      # the cable cap is exported at a print offset

KITS = {
    "pixel9pro": dict(dir="pixel9pro_case", tag="pixel9pro", phone="_phone9pro_in_case.stl"),
    "pixel9a":   dict(dir="pixel9a_case",   tag="pixel9a",   phone="_phone9a_in_case.stl"),
    "pixel6a":   dict(dir="pixel6a_case",   tag="pixel6a",   phone="_phone6a_in_case.stl"),
}
# name -> (file pattern, colour, extra translation)
PARTS = [
    ("case",                 "case_{tag}.stl",                     (0.16,0.18,0.20), None),
    ("top_cap",              "top_cap_{tag}.stl",                  (0.85,0.45,0.10), None),
    ("bottom_cap",           "bottom_cap_{tag}.stl",               (0.85,0.45,0.10), None),
    ("volume_button",        "volume_button_{tag}.stl",            (0.80,0.15,0.15), None),
    ("power_button",         "power_button_{tag}.stl",             (0.80,0.15,0.15), None),
    ("camera_protector_cap", "camera_protector_cap_{tag}.stl",     (0.20,0.60,0.35), None),
]
EXTRA = [("molle_adapter", os.path.join(SRC, "mount.stl"), (0.20,0.40,0.75))]

def load(p):
    m = trimesh.load(p); m.merge_vertices(); return m

def write_obj(parts, path):
    mtl = os.path.splitext(os.path.basename(path))[0] + ".mtl"
    with open(path, "w") as o, open(os.path.join(os.path.dirname(path), mtl), "w") as mf:
        o.write(f"# assembled model, mm\nmtllib {mtl}\n")
        base = 1
        for name, m, col in parts:
            mf.write(f"newmtl {name}\nKd {col[0]:.3f} {col[1]:.3f} {col[2]:.3f}\n"
                     f"Ka 0 0 0\nKs 0.05 0.05 0.05\nNs 20\nd 1\nillum 2\n\n")
            o.write(f"\no {name}\ng {name}\nusemtl {name}\n")
            for v in m.vertices: o.write(f"v {v[0]:.4f} {v[1]:.4f} {v[2]:.4f}\n")
            for f in m.faces:    o.write(f"f {f[0]+base} {f[1]+base} {f[2]+base}\n")
            base += len(m.vertices)

def write_3mf(parts, path):
    def hexc(c): return "#%02X%02X%02X" % tuple(int(round(255*x)) for x in c)
    objs, items, mats = [], [], []
    for i, (name, m, col) in enumerate(parts, start=2):
        mats.append(f'<base name="{name}" displaycolor="{hexc(col)}FF" />')
        v = "".join(f'<vertex x="{p[0]:.4f}" y="{p[1]:.4f}" z="{p[2]:.4f}"/>' for p in m.vertices)
        t = "".join(f'<triangle v1="{f[0]}" v2="{f[1]}" v3="{f[2]}"/>' for f in m.faces)
        objs.append(f'<object id="{i}" type="model" pid="1" pindex="{i-2}" name="{name}">'
                    f'<mesh><vertices>{v}</vertices><triangles>{t}</triangles></mesh></object>')
        items.append(f'<item objectid="{i}"/>')
    model = ('<?xml version="1.0" encoding="UTF-8"?>\n'
             '<model unit="millimeter" xml:lang="en-US" '
             'xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02">'
             f'<resources><basematerials id="1">{"".join(mats)}</basematerials>{"".join(objs)}</resources>'
             f'<build>{"".join(items)}</build></model>')
    rels = ('<?xml version="1.0" encoding="UTF-8"?>\n<Relationships '
            'xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Target="/3D/3dmodel.model" Id="rel0" '
            'Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
    ct = ('<?xml version="1.0" encoding="UTF-8"?>\n<Types '
          'xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
          '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
          '<Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", ct)
        z.writestr("_rels/.rels", rels)
        z.writestr("3D/3dmodel.model", model)

for kit, cfg in KITS.items():
    D = os.path.join(ROOT, cfg["dir"])
    OUT = os.path.join(D, OUTNAME)
    os.makedirs(OUT, exist_ok=True)
    parts = []
    for name, pat, col, _ in PARTS:
        f = os.path.join(D, pat.format(tag=cfg["tag"]))
        if not os.path.exists(f): print("  missing", f); continue
        parts.append((name, load(f), col))
    for name, f, col in EXTRA:
        parts.append((name, load(f), col))
    php = os.path.join(D, cfg["phone"])
    if INCLUDE_PHONE and os.path.exists(php):
        parts.append(("phone", load(php), (0.72,0.74,0.78)))
    for name, m, col in parts:
        m.export(os.path.join(OUT, f"{name}.stl"))
    write_obj(parts, os.path.join(OUT, f"{kit}_assembly.obj"))
    write_3mf(parts, os.path.join(OUT, f"{kit}_assembly.3mf"))
    merged = trimesh.util.concatenate([m for _, m, _ in parts])
    merged.export(os.path.join(OUT, f"{kit}_assembly_merged.stl"))
    b = np.array([m.bounds for _, m, _ in parts])
    lo, hi = b[:,0].min(axis=0), b[:,1].max(axis=0)
    print(f"{kit}: {len(parts)} parts, envelope {np.round(hi-lo,2).tolist()} mm -> {OUT}")
    for name, m, _ in parts: print(f"    {name:22s} {len(m.faces):6d} tris")
