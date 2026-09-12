# Assembled, per-part coloured model

**The STLs in the parent folder are already in assembly coordinates** — the case, both caps,
both plungers, the lens cap and `../../shared-mount/mount.stl` all share one frame, so nothing
needs moving. Import them and they belong where they land.

The two files here carry the same thing with colours and positions baked into a single import:

| file | what it's for |
|---|---|
| `*_assembly.obj` + `.mtl` | one import, 7 named parts, already positioned. Tinkercad accepts `.obj`; whether it reads the `.mtl` colours I can't confirm — if not, the parts are still separate and colourable by hand. Keep the `.mtl` beside the `.obj`. |
| `*_assembly.3mf` | 7 named objects with colours baked in. This is the one that definitely renders in colour — Bambu Studio, PrusaSlicer, Cura, Windows 3D Viewer. |

Colours: case dark slate · caps orange · buttons red · lens cap green · MOLLE adapter blue.

The phone reference models are **not** included here — they're third-party CAD and this repo
doesn't redistribute them. See each kit's NOTES for where to get them.

This is a visualisation, not a print layout. Print from the STLs in the parent folder.
