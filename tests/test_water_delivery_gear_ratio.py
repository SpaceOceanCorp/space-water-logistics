import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "models"))

from water_delivery_gear_ratio import (  # noqa: E402
    G0,
    earth_sourced_mass_in_leo,
    lunar_sourced_water_mined,
    propellant_per_payload,
    table,
)


class GearRatioTest(unittest.TestCase):
    def test_zero_delta_v_needs_no_propellant(self):
        self.assertEqual(propellant_per_payload(0.0, 450.0, 0.1), 0.0)

    def test_no_tankage_is_plain_rocket_equation(self):
        r = math.exp(3000.0 / (G0 * 300.0))
        self.assertAlmostEqual(propellant_per_payload(3000.0, 300.0, 0.0), r - 1, places=12)

    def test_infeasible_stage_returns_inf(self):
        self.assertTrue(math.isinf(propellant_per_payload(9000.0, 300.0, 0.5)))

    def test_leo_to_geo_by_hand(self):
        r = math.exp(4330.0 / (G0 * 450.0))
        p = (r - 1) / (1.1 - 0.1 * r)
        self.assertAlmostEqual(earth_sourced_mass_in_leo(4330.0, 450.0, 0.1), 1 + 1.1 * p, places=12)
        self.assertAlmostEqual(earth_sourced_mass_in_leo(4330.0, 450.0, 0.1), 3.20, places=2)

    def test_lunar_water_beats_earth_beyond_leo(self):
        for dest, earth, moon in table(450.0, 0.1):
            if dest != "LEO":
                self.assertLess(moon, earth, dest)

    def test_rejects_bad_inputs(self):
        with self.assertRaises(ValueError):
            propellant_per_payload(-1.0, 450.0, 0.1)
        with self.assertRaises(ValueError):
            lunar_sourced_water_mined(1000.0, 0.0, 0.1)


if __name__ == "__main__":
    unittest.main()
