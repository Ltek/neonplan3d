import { readFileSync } from "node:fs";
import { parseExport } from "./src/transfer.ts";
import { repairPlan } from "./src/import/simple.ts";
import { generateWalls } from "./src/geometry/walls.ts";
const text = readFileSync(process.argv[2], "utf8");
const b = parseExport(text);
const { building, warnings } = repairPlan(b);
console.log("repairPlan warnings:", JSON.stringify(warnings));
for (const f of building.floors) {
  const res = generateWalls(f.rooms, { exterior: building.settings.wall_exterior, interior: building.settings.wall_interior } as any, f.walls ?? []);
  const walls = (res as any).walls ?? [];
  const low = walls.filter((w: any) => w.height && w.height < f.height - 0.01).length;
  console.log(`${f.name}: rooms ${f.rooms.length}, openings ${f.openings.length}, furniture ${f.furniture.length}, outdoor ${f.outdoor.length}, generated walls ${walls.length} (low ${low}), wall warnings ${JSON.stringify((res as any).warnings)}`);
}
