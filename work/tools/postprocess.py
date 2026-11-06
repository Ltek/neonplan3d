"""Post-process the NeonPlan building made by the official importer (buildPlan) from neonplan_house.json:
open-plan edges get wall height 0, half walls / rails their height, wall thicknesses from the drawings, the decks and
the porch become outdoor areas. Writes a NeonPlan export file for Editor -> Backup -> Import.

usage: python3 postprocess.py built.json out.json"""
import json, math, sys, os, datetime
sys.path.insert(0, os.path.dirname(__file__))
import geometry as G
from build import pt, m

EPS = 0.005
EXT = 0.14    # 2x4 + 7/16" OSB + siding/stucco + 1/2" gypsum ~ 5.4" (Typical Construction Assemblies B1/B2, E1)
INT = 0.114   # 2x4 + 2 x 1/2" gypsum = 4.5"
BASE_EXT = 0.20  # 8" concrete foundation wall (S-1 "8\" WALL TYPICAL") / 2x6 walk-out walls


def on_seg(p, a, b, tol=EPS):
    dx, dz = b[0] - a[0], b[1] - a[1]
    L = math.hypot(dx, dz)
    t = ((p[0] - a[0]) * dx + (p[1] - a[1]) * dz) / L
    d = abs((p[0] - a[0]) * dz - (p[1] - a[1]) * dx) / L
    return d <= tol and -tol <= t <= L + tol, t, L


def main(src, dst):
    b = json.load(open(src))
    b["settings"]["wall_exterior"] = EXT
    b["settings"]["wall_interior"] = INT
    log = []
    for gf, f in zip(G.FLOORS, b["floors"]):
        assert gf["name"] == f["name"]
        opens = [(pt(e["a"]), pt(e["b"]), e["h"], e["why"]) for e in gf.get("open_edges", [])]
        splits_needed = [p for a, c, _, _ in opens for p in (a, c)]
        nodes = [p for r in f["rooms"] for p in r["points"]] + [p for w in f.get("walls", []) for p in (w["a"], w["b"])]
        # room edge membership count, to tell exterior edges (one room) from shared ones
        for r in f["rooms"]:
            P = r["points"]
            n = len(P)
            heights, splits, thick = [None] * n, [None] * n, [None] * n
            for i in range(n):
                a, c = P[i], P[(i + 1) % n]
                L = math.hypot(c[0] - a[0], c[1] - a[1])
                cuts = set()
                for q in nodes + splits_needed:
                    ok, t, _ = on_seg(q, a, c)
                    if ok and EPS < t < L - EPS:
                        cuts.add(round(t, 4))
                # split points that are no vertex of any room: they must be stored, or the importer merges them away
                extra = sorted(round(t, 3) for t in cuts if not any(on_seg(q, a, c)[0] and abs(on_seg(q, a, c)[1] - t) < EPS for q in nodes))
                if extra:
                    splits[i] = extra
                stops = [0.0] + sorted(cuts) + [L]
                parts = []
                for k in range(len(stops) - 1):
                    tm = (stops[k] + stops[k + 1]) / 2
                    mp = [a[0] + (c[0] - a[0]) * tm / L, a[1] + (c[1] - a[1]) * tm / L]
                    h = None
                    for oa, ob, oh, why in opens:
                        if on_seg(mp, oa, ob, 0.01)[0]:
                            h = round(oh, 3)
                            log.append(f"{f['name']}: '{r['name']}' edge {i} part {k}: height {h} ({why})")
                    parts.append(h)
                if any(h is not None for h in parts):
                    heights[i] = parts[0] if len(parts) == 1 else parts
                # exterior edge? (no other room shares it)
                mp = [(a[0] + c[0]) / 2, (a[1] + c[1]) / 2]
                shared = any(r2 is not r and any(on_seg(mp, r2["points"][j], r2["points"][(j + 1) % len(r2["points"])], 0.01)[0] for j in range(len(r2["points"]))) for r2 in f["rooms"])
                if not shared and gf["name"] == "Basement":
                    thick[i] = BASE_EXT
            if any(h is not None for h in heights):
                r["wall_heights"] = heights
            if any(s for s in splits):
                r["wall_splits"] = splits
            if any(t for t in thick):
                r["wall_thickness"] = thick
        # door looks the import format cannot carry (sliding glass doors). A door 2.2 m or wider comes in as a garage
        # door; a sliding door is put back to a door.
        for d in gf["doors"]:
            if not d.get("style"):
                continue
            tp = pt(d["at"])
            hit = None
            for o in f.get("openings", []):
                r = next(r for r in f["rooms"] if r["id"] == o["room_id"])
                P = r["points"]
                a0, a1 = P[o["edge"]], P[(o["edge"] + 1) % len(P)]
                L = math.hypot(a1[0] - a0[0], a1[1] - a0[1])
                c = [a0[0] + (a1[0] - a0[0]) * o["offset"] / L, a0[1] + (a1[1] - a0[1]) * o["offset"] / L]
                if math.hypot(c[0] - tp[0], c[1] - tp[1]) < 0.05 and o["type"] in ("door", "garage"):
                    hit = o
            assert hit, f"no opening for {d['label']}"
            if hit["type"] == "garage":
                hit["type"] = "door"
            hit["style"] = d["style"]
            hit["leaves"] = 1
            log.append(f"{f['name']}: '{d['label'][:40]}' style {d['style']}")
        # outdoor areas
        for k, o in enumerate(gf.get("outdoor", [])):
            f.setdefault("outdoor", []).append({"id": f"outdoor_{gf['name'][:4].lower()}_{k}", "type": o["type"], "name": o["name"], "points": [pt(p) for p in o["points"]]})
            log.append(f"{f['name']}: outdoor '{o['name']}' ({o['type']})")
    out = {"format": "neonplan3d", "version": 1, "exported_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"), "building": b}
    json.dump(out, open(dst, "w"), indent=1)
    print("\n".join(log))
    print("wrote", dst)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
