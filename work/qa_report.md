# QA report: NeonPlan reconstruction of the house plans

## 1. Result

| Item | Value |
|---|---|
| Floors | 3: Basement (−3.019 m), Main Floor (0), Upper Floor (+3.397 m) |
| Rooms | 34 (basement 3, main 14, upper 17) |
| Doors | 31 (basement 2, main 13, upper 16). These include 2 garage doors and 5 openings without a leaf: the mud hall→kitchen cased opening, the master arch, the master bedroom→bath passage, the hall-closet opening and bath 2 from bedroom 3. |
| Windows | 46 individual units (basement 5, main 30, upper 11). These include 9 transoms, 1 sidelight, 1 crawlspace access. |
| Furniture / fixtures | 23 (2 U-stairs, kitchen, laundry, bathroom fixtures) |
| Free walls | 8 (stair wall, media niche, foyer front at upper level, bath 2 partition, linen closet ×4) |
| Main floor overall | 16.980 × 14.541 m between wall centre lines (= 56'-0" × 48'-0" to face of studs = 17.069 × 14.630 m) |
| Upper floor overall | 15.761 × 13.932 m centre lines (= 52'-0" × 46'-0" face of studs) |
| Automated validation | **passed**: 0 errors, 2 warnings (`validation_output.txt`) |
| Official importer (repo code = live page code) | 34 rooms, 31 doors, 46 windows, 8 walls, 23 furniture, **0 warnings, nothing dropped, every opening at its given position (max shift 0.000 m)** |

## 2. Dimension provenance

From `geometry_data.json → constants_ft` (74 coordinate lines):

| Provenance | Coordinate lines | Windows | Doors |
|---|---|---|---|
| D: explicit architect dimension | 21 | 41 | 4 |
| M: measured on the calibrated raster (±½") | 50 | 4 | 15 |
| E: estimated / inferred | 3 | 1 | 12 |

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

## 6. Import testing

- I did **not** load the file in a browser on <https://neonplan3d.mastershort.de/import/>, so I make no claim about the import page UI.
- I verified that the page's script (`/import/neonplan-import.js`, fetched 2026-11-06) is byte-identical to `site/import/neonplan-import.js` in the repo at commit `ffbf4ac`. I then ran that repo's TypeScript import code in Node 24, on the same path the page uses (`readFile` → `readSimple` → `buildPlan` with the page's default options). Results:
  - `neonplan_house.json`: recognised as `simple`, 0 warnings, nothing dropped. The building parses with the editor's `parseExport` (what Editor → Backup → Import runs). Output: `neonplan_house.pagecheck.json`.
  - `neonplan_house.neonplan3d.json` (that output post-processed with open edges, wall heights, wall thickness, outdoor areas): recognised as a NeonPlan plan, `repairPlan` gives 0 warnings, and the editor's wall generator reports no overlaps.

## 7. How to reproduce

```
python3 tools/build.py                    # geometry.py -> neonplan_house.json, geometry_data.json, preview SVG, overlays
python3 validate_neonplan.py              # geometry checks (exit 1 on error)
node tools/page_path.ts <json> ...        # run inside a checkout of Mastershort/neonplan3d/frontend
python3 tools/postprocess.py built.json neonplan_house.neonplan3d.json
```
