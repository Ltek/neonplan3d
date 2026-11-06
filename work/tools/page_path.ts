import { readFileSync, writeFileSync } from "node:fs";
import { readFile } from "./src/import/detect.ts";
import { buildPlan } from "./src/import/builder.ts";
import { parseExport } from "./src/transfer.ts";
for (const p of process.argv.slice(2)) {
  const bytes = new Uint8Array(readFileSync(p));
  const r = await readFile(p.split("/").pop()!, bytes, { roles: {}, dxfUnit: null, mesh: { up: "auto", unit: null, levels: null }, lang: "en" } as any, {});
  let building, stats = null, warnings = r.warnings;
  if (r.building) building = structuredClone(r.building);
  else { const res = buildPlan(r.raw!, { square: true, furniture: true, mirror: false, turn: 0, lang: "en" }); building = res.building; stats = res.stats; warnings = [...warnings, ...res.warnings]; }
  const file = { format: "neonplan3d", version: 1, exported_at: new Date().toISOString(), building };
  const out = p.replace(/\.json$/, ".pagecheck.json");
  writeFileSync(out, JSON.stringify(file));
  const back = parseExport(JSON.stringify(file));   // what Editor -> Backup -> Import does
  console.log(p, "kind:", r.kind, "stats:", JSON.stringify(stats), "warnings:", JSON.stringify(warnings), "editor parse ok, floors:", back.floors.map((f) => `${f.name}:${f.rooms.length}r/${f.openings.length}o/${f.furniture.length}f/${(f.walls ?? []).length}w`).join(" "));
}
