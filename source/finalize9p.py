import os
ROOT_DEFAULT = os.environ.get("JUGG_ROOT",
    os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "work")))
import numpy as np, trimesh, os, sys, warnings
warnings.filterwarnings("ignore"); sys.path.insert(0,'.')
from mf import to_mf, to_tm
TOL=0.005
# finalize is NOT idempotent on its own: simplify() run twice decimates twice.  Record what
# has already been decimated and skip it, so re-running after a partial rebuild is safe.
import json
def _ledger(p):
    f=os.path.join(p,".finalized.json")
    try: return json.load(open(f))
    except Exception: return {}
def _save(p,led):
    json.dump(led, open(os.path.join(p,".finalized.json"),"w"), indent=1, sort_keys=True)

ROOT=ROOT_DEFAULT
SRC=os.path.join(ROOT,"jugg_case","msenturk115","juggernaut-tactical-molle-phone-case")
P=os.path.join(ROOT,"pixel9pro_case")
for f in sorted(os.listdir(P)):
    if not f.endswith(".stl") or f.startswith("_"): continue
    led=_ledger(P)
    m=trimesh.load(os.path.join(P,f)); m.merge_vertices()
    if led.get(f)==len(m.faces):
        print(f"  {f:44s} already decimated, skipped"); continue
    n0=len(m.faces); M=to_mf(m); v0=M.volume(); S=M.simplify(TOL)
    t=to_tm(S); t.merge_vertices()
    assert t.is_watertight and len(t.split(only_watertight=False))==1, f
    t.export(os.path.join(P,f))
    led[f]=len(t.faces); _save(P,led)
    print(f"  {f:44s} {n0:7d} -> {len(t.faces):6d} tris  dVol {abs(S.volume()-v0):7.3f}")
def L(p):
    m=trimesh.load(p); m.merge_vertices(); return m
case=to_mf(L(os.path.join(P,"case_pixel9pro.stl"))); ph=to_mf(L(os.path.join(P,"_phone9pro_in_case.stl")))
MT=to_mf(L(os.path.join(SRC,"mount.stl")))
print("\nre-verify after decimation:")
print(f"   case x mount {(case^MT).volume():8.4f}   case x phone {(case^ph).volume():8.4f}")
for n in ["top_cap","bottom_cap","bottom_cap_for_usb_cable","camera_protector_cap","volume_button","power_button"]:
    p=to_mf(L(os.path.join(P,f"{n}_pixel9pro.stl")))
    q=p.translate([38.42,0,0]) if n=="bottom_cap_for_usb_cable" else p
    a=(case^q).volume(); b=0.0 if n=="camera_protector_cap" else (ph^q).volume()
    print(f"      {n:26s} case {a:7.4f} phone {b:7.4f} {'OK' if max(a,b)<0.5 else '<-- CLASH'}")
worst=0.0
for dx in np.arange(0,172,2.0): worst=max(worst,(case ^ ph.translate([float(dx),0,0])).volume())
print(f"      insertion sweep worst {worst:.4f} mm^3  {'OK' if worst<0.5 else '<-- BLOCKED'}")
