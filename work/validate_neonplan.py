#!/usr/bin/env python3
"""Validate neonplan_house.json (neonplan-import format) for structure and geometry.

usage: python3 validate_neonplan.py [path/to/neonplan_house.json] [--json report.json]
Exit code 0 = no errors (warnings allowed), 1 = errors."""
import json, math, sys, itertools
from shapely.geometry import Polygon, LineString, Point
from shapely.ops import unary_union

ALLOWED_TOP = {"format", "units", "rooms_at", "floors"}
ALLOWED_FLOOR = {"name", "elevation", "height", "rooms", "walls", "doors", "windows", "furniture"}
ALLOWED = {"rooms": {"name", "points"}, "walls": {"from", "to", "thickness", "height"}, "doors": {"at", "width", "height"},
           "windows": {"at", "width", "height", "sill", "sill_board"}, "furniture": {"type", "name", "at", "width", "depth", "height", "rotation", "elevation"}}
FURN = set("sofa sofa_l sofa_u armchair stool coffee_table tv_board tv_wall sideboard shelf plant rug table table_round chair bench corner_bench bar_stool "
           "kitchen kitchen_wall kitchen_tall island worktop sink stove dishwasher fridge bed bunk_bed nightstand wardrobe dresser bathtub shower wc washbasin "
           "washer dryer desk office_chair tall_cabinet coat_rack stairs stairs_u radiator ac_unit robot_vacuum lamp_ceiling lamp_downlight lamp_spot lamp_panel "
           "lamp_pendant lamp_floor lamp_table lamp_wall led_strip".split())
TOL = 0.005     # m: coordinates closer than this count as the same point
REACH = 0.35    # m: the import page snaps an opening onto an edge within ~0.35 m (builder.ts); we demand much less
ON_EDGE = 0.02  # m: our requirement for "on the wall line"

# expected overall extents (wall centre lines, metres) from the architect's 52'-0" / 56'-0" / 48'-0" / 46'-0" strings
FT = 0.3048
T = 1.75 / 12
EXPECT = {"Main Floor": ((56 - 2 * T) * FT, (48 - 2 * T) * FT), "Upper Floor": ((52 - 2 * T) * FT, (46 - 2 * T) * FT)}

errors, warnings, info = [], [], []


def E(m): errors.append(m)
def W(m): warnings.append(m)
def I(m): info.append(m)


def area(P):
    return sum(P[i][0] * P[(i + 1) % len(P)][1] - P[(i + 1) % len(P)][0] * P[i][1] for i in range(len(P))) / 2


def edges(rooms):
    for ri, r in enumerate(rooms):
        P = r["points"]
        for i in range(len(P)):
            yield ri, i, tuple(P[i]), tuple(P[(i + 1) % len(P)])


def proj(p, a, b):
    dx, dz = b[0] - a[0], b[1] - a[1]
    L = math.hypot(dx, dz)
    t = ((p[0] - a[0]) * dx + (p[1] - a[1]) * dz) / (L * L)
    tc = min(1, max(0, t))
    q = (a[0] + tc * dx, a[1] + tc * dz)
    return math.hypot(p[0] - q[0], p[1] - q[1]), t * L, L


def main(path):
    try:
        d = json.load(open(path))
    except Exception as ex:
        E(f"JSON does not parse: {ex}"); return None
    I("JSON parses")
    for k in d:
        if k not in ALLOWED_TOP: E(f"unsupported top-level field '{k}'")
    if d.get("format") != "neonplan-import": E("format is not 'neonplan-import'")
    if d.get("units") != "m": E("units is not 'm'")
    if d.get("rooms_at") != "centre": E("rooms_at is not 'centre'")
    floors = d.get("floors")
    if not isinstance(floors, list) or not floors: E("no floors"); return d
    elev = [f.get("elevation") for f in floors]
    if elev != sorted(elev): E(f"floors not ordered lowest first: {elev}")
    for a, b in zip(floors, floors[1:]):
        if abs(a["elevation"] + a["height"] - b["elevation"]) > 0.01:
            W(f"'{a['name']}' elevation+height ({a['elevation'] + a['height']:.3f}) != next floor elevation {b['elevation']:.3f}")
    if 0 not in elev: E("no floor at elevation 0")
    outlines = {}
    for f in floors:
        fn = f.get("name")
        for k in f:
            if k not in ALLOWED_FLOOR: E(f"[{fn}] unsupported floor field '{k}'")
        if not isinstance(fn, str) or not fn: E("floor without name")
        if not isinstance(f.get("elevation"), (int, float)): E(f"[{fn}] elevation missing")
        if not isinstance(f.get("height"), (int, float)) or not (1.8 <= f["height"] <= 8): E(f"[{fn}] height missing or outside 1.8-8 m")
        rooms = f.get("rooms", [])
        polys = []
        wind = set()
        for r in rooms:
            for k in r:
                if k not in ALLOWED["rooms"]: E(f"[{fn}] room '{r.get('name')}' unsupported field '{k}'")
            P = r["points"]; nm = r["name"]
            if len(P) < 3: E(f"[{fn}] '{nm}' has < 3 points"); continue
            if len({(round(p[0], 3), round(p[1], 3)) for p in P}) < 3: E(f"[{fn}] '{nm}' < 3 distinct corners")
            for i in range(len(P)):
                if math.hypot(P[i][0] - P[(i + 1) % len(P)][0], P[i][1] - P[(i + 1) % len(P)][1]) < TOL:
                    E(f"[{fn}] '{nm}' duplicate consecutive point {P[i]}")
            if P[0] == P[-1]: E(f"[{fn}] '{nm}' repeats its first corner")
            a = area(P)
            if abs(a) < 0.3: E(f"[{fn}] '{nm}' area {abs(a):.2f} m2 (import page drops rooms < 0.3 m2)")
            wind.add(a > 0)
            pg = Polygon(P)
            if not pg.is_valid: E(f"[{fn}] '{nm}' self-intersecting / invalid polygon")
            # collinear interior vertices are allowed (they split a shared wall), count them
            xs = [p[0] for p in P]; zs = [p[1] for p in P]
            w, h = max(xs) - min(xs), max(zs) - min(zs)
            if min(w, h) < 0.6: W(f"[{fn}] '{nm}' is only {min(w, h):.2f} m wide")
            if abs(a) > 120: W(f"[{fn}] '{nm}' unusually large: {abs(a):.1f} m2")
            polys.append((nm, pg))
        if len(wind) > 1: E(f"[{fn}] mixed polygon winding")
        else: I(f"[{fn}] consistent winding ({'clockwise on screen' if wind == {True} else 'counter-clockwise on screen'})")
        # overlaps
        for (n1, p1), (n2, p2) in itertools.combinations(polys, 2):
            ov = p1.intersection(p2).area
            if ov > 0.01: E(f"[{fn}] rooms overlap: '{n1}' / '{n2}' {ov:.3f} m2")
        # shared boundaries: a vertex of one room lying on another room's edge must be a vertex of that room too
        verts = [(r["name"], tuple(p)) for r in rooms for p in r["points"]]
        E_ = list(edges(rooms))
        tjoint = 0
        for nm, v in verts:
            for ri, i, a, b in E_:
                if rooms[ri]["name"] == nm: continue
                dist, s, L = proj(v, a, b)
                if dist < TOL and TOL < s < L - TOL:
                    tjoint += 1
        I(f"[{fn}] {tjoint} T-junctions (a room corner on a neighbour's edge: NeonPlan splits that wall, D149)")
        # near-miss coordinates: two different vertices closer than 3 cm but not identical
        allv = sorted({v for _, v in verts})
        for a, b in itertools.combinations(allv, 2):
            dd = math.hypot(a[0] - b[0], a[1] - b[1])
            if 1e-9 < dd < 0.03: E(f"[{fn}] near-coincident corners {a} / {b} ({dd * 100:.1f} cm): use one coordinate")
        # parallel edges nearly but not exactly on the same line (gaps/slivers)
        for (r1, i1, a1, b1), (r2, i2, a2, b2) in itertools.combinations(E_, 2):
            if r1 == r2: continue
            for ax in (0, 1):
                if abs(a1[ax] - b1[ax]) < 1e-9 and abs(a2[ax] - b2[ax]) < 1e-9:
                    gap = abs(a1[ax] - a2[ax])
                    o = 1 - ax
                    ov = min(max(a1[o], b1[o]), max(a2[o], b2[o])) - max(min(a1[o], b1[o]), min(a2[o], b2[o]))
                    if 1e-6 < gap < 0.06 and ov > 0.05:
                        E(f"[{fn}] edges of '{rooms[r1]['name']}' and '{rooms[r2]['name']}' are {gap * 100:.1f} cm apart over {ov:.2f} m (sliver / double wall)")
        u = unary_union([p for _, p in polys])
        outlines[fn] = u
        xs, zs = u.bounds[0::2], u.bounds[1::2]
        I(f"[{fn}] {len(rooms)} rooms, {sum(abs(area(r['points'])) for r in rooms):.1f} m2, extents x {u.bounds[0]:.3f}..{u.bounds[2]:.3f}, z {u.bounds[1]:.3f}..{u.bounds[3]:.3f}")
        if u.geom_type != "Polygon": W(f"[{fn}] rooms form {len(u.geoms)} separate pieces")
        elif len(u.interiors): I(f"[{fn}] outline has {len(u.interiors)} hole(s) (open-to-below / courtyard)")
        if fn in EXPECT:
            ew, eh = EXPECT[fn]
            gw, gh = u.bounds[2] - u.bounds[0], u.bounds[3] - u.bounds[1]
            if abs(gw - ew) > 0.02 or abs(gh - eh) > 0.02: E(f"[{fn}] overall {gw:.3f} x {gh:.3f} m differs from drawing {ew:.3f} x {eh:.3f} m")
            else: I(f"[{fn}] overall {gw:.3f} x {gh:.3f} m matches the drawing's dimension strings ({ew:.3f} x {eh:.3f})")
        # walls
        for w in f.get("walls", []):
            for k in w:
                if k not in ALLOWED["walls"]: E(f"[{fn}] wall unsupported field '{k}'")
            if math.hypot(w["to"][0] - w["from"][0], w["to"][1] - w["from"][1]) < 0.05: E(f"[{fn}] zero-length wall {w}")
        free = [(tuple(w["from"]), tuple(w["to"])) for w in f.get("walls", [])]
        # openings
        seen = []
        for kind in ("doors", "windows"):
            for o in f.get(kind, []):
                for k in o:
                    if k not in ALLOWED[kind]: E(f"[{fn}] {kind[:-1]} unsupported field '{k}'")
                at = tuple(o["at"]); wdt = o["width"]
                best = None
                for ri, i, a, b in E_:
                    dist, s, L = proj(at, a, b)
                    if best is None or dist < best[0]: best = (dist, s, L, rooms[ri]["name"], i, a, b)
                fbest = None
                for a, b in free:
                    dist, s, L = proj(at, a, b)
                    if fbest is None or dist < fbest[0]: fbest = (dist, s, L, "free wall", -1, a, b)
                if fbest and (best is None or fbest[0] < best[0] - 1e-6) and best[0] > REACH:
                    best = fbest
                dist, s, L, rn, ei, a, b = best
                tag = f"[{fn}] {kind[:-1]} at {list(at)} w={wdt}"
                if dist > ON_EDGE: E(f"{tag}: {dist * 100:.1f} cm off the nearest wall line ('{rn}' edge {ei})")
                if s - wdt / 2 < -0.01 or s + wdt / 2 > L + 0.01:
                    E(f"{tag}: extends beyond its wall segment ('{rn}' edge {ei}, length {L:.2f} m, centre at {s:.2f} m)")
                lo, hi = (0.5, 5.0) if kind == "doors" else (0.25, 3.0)
                if not lo <= wdt <= hi: E(f"{tag}: implausible width")
                if kind == "windows":
                    if o["sill"] + o["height"] > f["height"] + 1e-6: E(f"{tag}: top {o['sill'] + o['height']:.2f} above storey height {f['height']:.2f}")
                    if o["sill"] < 0: E(f"{tag}: negative sill")
                if kind == "doors" and o.get("height", 2.01) > f["height"]: E(f"{tag}: door taller than storey")
                # duplicates: same line, overlapping span, overlapping heights
                lo_h = o.get("sill", 0) if kind == "windows" else 0
                hi_h = lo_h + o.get("height", 2.01)
                for (k2, at2, w2, l2, h2, seg) in seen:
                    if seg == (a, b) or seg == (b, a) or (proj(at2, a, b)[0] < ON_EDGE):
                        span = abs(proj(at2, a, b)[1] - s)
                        if span < (w2 + wdt) / 2 - 0.01 and lo_h < h2 - 0.05 and l2 < hi_h - 0.05:
                            E(f"{tag}: overlaps/duplicates {k2} at {list(at2)}")
                seen.append((kind[:-1], at, wdt, lo_h, hi_h, (a, b)))
        for u_ in f.get("furniture", []):
            for k in u_:
                if k not in ALLOWED["furniture"]: E(f"[{fn}] furniture unsupported field '{k}'")
            if u_.get("type") not in FURN: E(f"[{fn}] furniture type '{u_.get('type')}' not supported")
            if not any(p.buffer(0.05).contains(Point(u_["at"])) for _, p in polys): W(f"[{fn}] {u_['type']} at {u_['at']} is not inside any room")
            if u_.get("rotation", 0) % 90: W(f"[{fn}] {u_['type']} rotated {u_['rotation']} deg")
        I(f"[{fn}] {len(f.get('doors', []))} doors, {len(f.get('windows', []))} windows, {len(f.get('furniture', []))} furniture, {len(f.get('walls', []))} free walls")
    # vertical alignment between floors
    names = [f["name"] for f in floors]
    if "Main Floor" in outlines and "Upper Floor" in outlines:
        m, u = outlines["Main Floor"], outlines["Upper Floor"]
        out = u.difference(m.buffer(0.02)).area
        if out > 0.5: W(f"upper floor overhangs the main floor by {out:.2f} m2")
        else: I(f"upper floor sits on the main floor footprint (overhang {out:.2f} m2)")
        # shared exterior lines
        for v, lab in ((m.bounds[2], "right wall x"),):
            if abs(u.bounds[2] - v) > 0.005: E(f"{lab}: main {v:.3f} vs upper {u.bounds[2]:.3f}")
            else: I(f"{lab} aligned on main and upper ({v:.3f} m)")
        if abs(u.bounds[1] - m.bounds[1]) > 0.005: E("rear wall not aligned main/upper")
        else: I(f"rear wall aligned on main and upper (z {m.bounds[1]:.3f} m)")
    # area schedule (sheet A2/A3: main 1451, upper 1425, finished basement 889, total basement 1018 sq ft)
    SF = 0.3048 ** 2
    sched = {"Main Floor": (1451, lambda n: n not in ("3-Car Garage",)), "Upper Floor": (1425, lambda n: True), "Basement": (889, lambda n: n not in ("Mechanical Room", "Crawlspace"))}
    for f in floors:
        if f["name"] in sched:
            want, keep = sched[f["name"]]
            got = sum(abs(area(r["points"])) for r in f["rooms"] if keep(r["name"])) / SF
            dev = (got - want) / want * 100
            msg = f"[{f['name']}] centre-line area {got:.0f} sq ft vs area schedule {want} sq ft ({dev:+.1f}%)"
            (W if abs(dev) > 5 else I)(msg)
    # stairs alignment
    st = {f["name"]: [r for r in f["rooms"] if r["name"] == "Stairs"] for f in floors}
    sf = {f["name"]: [x for x in f.get("furniture", []) if x["type"] in ("stairs", "stairs_u")] for f in floors}
    if st.get("Main Floor") and st.get("Upper Floor"):
        a, b = Polygon(st["Main Floor"][0]["points"]), Polygon(st["Upper Floor"][0]["points"])
        if a.symmetric_difference(b).area > 0.01: E("stair footprints differ between main and upper")
        else: I("stair room identical on main and upper floor")
    if sf.get("Basement") and sf.get("Main Floor"):
        a, b = sf["Basement"][0], sf["Main Floor"][0]
        if math.hypot(a["at"][0] - b["at"][0], a["at"][1] - b["at"][1]) > 0.01 or abs(a["width"] - b["width"]) > 0.01 or abs(a["depth"] - b["depth"]) > 0.01:
            E("basement and main stairs differ in footprint")
        else: I("basement and main-floor stairs share one footprint")
    return d


if __name__ == "__main__":
    argv = sys.argv[1:]
    if "--json" in argv: del argv[argv.index("--json"):argv.index("--json") + 2]
    args = [a for a in argv if not a.startswith("--")]
    path = args[0] if args else "/shared/user/home/neonplan_house.json"
    main(path)
    print(f"Validation of {path}\n")
    for m in info: print("  ok   ", m)
    for m in warnings: print("  WARN ", m)
    for m in errors: print("  ERROR", m)
    print(f"\n{len(errors)} errors, {len(warnings)} warnings")
    if "--json" in sys.argv:
        json.dump({"errors": errors, "warnings": warnings, "info": info}, open(sys.argv[sys.argv.index("--json") + 1], "w"), indent=1)
    sys.exit(1 if errors else 0)
