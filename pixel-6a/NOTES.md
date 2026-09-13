# Pixel 6a — what changed from the S8 original

Phone: 152.20 × 71.79 × 8.90 mm, corner radius 5.22–5.41 mm, camera **visor** 66.86 × 16.65 mm
where it meets the back and standing **1.50 mm** proud, power and volume both on the right
edge. Measured from `Pixel6AModel.3mf` — 13 separate solids: body, screen, visor, lenses,
flash, both buttons, and the bottom-edge port recesses.

| # | Change | Reason |
|---|--------|--------|
| 1 | Case lengthened **+2.90 mm** (slice inserted at x = 59.5, halves moved 1.45 mm apart) | The 6a is 3.3 mm longer than the S8. |
| 2 | Groove rib re-trimmed to x 57.44 – 61.44 | Same tab-clearance reason as the 9a. |
| 3 | Pocket recut to **153.40 × 72.69 × 9.20 mm** | The outline is taken from the phone's own silhouette (port notches filled) offset 0.45 mm/side and 0.60 mm/end, so the 6a's four slightly different corner radii are followed exactly rather than approximated by one radius. |
| 4 | Pocket entrance squared off and carried through the top-cap socket | Slide-in clearance. |
| 5 | Old S8 camera hole and hood deleted, back plate closed | — |
| 6 | New camera opening **17.85 × 68.06 mm** at x 108.20–126.05, y −55.04…13.01 | Visor footprint + 0.60 mm. It spans nearly the full pocket width, leaving a 2.32 mm floor ledge each side — that is simply what a Pixel 6-series visor requires. |
| 7 | **Raised visor shelf** across the back, x 104.90–141.35, 1.80 mm proud, 45° taper | Does the job of the 9a's hood *and* carries the slide channel. The visor ends up recessed 1.8 mm inside it. |
| 8 | Slide channel, floor z = −2.60, from the opening to the top end | The visor is 1.50 mm proud — far too much to clear a 1.5 mm back plate, so the shelf adds the depth from outside. The plate stays 1.60 mm. |
| 9 | Old S8 button holes filled, grooves reopened | — |
| 10 | New button openings on the −Y wall: volume x 60.47–80.45, power x 88.62–98.60, z 2.70–5.15 | Plus a 0.30 mm relief groove; the 6a's buttons stand only 0.40 mm proud. |
| 11 | Bottom wall: three new openings | 6a bottom edge, measured from the model: speaker grille, centred USB-C, left grille. |
| 12 | Screen opening **147.40 × 66.69 mm**, 1.2 mm chamfer, lip underside z = 8.30 | 3.0 mm lip, clearing the 141.3 × 63.6 mm display by 1.6–3.1 mm. |
| 13 | Top cap gains a mic hole | The 6a's top mic sits between the stock cap's two vents. |

## Files

| File | Notes |
|------|-------|
| `case_pixel6a.stl` | the case, 163.83 × 86.59 × 17.20 mm |
| `top_cap_pixel6a.stl` | stock cap moved +1.45 mm, new hole over the 6a's top mic |
| `bottom_cap_pixel6a.stl` | stock cap moved −1.45 mm, S8 slots replaced with 6a speaker / left-grille slots |
| `bottom_cap_for_usb_cable_pixel6a.stl` | same, cable window dropped to z 1.55 for the 6a's lower USB-C |
| `volume_button_pixel6a.stl` | two-pad rocker plunger with a thinned centre web |
| `power_button_pixel6a.stl` | single-pad plunger |
| `camera_protector_cap_pixel6a.stl` | wedge-fit cap over the visor shelf; its rim is cut to the case's real back profile so it seats flat |

## Thinnest features

side walls 2.66 mm (2.36 mm across the button relief band) · back plate 1.50 mm
(1.60 mm under the slide channel, inside the shelf) · button flange shoulder 1.56 mm ·
back-plate ledge beside the camera opening 2.32 mm · front lip 3.00 mm wide

The 6a case is the sturdier of the two everywhere except the camera band, where the visor's
width is what dictates the opening.

## Lens cap trimmed flush (added after first print review)

The camera shelf runs right to the end of the case, so the lens cap's end wall wrapped around
the case's end face and stood **1.42 mm proud of the top of the phone**. The cap is now cut off
flush at the case's +X end face — it still wedges on the two tapered side walls and the −X end
wall, and now measures 0.00 mm³ beyond the case. See `preview/lenscap_flush_before_after.png`.

## Top-cap tongue (added after first print review)

The camera slide channel has to run out through the top-cap socket, otherwise the phone can't
be slid in with the cap off. That left a **1.70 mm** open trench between the cap's underside and
the channel floor, open at the case's end face. The top cap now carries a tongue that plugs it,
shaped by boolean (trench box minus the case and the phone, each grown 0.20 mm) so it cannot
foul either. Against the untouched cap over a full 26 mm withdrawal sweep the tongue adds
**+0.0000 mm³** of interference. The case itself is unchanged.
See `../pixel-9-pro/preview/topcap_gap_before_after.png`.

## Charging port (fixed after first print review)

Two things were wrong with the **`bottom_cap_for_usb_cable_*`** caps:

1. The block that erases the stock S8 speaker slots was cut far too wide (Y −50…6) and ran
   straight across the cable window, leaving a **3.4 mm bar through the middle of it**. The old
   slots only occupy Y −44.22…−32.82, so the erase block is now exactly that band.
2. The stock window (Z 2.45…7.55) was aligned to the **S8's** USB-C, which sits 1.5–1.9 mm
   higher in the pocket than these phones'. It is now recut as one clean window at Z 0.80…7.55,
   centred on the actual port.

Measured clear aperture for a plug driven through **cap + case** to the phone's port:

| | before | after |
|---|---|---|
| Pixel 9 Pro | 11.0 × 3.25 mm | **13.0 × 4.00 mm** |
| Pixel 9a | 11.0 × 3.00 mm | **12.5 × 5.00 mm** |
| Pixel 6a | 10.5 × 3.25 mm | **13.0 × 4.25 mm** |

A USB-C plug shell is 8.3 × 2.6 mm, so it passes with room. A chunky cable overmould
(~5–6.5 mm tall) may still not seat fully on the 9 Pro and 6a — the remaining limit is a thin
shelf in the case's cap recess, and removing it only buys another 0.25–0.50 mm, which is not
worth reprinting a case for. Only the caps changed; the cases are untouched.

See `preview/usb_port_before_after.png`.
