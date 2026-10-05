import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "models"))

from lunar_settlement_water import landers_per_day, net_loss_t_per_year, years_to_exhaust  # noqa: E402

M, USE = 1e9, 500.0


class LunarSettlementWaterTest(unittest.TestCase):
    def test_reproduces_paper_table_3(self):
        # Elvis & McDowell (2026) Table 3; the paper rounds 333 to 330 and 33.3 to 33
        table = {0.0: (20, 2), 0.94: (330, 33), 0.98: (1000, 100), 0.99: (2000, 200), 0.999: (20000, 2000)}
        for e, (small, large) in table.items():
            self.assertAlmostEqual(years_to_exhaust(M, 1e5, USE, e), small, delta=0.02 * small)
            self.assertAlmostEqual(years_to_exhaust(M, 1e6, USE, e), large, delta=0.02 * large)

    def test_import_demand_for_a_million_people(self):
        # paper: ~10 million tons/yr, 27 landers per Earth day at 1,000 t
        self.assertAlmostEqual(net_loss_t_per_year(1e6, USE, 0.98), 1e7, places=3)
        self.assertEqual(int(landers_per_day(1e6, USE, 0.98)), 27)

    def test_perfect_recycling_never_runs_out(self):
        self.assertTrue(math.isinf(years_to_exhaust(M, 1e6, USE, 1.0)))

    def test_rejects_bad_inputs(self):
        for args in ((0, USE, 0.9), (1e6, 0, 0.9), (1e6, USE, 1.5)):
            with self.assertRaises(ValueError):
                net_loss_t_per_year(*args)
        with self.assertRaises(ValueError):
            landers_per_day(1e6, USE, 0.98, lander_t=0)


if __name__ == "__main__":
    unittest.main()
