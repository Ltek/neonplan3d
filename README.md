# neonplan3d

A NeonPlan 3D model of a three-level house (basement, main and upper floor), reconstructed from scanned architectural plans.

| File | Use |
|---|---|
| `neonplan_house.json` | `neonplan-import` file for <https://neonplan3d.mastershort.de/import/> |
| `neonplan_house.neonplan3d.json` | Complete NeonPlan file with open-plan edges, half walls, wall thicknesses and outdoor areas set. Load it with Editor → Backup → Import. |
| `work/source_analysis.md` | How the source sheets were read and calibrated |
| `work/qa_report.md` | Validation results, assumptions and open questions |
| `work/neonplan_preview.svg` | 2D preview of all floors |
| `work/compare/` | The reconstruction overlaid on each source sheet |
| `work/validate_neonplan.py` | Geometry checks for the import file |
| `work/tools/` | Scripts that build the files from `geometry.py` |
