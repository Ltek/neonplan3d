"""Reconstructed geometry of the house, in FEET, centre-line of walls.

Master frame (same for every floor): X = feet to the right of the outer face of studs of the garage left wall,
Z = feet down the sheet from the outer face of studs of the rear (top) wall. These are the zero lines of the
architect's dimension strings (52'-0" / 56'-0" / 48'-0" / 46'-0"), which all three plans share.

Every coordinate constant carries provenance:
  D = explicit architect dimension (face of stud) +/- half the 2x4 stud (1.75" = 0.146 ft) to reach the centre line
  M = measured from the calibrated raster (homography fit to the dimension extension lines, residual <= 0.06 ft)
  E = estimated / inferred (symbol position, door leaf, etc.)
"""

T = 0.146  # half a 3.5" stud: face of stud -> centre line (exterior dims are to face of studs, Main Floor Note 6)

C = {}      # name -> (value_ft, provenance, note)


def c(name, val, prov, note=""):
    C[name] = (round(val, 3), prov, note)
    return round(val, 3)


# ---------------------------------------------------------------- shared exterior lines (all floors)
X_GAR_L = c("X_GAR_L", 0 + T, "D", "garage left wall, 56'-0\" chain origin")
X_DECK = c("X_DECK", 4 + T, "D", "4'-0\" chain: garage jog / laundry & master bath left wall")
X_BRK_L = c("X_BRK_L", 14.667 + T, "D", "10'-8\" chain: breakfast / laundry / dressing left wall line")
X_REAR_R = c("X_REAR_R", 42.667 - T, "D", "10'-8\"+28'-0\": end of rear wall, fireplace jog, master bedroom bearing wall")
X_CHASE = c("X_CHASE", 44.667 - T, "D", "2'-0\" fireplace/media chase bump")
X_R = c("X_R", 56 - T, "D", "52'-0\" / 56'-0\" right face")
X_GAR_R = c("X_GAR_R", 34 + T, "D", "19'-4\" chain (14'-8\"..34'-0\"): garage right wall")
X_DEN_L = c("X_DEN_L", 42.15, "M", "den left (porch side) wall; 9'-0\"/13'-0\" chain puts porch post face at 43'-0\"")
X_UP_BR2_L = c("X_UP_BR2_L", 20 + T, "D", "upper 5'-4\" chain: bedroom 2 left wall")
X_BAY_L = c("X_BAY_L", 23.25 + T, "D", "upper 3'-3\" chain: bay left")
X_BAY_R = c("X_BAY_R", 31.75 - T, "D", "upper 11'-9\" chain: bay right")

Z_REAR = c("Z_REAR", 0 + T, "D", "rear wall, 48'-0\"/46'-0\" chain origin")
Z_CHASE = c("Z_CHASE", 2 + T, "D", "right chain 2'-0\": fireplace jog")
Z_DECK = c("Z_DECK", 10 + T, "D", "left chain 5'-0\"+5'-0\": laundry / master bath top (under/over covered deck)")
Z_WIC_TOP = c("Z_WIC_TOP", 5 + T, "D", "upper left chain 5'-0\": master WIC top")
Z_DIN_TOP = c("Z_DIN_TOP", 16 - (-T), "D", "right chain 2'-0\"+14'-0\": dining / bedroom 3 top wall")
Z_GAR_TOP = c("Z_GAR_TOP", 23.85, "M", "garage top wall under pantry/mud hall (13'-8 1/2\" chain = 23.71 face)")
Z_STAIR_BOT = c("Z_STAIR_BOT", 27.5, "M", "garage / kitchen / stair / foyer / dining line (27.42-27.6 measured; right chain 27'-8\")")
Z_DEN_FRONT = c("Z_DEN_FRONT", 46 - T, "D", "right chain 46'-0\": den front / bedroom 4 front")
Z_GAR_DOOR1 = c("Z_GAR_DOOR1", 46 - T, "D", "left chain 2'-0\": single garage door wall")
Z_GAR_DOOR2 = c("Z_GAR_DOOR2", 48 - T, "D", "left chain 48'-0\": double garage door wall")
Z_GAR_JOG = c("Z_GAR_JOG", 44 - T, "D", "left chain 20'-3 1/2\"+2'-0\": garage left jog")
Z_FOYER_FRONT = c("Z_FOYER_FRONT", 39.85, "M", "front door wall (foyer)")
Z_UP_FRONT_L = c("Z_UP_FRONT_L", 40 - T, "D", "upper left chain: bedroom 2 front / upper front over foyer")
Z_BAY = c("Z_BAY", 42.75 - T, "M", "bedroom 2 bay front (measured 42.55-42.6)")

# ---------------------------------------------------------------- main floor interior lines
X_PANTRY_R = c("X_PANTRY_R", 8.80, "M", "pantry right wall (2468 PKT) - NOT BUILT per owner, unused")
X_CLOS_L = c("X_CLOS_L", 12.46, "M", "NOT BUILT per owner, unused: coat closet left wall (2'-4 1/2\" inside)")
Z_LAUND_BOT = c("Z_LAUND_BOT", 16.13, "M", "laundry bottom wall (2868 PKT)")
Z_CLOS_BOT = c("Z_CLOS_BOT", 20.20, "M", "coat closet bottom wall - NOT BUILT per owner, unused")
Z_BRK_KIT = c("Z_BRK_KIT", 8.50, "E", "no wall: breakfast / kitchen split taken at the 5'-5\"/6'-1\" dimension line")
X_STAIR_L = c("X_STAIR_L", 26.27, "M", "stair left wall / kitchen right; also breakfast|great-room split (1'-0\" pier at 25.46-26.46)")
X_STAIR_R = c("X_STAIR_R", 35.80, "M", "stair right end (newel / rail)")
Z_STAIR_MID = c("Z_STAIR_MID", 23.80, "M", "stair: line between the two runs (rail #10 at the landing)")
Z_STAIR_TOP = c("Z_STAIR_TOP", 20.12, "M", "stair top (handrail #10 main, 36\" AFF wall upper)")
X_DIN_L = c("X_DIN_L", 42.40, "E", "no wall: dining flat arch (#34) line")
X_HALF_END = c("X_HALF_END", 47.30, "M", "end of 36\" half wall (#22) dining|hall, full wall beyond")
X_POW_L = c("X_POW_L", 50.55, "M", "powder left wall")
Z_CLO_TOP = c("Z_CLO_TOP", 31.30, "M", "coat closet front (bifolds)")
X_CLO2_L = c("X_CLO2_L", 43.35, "M", "coat closet left wall")
Z_DEN_TOP = c("Z_DEN_TOP", 33.85, "M", "den top / powder & closet bottom")

# ---------------------------------------------------------------- upper floor interior lines
X_UP_WIC2_L = c("X_UP_WIC2_L", 12.60, "M", "second master closet left wall")
X_UP_LIN_L = c("X_UP_LIN_L", 11.25, "M", "master linen left wall")
Z_UP_LIN_TOP = c("Z_UP_LIN_TOP", 20.40, "M", "master linen top")
X_UP_WIC2_DIAG = c("X_UP_WIC2_DIAG", 14.2 + (2 + 4 / 12) / 2, "O", "WIC 2: 45 deg corner wall from the old door's right end to the linen's top-left corner (owner)")
Z_UP_WIC_BOT = c("Z_UP_WIC_BOT", 12.25, "M", "master WIC bottom (right part)")
X_UP_MB_RIDGE = c("X_UP_MB_RIDGE", (26.27 + 42.667 - T) / 2, "O", "master bedroom: ceiling ridge line, centred between the side walls (owner)")
Z_UP_MID = c("Z_UP_MID", 16.146, "M", "master bath corridor bottom / WC & WIC2 top / master bedroom bottom")
Z_UP_WC_BOT = c("Z_UP_WC_BOT", 19.30, "M", "master WC / bath 3 wall")
Z_UP_MBATH_BOT = c("Z_UP_MBATH_BOT", 24 - T, "D", "upper left chain 10'-0\"+14'-0\": master bath bottom")
Z_UP_DRESS_BOT = c("Z_UP_DRESS_BOT", 31.35, "M", "bedroom 2 dressing room bottom")
X_UP_HALLCL_L = c("X_UP_HALLCL_L", 31.90, "M", "hall closet left / bedroom 2 right wall")
X_UP_HALLCL_R = c("X_UP_HALLCL_R", 34.60, "M", "hall closet right wall")
Z_UP_HALLCL_TOP = c("Z_UP_HALLCL_TOP", 35.00, "M", "hall closet top (2'-4 1/2\" opening)")
X_UP_HALL_R = c("X_UP_HALL_R", 41.65, "M", "upper hall right wall")
X_UP_VOID_L = c("X_UP_VOID_L", 36.30, "E", "open-to-foyer rail line")
Z_UP_VOID_TOP = c("Z_UP_VOID_TOP", 33.90, "M", "bedroom 4 top / open-to-foyer rail")
# owner's edited upper plan ("preview-upper-v6-UPDATED")
Z_UP_STAIR_VOID = c("Z_UP_STAIR_VOID", 21.50, "O", "upper floor: bottom of the opening over the stair (owner)")
X_UP_STAIR_ARR = c("X_UP_STAIR_ARR", 29.83, "O", "upper floor: rail along the stair opening from here to the right; open to its left (top of the stair)")
X_UP_BR2_R = c("X_UP_BR2_R", 33.75, "O", "bedroom 2 right wall below the hall closet, also the left side of the open-to-foyer area (owner)")
Z_UP_HCL_TOP = c("Z_UP_HCL_TOP", 30.90, "O", "hall closet top (door), where the 1668 linen was")
Z_UP_RAIL_STUB = c("Z_UP_RAIL_STUB", 32.16, "O", "short wall at the right end of the foyer rail (owner)")
X_UP_CLOS_R = c("X_UP_CLOS_R", 44.80, "M", "bedroom 3 / 4 closet front (6068 BP)")
Z_UP_BR3_CL_BOT = c("Z_UP_BR3_CL_BOT", 24.00, "M", "bedroom 3 closet bottom")
Z_UP_BR4_CL_TOP = c("Z_UP_BR4_CL_TOP", 37.20, "M", "bedroom 4 closet top")
X_UP_BATH2_L = c("X_UP_BATH2_L", 45.11, "M", "bath 2 left wall")
X_UP_BATH2_MID = c("X_UP_BATH2_MID", 50.35, "M", "bath 2 vanity | WC-tub partition")

# ---------------------------------------------------------------- basement lines (8\" concrete + 2x6 walk-out walls)
B_Z_REAR = c("B_Z_REAR", 0.185, "M", "basement rear 2x6 walk-out wall")
B_X_WALK = c("B_X_WALK", 14.915, "M", "basement 2x6 wall with 6080 SGD")
B_Z_STEP = c("B_Z_STEP", 10.144, "M", "basement 2x6 wall with 4040 SL")
B_X_L = c("B_X_L", 4.22, "M", "basement left foundation wall")
B_Z_L_BOT = c("B_Z_L_BOT", 23.40, "M", "basement left part bottom (garage foundation)")
B_X_STEP2 = c("B_X_STEP2", 15.25, "M", "basement wall at garage corner")
B_Z_BOT = c("B_Z_BOT", 27.40, "M", "basement bottom foundation wall")
B_X_R1 = c("B_X_R1", 41.75, "M", "basement rear-right foundation jog")
B_Z_R1 = c("B_Z_R1", 2.19, "M", "basement foundation jog (2'-0\")")
B_X_R2 = c("B_X_R2", 44.52, "M", "basement right foundation wall (great room chase)")
B_Z_R2 = c("B_Z_R2", 16.20, "M", "basement foundation step under dining")
B_X_RR = c("B_X_RR", 55.26, "M", "basement right foundation wall (mechanical)")
B_X_MECH = c("B_X_MECH", 39.90, "M", "mechanical room left wall (owner: no door in it)")
B_X_CRAWL_L = c("B_X_CRAWL_L", 34.50, "M", "crawlspace left foundation wall")
B_Z_CRAWL_PORCH = c("B_Z_CRAWL_PORCH", 39.30, "M", "crawlspace / porch foundation")
B_X_CRAWL_PORCH = c("B_X_CRAWL_PORCH", 42.20, "M", "crawlspace / porch foundation")
# as built: owner's as-built basement sketch (dimensions) + markup "corrections-basement" (the new stair hall / angled
# walls). Provenance O = owner. Sketch positions are good to about +/- 1 ft; written dimensions are used first.
B_X_OFFICE = c("B_X_OFFICE", 16.48, "O", "office 'new wall', 1'-2\" past the old wall on the walk-out line (old wall removed)")
B_X_BATH_TOP = c("B_X_BATH_TOP", 25.20, "O", "bathroom wall toward the stair: 9'-5\" clear (4'-10\" shower + 4'-3\" toilet zone) from the foundation jog")
B_Z_BATH_L = c("B_Z_BATH_L", Z_STAIR_TOP - 4 / 12, "O", "bathroom / closet wall toward the theater: 4\" in front of the stair wall (owner); bathroom 7'-1\" clear")
B_Z_CLOS_BOT = c("B_Z_CLOS_BOT", B_Z_BATH_L + 0.1875 + 41 / 12 + 0.1875, "O", "office closet | toilet area wall: closet 3'-5\" clear (as built), toilet area 3'-3\" clear")
B_X_OFFICE_DOOR = c("B_X_OFFICE_DOOR", B_Z_BATH_L - 0.1875 - 4 / 12 - 1.5, "O", "office door centre: 4\" of wall between it and the closet/bathroom wall (owner)")
B_X_CLOS_TOP = c("B_X_CLOS_TOP", 20.00, "O", "office closet wall toward the bathroom (closet 'enclose for closet', 4'-3\" zone)")
B_Z_STAIR_BOT = c("B_Z_STAIR_BOT", 23.80, "O", "basement stair: its wall toward the mechanical room (owner's edited plan)")
B_X_STAIR_END = c("B_X_STAIR_END", B_X_MECH, "O", "basement stair: its end at the hall, open (owner's edited plan)")
B_Z_HALL_R = c("B_Z_HALL_R", 20.40, "O", "hall: end of its straight wall to the mechanical room (owner's edited plan)")
B_X_HALL_BOT = c("B_X_HALL_BOT", 40.80, "O", "hall: corner of the angled wall to the mechanical room at the stair wall (owner's edited plan)")
B_X_BAFFLE = c("B_X_BAFFLE", B_X_R1 - 0.328 - 0.1875, "O", "theater baffle wall, full width from the rear wall (owner's edited plan); its back touches the 2'-0\" foundation jog, face 25'-11\" from the walk-out wall")
B_Z_BAFFLE_END = c("B_Z_BAFFLE_END", 13.30, "O", "baffle wall end / side wall with the slide-out equipment cabinet (sketch)")
B_Z_SOFFIT = c("B_Z_SOFFIT", Z_STAIR_TOP - 7, "O", "theater / office: 8'-0\" ceiling for the first 7'-0\" from the stair wall (owner); 9'-0\" behind it")
THICK_SOUND = 0.23  # m (9"): "thick sound reducing walls" - no thickness given, assumed

# ---------------------------------------------------------------- vertical (from building sections A5/A6)
FT = 0.3048
H_BASE = (8 + 8 / 12) + (1 + 2.875 / 12)       # 8'-8" slab-to-top-of-foundation + 1'-2 7/8" floor system
H_MAIN = (10 + 1.125 / 12) + (1 + 0.625 / 12)  # 10'-1 1/8" plate + 1'-0 5/8" floor system
H_UP = 8 + 1.125 / 12                          # 8'-1 1/8" upper plate
HEAD_MAIN = 8 + 0.875 / 12                     # Main Floor Note 13: window head 8'-0 7/8"
HEAD_UP = 7 + 0.875 / 12                       # Upper Floor Note 12: window head 7'-0 7/8"
HEAD_BASE = 7 + 0.875 / 12                     # assumption: no basement head height given
DOOR_H = 6 + 8 / 12


def rect(x0, z0, x1, z1):
    return [[x0, z0], [x1, z0], [x1, z1], [x0, z1]]


# rooms: name, points, provenance, note
FLOORS = []

# =============================================================== BASEMENT
B = {"name": "Basement", "elev_ft": -H_BASE, "height_ft": H_BASE, "sheet": "A1", "rooms": [], "walls": [], "doors": [], "windows": [], "furniture": [], "outdoor": []}
B["rooms"] += [
    {"name": "Theater", "prov": "M", "ceiling_ft": 9.0,
     "points": [[B_X_WALK, B_Z_REAR], [B_X_R1, B_Z_REAR], [B_X_R1, B_Z_R1], [B_X_R2, B_Z_R1], [B_X_R2, B_Z_SOFFIT], [B_X_OFFICE, B_Z_SOFFIT], [B_X_OFFICE, B_Z_STEP], [B_X_WALK, B_Z_STEP]],
     "note": "main basement room, 9'-0\" ceiling (owner)"},
    {"name": "Theater (8 ft)", "part_of": "Theater", "prov": "O", "ceiling_ft": 8.0,
     "points": [[B_X_OFFICE, B_Z_SOFFIT], [B_X_R2, B_Z_SOFFIT], [B_X_R2, B_Z_R2], [B_X_STAIR_END, Z_STAIR_TOP], [B_X_BATH_TOP, Z_STAIR_TOP], [B_X_BATH_TOP, B_Z_BATH_L],
                [B_X_CLOS_TOP, B_Z_BATH_L], [B_X_OFFICE, B_Z_BATH_L]],
     "note": "the theater's 7'-0\" strip along the stair wall with an 8'-0\" ceiling (owner); open to the theater"},
    {"name": "Office (9 ft)", "part_of": "Office", "prov": "O", "ceiling_ft": 9.0, "points": [[B_X_L, B_Z_STEP], [B_X_WALK, B_Z_STEP], [B_X_OFFICE, B_Z_STEP], [B_X_OFFICE, B_Z_SOFFIT], [B_X_L, B_Z_SOFFIT]],
     "note": "the office's part behind the 8'-0\" strip, 9'-0\" ceiling (owner); open to the office"},
    {"name": "Office", "prov": "O", "ceiling_ft": 8.0, "points": [[B_X_L, B_Z_SOFFIT], [B_X_OFFICE, B_Z_SOFFIT], [B_X_OFFICE, B_Z_BATH_L], [B_X_WALK, B_Z_BATH_L], [B_X_WALK, B_Z_L_BOT], [B_X_L, B_Z_L_BOT]],
     "note": "as-built 12'-10\" wide; 8'-0\" ceiling from 7'-0\" in front of the stair wall line (owner)"},
    {"name": "Office Closet", "prov": "O", "ceiling_ft": 9.0, "points": [[B_X_WALK, B_Z_BATH_L], [B_X_OFFICE, B_Z_BATH_L], [B_X_CLOS_TOP, B_Z_BATH_L], [B_X_CLOS_TOP, B_Z_CLOS_BOT], [B_X_STEP2, B_Z_CLOS_BOT], [B_X_STEP2, B_Z_L_BOT], [B_X_WALK, B_Z_L_BOT]],
     "note": "'enclose for closet', 3'-5\" clear (as built)"},
    {"name": "Bathroom", "prov": "O", "ceiling_ft": 9.0,
     "points": [[B_X_CLOS_TOP, B_Z_BATH_L], [B_X_BATH_TOP, B_Z_BATH_L], [B_X_BATH_TOP, B_Z_STAIR_BOT], [B_X_BATH_TOP, B_Z_BOT], [B_X_STEP2, B_Z_BOT], [B_X_STEP2, B_Z_CLOS_BOT], [B_X_CLOS_TOP, B_Z_CLOS_BOT]],
     "note": "as built 9'-5\" deep (CH 9'-0\", 7'-11\" over the toilet); tub replaced by a curbless walk-around shower"},
    {"name": "Stairs", "prov": "O", "points": rect(B_X_BATH_TOP, Z_STAIR_TOP, B_X_STAIR_END, B_Z_STAIR_BOT),
     "note": "owner's edited plan: one straight flight, open to the hall at its end"},
    {"name": "Hall", "prov": "O", "points": [[B_X_STAIR_END, Z_STAIR_TOP], [B_X_R2, B_Z_R2], [B_X_R2, B_Z_HALL_R], [B_X_HALL_BOT, B_Z_STAIR_BOT], [B_X_STAIR_END, B_Z_STAIR_BOT]],
     "note": "owner's edited plan: angled walls with 36\" doors to the theater and to the mechanical room"},
    {"name": "Mechanical Room", "prov": "O", "points": [[B_X_R2, B_Z_R2], [B_X_RR, B_Z_R2], [B_X_RR, B_Z_BOT], [B_X_CRAWL_L, B_Z_BOT], [B_X_BATH_TOP, B_Z_BOT], [B_X_BATH_TOP, B_Z_STAIR_BOT],
                                                       [B_X_STAIR_END, B_Z_STAIR_BOT], [B_X_HALL_BOT, B_Z_STAIR_BOT], [B_X_R2, B_Z_HALL_R]],
     "note": "2 water heaters, furnace, sump; runs under the stair to the bathroom (owner's edited plan); entered from the hall"},
    {"name": "Crawlspace", "prov": "M", "points": [[B_X_CRAWL_L, B_Z_BOT], [B_X_RR, B_Z_BOT], [B_X_RR, Z_DEN_FRONT], [B_X_CRAWL_PORCH, Z_DEN_FRONT],
                                                 [B_X_CRAWL_PORCH, B_Z_CRAWL_PORCH], [B_X_CRAWL_L, B_Z_CRAWL_PORCH]],
     "note": "crawlspace #13 under den/foyer; its floor is higher than the basement slab (stepped footing), not modelled"},
]
B["open_edges"] = [{"a": [B_X_STAIR_END, Z_STAIR_TOP], "b": [B_X_STAIR_END, B_Z_STAIR_BOT], "h": 0, "why": "stair open to the hall (owner's edited plan)"},
                   {"a": [B_X_OFFICE, B_Z_SOFFIT], "b": [B_X_R2, B_Z_SOFFIT], "h": 0, "why": "theater: edge of the 8 ft ceiling strip (one room)"},
                   {"a": [B_X_L, B_Z_SOFFIT], "b": [B_X_OFFICE, B_Z_SOFFIT], "h": 0, "why": "office: edge of the 8 ft ceiling strip (one room)"}]
B["thick_edges"] = [
    {"a": [B_X_R2, B_Z_R2], "b": [B_X_STAIR_END, Z_STAIR_TOP], "t": THICK_SOUND, "why": "thick sound reducing wall, theater | hall"},
]
B["walls"] += [
    {"from": [B_X_BAFFLE, B_Z_REAR], "to": [B_X_BAFFLE, B_Z_BAFFLE_END], "thickness_ft": 0.375, "prov": "O", "note": "theater baffle wall with the 130\" 16:9 AT screen"},
    {"from": [B_X_BAFFLE, B_Z_BAFFLE_END], "to": [B_X_R2, B_Z_BAFFLE_END], "thickness_ft": 0.375, "prov": "O", "note": "baffle side wall: slide-out equipment cabinet, hidden door (not modelled)"},
]
B["doors"] += [
    {"at": [B_X_WALK, 4.6], "w": 71 / 12, "h": 7.0, "label": "sliding glass door walk-out, as built 71\" x 84\"", "prov": "O", "style": "sliding"},
    {"at": [B_X_OFFICE, B_X_OFFICE_DOOR], "w": 3.0, "h": DOOR_H, "label": "36\" door office (owner markup)", "prov": "O"},
    {"at": [B_X_WALK, (B_Z_BATH_L + B_Z_L_BOT) / 2], "w": 3.0, "h": DOOR_H, "label": "36\" door office closet", "prov": "O"},
    {"at": [21.60, B_Z_BATH_L], "w": 3.0, "h": DOOR_H, "label": "36\" door bathroom", "prov": "O"},
    {"at": [(B_X_STAIR_END + B_X_R2) / 2, (Z_STAIR_TOP + B_Z_R2) / 2], "w": 3.0, "h": DOOR_H, "label": "36\" door on angle, theater to hall", "prov": "O"},
    {"at": [(B_X_R2 + B_X_HALL_BOT) / 2, (B_Z_HALL_R + B_Z_STAIR_BOT) / 2], "w": 3.0, "h": DOOR_H, "label": "36\" door on angle, hall to mechanical room", "prov": "O"},
]
B["windows"] += [
    {"at": [20.667, B_Z_REAR], "w": 34 / 12, "h": 5, "head": HEAD_BASE, "label": "SH, as built 34\" x 60\"", "prov": "O"},
    {"at": [28.667, B_Z_REAR], "w": 34 / 12, "h": 5, "head": HEAD_BASE, "label": "SH, as built 34\" x 60\"", "prov": "O"},
    {"at": [36.667, B_Z_REAR], "w": 34 / 12, "h": 5, "head": HEAD_BASE, "label": "SH, as built 34\" x 60\"", "prov": "O"},
    {"at": [9.10, B_Z_STEP], "w": 4, "h": 4, "head": HEAD_BASE, "label": "4040 SL", "prov": "M"},
    {"at": [48.0, B_Z_BOT], "w": 2 + 8 / 12, "h": 2.5, "sill": 5.5, "label": "2'-8\" HDR crawlspace access (30x30)", "prov": "E"},
]
B["furniture"] += [
    {"type": "stairs_u", "x": (X_STAIR_L + X_STAIR_R) / 2, "z": (Z_STAIR_TOP + B_Z_BOT) / 2, "w": B_Z_BOT - Z_STAIR_TOP, "d": X_STAIR_R - X_STAIR_L, "rot": 270,
     "mirror": True, "h_ft": H_BASE,
     "label": "UP 16R to main floor (owner's photos): from the hall end up the rear half, landing at the far end, back up the front half to the main floor's down-stair side; the mechanical room runs under the second flight", "prov": "O"},
    {"type": "shower", "x": (B_X_CLOS_TOP + 0.19 + B_X_BATH_TOP - 0.19) / 2, "z": (B_Z_CLOS_BOT + 0.19 + B_Z_BOT - 0.33) / 2, "w": B_X_BATH_TOP - B_X_CLOS_TOP - 0.38, "d": B_Z_BOT - 0.33 - B_Z_CLOS_BOT - 0.19,
     "rot": 0, "label": "curbless walk-around shower, no door (4'-10\")", "prov": "O"},
    {"type": "wc", "x": B_X_STEP2 + 0.33 + 1.2, "z": (B_Z_CLOS_BOT + 0.19 + B_Z_BOT - 0.33) / 2, "w": 1.4, "d": 2.4, "rot": 270, "label": "toilet (moved, owner sketch)", "prov": "O"},
]
FLOORS.append(B)

# =============================================================== MAIN FLOOR
M = {"name": "Main Floor", "elev_ft": 0.0, "height_ft": H_MAIN, "sheet": "A2", "rooms": [], "walls": [], "doors": [], "windows": [], "furniture": [], "outdoor": []}
M["rooms"] += [
    {"name": "3-Car Garage", "prov": "D", "points": [[X_GAR_L, Z_GAR_TOP], [X_BRK_L, Z_GAR_TOP], [X_BRK_L, Z_STAIR_BOT], [X_GAR_R, Z_STAIR_BOT], [X_GAR_R, Z_GAR_DOOR2],
                                                   [X_BRK_L, Z_GAR_DOOR2], [X_BRK_L, Z_GAR_DOOR1], [X_DECK, Z_GAR_DOOR1], [X_DECK, Z_GAR_JOG], [X_GAR_L, Z_GAR_JOG]]},
    {"name": "Laundry", "prov": "D", "points": rect(X_DECK, Z_DECK, X_BRK_L, Z_LAUND_BOT)},
    {"name": "Mud Room", "prov": "M", "points": rect(X_DECK, Z_LAUND_BOT, X_BRK_L, Z_GAR_TOP),
     "note": "owner markup: the pantry wall + pocket door and the coat closet walls + door drawn on A3.1 were not built"},
    {"name": "Breakfast", "prov": "D", "points": rect(X_BRK_L, Z_REAR, X_STAIR_L, Z_BRK_KIT)},
    {"name": "Kitchen", "prov": "M", "points": [[X_BRK_L, Z_BRK_KIT], [X_STAIR_L, Z_BRK_KIT], [X_STAIR_L, Z_STAIR_TOP], [X_STAIR_L, Z_STAIR_BOT], [X_BRK_L, Z_STAIR_BOT],
                                              [X_BRK_L, Z_GAR_TOP], [X_BRK_L, Z_LAUND_BOT], [X_BRK_L, Z_DECK]]},
    {"name": "Living Room", "prov": "D", "points": [[X_STAIR_L, Z_REAR], [X_REAR_R, Z_REAR], [X_REAR_R, Z_CHASE], [X_CHASE, Z_CHASE], [X_CHASE, Z_DIN_TOP], [X_DIN_L, Z_DIN_TOP],
                                                 [X_DIN_L, Z_STAIR_BOT], [X_STAIR_R, Z_STAIR_BOT], [X_STAIR_R, Z_STAIR_MID], [X_STAIR_R, Z_STAIR_TOP], [X_STAIR_L, Z_STAIR_TOP], [X_STAIR_L, Z_BRK_KIT]],
     "note": "'Great Room' on the drawing (owner: living room); includes the 2'-0\" fireplace / TV nook and the hall to the foyer"},
    {"name": "Stairs", "prov": "M", "points": [[X_STAIR_L, Z_STAIR_TOP], [X_STAIR_R, Z_STAIR_TOP], [X_STAIR_R, Z_STAIR_MID], [X_STAIR_R, Z_STAIR_BOT], [X_STAIR_L, Z_STAIR_BOT]]},
    {"name": "Dining Room", "prov": "D", "points": [[X_DIN_L, Z_DIN_TOP], [X_CHASE, Z_DIN_TOP], [X_R, Z_DIN_TOP], [X_R, Z_STAIR_BOT], [X_POW_L, Z_STAIR_BOT], [X_HALF_END, Z_STAIR_BOT], [X_DIN_L, Z_STAIR_BOT]]},
    {"name": "Foyer", "prov": "M", "points": [[X_GAR_R, Z_STAIR_BOT], [X_STAIR_R, Z_STAIR_BOT], [X_DIN_L, Z_STAIR_BOT], [X_HALF_END, Z_STAIR_BOT], [X_POW_L, Z_STAIR_BOT], [X_POW_L, Z_CLO_TOP],
                                            [X_CLO2_L, Z_CLO_TOP], [X_CLO2_L, Z_DEN_TOP], [X_DEN_L, Z_DEN_TOP], [X_DEN_L, Z_FOYER_FRONT], [X_GAR_R, Z_FOYER_FRONT]],
     "note": "2-story foyer incl. the hall to powder, coat closet and den"},
    {"name": "Coat Closet (Foyer)", "prov": "M", "points": rect(X_CLO2_L, Z_CLO_TOP, X_POW_L, Z_DEN_TOP)},
    {"name": "Powder", "prov": "M", "points": rect(X_POW_L, Z_STAIR_BOT, X_R, Z_DEN_TOP)},
    {"name": "Playroom", "prov": "D", "note": "'Den / Flex' on the drawing (owner: playroom)", "points": rect(X_DEN_L, Z_DEN_TOP, X_R, Z_DEN_FRONT)},
]
# edges without walls / lower walls (applied to the full NeonPlan file only; the simple format has no such field)
M["open_edges"] = [
    {"a": [X_STAIR_L, Z_REAR], "b": [X_STAIR_L, Z_BRK_KIT], "h": 0, "why": "breakfast | great room open (1'-0\" pier only)"},
    {"a": [X_BRK_L, Z_BRK_KIT], "b": [X_STAIR_L, Z_BRK_KIT], "h": 0, "why": "breakfast | kitchen open"},
    {"a": [X_STAIR_L, Z_BRK_KIT], "b": [X_STAIR_L, Z_STAIR_TOP], "h": 0, "why": "kitchen | great room open"},
    {"a": [X_DIN_L, Z_DIN_TOP], "b": [X_DIN_L, Z_STAIR_BOT], "h": 0, "why": "dining flat arch #34"},
    {"a": [X_STAIR_R, Z_STAIR_BOT], "b": [X_DIN_L, Z_STAIR_BOT], "h": 0, "why": "great-room hall | foyer, columns + flat arch"},
    {"a": [X_DIN_L, Z_STAIR_BOT], "b": [X_HALF_END, Z_STAIR_BOT], "h": 0.914, "why": "#22 half wall 36\" AFF (A6: '30\" AFF wall')"},
    {"a": [X_STAIR_L, Z_STAIR_TOP], "b": [X_STAIR_R, Z_STAIR_TOP], "h": 0.914, "why": "#10 handrail at stair"},
    {"a": [X_STAIR_R, Z_STAIR_TOP], "b": [X_STAIR_R, Z_STAIR_MID], "h": 0, "why": "stair up: open end facing the dining room (owner)"},
    {"a": [X_STAIR_R, Z_STAIR_MID], "b": [X_STAIR_R, Z_STAIR_BOT], "h": 0, "why": "stair down: open end facing the dining room (owner)"},
]
M["walls"] += [{"from": [X_STAIR_L, Z_STAIR_MID], "to": [X_STAIR_R, Z_STAIR_MID], "thickness_ft": 0.375, "prov": "O",
                "note": "divider wall between the up stair (rear half) and the down stair (front half) (owner); full height assumed"}]
M["doors"] += [
    {"at": [36.8, Z_FOYER_FRONT], "w": 3, "h": DOOR_H, "label": "3068 front door (#34 porch)", "prov": "M"},
    {"at": [X_DEN_L, 36.3], "w": 4, "h": DOOR_H, "label": "2-2068 den french doors", "prov": "M"},
    {"at": [45.2, Z_CLO_TOP], "w": 3.3, "h": DOOR_H, "label": "2-2068 bifold pair (angled)", "prov": "E"},
    {"at": [48.7, Z_CLO_TOP], "w": 3.3, "h": DOOR_H, "label": "2-2068 bifold pair (angled)", "prov": "E"},
    {"at": [X_POW_L, 29.4], "w": 2 + 4 / 12, "h": DOOR_H, "label": "2468 powder", "prov": "M"},
    {"at": [12.33, Z_GAR_TOP], "w": 2 + 8 / 12, "h": DOOR_H, "label": "2868 #4 self-closing rated door, garage", "prov": "M"},
    {"at": [X_BRK_L, 22.0], "w": 3.0, "h": DOOR_H, "label": "opening mud room | kitchen, no door (owner)", "prov": "O", "style": "passage"},
    {"at": [10.2, Z_LAUND_BOT], "w": 2 + 8 / 12, "h": DOOR_H, "label": "2868 PKT laundry", "prov": "M"},
    {"at": [X_BRK_L, 5.0], "w": 6, "h": DOOR_H, "label": "6080 SGD to covered deck", "prov": "M", "style": "sliding"},
    {"at": [50.333, Z_DIN_TOP], "w": 9.0, "h": 8.0, "label": "sliding glass door to the dining deck, 108\" x 8'-0\" (owner; replaces 3 x 2650 SH, centred on them)", "prov": "O", "style": "sliding"},
    {"at": [9.333, Z_GAR_DOOR1], "w": 8, "h": 8, "label": "8080 O.G.D.", "prov": "D"},
    {"at": [24.833, Z_GAR_DOOR2], "w": 16, "h": 8, "label": "16080 O.G.D.", "prov": "D"},
]
WT = dict(head=HEAD_MAIN)
M["windows"] += [
    *[{"at": [x, Z_REAR], "w": 3, "h": 5, **WT, "label": "3050 SH", "prov": "D"} for x in (18.208, 21.917, 29.167, 32.667, 36.167, 39.667)],
    *[{"at": [x, Z_REAR], "w": 3, "h": 1.75, "sill": HEAD_MAIN + 0.33, "label": "3020 TRANS (height cut to fit under 10'-1 1/8\" plate)", "prov": "D"} for x in (18.208, 21.917, 29.167, 32.667, 36.167, 39.667)],
    *[{"at": [x, Z_DIN_TOP], "w": 2.5, "h": 1.75, "sill": HEAD_MAIN + 0.33, "label": "2620 TRANS", "prov": "D"} for x in (47.333, 50.333, 53.333)],
    *[{"at": [X_R, z], "w": 2, "h": 2, **WT, "label": "2020 FX", "prov": "D"} for z in (19.333, 21.833, 24.333)],
    {"at": [X_R, 29.875], "w": 2, "h": 2, **WT, "label": "2020 FX powder", "prov": "D"},
    {"at": [X_R, 36.42], "w": 3, "h": 6, **WT, "label": "3060 SH den", "prov": "D"},
    *[{"at": [x, Z_DEN_FRONT], "w": w, "h": 6, **WT, "label": f"{int(w)}060 SH den", "prov": "D"} for x, w in ((45.75, 2), (49.0, 3.5), (52.25, 2))],
    {"at": [X_DECK, 14.458], "w": 2.5, "h": 3.5, **WT, "label": "2636 SH laundry", "prov": "D"},
    {"at": [X_DECK, 14.458], "w": 2.5, "h": 1.75, "sill": HEAD_MAIN + 0.33, "label": "2620 TRANS laundry", "prov": "D"},
    {"at": [39.0, Z_FOYER_FRONT], "w": 1 + 2 / 12, "h": DOOR_H, "sill": 0.0, "label": "1268 sidelight", "prov": "M"},
    {"at": [37.55, Z_FOYER_FRONT], "w": 4.5, "h": 1.5, "sill": DOOR_H + 0.25, "label": "4616 TRANS over front door", "prov": "M"},
]
# fix 3660 label
for w in M["windows"]:
    if w["label"] == "3060 SH den" and w["at"][1] == Z_DEN_FRONT:
        w["label"] = "3660 SH den"
M["furniture"] += [
    {"type": "stairs_u", "x": (X_STAIR_L + X_STAIR_R) / 2, "z": (Z_STAIR_TOP + B_Z_BOT) / 2, "w": B_Z_BOT - Z_STAIR_TOP, "d": X_STAIR_R - X_STAIR_L, "rot": 270,
     "mirror": True, "h_ft": H_MAIN,
     "label": "UP 18R: 8 treads, landing, 7 treads (A6; owner's photos): up the rear half from the dining side, landing at the far end, back up over the down stair to the upper hall", "prov": "M"},
    {"type": "fridge", "x": 18.5, "z": 26.3, "w": 3.0, "d": 2.4, "rot": 180, "label": "REF.", "prov": "M"},
    {"type": "kitchen_tall", "x": 16.2, "z": 26.2, "w": 2.4, "d": 2.3, "rot": 180, "label": "double oven", "prov": "M"},
    {"type": "kitchen", "x": 21.8, "z": 26.3, "w": 4.4, "d": 2.0, "rot": 180, "label": "base cabinets", "prov": "M"},
    {"type": "kitchen", "x": 15.85, "z": 15.1, "w": 9.6, "d": 2.0, "rot": 270, "label": "base cabinets (220V range position at ~12.8)", "prov": "M"},
    {"type": "kitchen", "x": 25.1, "z": 23.5, "w": 6.9, "d": 2.0, "rot": 90, "label": "base cabinets under 24\" soffit", "prov": "M"},
    # fireplace + built-in TV cabinet in the 2'-0" nook (owner). NeonPlan has no fireplace; its own importers use a sideboard.
    {"type": "sideboard", "x": (X_REAR_R + X_CHASE) / 2, "z": Z_CHASE + (Z_DIN_TOP - Z_CHASE) / 6, "w": (Z_DIN_TOP - Z_CHASE) / 3 - 0.2, "d": X_CHASE - X_REAR_R - 0.3, "rot": 90, "show": "fireplace",
     "label": "fireplace: 1/3 of the nook (owner); rear end assumed", "prov": "O"},
    {"type": "tv_board", "x": (X_REAR_R + X_CHASE) / 2, "z": Z_CHASE + (Z_DIN_TOP - Z_CHASE) * 2 / 3, "w": (Z_DIN_TOP - Z_CHASE) * 2 / 3 - 0.2, "d": X_CHASE - X_REAR_R - 0.3, "rot": 90, "show": "TV cabinet",
     "label": "built-in TV cabinet: the other 2/3 of the nook (owner)", "prov": "O"},
    {"type": "island", "x": 22.8, "z": 10.7, "w": 10.0, "d": 40 / 12, "rot": 90, "label": "kitchen island approx. 10'-0\" x 3'-4\" (owner markup; position from the sketch, +/- 1 ft)", "prov": "E"},
    {"type": "dryer", "x": 13.45, "z": 11.55, "w": 2.2, "d": 2.2, "rot": 90, "label": "#24 +36 220V", "prov": "M"},
    {"type": "washer", "x": 13.45, "z": 14.3, "w": 2.2, "d": 2.2, "rot": 90, "label": "#2 washer box", "prov": "M"},
]
M["outdoor"] += [
    {"type": "terrace", "name": "Covered Deck", "points": rect(X_DECK - T, Z_REAR - T, X_BRK_L - T, Z_DECK - T), "prov": "D"},
    {"type": "terrace", "name": "Uncovered Deck", "points": rect(X_DECK - T, -7.0, X_BRK_L - T, Z_REAR - T), "prov": "D"},
    {"type": "terrace", "name": "Porch", "points": rect(X_GAR_R, Z_FOYER_FRONT, X_DEN_L, Z_DEN_FRONT), "prov": "M"},
    {"type": "terrace", "name": "Dining Deck", "points": rect(X_CHASE + T, Z_DIN_TOP - T - 18, X_CHASE + T + 20, Z_DIN_TOP - T), "prov": "E",
     "note": "owner markup: approx. 20 ft wide x 18 ft deep, against the dining wall from the fireplace chase; exact position unconfirmed"},
]
FLOORS.append(M)

# =============================================================== UPPER FLOOR
U = {"name": "Upper Floor", "elev_ft": H_MAIN, "height_ft": H_UP, "sheet": "A3", "rooms": [], "walls": [], "doors": [], "windows": [], "furniture": [], "outdoor": []}
U["rooms"] += [
    {"name": "Master Bedroom", "prov": "D", "points": rect(X_STAIR_L, Z_REAR, X_UP_MB_RIDGE, Z_UP_MID), "gable": True,
     "note": "pitched ceiling 8'-0\" at the side walls to 12'-0\" at the centre line, ridge running from the window wall (owner); left half"},
    {"name": "Master Bedroom (right)", "part_of": "Master Bedroom", "prov": "D", "points": rect(X_UP_MB_RIDGE, Z_REAR, X_REAR_R, Z_UP_MID), "gable": True,
     "note": "right half of the master bedroom, open to the left half (NeonPlan walls slope only from one end of an edge to the other)"},
    {"name": "Master WIC", "prov": "D", "points": [[X_BRK_L, Z_WIC_TOP], [X_STAIR_L, Z_WIC_TOP], [X_STAIR_L, Z_UP_WIC_BOT], [X_UP_BR2_L, Z_UP_WIC_BOT], [X_UP_BR2_L, Z_DECK], [X_BRK_L, Z_DECK]]},
    {"name": "Master Bath", "prov": "M", "points": [[X_DECK, Z_DECK], [X_BRK_L, Z_DECK], [X_UP_BR2_L, Z_DECK], [X_UP_BR2_L, Z_UP_WIC_BOT], [X_STAIR_L, Z_UP_WIC_BOT], [X_STAIR_L, Z_UP_MID],
                                                  [X_UP_BR2_L, Z_UP_MID], [X_UP_WIC2_DIAG, Z_UP_MID], [X_UP_LIN_L, Z_UP_LIN_TOP], [X_UP_LIN_L, Z_UP_MBATH_BOT], [X_DECK, Z_UP_MBATH_BOT]]},
    {"name": "Master Linen", "prov": "M", "points": rect(X_UP_LIN_L, Z_UP_LIN_TOP, X_UP_WIC2_L, Z_UP_MBATH_BOT)},
    {"name": "Master WIC 2", "prov": "M", "points": [[X_UP_WIC2_DIAG, Z_UP_MID], [X_UP_BR2_L, Z_UP_MID], [X_UP_BR2_L, Z_UP_MBATH_BOT], [X_UP_WIC2_L, Z_UP_MBATH_BOT], [X_UP_WIC2_L, Z_UP_LIN_TOP], [X_UP_LIN_L, Z_UP_LIN_TOP]],
     "note": "second 'WIC' on the drawing; its door corner cut at 45 deg (owner)"},
    {"name": "Master WC", "prov": "M", "points": rect(X_UP_BR2_L, Z_UP_MID, X_STAIR_L, Z_UP_WC_BOT), "note": "unnamed toilet room of the master bath"},
    {"name": "Bath 3", "prov": "M", "points": rect(X_UP_BR2_L, Z_UP_WC_BOT, X_STAIR_L, Z_STAIR_BOT), "note": "plan label 'Bath 2' corrected by hand to 'Bath 3' (A6 stair section: 'Bath 3')"},
    {"name": "Bedroom 2 Dressing", "prov": "D", "points": rect(X_BRK_L, Z_UP_MBATH_BOT, X_UP_BR2_L, Z_UP_DRESS_BOT), "note": "unnamed room between bath 3 and bedroom 2"},
    {"name": "Bedroom 2", "prov": "D", "points": [[X_UP_BR2_L, Z_STAIR_BOT], [X_STAIR_L, Z_STAIR_BOT], [X_UP_HALLCL_L, Z_STAIR_BOT], [X_UP_HALLCL_L, Z_UP_HCL_TOP], [X_UP_HALLCL_L, Z_UP_VOID_TOP],
                                                [X_UP_BR2_R, Z_UP_VOID_TOP], [X_UP_BR2_R, Z_UP_FRONT_L],
                                                [X_BAY_R, Z_UP_FRONT_L], [X_BAY_R, Z_BAY], [X_BAY_L, Z_BAY], [X_BAY_L, Z_UP_FRONT_L], [X_UP_BR2_L, Z_UP_FRONT_L], [X_UP_BR2_L, Z_UP_DRESS_BOT]],
     "note": "with the window-seat bay; takes in the old hall closet (owner's edited plan)"},
    {"name": "Hall Closet", "prov": "O", "points": rect(X_UP_HALLCL_L, Z_UP_HCL_TOP, X_UP_BR2_R, Z_UP_VOID_TOP),
     "note": "where the 1668 linen was (owner); its bottom put on the foyer rail line (drawn 3.6\" higher)"},
    {"name": "Stairs", "prov": "O", "points": [[X_STAIR_L, Z_UP_STAIR_VOID], [X_UP_STAIR_ARR, Z_UP_STAIR_VOID], [X_STAIR_R, Z_UP_STAIR_VOID], [X_STAIR_R, Z_STAIR_BOT], [X_STAIR_L, Z_STAIR_BOT]],
     "note": "top of the stair; the opening over the stair (x 26.27-35.80, z 16.15-21.50) is left out of the floor (owner)"},
    {"name": "Upper Hall", "prov": "M", "points": [[X_STAIR_R, Z_UP_MID], [X_UP_HALL_R, Z_UP_MID], [X_UP_HALL_R, Z_UP_BR3_CL_BOT], [X_UP_HALL_R, Z_STAIR_BOT], [X_UP_BATH2_L, Z_STAIR_BOT],
                                                 [X_UP_BATH2_L, Z_UP_VOID_TOP], [X_UP_HALL_R, Z_UP_VOID_TOP], [X_UP_BR2_R, Z_UP_VOID_TOP], [X_UP_BR2_R, Z_UP_HCL_TOP], [X_UP_HALLCL_L, Z_UP_HCL_TOP],
                                                 [X_UP_HALLCL_L, Z_STAIR_BOT], [X_STAIR_R, Z_STAIR_BOT], [X_STAIR_R, Z_UP_STAIR_VOID]],
     "note": "landing + hall; the stair opening and the open-to-foyer area (x 33.75-41.65, z 33.9-39.85) are left out of the floor"},
    {"name": "Bedroom 3", "prov": "D", "points": [[X_UP_CLOS_R, Z_DIN_TOP], [X_R, Z_DIN_TOP], [X_R, Z_STAIR_BOT], [X_UP_BATH2_L, Z_STAIR_BOT], [X_UP_HALL_R, Z_STAIR_BOT], [X_UP_HALL_R, Z_UP_BR3_CL_BOT], [X_UP_CLOS_R, Z_UP_BR3_CL_BOT]]},
    {"name": "Bedroom 3 Closet", "prov": "M", "points": rect(X_UP_HALL_R, Z_DIN_TOP, X_UP_CLOS_R, Z_UP_BR3_CL_BOT)},
    {"name": "Bath 2", "prov": "M", "points": rect(X_UP_BATH2_L, Z_STAIR_BOT, X_R, Z_UP_VOID_TOP)},
    {"name": "Bedroom 4", "prov": "D", "points": [[X_UP_HALL_R, Z_UP_VOID_TOP], [X_UP_BATH2_L, Z_UP_VOID_TOP], [X_R, Z_UP_VOID_TOP], [X_R, Z_DEN_FRONT], [X_UP_CLOS_R, Z_DEN_FRONT], [X_UP_CLOS_R, Z_UP_BR4_CL_TOP], [X_UP_HALL_R, Z_UP_BR4_CL_TOP]]},
    {"name": "Bedroom 4 Closet", "prov": "M", "points": rect(X_UP_HALL_R, Z_UP_BR4_CL_TOP, X_UP_CLOS_R, Z_DEN_FRONT)},
]
U["open_edges"] = [
    {"a": [X_UP_MB_RIDGE, Z_REAR], "b": [X_UP_MB_RIDGE, Z_UP_MID], "h": 0, "why": "master bedroom: its two halves are one room (ceiling ridge)"},
    {"a": [X_STAIR_R, Z_UP_MID], "b": [X_STAIR_R, Z_UP_STAIR_VOID], "h": 0.914, "why": "rail along the stair opening (owner)"},
    {"a": [X_UP_STAIR_ARR, Z_UP_STAIR_VOID], "b": [X_STAIR_R, Z_UP_STAIR_VOID], "h": 0.914, "why": "rail along the stair opening (owner)"},
    {"a": [X_STAIR_L, Z_UP_STAIR_VOID], "b": [X_UP_STAIR_ARR, Z_UP_STAIR_VOID], "h": 0, "why": "top of the stair (owner)"},
    {"a": [X_STAIR_R, Z_UP_STAIR_VOID], "b": [X_STAIR_R, Z_STAIR_BOT], "h": 0, "why": "stair top open to the hall (owner)"},
    {"a": [X_UP_HALL_R, Z_UP_VOID_TOP], "b": [X_UP_BR2_R, Z_UP_VOID_TOP], "h": 0.914, "why": "rail, open to foyer below"},
]
U["walls"] += [
    {"from": [X_UP_BR2_R, Z_UP_FRONT_L], "to": [X_UP_HALL_R, Z_UP_FRONT_L], "thickness_ft": 0.45, "prov": "D", "note": "front wall of the 2-story foyer"},
    {"from": [X_UP_HALL_R, Z_UP_RAIL_STUB], "to": [X_UP_HALL_R, Z_UP_VOID_TOP], "thickness_ft": 0.375, "prov": "O", "note": "short wall at the end of the foyer rail (owner)"},
    {"from": [X_UP_BATH2_MID, Z_STAIR_BOT], "to": [X_UP_BATH2_MID, Z_UP_VOID_TOP], "thickness_ft": 0.29, "prov": "M", "note": "bath 2 vanity | WC-tub partition"},
]
U["doors"] += [
    {"at": [X_UP_HALLCL_L, 29.3], "w": 2.5, "h": DOOR_H, "label": "2668 bedroom 2", "prov": "E"},
    {"at": [X_UP_BR2_L, 29.9], "w": 2.5, "h": DOOR_H, "label": "2668 dressing | bedroom 2", "prov": "M"},
    {"at": [21.70, Z_STAIR_BOT], "w": 2 + 4 / 12, "h": DOOR_H, "label": "2468 bath 3, in its bottom wall (owner markup; opening x 20.5-22.9 on A3.2)", "prov": "M"},
    {"at": [32.67, Z_UP_HCL_TOP], "w": 1.5, "h": DOOR_H, "label": "1668 hall closet (owner: the old linen door)", "prov": "O"},
    {"at": [39.27, Z_UP_MID], "w": 4 + 8 / 12, "h": DOOR_H, "label": "(2) 2468 master bedroom double doors (owner markup; A3.2 width x 36.95-41.6)", "prov": "M"},
    {"at": [X_STAIR_L, 14.4], "w": 2 + 9.5 / 12, "h": DOOR_H, "label": "master bedroom | bath opening 2'-9 1/2\"", "prov": "D"},
    {"at": [21.80, Z_UP_WIC_BOT], "w": 2 + 4 / 12, "h": DOOR_H, "label": "2468 master WIC, in its bottom wall (owner markup; opening x 20.6-23.0 on A3.2)", "prov": "M"},
    {"at": [21.45, Z_UP_MID], "w": 2 + 4 / 12, "h": DOOR_H, "label": "2468 master WC (drawn at 45 deg)", "prov": "E"},
    {"at": [(X_UP_WIC2_DIAG + X_UP_LIN_L) / 2, (Z_UP_MID + Z_UP_LIN_TOP) / 2], "w": 2 + 4 / 12, "h": DOOR_H, "label": "2468 WIC 2, in the 45 deg corner wall (owner)", "prov": "O"},
    {"at": [X_UP_LIN_L, 22.23], "w": 2.5, "h": DOOR_H, "label": "master linen door (owner)", "prov": "O"},
    {"at": [43.40, Z_STAIR_BOT], "w": 2.5, "h": DOOR_H, "label": "2668 bedroom 3, in its bottom wall (owner markup; opening x 42.0-44.8 on A3.2)", "prov": "M"},
    {"at": [X_UP_CLOS_R, 20.0], "w": 6, "h": DOOR_H, "label": "6068 BP", "prov": "M"},
    {"at": [48.6, Z_STAIR_BOT], "w": 2 + 4 / 12, "h": DOOR_H, "label": "bath 2 from bedroom 3", "prov": "E"},
    {"at": [48.3, Z_UP_VOID_TOP], "w": 2 + 4 / 12, "h": DOOR_H, "label": "2468 bath 2 from bedroom 4 (45 deg)", "prov": "E"},
    {"at": [X_UP_BATH2_MID, 32.25], "w": 2 + 4 / 12, "h": DOOR_H, "label": "2468 bath 2 WC/tub (owner markup; opening z 30.9-33.6 on A3.2)", "prov": "M"},
    {"at": [43.30, Z_UP_VOID_TOP], "w": 2.5, "h": DOOR_H, "label": "2668 bedroom 4, in its top wall (owner markup; opening x 42.0-44.6 on A3.2)", "prov": "M"},
    {"at": [X_UP_CLOS_R, 41.5], "w": 6, "h": DOOR_H, "label": "6068 BP", "prov": "M"},
]
WU = dict(head=HEAD_UP)
U["windows"] += [
    *[{"at": [x, Z_REAR], "w": 3, "h": 5, **WU, "label": "3050 SH", "prov": "D"} for x in (29.167, 32.667, 36.167, 39.667)],
    {"at": [6.708, Z_DECK], "w": 4, "h": 4, **WU, "label": "4040 SL (TEMP)", "prov": "D"},
    {"at": [X_DECK, 14.5], "w": 6, "h": 4, **WU, "label": "6040 FX (TEMP)", "prov": "D"},
    {"at": [50.0, Z_DIN_TOP], "w": 6, "h": 5, **WU, "label": "6050 SL #8", "prov": "D"},
    {"at": [49.0, Z_DEN_FRONT], "w": 3.5, "h": 5.5, **WU, "label": "3656 ARCHTOP", "prov": "D"},
    {"at": [25.75, Z_BAY], "w": 3, "h": 5, **WU, "label": "3050 SH", "prov": "D"},
    {"at": [29.25, Z_BAY], "w": 3, "h": 5, **WU, "label": "3050 SH #8", "prov": "D"},
    {"at": [38.3, Z_UP_FRONT_L], "w": 2, "h": 2, **WU, "label": "2020 FX (foyer, upper level)", "prov": "M"},
]
U["furniture"] += [
    {"type": "bathtub", "x": 6.6, "z": 14.6, "w": 6.0, "d": 3.5, "rot": 270, "label": "42\"x72\" tub", "prov": "M"},
    {"type": "shower", "x": (X_DECK + 0.23 + 8.39) / 2, "z": (18.58 + Z_UP_MBATH_BOT - 0.23) / 2, "w": Z_UP_MBATH_BOT - 0.23 - 18.58, "d": 8.39 - X_DECK - 0.23, "rot": 270, "label": "shower, wall to wall (owner)", "prov": "O"},
    {"type": "sink", "x": 10.85, "z": 11.15, "w": 3.5, "d": 1.8, "rot": 0, "label": "master vanity: basin 1 (one counter x 9.1-20.0, owner markup)", "prov": "M"},
    {"type": "worktop", "x": 14.45, "z": 11.15, "w": 3.7, "d": 1.8, "rot": 0, "label": "master vanity: counter between the basins", "prov": "M"},
    {"type": "sink", "x": 18.15, "z": 11.15, "w": 3.7, "d": 1.8, "rot": 0, "label": "master vanity: basin 2", "prov": "M"},
    {"type": "wc", "x": 24.7, "z": 17.5, "w": 1.4, "d": 2.4, "rot": 90, "label": "master WC", "prov": "M"},
    {"type": "bathtub", "x": 22.6, "z": 20.6, "w": 5.0, "d": 2.7, "rot": 0, "label": "bath 3 tub", "prov": "M"},
    {"type": "wc", "x": 24.8, "z": 23.0, "w": 1.4, "d": 2.4, "rot": 90, "label": "bath 3 WC", "prov": "M"},
    {"type": "washbasin", "x": 25.0, "z": 26.0, "w": 2.0, "d": 1.8, "rot": 90, "label": "bath 3 lav", "prov": "M"},
    {"type": "washbasin", "x": 46.0, "z": 29.2, "w": 1.8, "d": 1.8, "rot": 270, "label": "bath 2 sink", "prov": "M"},
    {"type": "washbasin", "x": 46.0, "z": 31.6, "w": 1.8, "d": 1.8, "rot": 270, "label": "bath 2 sink", "prov": "M"},
    {"type": "wc", "x": 51.8, "z": 29.4, "w": 1.4, "d": 2.4, "rot": 0, "label": "bath 2 WC", "prov": "M"},
    {"type": "bathtub", "x": 54.5, "z": 31.0, "w": 5.0, "d": 2.6, "rot": 90, "label": "bath 2 tub/shower", "prov": "M"},
]
FLOORS.append(U)

# ceilings (owner): main floor 10'-0" (not the 2-storey foyer or the open stair), upper floor 8'-0" (master bedroom pitched
# 8'-0" to 12'-0", see "gable"); basement as set per room above
for r in M["rooms"]:
    if r["name"] not in ("Foyer", "Stairs"):
        r.setdefault("ceiling_ft", 10.0)
for r in U["rooms"]:
    r.setdefault("ceiling_ft", 8.0)
GABLE = {"ridge_x": X_UP_MB_RIDGE, "half": X_UP_MB_RIDGE - X_STAIR_L, "low_ft": 8.0, "high_ft": 12.0}
