import { readFileSync, writeFileSync } from "node:fs";
import { readSimple, isSimple } from "./src/import/simple.ts";
import { buildPlan } from "./src/import/builder.ts";
const src = JSON.parse(readFileSync(process.argv[2], "utf8"));
console.log("isSimple:", isSimple(src));
const raw = readSimple(src);
const res = buildPlan(raw);
console.log(JSON.stringify({ stats: res.stats, warnings: res.warnings }, null, 1));
writeFileSync(process.argv[3], JSON.stringify(res.building, null, 1));
