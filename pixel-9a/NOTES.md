# Pixel 9a — what changed from the S8 original

Phone: 154.70 × 73.30 × 8.90 mm, 12.03 mm corner radius, camera bar 31.2 × 18.0 mm standing
0.60 mm proud, power and volume both on the right edge. Measured from `pixel9a-phone.stl`.

| # | Change | Reason |
|---|--------|--------|
| 1 | Case lengthened **+5.40 mm** (slice inserted at x = 59.5, halves moved 2.70 mm apart) | The 9a is 5.8 mm longer than the S8. |
| 2 | Groove rib re-trimmed to x 57.44 – 61.44 | The stretch grew it to 9.4 mm; the adapter's tabs need it inside their 4.98 mm gap. |
| 3 | Pocket recut to **155.90 × 74.20 × 9.20 mm**, R 12.48 | 0.60 mm/end, 0.45 mm/side, 0.30 mm depth. The original was 3.9 mm loose across — it was sized for a phone already in a slim case. |
| 4 | Pocket entrance squared off and carried through the top-cap socket | Lets the phone slide straight in once the top cap is off. |
| 5 | Old S8 camera hole and hood deleted, back plate closed | Wrong size, wrong place. |
| 6 | New camera opening: **19.5 × 32.7 mm pill** at x 104.33–123.83, y −51.12…−18.42 | Camera bar + 0.75 mm; pill shape matches the bar. |
| 7 | New hood, 2.2 mm proud, 45° taper, 3.0 mm rim | Same idea as the original hood; starts past x = 97.34 so it can't touch the adapter. |
| 8 | **Camera slide runway** — 0.70 mm channel in the pocket floor from the opening to the top end, with a boss outside | The bar is 0.60 mm proud; without this it jams on the pocket floor going in. The boss keeps the plate 1.40 mm. |
| 9 | Old S8 button holes filled, grooves reopened | The 9a has both buttons on one edge; the S8 had them split. |
| 10 | New button openings on the −Y wall: volume x 53.70–75.70, power x 82.70–94.70, z 2.05–5.05 | Plus a 0.40 mm relief groove along the slide path for the 0.6 mm-proud buttons. |
| 11 | Bottom wall: S8 holes (4 slots + USB + 3.5 mm jack) filled, three new openings cut | 9a bottom edge: speaker grille, centred USB-C + mic, left grille. No headphone jack. |
| 12 | Screen opening **149.90 × 68.20 mm**, R 9.48, 1.2 mm chamfer, lip underside z = 8.30 | 3.0 mm lip: about 2.6 mm of overlap on the phone's front face, clearing the 146.1 × 65.1 mm display by 1.5–1.9 mm. |
| 13 | Recessed back window widened around the hood | Gives the lens cap a flat seat; entirely past the adapter. |

## Files

| File | Notes |
|------|-------|
| `case_pixel9a.stl` | the case, 166.34 × 86.59 × 17.60 mm |
| `top_cap_pixel9a.stl` | stock cap moved +2.70 mm; its existing vent already lines up with the 9a's top mic |
| `bottom_cap_pixel9a.stl` | stock cap moved −2.70 mm, S8 slots replaced with 9a speaker / mic / left-grille slots (USB stays covered) |
| `bottom_cap_for_usb_cable_pixel9a.stl` | same, cable window dropped to z 1.95 so a plug clears the port |
| `volume_button_pixel9a.stl` | two-pad rocker plunger with a thinned centre web |
| `power_button_pixel9a.stl` | single-pad plunger |
| `camera_protector_cap_pixel9a.stl` | wedge-fit lens cap for the new hood, with grip ribs |

## Thinnest features

side walls 1.90 mm (1.50 mm across the button relief band) · back plate 1.50 mm
(1.40 mm under the runway; one 1.7 mm-wide bridge at x 126.8–128.5 is 0.80 mm) ·
button flange shoulder 0.70 mm · front lip 3.00 mm wide

## Top-cap tongue (added after first print review)

The camera slide channel has to run out through the top-cap socket, otherwise the phone can't
be slid in with the cap off. That left a **0.70 mm** open trench between the cap's underside and
the channel floor, open at the case's end face. The top cap now carries a tongue that plugs it,
shaped by boolean (trench box minus the case and the phone, each grown 0.20 mm) so it cannot
foul either. Against the untouched cap over a full 26 mm withdrawal sweep the tongue adds
**+0.0000 mm³** of interference. The case itself is unchanged.
See `../pixel-9-pro/preview/topcap_gap_before_after.png`.
