# Source analysis: house plans

## 1. Inventory

All seven PDFs are single-page **raster scans**. None has vector content or a text layer: there are 0 vector drawings and 0 text characters, and each page holds one 1-bit image at 300 dpi on a 36" × 24" sheet. So no vector geometry could be extracted. All geometry comes from calibrated measurement of the scans, snapped to the written dimensions.

| File | Image (px) | Sheet | Content | Used for |
|---|---|---|---|---|
| `A1.PDF` | 10800 × 7216 | A2 | Basement / Crawlspace Plan, 1/4" = 1'-0", Crawl Space / Basement Option Notes, Typical Construction Assemblies, Area Schedule | Basement level |
| `A2.pdf` | 10800 × 7200 | A3.1 | Main Floor Plan, 1/4" = 1'-0", Main Floor Notes 1-35 | Main level |
| `A3.pdf` | 10800 × 7216 | A3.2 | Upper Floor Plan, 1/4" = 1'-0", Upper Floor Notes 1-19 | Upper level |
| `A4.pdf` | 10800 × 7200 | A4 | Front / Left / Rear / Right Elevations, Exterior Elevation Notes, hand note "Deck stairs off side not the rear" | Window sanity check, roof form (not imported) |
| `A5.PDF` | 10800 × 7200 | A5 | Building Sections A-A … E-E, Roof Plan | Storey heights, room stacking |
| `A6.PDF` | 10800 × 7200 | A6 | Interior Elevations (Great Room/Dining/Foyer, Tech Niche, Master Bath, Family Room), Stair Section | Stair geometry, half-wall heights |
| `As Built.pdf` | 10800 × 7248 | S-1 | Footing pad foundation plan by the structural engineer, stamped, hand-marked "AS BUILT", isometric | Cross-check of the foundation outline (56'-0" × 48'-0", 8" walls) |

Title block: builder, architect, plan number and site details (not reproduced here).

## 2. Floors identified

| Level | Sheet | Elevation | Storey height used | Source |
|---|---|---|---|---|
| Basement (walk-out) | A2 | −3.019 m | 3.019 m | A6 stair section: 8'-8" slab to top of foundation + 1'-2⅞" floor system |
| Main Floor | A3.1 | 0 | 3.397 m | A5/A6: 10'-1⅛" main plate + 1'-0⅝" floor system (floor-to-floor) |
| Upper Floor | A3.2 | +3.397 m | 2.467 m | A5/A6: 8'-1⅛" upper plate (the master bedroom vault is not modelled) |

The ceiling heights (10'-0" main, 8'-0" upper, 9'-4" powder, 8'-10" mud hall) differ from the storey heights above and are not imported.

## 3. Scale and calibration

The nominal scale is 1/4" = 1'-0", which would be 75 px/ft at 300 dpi. The scans are slightly distorted: on A2 the X scale is 74.83 px/ft at the top and 74.43 at the bottom, the Y scale is about 75.1 px/ft, sheet A3 is rotated about 0.3°, and there is a small keystone. Each sheet therefore got a **homography** fitted to 13–29 dimension extension lines. Those lines were detected automatically, as long straight pixel runs crossing the dimension strings, and each was paired with the value the chain gives it.

| Sheet | Control lines | Max residual |
|---|---|---|
| A1 basement | 19 | 3.8 px (0.6") |
| A2 main | 15 | 2.8 px (0.45") |
| A3 upper | 29 | 4.4 px (0.7") |

The calibrated lines then reproduce the chains, for example A2 bottom chain: 3.98 / 14.71 / 33.92 / 42.96 / 55.99 ft against 4'-0" / 14'-8" / 34'-0" / 43'-0" / 56'-0". So the calibrated raster measures to about ±½".

## 4. Coordinate system

- **Master frame (internal, feet):** X = 0 at the outer face of studs of the garage left wall, Z = 0 at the outer face of studs of the rear wall. These are the zero lines of the 52'-0" / 56'-0" / 48'-0" / 46'-0" strings that appear on all three plans, so the floors share one reference with no per-floor centring.
- **Export (metres):** shifted by the 1¾" half-stud so that the wall **centre lines** of the garage-left and rear walls are `[0, 0]`, then converted to metres. `rooms_at: "centre"`.
- Exterior dimensions are to **face of studs** (Main Floor Note 6, Upper Note 5), and every wall is drawn as two lines 3.5–3.8" apart, which is the 2×4 stud. Centre lines are therefore face ± 1.75". The drawings do not give total wall thicknesses. From Typical Construction Assemblies B1/B2/E1/E2 they come to about 5.4" exterior and 4.5" interior. These go into the full NeonPlan file (0.14 m / 0.114 m) and are not needed for the import JSON.

## 5. Dimensions available and used

- **Overall:** 52'-0" (rear and upper), 56'-0" (front), 48'-0" (main depth), 46'-0" (upper depth); 10'-8" + 28'-0" + 13'-4"; 4'-0" + 10'-8" + 19'-4" + 9'-0" + 13'-0".
- **Chains:** window-centre chains on every elevation of every floor, the left/right chains (5'-0", 5'-0", 13'-8½", 20'-3½", 2'-0", 2'-0" / 2'-0", 14'-0", 3'-4", 2'-6", 2'-6", 3'-4", …), and the upper chains (2'-8½", 7'-11½", 5'-4", 6'-2", 3'-0", 3'-6" ×3, 7'-4", 6'-0"; bottom 10'-8", 5'-4", 3'-3", 2'-6", 3'-6", 2'-6", 6'-9", 3'-6", 7'-0", 7'-0").
- **Interior:** many interior dimensions are written (11'-6", 8'-10", 9'-3", 5'-8", 13'-6", 5'-2", 8'-5½", 14'-8", 3'-8", …). Interior walls were placed on the measured centre of their drawn stud lines and checked against these.
- **Vertical:** plate heights from A5 and A6; window head heights from Main Note 13 (8'-0⅞") and Upper Note 12 (7'-0⅞"); window sizes from the unit codes (WWHH, e.g. 3050 SH = 3'-0" × 5'-0" single hung; 2620 TRANS = 2'-6" × 2'-0" transom).
- **Door sizes** from codes (2868 = 2'-8" × 6'-8", 2468, 2668, 3068, 2-2068, 6068 BP, 8080 / 16080 O.G.D.).

## 6. Architectural features identified

- **Basement (walk-out):** finished Basement #1 with a dashed Bath R.I. (rough-in only); a Mechanical area (furnace, water heater, sump pit, 2868 door); Crawlspace #13 under the den and foyer behind a 2'-8" header opening; unexcavated areas under the garage and porch; a 2×6 walk-out wall with 6080 SGD; 4040 SL egress; 3 × 3050 SH; a stepped foundation; a U-stair (UP 16R).
- **Main:** 3-Car Garage (8080 + 16080 O.G.D.), Laundry, Pantry, unnamed mud hall with 2868 #4 self-closing rated door, unnamed coat closet, Breakfast, Kitchen (island, D.W., double oven, Ref., soffit), Great Room (raised stone hearth fireplace + media/TV niche chase), Dining Room (flat arch #34, 36" half wall #22 to the hall), 2-story Foyer, Powder, coat closet with 2-2068 bifolds, Den / Flex (2-2068 french doors), U-stair (UP 18R), Covered Deck, Uncovered Deck, Porch with two posts.
- **Upper:** Master Bedroom (vaulted, bearing walls both sides), Master WIC, Master Bath (42"×72" tub, 34"×60" shower with seat, glass enclosure, 2 lavs), 2nd master WIC, master linen, master WC, Bath 3 (hand-corrected from "Bath 2"), unnamed Bedroom 2 dressing room, Bedroom 2 with window-seat bay, Bedrooms 3 and 4 with 6068 BP closets, Bath 2 (Jack-and-Jill, two lavs, tub/shower), hall closet, linen, hall with stair landing, open-to-foyer void, arch opening to master (spring 7'-4").
- **Stair:** a U-stair with the same plan footprint on all three levels: X 26.27–35.80 ft, Z 20.12–27.4/27.5 ft. Main→upper per A6 is 8 treads at 10", a landing, then 7 treads at 10". Basement→main is a second U below it.

## 7. Assumptions and uncertainties found during analysis

1. **Open plan:** Breakfast, Kitchen and Great Room share one space, and the Dining Room and the great-room hall are open (flat arches). Their split lines are inferred (provenance E). The simple import format has no way to say "no wall", so the import page will put walls on these lines. The full NeonPlan file has them set to height 0.
2. **Wall thicknesses** are inferred from the assembly notes, not dimensioned.
3. **Basement window heads** are not given. 7'-0⅞" is assumed.
4. **2020 FX units** (dining ×3, powder) are taken as 2'-0" × 2'-0" fixed with the 8'-0⅞" head. Their real heights are not given on the plan.
5. **Upper floor area** comes out 7.8% above the area schedule (see the QA report).
6. **Door positions drawn at 45°** (closets, master WC, WIC 2, bath 2) are placed on the nearest orthogonal wall.
7. **Hand notes on S-1** (a post pad that may need relocating, "12" ftg, DBL plate except exterior gar walls") and on A4 ("Deck stairs off side not the rear") are structural or site notes and do not change room geometry.
