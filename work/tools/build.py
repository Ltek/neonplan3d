"""Build neonplan_house.json (neonplan-import), geometry_data.json, neonplan_preview.svg and the overlay images
from tools/geometry.py. Run: python3 tools/build.py"""
import json, sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import geometry as G
from calib import apply

WORK = "/shared/user/home/neonplan_work"
OUT_JSON = "/shared/user/home/neonplan_house.json"
FT = G.FT
# shift: garage-left / rear-wall centre lines become 0,0 (the top-left corner of the building's wall centre lines)
SX = G.X_GAR_L
SZ = G.Z_REAR


def m(v):
    return round(v * FT, 3)


def pt(p):
    return [m(p[0] - SX), m(p[1] - SZ)]


def build_import():
    floors = []
    for f in G.FLOORS:
        fl = {"name": f["name"], "elevation": m(f["elev_ft"]), "height": m(f["height_ft"]), "rooms": [], "walls": [], "doors": [], "windows": [], "furniture": []}
        for r in f["rooms"]:
            fl["rooms"].append({"name": r["name"], "points": [pt(p) for p in r["points"]]})
        for w in f["walls"]:
            if w.get("full_only"):  # the importer drops walls that lie along room edges (or thicker than 0.6 m): added by postprocess.py
                continue
            fl["walls"].append({"from": pt(w["from"]), "to": pt(w["to"]), "thickness": m(w["thickness_ft"])})
        for d in f["doors"]:
            fl["doors"].append({"at": pt(d["at"]), "width": m(d["w"]), "height": m(d["h"])})
        for w in f["windows"]:
            sill = w["sill"] if "sill" in w else w["head"] - w["h"]
            o = {"at": pt(w["at"]), "width": m(w["w"]), "height": m(w["h"]), "sill": m(sill)}
            if sill < 0.3:
                o["sill_board"] = "none"
            fl["windows"].append(o)
        for u in f["furniture"]:
            fl["furniture"].append({"type": u["type"], "at": pt([u["x"], u["z"]]), "width": m(u["w"]), "depth": m(u["d"]), "rotation": u["rot"]})
        if not fl["walls"]:
            del fl["walls"]
        floors.append(fl)
    return {"format": "neonplan-import", "units": "m", "rooms_at": "centre", "floors": floors}


def build_geometry_data():
    out = {"source": "scanned house plans (sheets A1-A6, S-1 foundation plan)",
           "frame": {"units_internal": "ft", "units_export": "m", "origin": "outer face of studs: garage left wall (X) and rear wall (Z)",
                     "export_shift_ft": [SX, SZ], "x": "right", "z": "down the sheet", "rooms_at": "centre"},
           "provenance_codes": {"D": "explicit dimension (face of stud) +/- 1.75\" to the stud centre", "M": "measured on the calibrated raster", "E": "estimated / inferred"},
           "constants_ft": {k: {"value": v[0], "prov": v[1], "note": v[2]} for k, v in G.C.items()},
           "vertical_ft": {"basement_floor_to_floor": G.H_BASE, "main_floor_to_floor": G.H_MAIN, "upper_plate": G.H_UP, "window_head_main": G.HEAD_MAIN,
                           "window_head_upper": G.HEAD_UP, "window_head_basement_assumed": G.HEAD_BASE},
           "floors": []}
    for f in G.FLOORS:
        out["floors"].append({k: f[k] for k in f})
    return out


# ------------------------------------------------------------------ SVG preview
COL = {"room": "#2b6cb0", "wall": "#111", "door": "#d97706", "win": "#0ea5e9", "furn": "#6b7280", "out": "#16a34a"}


def view_floors():
    """Floors as drawn in the preview and the overlays: a level merged into another one (the garage, 4 steps below
    the main floor) is drawn with it."""
    out = []
    for f in G.FLOORS:
        if f.get("merge_into"):
            continue
        g = dict(f)
        for x in G.FLOORS:
            if x.get("merge_into") == f["name"]:
                for k in ("rooms", "walls", "doors", "windows", "furniture", "outdoor", "open_edges"):
                    g[k] = list(x.get(k, [])) + list(g.get(k, []))
        out.append(g)
    return out


def svg_preview(path):
    S = 9.0  # px per ft
    pad = 60
    W = 72 * S + 2 * pad
    gap = 70
    floor_h = 58 * S
    H = len(view_floors()) * (floor_h + gap) + pad * 2 + 40
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W:.0f}" height="{H:.0f}" viewBox="0 0 {W:.0f} {H:.0f}" font-family="Helvetica,Arial,sans-serif">',
         '<rect width="100%" height="100%" fill="white"/>',
         f'<text x="{pad}" y="30" font-size="12" font-weight="bold">House plan - NeonPlan reconstruction (wall centre lines; [0,0] = garage-left and rear wall centre lines)</text>']
    for fi, f in enumerate(reversed(view_floors())):
        oy = pad + 30 + fi * (floor_h + gap) + 30
        ox = pad
        X = lambda x: ox + (x - SX + 1.0) * S
        Z = lambda z: oy + (z - SZ + 8.0) * S
        o.append(f'<text x="{ox}" y="{oy - 8}" font-size="16" font-weight="bold">{f["name"]}  (elevation {m(f["elev_ft"]):+.3f} m, storey {m(f["height_ft"]):.3f} m)</text>')
        for a in f.get("outdoor", []):
            pts = " ".join(f"{X(p[0]):.1f},{Z(p[1]):.1f}" for p in a["points"])
            o.append(f'<polygon points="{pts}" fill="#dcfce7" stroke="{COL["out"]}" stroke-dasharray="4 3"/>')
            cx = np.mean([p[0] for p in a["points"]]); cz = np.mean([p[1] for p in a["points"]])
            o.append(f'<text x="{X(cx):.1f}" y="{Z(cz):.1f}" font-size="10" fill="{COL["out"]}" text-anchor="middle">{a["name"]} (outdoor)</text>')
        open_e = f.get("open_edges", [])
        for r in f["rooms"]:
            pts = " ".join(f"{X(p[0]):.1f},{Z(p[1]):.1f}" for p in r["points"])
            o.append(f'<polygon points="{pts}" fill="#eff6ff" fill-opacity="0.7" stroke="none"/>')
        # walls: every room edge, thin if open/low
        drawn = set()
        stair_open = []
        # open edges are drawn dashed only round a stair (the stair opening); other open edges between rooms are left out
        stair_keys = {tuple(sorted([(round(P[i][0], 2), round(P[i][1], 2)), (round(P[(i + 1) % len(P)][0], 2), round(P[(i + 1) % len(P)][1], 2))]))
                      for r in f["rooms"] if r["name"] == "Stairs" for P in [r["points"]] for i in range(len(P))}
        for r in f["rooms"]:
            P = r["points"]
            for i in range(len(P)):
                a, b = P[i], P[(i + 1) % len(P)]
                key = tuple(sorted([(round(a[0], 2), round(a[1], 2)), (round(b[0], 2), round(b[1], 2))]))
                if key in drawn:
                    continue
                drawn.add(key)
                low = None
                for e in open_e:
                    if seg_on(a, b, e["a"], e["b"]):
                        low = e["h"]
                if low == 0:
                    if key in stair_keys:
                        stair_open.append((a, b))
                    continue
                elif low:
                    o.append(f'<line x1="{X(a[0]):.1f}" y1="{Z(a[1]):.1f}" x2="{X(b[0]):.1f}" y2="{Z(b[1]):.1f}" stroke="#475569" stroke-width="2"/>')
                else:
                    o.append(f'<line x1="{X(a[0]):.1f}" y1="{Z(a[1]):.1f}" x2="{X(b[0]):.1f}" y2="{Z(b[1]):.1f}" stroke="{COL["wall"]}" stroke-width="3.5" stroke-linecap="square"/>')
        for w in f["walls"]:
            o.append(f'<line x1="{X(w["from"][0]):.1f}" y1="{Z(w["from"][1]):.1f}" x2="{X(w["to"][0]):.1f}" y2="{Z(w["to"][1]):.1f}" stroke="#334155" stroke-width="2.5"/>')
        for u in f["furniture"]:
            fw, fd = u["w"], u["d"]
            if u["rot"] in (90, 270):
                fw, fd = fd, fw
            o.append(f'<rect x="{X(u["x"] - fw / 2):.1f}" y="{Z(u["z"] - fd / 2):.1f}" width="{fw * S:.1f}" height="{fd * S:.1f}" fill="none" stroke="{COL["furn"]}" stroke-width="1"/>')
            o.append(f'<text x="{X(u["x"]):.1f}" y="{Z(u["z"]) + 3:.1f}" font-size="7" fill="{COL["furn"]}" text-anchor="middle">{esc(u.get("show", u["type"]))}</text>')
        # stair openings (no wall): dashed, on top of the stair symbol
        for a, b in stair_open:
            o.append(f'<line x1="{X(a[0]):.1f}" y1="{Z(a[1]):.1f}" x2="{X(b[0]):.1f}" y2="{Z(b[1]):.1f}" stroke="#0f172a" stroke-width="1.5" stroke-dasharray="4 3"/>')
        for kind, L, col in (("win", f["windows"], COL["win"]), ("door", f["doors"], COL["door"])):
            for d in L:
                a, b = opening_ends(f, d)
                if d.get("style") == "passage":  # an opening without a door: a gap in the wall
                    o.append(f'<line x1="{X(a[0]):.1f}" y1="{Z(a[1]):.1f}" x2="{X(b[0]):.1f}" y2="{Z(b[1]):.1f}" stroke="#eff6ff" stroke-width="5"/>')
                    continue
                o.append(f'<line x1="{X(a[0]):.1f}" y1="{Z(a[1]):.1f}" x2="{X(b[0]):.1f}" y2="{Z(b[1]):.1f}" stroke="{col}" stroke-width="5" stroke-opacity="0.85"/>')
        for r in label_rooms(f["rooms"]):
            cx, cz = label_point(r["points"])
            area = r.get("area_ft2", poly_area(r["points"])) * FT * FT
            o.append(f'<text x="{X(cx):.1f}" y="{Z(cz):.1f}" font-size="10" text-anchor="middle" fill="{COL["room"]}" font-weight="bold">{esc(r["name"])}</text>')
            o.append(f'<text x="{X(cx):.1f}" y="{Z(cz) + 11:.1f}" font-size="8" text-anchor="middle" fill="{COL["room"]}">{area:.1f} m²</text>')
        # overall dimensions
        xs = [p[0] for r in f["rooms"] for p in r["points"]]; zs = [p[1] for r in f["rooms"] for p in r["points"]]
        x0, x1, z0, z1 = min(xs), max(xs), min(zs), max(zs)
        yy = Z(z1) + 22
        o.append(f'<line x1="{X(x0):.1f}" y1="{yy:.1f}" x2="{X(x1):.1f}" y2="{yy:.1f}" stroke="#111"/>')
        o.append(f'<text x="{(X(x0) + X(x1)) / 2:.1f}" y="{yy + 12:.1f}" font-size="10" text-anchor="middle">{m(x1 - x0):.3f} m ({x1 - x0:.2f} ft) wall centre to wall centre</text>')
        xx = X(x1) + 20
        o.append(f'<line x1="{xx:.1f}" y1="{Z(z0):.1f}" x2="{xx:.1f}" y2="{Z(z1):.1f}" stroke="#111"/>')
        o.append(f'<text x="{xx + 4:.1f}" y="{(Z(z0) + Z(z1)) / 2:.1f}" font-size="10" transform="rotate(90 {xx + 4:.1f} {(Z(z0) + Z(z1)) / 2:.1f})" text-anchor="middle">{m(z1 - z0):.3f} m ({z1 - z0:.2f} ft)</text>')
        # scale bar + origin
        o.append(f'<circle cx="{X(SX):.1f}" cy="{Z(SZ):.1f}" r="3" fill="red"/><text x="{X(SX) + 4:.1f}" y="{Z(SZ) - 4:.1f}" font-size="9" fill="red">[0,0]</text>')
        sb = 5 / FT
        o.append(f'<line x1="{ox:.1f}" y1="{oy + floor_h - 6:.1f}" x2="{ox + sb * S:.1f}" y2="{oy + floor_h - 6:.1f}" stroke="#111" stroke-width="3"/><text x="{ox:.1f}" y="{oy + floor_h - 10:.1f}" font-size="9">5 m</text>')
    o.append(f'<text x="{pad}" y="{H - 14:.0f}" font-size="7.5">Legend: black = wall, grey = low wall/rail, dashed = stair opening (no wall), gap = opening without a door, orange = door, blue = window, green dashed = outdoor (not imported), grey box = fixture/furniture.</text>')
    o.append("</svg>")
    open(path, "w").write("\n".join(o))


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;")


def seg_on(a, b, c, d, tol=0.02):
    # is segment a-b collinear with and inside c-d?
    def on(p):
        cx, cz = d[0] - c[0], d[1] - c[1]
        L = math.hypot(cx, cz)
        t = ((p[0] - c[0]) * cx + (p[1] - c[1]) * cz) / (L * L)
        dist = abs((p[0] - c[0]) * cz - (p[1] - c[1]) * cx) / L
        return dist < tol and -1e-3 <= t <= 1 + 1e-3
    return on(a) and on(b)


def poly_area(P):
    return abs(sum(P[i][0] * P[(i + 1) % len(P)][1] - P[(i + 1) % len(P)][0] * P[i][1] for i in range(len(P)))) / 2


def label_rooms(rooms):
    """Rooms as labelled: parts of one room (split only for a ceiling, "part_of") get one label on their union."""
    from shapely.geometry import Polygon
    from shapely.ops import unary_union
    out, parts = [], {}
    for r in rooms:
        if r.get("part_of"):
            parts.setdefault(r["part_of"], []).append(r)
        else:
            out.append(r)
    for r in out:
        if r["name"] in parts:
            u = unary_union([Polygon(r["points"])] + [Polygon(p["points"]) for p in parts[r["name"]]])
            r = dict(r, points=[list(c) for c in u.exterior.coords[:-1]], area_ft2=sum(poly_area(x["points"]) for x in [r] + parts[r["name"]]))
        yield r


def label_point(P):
    from shapely.geometry import Polygon
    pg = Polygon(P)
    c = pg.centroid
    if pg.contains(c):
        return c.x, c.y
    p = pg.representative_point()
    return p.x, p.y


def nearest_edge(f, at, include_walls=True):
    best = None
    edges = [(r["points"][i], r["points"][(i + 1) % len(r["points"])]) for r in f["rooms"] for i in range(len(r["points"]))]
    if include_walls:
        edges += [(w["from"], w["to"]) for w in f["walls"]]
    for a, b in edges:
        dx, dz = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dz)
        t = ((at[0] - a[0]) * dx + (at[1] - a[1]) * dz) / (L * L)
        tc = min(1, max(0, t))
        px, pz = a[0] + tc * dx, a[1] + tc * dz
        dist = math.hypot(at[0] - px, at[1] - pz)
        if best is None or dist < best[0]:
            best = (dist, a, b, t * L, L)
    return best


def opening_ends(f, d):
    dist, a, b, s, L = nearest_edge(f, d["at"])
    ux, uz = (b[0] - a[0]) / L, (b[1] - a[1]) / L
    h = d["w"] / 2
    return (d["at"][0] - ux * h, d["at"][1] - uz * h), (d["at"][0] + ux * h, d["at"][1] + uz * h)


# ------------------------------------------------------------------ overlays on the source sheets
def overlays():
    from PIL import Image, ImageDraw, ImageFont
    Image.MAX_IMAGE_PIXELS = None
    CAL = json.load(open(f"{WORK}/calib.json"))
    font = ImageFont.load_default(size=44)
    for f in view_floors():
        H = np.array(CAL[f["sheet"]])
        im = Image.open(f"{WORK}/src/{f['sheet']}.png").convert("RGB")
        P = lambda p: apply(H, p[0], p[1])
        us = [P(p)[0] for r in f["rooms"] for p in r["points"]]; vs = [P(p)[1] for r in f["rooms"] for p in r["points"]]
        box = (int(min(us)) - 500, int(min(vs)) - 700, int(max(us)) + 500, int(max(vs)) + 500)
        im = im.crop(box)
        Q = lambda p: (P(p)[0] - box[0], P(p)[1] - box[1])
        lay = Image.new("RGBA", im.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        for a in f.get("outdoor", []):
            d.polygon([Q(p) for p in a["points"]], outline=(22, 163, 74, 255), fill=(22, 163, 74, 40))
        for r in f["rooms"]:
            pts = [Q(p) for p in r["points"]]
            d.polygon(pts, fill=(37, 99, 235, 45))
            d.line(pts + [pts[0]], fill=(220, 20, 60, 230), width=7)
        for w in f["walls"]:
            d.line([Q(w["from"]), Q(w["to"])], fill=(147, 51, 234, 230), width=7)
        for L, col in ((f["windows"], (2, 132, 199, 255)), (f["doors"], (234, 88, 12, 255))):
            for o in L:
                a, b = opening_ends(f, o)
                d.line([Q(a), Q(b)], fill=col, width=18)
        for u in f["furniture"]:
            fw, fd = (u["d"], u["w"]) if u["rot"] in (90, 270) else (u["w"], u["d"])
            d.rectangle([Q((u["x"] - fw / 2, u["z"] - fd / 2)), Q((u["x"] + fw / 2, u["z"] + fd / 2))], outline=(16, 185, 129, 255), width=5)
        for r in label_rooms(f["rooms"]):
            cx, cz = label_point(r["points"])
            x, y = Q((cx, cz))
            d.text((x, y), r["name"], fill=(185, 28, 28, 255), font=font, anchor="mm", stroke_width=3, stroke_fill=(255, 255, 255, 255))
        d.text((40, 40), f"{f['name']} - reconstruction (red = room centre lines, orange = doors, blue = windows, purple = free walls, green = fixtures/outdoor) over sheet {f['sheet']}",
               fill=(0, 0, 0, 255), font=font)
        out = Image.alpha_composite(im.convert("RGBA"), lay).convert("RGB")
        s = 3600 / out.size[0]
        out = out.resize((3600, int(out.size[1] * s)), Image.LANCZOS)
        fn = f"{WORK}/compare_{f['name'].lower().replace(' ', '_')}.png"
        out.save(fn, optimize=True)
        print("wrote", fn)


if __name__ == "__main__":
    plan = build_import()
    json.dump(plan, open(OUT_JSON, "w"), indent=1)
    json.dump(build_geometry_data(), open(f"{WORK}/geometry_data.json", "w"), indent=1)
    svg_preview(f"{WORK}/neonplan_preview.svg")
    if "--no-overlay" not in sys.argv:
        overlays()
    print("ok", OUT_JSON)
