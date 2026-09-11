# Juggernaut-style MOLLE case — Pixel 9a and Pixel 6a

Two 3D-printable rugged phone cases that drop into the **unmodified** MOLLE adapter from
msenturk115's *Juggernaut Tactical MOLLE Phone Case*, which was drawn around a Galaxy S8.

Both cases were rebuilt around a real 3D model of each phone. Every fit — the adapter, the
phone, the end caps, the button plungers — is verified by boolean intersection, not by eye.

| | Pixel 9a | Pixel 6a |
|---|---|---|
| phone | 154.70 × 73.30 × 8.90 mm, R 12.03 | 152.20 × 71.79 × 8.90 mm, R 5.2–5.4 |
| camera | 31.2 × 18.0 mm pill, 0.6 mm proud | 66.9 × 16.7 mm visor, 1.5 mm proud |
| case | 166.34 × 86.59 × 17.60 mm | 163.83 × 86.59 × 17.20 mm |
| pocket | 155.90 × 74.20 × 9.20 mm | 153.40 × 72.69 × 9.20 mm |
| side wall | 1.90 mm | 2.66 mm |
| stretch vs. the S8 original | +5.40 mm | +2.90 mm |

![Pixel 9a](pixel-9a/preview/F_drawing.png)

![Pixel 6a](pixel-6a/preview/S_drawing.png)

## What's here

```
pixel-9a/            7 STLs + preview renders      see pixel-9a/NOTES.md
pixel-6a/            7 STLs + preview renders      see pixel-6a/NOTES.md
shared-mount/        mount.stl, molle.stl, molle_mount.stl  -- ORIGINAL, UNMODIFIED
source/              the parametric build + verification scripts
*.zip                everything above in one archive
```

`shared-mount/` is copied verbatim from the original design. Neither case moves or edits it,
so one printed adapter takes either case.

## Printing

Back (−Z) on the plate, PETG or ABS/ASA, 4 perimeters, 30 % infill or more.

Print the two button plungers first, drop them into their recesses **from inside the pocket**,
then take the top cap off and slide the phone in from the top — the phone traps the plungers.
Use `bottom_cap_for_usb_cable_*` instead of `bottom_cap_*` when you want to charge with the
cap on.

If the phone is tight after printing, scale the case to 100.3 % **in X and Y only**.

## How the mount interface is preserved

The adapter grips the case through four spring tabs that hook over a horizontal ledge at
**z = 1.00 mm** in the groove running along both sides of the case. Those tabs sit at
x 36.9–56.9 and 61.9–82.0, with a 4.98 mm tab-free window at x 56.95–61.93.

Both cases therefore keep, untouched:

* outer rail faces y = −62.48 / +20.45, rail underside z = −3.00, and the 45° chamfers
* the side groove (in to y = −60.02 / +17.98, z 1.00 – 9.00) and its z = 1.00 snap ledge
* the groove rib, re-trimmed after the stretch back to x 57.44 – 61.44 so it stays inside the
  tab-free window
* the T-slots at both ends that the end caps slide into

Each case is lengthened by splitting the original at x = 59.5 — inside that tab-free window —
and inserting a slice of its own constant mid-section, so the rail pattern the adapter sees is
unchanged. The button plungers stop at y = −60.95, clear of the tab tips at y = −61.10.

## Verified

For both phones, by boolean intersection (0.000 mm³):

* case ∩ mount.stl — the adapter still seats
* case ∩ phone, seated and at every extreme of the clearance envelope
* the phone slid in from the +X end in 2 mm steps over the full length, at each corner of the
  clearance envelope
* case ∩ and phone ∩ each of the four caps and both button plungers
* every phone feature — speaker, USB-C, mic(s), camera, buttons — unobstructed
* every STL: one body, watertight

Re-run it yourself: see `source/`.

## Rebuilding

```bash
pip install numpy trimesh manifold3d shapely
export JUGG_ROOT=/path/to/work      # holds the extracted original zip + the phone models
python source/pixel9a/build_case.py && python source/pixel9a/build_parts.py
python source/pixel6a/build_case6a.py && python source/pixel6a/build_parts6a.py
python source/finalize.py           # decimate to 5 um and re-verify everything
```

Every dimension lives in `source/pixel9a/params.py` and `source/pixel6a/params6a.py`.

## Credit and licence

The original **Juggernaut Tactical MOLLE Phone Case** is by **msenturk115**. The MOLLE adapter,
the end caps, and the case's outer shell and rail geometry are their work; this repo only
refits the phone-facing side for two Pixels. Please check the original model's licence before
selling anything printed from this, and credit msenturk115.

The Pixel 6a reference model (`Pixel6AModel.3mf` / `.step`) is a third-party CAD model and is
**not** redistributed here; only measurements taken from it are.
