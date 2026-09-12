import os
ROOT_DEFAULT = os.environ.get("JUGG_ROOT",
    os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "work")))
"""Final gate: verify the exact STLs sitting in the repo folder, all three kits."""
import numpy as np, trimesh, os, sys, importlib, warnings
warnings.filterwarnings("ignore"); sys.path.insert(0,'.')
from mf import to_mf, to_tm
ROOT=ROOT_DEFAULT
REPO=os.path.join(ROOT,"juggernaut-molle-pixel-cases")
def L(p):
    m=trimesh.load(p); m.merge_vertices(); return m
MT=to_mf(L(os.path.join(REPO,"shared-mount","mount.stl")))
KITS=[("9pro","pixel-9-pro","params9p",os.path.join(ROOT,"pixel9pro_case","_phone9pro_in_case.stl")),
      ("9a","pixel-9a","params",os.path.join(ROOT,"pixel9a_case","_phone9a_in_case.stl")),
      ("6a","pixel-6a","params6a",os.path.join(ROOT,"pixel6a_case","_phone6a_in_case.stl"))]
ok=True
for tag,folder,pmod,phone_src in KITS:
    P=importlib.import_module(pmod); D=os.path.join(REPO,folder)
    case=to_mf(L(os.path.join(D,f"case_pixel{tag}.stl"))); ph=to_mf(L(phone_src))
    print(f"\n== Pixel {tag} ==")
    for lab,v in [("case x mount",(case^MT).volume()),("case x phone",(case^ph).volume())]:
        good=v<0.5; ok&=good; print(f"   {lab:34s}{v:9.4f} mm^3 {'OK' if good else '<-- CLASH'}")
    for n in ["top_cap","bottom_cap","bottom_cap_for_usb_cable","camera_protector_cap","volume_button","power_button"]:
        p=to_mf(L(os.path.join(D,f"{n}_pixel{tag}.stl")))
        q=p.translate([38.42,0,0]) if n=="bottom_cap_for_usb_cable" else p
        a=(case^q).volume(); b=0.0 if n=="camera_protector_cap" else (ph^q).volume()
        good=max(a,b)<0.5; ok&=good
        print(f"   {n:26s} case {a:7.4f} phone {b:7.4f} {'OK' if good else '<-- CLASH'}")
    worst=max((case ^ ph.translate([float(dx),0,0])).volume() for dx in np.arange(0,172,2.0))
    good=worst<0.5; ok&=good; print(f"   insertion sweep worst      {worst:9.4f} mm^3 {'OK' if good else '<-- BLOCKED'}")
    for f in sorted(os.listdir(D)):
        if not f.endswith(".stl"): continue
        m=L(os.path.join(D,f)); nb=len(m.split(only_watertight=False))
        g=m.is_watertight and nb==1; ok&=g
        print(f"   {f:42s} tris {len(m.faces):6d} bodies {nb} watertight {m.is_watertight} {'' if g else '<-- BAD'}")
print("\nALL CHECKS PASS" if ok else "\nSOMETHING FAILED")
