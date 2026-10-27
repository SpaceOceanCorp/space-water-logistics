"""The calculator page (docs/models.js) must give the same answers as the Python models."""

import json
import math
import shutil
import subprocess
import sys
import unittest
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "models"))

import crew_water_loop as cwl  # noqa: E402
import lunar_settlement_water as lsw  # noqa: E402
import water_delivery_gear_ratio as gr  # noqa: E402

LOOP_CASES = [{}, {"crew": 6, "days": 365, "eta_urine": 0.98}, {"o2": 0.0, "eta_hygiene": 0.9, "reserve": 0.0},
              {"eta_urine": 1.0, "eta_hygiene": 1.0, "condensate": 5.0}]
LUNAR_CASES = [(1e9, 1e5, 500, 0.98), (1e9, 1e6, 500, 0.999), (5e8, 1e3, 125, 0.0), (1e9, 1e6, 500, 1.0)]
GEAR_CASES = [(450, 0.1), (320, 0.05), (380, 0.2), (300, 0.5)]

JS = """
const m = require(process.argv[1]);
const input = JSON.parse(require('fs').readFileSync(0, 'utf8'));
const out = {
  loop: input.loop.map(c => m.waterLoopBudget(c)),
  lunar: input.lunar.map(([M, N, u, e]) => [m.yearsToExhaust(M, N, u, e), m.landersPerDay(N, u, e), m.netLossTPerYear(N, u, e)]),
  gear: input.gear.map(([isp, s]) => m.gearTable(isp, s)),
};
process.stdout.write(JSON.stringify(out, (k, v) => (v === Infinity ? 'inf' : v)));
"""


def close(a, b):
    if a == "inf" or b == "inf" or (isinstance(b, float) and math.isinf(b)):
        return (a == "inf" or math.isinf(a)) and (b == "inf" or math.isinf(b))
    return math.isclose(a, b, rel_tol=1e-12, abs_tol=1e-12)


@unittest.skipIf(shutil.which("node") is None, "node not installed")
class ParityTest(unittest.TestCase):
    def test_js_matches_python(self):
        payload = json.dumps({"loop": LOOP_CASES, "lunar": LUNAR_CASES, "gear": GEAR_CASES})
        res = subprocess.run(["node", "-e", JS, str(ROOT / "docs" / "models.js")], input=payload,
                             capture_output=True, text=True, check=True)
        js = json.loads(res.stdout)
        for case, got in zip(LOOP_CASES, js["loop"], strict=True):
            want = asdict(cwl.water_loop_budget(cwl.WaterLoopInputs(**case)))
            for k, v in want.items():
                self.assertTrue(close(got[k], v), f"loop {case} {k}: js {got[k]} py {v}")
        for (M, N, u, e), got in zip(LUNAR_CASES, js["lunar"], strict=True):
            want = [lsw.years_to_exhaust(M, N, u, e), lsw.landers_per_day(N, u, e), lsw.net_loss_t_per_year(N, u, e)]
            for g, w in zip(got, want, strict=True):
                self.assertTrue(close(g, w), f"lunar {(M, N, u, e)}: js {g} py {w}")
        for (isp, s), got in zip(GEAR_CASES, js["gear"], strict=True):
            for (gd, ge, gm), (wd, we, wm) in zip(got, gr.table(isp, s), strict=True):
                self.assertEqual(gd, wd)
                self.assertTrue(close(ge, we) and close(gm, wm), f"gear {isp} {s} {wd}")


if __name__ == "__main__":
    unittest.main()
