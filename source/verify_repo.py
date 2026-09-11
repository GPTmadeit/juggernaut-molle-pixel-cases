"""Final gate: verify the exact STLs sitting in the repo folder."""
import numpy as np, trimesh, os, sys, warnings
warnings.filterwarnings("ignore"); sys.path.insert(0,'.')
from mf import to_mf, to_tm
ROOT=r"C:\Users\carlb\OneDrive\Documents\Jugg Case Pixel"
REPO=os.path.join(ROOT,"juggernaut-molle-pixel-cases")
def L(p):
    m=trimesh.load(p); m.merge_vertices(); return m
MT=to_mf(L(os.path.join(REPO,"shared-mount","mount.stl")))
import params as P9, params6a as P6
ok=True
for tag,folder,P,phone_src,dxusb in [("9a","pixel-9a",P9,os.path.join(ROOT,"pixel9a_case","_phone9a_in_case.stl"),38.42),
                                     ("6a","pixel-6a",P6,os.path.join(ROOT,"pixel6a_case","_phone6a_in_case.stl"),38.42)]:
    D=os.path.join(REPO,folder)
    case=to_mf(L(os.path.join(D,f"case_pixel{tag}.stl")))
    ph  =to_mf(L(phone_src))
    print(f"\n== Pixel {tag} ==")
    for lab,v in [("case x mount",(case^MT).volume()),("case x phone",(case^ph).volume())]:
        s='OK' if v<0.5 else '<-- CLASH'; ok &= v<0.5
        print(f"   {lab:34s}{v:9.4f} mm^3 {s}")
    for n in ["top_cap","bottom_cap","bottom_cap_for_usb_cable","camera_protector_cap","volume_button","power_button"]:
        p=to_mf(L(os.path.join(D,f"{n}_pixel{tag}.stl")))
        q=p.translate([dxusb,0,0]) if n=="bottom_cap_for_usb_cable" else p
        a=(case^q).volume(); b=0.0 if n=="camera_protector_cap" else (ph^q).volume()
        s='OK' if max(a,b)<0.5 else '<-- CLASH'; ok &= max(a,b)<0.5
        print(f"   {n:26s} case {a:7.4f} phone {b:7.4f} {s}")
    worst=0.0
    for dx in np.arange(0,170,2.0):
        worst=max(worst,(case ^ ph.translate([float(dx),0,0])).volume())
    s='OK' if worst<0.5 else '<-- BLOCKED'; ok &= worst<0.5
    print(f"   insertion sweep worst      {worst:9.4f} mm^3 {s}")
    for f in sorted(os.listdir(D)):
        if not f.endswith(".stl"): continue
        m=L(os.path.join(D,f)); b=len(m.split(only_watertight=False))
        good = m.is_watertight and b==1; ok &= good
        print(f"   {f:42s} tris {len(m.faces):6d} bodies {b} watertight {m.is_watertight} {'' if good else '<-- BAD'}")
print("\nALL CHECKS PASS" if ok else "\nSOMETHING FAILED")
