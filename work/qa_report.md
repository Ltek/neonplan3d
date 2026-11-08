# QA report: NeonPlan reconstruction of the house plans

## 1. Result

| Item | Value |
|---|---|
| Floors | 3: Basement (−3.019 m), Main Floor (0), Upper Floor (+3.397 m) |
| Rooms | 40 (basement 10, main 12, upper 18), counting the ceiling-height parts of the theater, office and master bedroom |
| Doors | 34 (basement 6, main 12, upper 16), including 2 garage doors and 3 sliding glass doors |
| Windows | 43 units (basement 5, main 27, upper 11), including 9 transoms, 1 sidelight, 1 crawlspace access |
| Furniture / fixtures | 23 (2 U-stairs, kitchen, laundry, bathroom fixtures) |
| Free walls | 8 (stair wall, media niche, foyer front at upper level, bath 2 partition, linen closet ×4) |
| Main floor overall | 16.980 × 14.541 m between wall centre lines (= 56'-0" × 48'-0" to face of studs = 17.069 × 14.630 m) |
| Upper floor overall | 15.761 × 13.932 m centre lines (= 52'-0" × 46'-0" face of studs) |
| Automated validation | **passed**: 0 errors, 2 warnings (`validation_output.txt`) |
| Official importer (repo code = live page code) | 40 rooms, 35 doors, 43 windows, 5 walls, 43 furniture, **0 warnings, nothing dropped, every opening at its given position (max shift 0.000 m)** |

## 2. Dimension provenance

From `geometry_data.json → constants_ft` (74 coordinate lines):

| Provenance | Coordinate lines | Windows | Doors |
|---|---|---|---|
| D: explicit architect dimension | 21 | 41 | 4 |
| M: measured on the calibrated raster (±½") | 50 | 4 | 15 |
| E: estimated / inferred | 3 | 1 | 12 |

The owner's corrections added two more codes: O (owner markup or as-built note) and P (owner's photos, for furniture). The counts above are for the v1 reconstruction.

All exterior walls on all floors, the overall sizes and 41 of 46 window centres come from written dimensions. Most interior partitions are measured: their stud lines were located on the calibrated scan, and where interior dimensions exist they agree within about 1".

## 3. Geometry validation (validate_neonplan.py)

Checks passed:
- JSON parses; format `neonplan-import`, units `m`, rooms_at `centre`; only supported fields and furniture types are used.
- Floors are ordered lowest first. Each elevation plus height equals the next floor's elevation.
- Every room has ≥ 3 distinct corners, no repeated or duplicate points, no self-intersection, area ≥ 0.3 m², and consistent winding on every floor.
- No room overlaps another (tolerance 0.01 m²).
- No near-coincident corners (< 3 cm apart but not identical) and no parallel edges 0.1–6 cm apart. In other words, shared walls use identical coordinates and no slivers or double walls exist.
- Every door and window lies on a room edge or a free wall within 2 cm (the actual value is 0) and stays within its wall segment. Widths are plausible. Windows fit under the storey height. Doors appear once only.
- The main and upper outlines match the 56'×48' and 52'×46' strings to within 1 mm.
- The rear wall and right wall coincide on the main and upper floors. The upper floor overhangs the main floor by only 0.24 m², in the bedroom 2 bay.
- The stair room is identical on the main and upper floors, and the basement and main stairs share one footprint.
- Furniture lies inside rooms with orthogonal rotations.

Warnings, not corrected:
1. `Master Linen` is 0.41 m wide. That is the drawn linen cabinet, about 1'-4" inside.
2. The upper floor has 1536 sq ft of centre-line area against the area schedule's 1425 sq ft (+7.8%). See §5.

Area cross-check against the schedule on A2/A3:

| Level | Reconstruction (centre lines) | Schedule | Δ |
|---|---|---|---|
| Finished basement (room "Basement") | 889 sq ft | 889 | 0.0% |
| Total basement (Basement + Mechanical) | 1061 sq ft | 1018 | +4.2% |
| Main floor (without garage) | 1434 sq ft | 1451 | −1.2% |
| Upper floor | 1536 sq ft | 1425 | +7.8% |

## 4. Visual comparison

The overlays `compare_basement.png`, `compare_main_floor.png` and `compare_upper_floor.png` project the reconstructed centre lines (red), doors (orange), windows (blue), free walls (purple) and fixtures (green) back onto each scan through the same homography. I reviewed all three:
- No systematic scale, rotation or offset error is visible. The red centre lines run between the drawn stud lines over the whole sheet, including the far corners.
- Every window bar sits on its drawn window unit. Doors sit on their drawn openings.
- Room shapes, closets, the bay, the fireplace chase, the garage jogs and the stepped foundation all match.

Corrections made during the comparison and validation, each recorded:
- The upper WIC door was narrowed from 2'-4" to 1'-11". The drawn wall it sits in is only 2'-1" long, and the validator flagged that the door overran the segment.
- The master WC door was moved 0.45 ft along its wall for the same reason.
- The main-floor stair object was given the basement stair's depth (27.40 ft against 27.50 ft) so both share one footprint. The difference is 1.2".

## 5. Known discrepancies and unresolved uncertainties

1. **Open plan (most visible issue in 3D).** Breakfast / Kitchen / Great Room, Great Room / Dining, and the great-room hall / Foyer have no walls in the drawing. Their boundaries are inferred. `neonplan-import` cannot express "no wall", so the import page will build full walls on these lines. The full NeonPlan file `neonplan_house.neonplan3d.json` sets those edges to height 0, and sets 0.914 m for the #22 half wall, the stair rails and the open-to-foyer rails. If you use the simple file instead, set those wall heights to 0 in the editor.
2. **Upper floor area +7.8% against the schedule.** No geometric error was found: overall sizes, chains and overlay all match. Plausible causes: the schedule leaves out the stair opening (about 70 sq ft) and low or sloped-ceiling areas (the "SLOPED 8'-0" CLG" WIC). Not resolved.
3. **Stair direction.** NeonPlan's `stairs_u` puts the first flight on the left of its front edge and has no mirror option. With the landing on the correct (left, X 26.3 ft) side, the flights come out swapped: NeonPlan draws the first flight in the lower run, while the drawing has it in the upper run. The footprint and landing are correct.
4. **Doors drawn at 45°** (main coat closet, master WC, WIC 2, bath 2 from bedroom 4) and the zig-zag bifolds of the foyer coat closet were placed on the nearest orthogonal wall at estimated centres (provenance E).
5. **Entrances not confirmed from the plan:** Bedroom 2's door (placed on the hall wall) and the master arch (5'-0" opening at an estimated X). The "(2) 2468" double doors near the master entry could not be assigned to a wall and are **omitted**.
6. **Basement:** the Mechanical room's top wall (X 39.9–44.5 ft) may be open to the basement, because only a beam is drawn there. The crawlspace floor is higher than the slab, which is not modelled. The crawlspace access is modelled as a window (2'-8" × 2'-6", sill 5'-6"), and its sill is estimated. Basement window heads (7'-0⅞") are assumed. Bath R.I. is a rough-in with dashed future walls and was not modelled as a room.
7. **Heights not modelled:** the vaulted master ceiling, the 2-story foyer (shown only by the upper void), the 9'-0" kitchen soffit, and the 10'-0" against 3.397 m storey. Main-floor transoms are cut to 1'-9" so they stay under the storey line. The two upper rear 3020 transoms over the vaulted master are **omitted**: they sit above the 8'-1⅛" upper storey.
8. **2020 FX windows** (3 in dining, 1 in powder): 2'×2' fixed with an assumed 8'-0⅞" head.
9. **Furniture left out on purpose:** fireplace and raised hearth (no NeonPlan type), media niche, furnace, water heater, sump, pantry shelves, closet rods, optional laundry sink, optional den cabinets, the dishwasher (inside the island footprint) and the Powder WC/lav (not visibly drawn). Kitchen cabinets and the island are approximations of the drawn footprints.
10. **Not imported:** decks, porch and steps are not rooms. They are in the full NeonPlan file as outdoor terraces. Also not imported: the unexcavated areas, the roof, and the deck stairs (hand note A4: "Deck stairs off side not the rear").
11. **As-built:** S-1 is marked "AS BUILT" and its 56'-0" × 48'-0" outline and wall lines agree with A2. The architectural sheets are the permit set and not as-built. Field changes to partitions, if any, are unknown.

## 6. Owner corrections (markup of 2026-11-06)

Applied in `work/tools/geometry.py`. Where the owner moved a door, it was placed on the opening drawn on A3.2 at that spot (provenance M); the new overlays show each one on its drawn opening.

| Floor | Change |
|---|---|
| Upper | Master WIC door moved to the WIC's bottom wall (x 21.8 ft) |
| Upper | Master bedroom entry: the (2) 2468 double doors, 4'-8", centred x 39.27 ft on the master's bottom wall; the "arch to master" at x 31.1 is removed |
| Upper | Bath 3 door moved to its bottom wall (x 21.7 ft) |
| Upper | Bedroom 3 door moved to its bottom wall (x 43.4 ft); bedroom 4 door to its top wall (x 43.3 ft) |
| Upper | Bath 2 WC/tub door moved down the partition (z 32.25 ft) |
| Upper | Master vanity: one long counter (x 9.1–20.0 ft) with 2 basins instead of 2 loose washbasins |
| Upper | Owner's edited plan: the opening over the stair is at its top (x 26.3–35.8, z 16.1–21.5 ft) with a rail on its right side and along its bottom; the top of the stair is open to the hall |
| Upper | Hall closet where the 1668 linen was, with its 1'-6" door from the hall (its bottom put on the foyer rail line, 3.6" lower than drawn). Bedroom 2 takes in the old hall closet; its wall is the left side of the open-to-foyer area, which now runs to it. Short wall at the right end of the foyer rail |
| Upper | Master WIC 2: its door corner cut at 45° (from the old door's right end to the linen's top-left corner), with the 2468 door in the angled wall. Master linen door on its left side. Master shower wall to wall (outer wall to the tub's edge, down to the bottom wall). The vanity's middle section is a plain counter |
| Main | Owner: "Mud Hall / Pantry" is the Mud Room (not a pantry); its opening to the kitchen has no door (NeonPlan "passage" style in the full file). "Great Room" is the Living Room. The 2'-0" nook holds the fireplace (1/3 of it, at the rear end: assumed) and a built-in TV cabinet (the other 2/3); the floating niche wall is removed. NeonPlan has no fireplace type, so it is a sideboard named "fireplace" (NeonPlan's own importers do the same) |
| Main | Stair split by a divider wall (full height assumed) into the up stair (rear half) and the down stair to the basement (front half); both ends facing the dining room are open (owner). "Den / Flex" renamed Playroom |
| All | Ceilings (owner, full NeonPlan file): main floor 10'-0" (not the 2-storey foyer or the open stair). Upper floor 8'-0"; the master bedroom's ceiling is pitched from 8'-0" at its side walls to 12'-0" at its centre line, the ridge running from the window wall: it is modelled as two halves (one label in the preview) with sloping walls on the window wall and the opposite wall. Basement: theater, bathroom and office closet 9'-0"; the first 7'-0" of the theater in front of the stair wall 8'-0"; the office 8'-0" from the window wall to the closet door opening, 9'-0" beyond it (theater and office each split into two parts without a wall between them) |
| All | Stairs from the owner's photos: both are U-stairs in the same footprint (x 26.3–35.8, z 20.1–27.4 ft). Main to upper: up the rear half from the dining side, landing at the far end, back up over the down stair to the upper hall. Basement to main: up the rear half from the basement hall end, landing at the far end, back up the front half to the main floor's down-stair side; the mechanical room runs under that second flight. In the full NeonPlan file both are mirrored U-stairs at full storey height, so each opens the floor above over its footprint |
| All | Roof (full NeonPlan file): 13 custom roof sections drawn from the A5 roof plan, the building sections and the owner's front and back photos: the main hip roof, the master bedroom's rear gable, the hip over the master bath whose front slope runs down over the garage, the WIC hip, the hip over bedrooms 3 and 4, front gables over bedroom 4 and bedroom 2's bay (12:12), the porch gable on two posts, lean-tos over the garage front, the garage's left strip, the breakfast nook, the covered deck (open, on posts) and the fireplace nook. Eaves at the upper or main plate, 1'-0" overhang. Simplified: hip ends at the side pitch, valleys where sections overlap; the garage front slopes are 26° (instead of the plan's 8:12) so they meet the roofs above |
| Main | Furniture from the owner's photos (provenance P, sizes estimated from the photos, about ±1 ft): range with base and wall cabinets on the hood wall, tall pantry cabinets by the stair wall, 6 bar stools on the island's living-room side, a sofa under the rear windows, a sectional (long side facing the fireplace/TV, short side facing the windows) with ottoman, round coffee table and sofa table. Porch extended to the front of its posts (A2: post pads at z 49.5–51.5 ft) |
| All | Floor finishes (full file): carpet on the stairs, theater, office and basement hall; tiles in the theater's 8 ft strip and the basement bathroom; concrete in the garage, mechanical room and crawlspace; other rooms NeonPlan's default wood |
| Garage | Owner: the garage slab is 4 steps below the mud room door, so the garage is its own level 2'-6" below the main floor (risers about 7½", assumed), with 4 steps up to the mud room door. 1-car side ceiling 9'-6" (owner: 9–10 ft) at the garage plate; 2-car side ceiling at the underside of the upper floor, 12'-7" above the slab (owner: 12–15 ft). Where it meets the house its own walls are a 2'-6" curb with the house walls standing on it. The garage roofs' eaves are at the garage plate, which also lets the long slope over the garage run at the roof plan's 8:12. The main floor gets a stairwell opening over the basement stair (NeonPlan opens a floor only for stairs on the level directly below, now the garage). In the preview the garage is drawn with the main floor |
| Basement | Walk-out patio under the covered deck, outside the basement sliding door (owner). NeonPlan's ground is one flat level, so the sloped lot (the garage side underground, the patio side open) is not modelled |
| All | Preview: open edges between rooms are no longer drawn; only stair openings are dashed (main floor: the stair's side facing the dining room) |
| Main | Pantry wall + pocket door and the coat-closet walls + door are not built: Pantry, Mud Hall and Coat Closet are one room "Mud Hall / Pantry" |
| Main | Kitchen island replaced by one island about 10'-0" × 3'-4", centred on the sketch's box (the box is not to scale; ±1 ft) |
| Main | Dining room: the 3 × 2650 SH windows are one sliding glass door, 108" × 8'-0" (owner), centred on the old group; the 3 transoms above are kept |
| Main | Stair entrance on the lower run of the stair's right side: no rail there (full NeonPlan file) |
| Main | New "Dining Deck" outdoor area, 20 ft wide × 18 ft deep, against the dining wall starting at the fireplace chase (full NeonPlan file only; position assumed) |
| Main | Front door drawn on top of its transom in the preview and overlays (it was hidden under the blue transom bar) |

Basement, from the owner's as-built sketch (written dimensions) and markup (the new stair hall and angled walls). Provenance O; sketch positions are good to about ±1 ft:

| Change |
|---|
| Rooms named as the owner gave them: Theater (main room), Office (with its closet), Bathroom, Mechanical Room; plus Stairs, Stair Hall and the Crawlspace |
| Stair, hall and mechanical room as on the owner's edited plan: the stair is one straight flight (x 26.3–39.3 ft, 3'-8" wide), open at its end to a small Hall. The Hall has a 36" door on an angled wall to the theater and another to the Mechanical Room. The mechanical room wraps round under the stair to the bathroom. The angled wall to the theater is a "thick sound reducing wall", modelled 0.23 m (9", thickness assumed). Which end of the flight is the bottom is assumed (the hall end) |
| Office: the old wall on the walk-out wall line is removed; the new wall is 1'-2" further into the theater, with a 36" door. As-built width 12'-10" |
| Office closet ("enclose for closet") between the office and the bathroom, 3'-5" clear as built, 36" door from the office. The wall it shares with the bathroom's toilet area leaves that area 3'-3½" clear, so the two are nearly the same width (owner) |
| Bathroom 9'-5" clear (4'-10" shower + 4'-3" toilet zone) from the foundation; it includes the strip down to the foundation jog. The closet/bathroom wall toward the theater is 4" in front of the stair wall (owner), so the office door gets a 4" piece of wall beside it. Curbless walk-around shower and the moved toilet; no sink is shown on the sketch, none modelled. 36" door from the theater |
| Theater: baffle wall with the 130" screen, the full width of the room from the rear wall, its back against the 2'-0" foundation jog (face 25'-11" from the walk-out wall), ending at a short side wall (equipment cabinet, hidden door not modelled). |
| Ceiling heights (full NeonPlan file): theater and bathroom 9'-0". The 8'-0" soffit strip in the theater and the office's 8'-1"/9'-0" are not modelled |
| All basement doors 36" wide; rear windows 34" × 60" and the walk-out sliding door 71" × 84" (as built) |
| The basement's finished area (without the mechanical room and crawlspace) is 865 sq ft against 889 in the area schedule |

Sliding glass doors: the import format has no door styles and turns any door 2.2 m or wider into a garage door. The full NeonPlan file sets the 3 sliding doors to NeonPlan's "sliding" door style (and the 8 ft dining door back from garage to door).

## 7. Import testing

- I did **not** load the file in a browser on <https://neonplan3d.mastershort.de/import/>, so I make no claim about the import page UI.
- I verified that the page's script (`/import/neonplan-import.js`, fetched 2026-11-06) is byte-identical to `site/import/neonplan-import.js` in the repo at commit `ffbf4ac`. I then ran that repo's TypeScript import code in Node 24, on the same path the page uses (`readFile` → `readSimple` → `buildPlan` with the page's default options). Results:
  - `neonplan_house.json`: recognised as `simple`, 0 warnings, nothing dropped. The building parses with the editor's `parseExport` (what Editor → Backup → Import runs). Output: `neonplan_house.pagecheck.json`.
  - `neonplan_house.neonplan3d.json` (that output post-processed with open edges, wall heights, wall thickness, outdoor areas): recognised as a NeonPlan plan, `repairPlan` gives 0 warnings, and the editor's wall generator reports no overlaps.

## 8. How to reproduce

```
python3 tools/build.py                    # geometry.py -> neonplan_house.json, geometry_data.json, preview SVG, overlays
python3 validate_neonplan.py              # geometry checks (exit 1 on error)
node tools/page_path.ts <json> ...        # run inside a checkout of Mastershort/neonplan3d/frontend
python3 tools/postprocess.py built.json neonplan_house.neonplan3d.json
```
