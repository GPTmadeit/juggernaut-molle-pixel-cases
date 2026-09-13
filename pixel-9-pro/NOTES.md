# Pixel 9 Pro — Juggernaut MOLLE case

Phone: **152.80 × 72.00 × 8.50 mm**, 12.00 mm corner radius, camera bar **64.44 × 21.50 mm
standing 3.52 mm proud**, power and volume both on the right edge.

Measured from `pixel_9_pro.stl` (the1dynasty, [Thingiverse 6746749](https://www.thingiverse.com/thing:6746749)),
scaled ×1000 — the file is in metres — and repaired (96 zero-area triangles from the Blender
export removed; it then closes cleanly, genus 0).

## Source-model confidence — read this

That dummy was **modelled in Blender from spec sheets before the author had the phone**, so it
is not caliper-measured the way the 9a and 6a models were. What I could check:

* overall size **152.80 × 72.00 × 8.50** matches Google's published figures exactly
* corner radius fits R = 12.00 on three of four corners to within **0.005 mm**
* it *does* carry bottom-edge port recesses (speaker, USB-C with its tongue, mic, one more hole)
  and a top mic — better than I expected
* **its USB-C is dead-centre on the bottom edge (Y = −21.02, the pocket centreline), which the
  independent Pixel 9 Pro XL STEP** (Sri Ram, GrabCAD, converted via OpenCASCADE) **agrees with.**
  Speaker and mic offsets from the centreline agree between the two models to ~1.5 mm.

So: outer dimensions and the camera bar I trust. Port *positions* are the soft spot, which is
why the bottom openings below are cut oversize.

## What changed from the S8 original

| # | Change | Reason |
|---|--------|--------|
| 1 | Case lengthened **+3.50 mm** (slice inserted at x = 59.5, halves moved 1.75 mm apart) | The 9 Pro is 3.9 mm longer than the S8. |
| 2 | Groove rib re-trimmed to x 57.44 – 61.44 | Keeps it inside the adapter's 4.98 mm tab-free window. |
| 3 | Pocket **154.00 × 72.90 × 8.80 mm**, R 12.45 | 0.60 mm/end, 0.45 mm/side, 0.30 mm depth. |
| 4 | Pocket entrance squared off and carried through the top-cap socket | Slide-in clearance. |
| 5 | Old S8 camera hole and hood deleted, back plate closed | — |
| 6 | New camera opening **22.90 × 65.84 mm**, R 11.15, at x 100.69–123.59, y −53.94…11.90 | Camera bar + 0.70 mm. Leaves a 3.53 mm floor ledge each side. |
| 7 | **Raised camera shelf**, x 97.49–141.65, **3.60 mm proud** (z −6.00 … −2.40), 45° taper | The bar stands 3.52 mm proud — nothing like that clears a 1.5 mm back plate, so the shelf both hoods the bar and provides the depth. |
| 8 | Slide channel, floor z = −4.62, spanning the whole opening to the top end | The bar has to travel from the pocket entrance to its seat. Plate under it stays **1.38 mm**. |
| 9 | Old S8 button holes filled, grooves reopened | — |
| 10 | New button openings on the −Y wall: volume x 54.24–76.13, power x 83.14–95.00, z 1.83–4.82 | Plus a 0.35 mm relief groove; the buttons stand 0.47 mm proud. |
| 11 | Bottom wall: four openings, **cut oversize** (speaker 17.3 × 2.9, USB-C 15.0 × 6.05, mic 4.05 × 3.45, second hole 3.9 × 3.3) | Absorbs the ±1.5 mm of uncertainty in the source model's port positions. |
| 12 | Screen opening **148.00 × 66.90 mm**, 1.2 mm chamfer, lip underside z = 7.90 | 3.0 mm lip all round. |
| 13 | Top cap shifted +1.75 mm, no new mic hole needed | The 9 Pro's top mic (y −45.22…−44.02) already falls inside the stock cap's vent at y −46.54…−43.54. |
| 14 | Top cap gains a **tongue** filling the slide-channel trench | See the section at the bottom. |

## Files

`case_pixel9pro.stl` · `top_cap_pixel9pro.stl` · `bottom_cap_pixel9pro.stl` ·
`bottom_cap_for_usb_cable_pixel9pro.stl` · `volume_button_pixel9pro.stl` ·
`power_button_pixel9pro.stl` · `camera_protector_cap_pixel9pro.stl`

`mount_UNCHANGED.stl`, `molle_UNCHANGED.stl`, `molle_mount_UNCHANGED.stl` — copied from the
original design, **not modified**. The same printed adapter takes the 9a, 6a and 9 Pro cases.

`assembly/` — the coloured, fully assembled model. See `assembly/README.md`.

## Verified by boolean intersection (all 0.000 mm³ or float-noise)

case ∩ mount · case ∩ phone seated and at every clearance extreme · phone slid in from the +X
end in 2 mm steps over the full length at five clearance corners · case ∩ and phone ∩ all four
caps and both plungers · speaker, USB-C, both mics and the camera bar unobstructed ·
every STL single-body and watertight.

## Thinnest features

side walls 2.55 mm (2.20 mm across the button relief band) · back plate 1.50 mm
(1.38 mm under the slide channel, inside the shelf) · button flange shoulder 1.40 mm ·
back-plate ledge beside the camera opening 3.53 mm · front lip 3.00 mm wide

## Printing

Case is **164.4 × 86.6 × 19.0 mm** — 1.4 mm thicker than the 9a's, entirely because of the
camera shelf. Back (−Z) on the plate, PETG or ABS/ASA, 4 perimeters, 30 % infill or more.

Plungers in from inside the pocket first, then top cap off and slide the phone in from the top.
If it's tight, scale the case 100.3 % in X and Y only.

## Top-cap tongue (added after first print review)

The camera-bump slide channel has to run out through the top-cap socket, otherwise the phone
can't be slid in with the cap off. That left an open trench between the cap's underside and
the channel floor, open at the case's end face:

| | trench |
|---|---|
| Pixel 9a | 0.70 mm tall |
| Pixel 6a | 1.70 mm |
| Pixel 9 Pro | 3.72 mm |

Fixed on the **cap**, not the case: the top cap now carries a tongue that plugs the trench,
shaped by boolean (trench box minus the case and the phone, each grown 0.20 mm) so it cannot
foul either. Measured against the untouched cap over a full 26 mm withdrawal sweep, the tongue
adds **+0.0000 mm³** of interference — it slides in and out exactly as the stock cap did.

See `preview/topcap_gap_before_after.png`.

## Lens cap trimmed flush (added after first print review)

The camera shelf runs right to the end of the case, so the lens cap's end wall wrapped around
the case's end face and stood **1.42 mm proud of the top of the phone**. The cap is now cut off
flush at the case's +X end face — it still wedges on the two tapered side walls and the −X end
wall, and now measures 0.00 mm³ beyond the case. See `preview/lenscap_flush_before_after.png`.
