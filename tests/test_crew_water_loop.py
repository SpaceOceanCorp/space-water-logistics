import sys
import unittest
from dataclasses import replace
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "models"))

from crew_water_loop import WATER_PER_O2, WaterLoopInputs, water_loop_budget  # noqa: E402


class CrewWaterLoopTest(unittest.TestCase):
    def test_electrolysis_ratio(self):
        self.assertAlmostEqual(WATER_PER_O2, 1.12601, places=5)

    def test_iss_defaults_by_hand(self):
        b = water_loop_budget(WaterLoopInputs())
        demand = 2.5 + 0.4 + 0.3 + 0.82 * WATER_PER_O2
        recovered = 0.85 * (1.2 + 0.3) + 2.27
        self.assertAlmostEqual(b.demand, demand, places=12)
        self.assertAlmostEqual(b.recovered, recovered, places=12)
        self.assertAlmostEqual(b.makeup, demand - recovered, places=12)
        self.assertAlmostEqual(b.mission, (demand - recovered) * 4 * 180 * 1.1, places=9)
        # matches the sidus-tools water-loop calculator (PR #212)
        self.assertAlmostEqual(b.mission, 458.0346, places=3)

    def test_open_loop_ships_everything(self):
        b = water_loop_budget(WaterLoopInputs(eta_urine=0, eta_condensate=0))
        self.assertEqual(b.closure, 0)
        self.assertAlmostEqual(b.mission, b.open_loop, places=9)

    def test_surplus_not_negative_makeup(self):
        b = water_loop_budget(WaterLoopInputs(o2=0, eta_hygiene=1))
        self.assertEqual(b.makeup, 0)
        self.assertGreater(b.surplus, 0)
        self.assertEqual(b.closure, 1)

    def test_rejects_bad_inputs(self):
        base = WaterLoopInputs()
        for kw in ({"eta_urine": 1.1}, {"potable": -1}, {"crew": 0}, {"days": 0}, {"reserve": -0.1}):
            with self.assertRaises(ValueError):
                replace(base, **kw)


if __name__ == "__main__":
    unittest.main()
