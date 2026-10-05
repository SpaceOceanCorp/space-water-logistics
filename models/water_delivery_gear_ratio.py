"""
Water delivery gear ratio: Earth-sourced vs lunar-sourced water in cislunar space.

Purpose
    How much mass has to be moved (Earth source) or mined (lunar source) to put
    1 kg of water at a destination such as LEO, GEO, EML-1 or low lunar orbit.
    This is the "gear ratio" that decides where off-Earth water starts to beat
    launching water from Earth.

Assumptions
    - Single ideal chemical stage per leg, Tsiolkovsky equation.
    - Stage dry mass is a fixed fraction of the propellant it carries
      (dry_frac, 0.1 = 10% tankage and structure). The stage is expended.
    - Earth source: water and propellant both start in LEO (Earth-to-LEO launch
      is counted separately as "mass in LEO"). Earth-to-LEO launch is the same
      for every Earth-sourced destination and is not modeled here.
    - Lunar source: water is mined on the lunar surface, and the propellant is
      made from the same water by electrolysis (H2/O2), so every kg of
      propellant costs about 1 kg of mined water. Excess O2 from running
      fuel-rich of stoichiometric is ignored.
    - Delta-v values: Wikipedia "Delta-v budget", table "Earth-Moon space, high
      thrust" (LEO-Ken column/row, km/s). Returns to LEO assume aerobraking.
      Override them for your own architecture.

Units
    Delta-v in m/s, Isp in s, masses in kg per kg of delivered water.

Limitations
    Screening model only: no boil-off, no reusable stages, no transfer losses,
    no mining or processing equipment mass, no cost. A reusable lunar tanker
    would make the lunar case better than shown here.
"""

from __future__ import annotations

import math

G0 = 9.80665  # standard gravity, m/s^2

# Delta-v [m/s], Wikipedia "Delta-v budget", Earth-Moon space, high thrust.
DV_FROM_LEO = {"GEO": 4330.0, "EML-1": 3770.0, "LLO": 4040.0}
DV_FROM_MOON_SURFACE = {"LEO": 2740.0, "GEO": 3920.0, "EML-1": 2520.0, "LLO": 1870.0}


def propellant_per_payload(dv: float, isp: float, dry_frac: float) -> float:
    """Propellant [kg] per kg of payload for one expendable stage.

    Mass ratio R = exp(dv / (g0 Isp)) = (P + p (1 + s)) / (P + s p),
    which gives p / P = (R - 1) / (1 + s - s R). Returns inf when the stage
    cannot reach dv at any size (denominator <= 0).
    """
    if dv < 0 or isp <= 0 or dry_frac < 0:
        raise ValueError("dv >= 0, isp > 0 and dry_frac >= 0 required")
    r = math.exp(dv / (G0 * isp))
    denom = 1 + dry_frac - dry_frac * r
    if denom <= 0:
        return math.inf
    return (r - 1) / denom


def earth_sourced_mass_in_leo(dv: float, isp: float, dry_frac: float) -> float:
    """kg that must be in LEO (water + propellant + stage) per kg delivered."""
    p = propellant_per_payload(dv, isp, dry_frac)
    return 1 + p * (1 + dry_frac)


def lunar_sourced_water_mined(dv: float, isp: float, dry_frac: float) -> float:
    """kg of lunar water mined (payload + propellant feedstock) per kg delivered.

    The stage dry mass is hardware, not water, so it is not counted here.
    """
    return 1 + propellant_per_payload(dv, isp, dry_frac)


def table(isp: float = 450.0, dry_frac: float = 0.1) -> list[tuple[str, float, float]]:
    """(destination, kg in LEO per kg if Earth-sourced, kg mined per kg if lunar)."""
    rows = []
    for dest, dv_moon in DV_FROM_MOON_SURFACE.items():
        earth = 1.0 if dest == "LEO" else earth_sourced_mass_in_leo(DV_FROM_LEO[dest], isp, dry_frac)
        rows.append((dest, earth, lunar_sourced_water_mined(dv_moon, isp, dry_frac)))
    return rows


def _self_check() -> None:
    # zero delta-v needs no propellant
    assert propellant_per_payload(0.0, 450.0, 0.1) == 0.0
    # no tankage reduces to the plain rocket equation: p/P = R - 1
    r = math.exp(3000.0 / (G0 * 300.0))
    assert abs(propellant_per_payload(3000.0, 300.0, 0.0) - (r - 1)) < 1e-12
    # heavy tankage makes a hard leg impossible
    assert math.isinf(propellant_per_payload(9000.0, 300.0, 0.5))


if __name__ == "__main__":
    _self_check()
    isp, dry_frac = 450.0, 0.1  # H2/O2 class engine, 10% stage dry mass
    print(f"Isp {isp:.0f} s, stage dry mass {dry_frac:.0%} of propellant\n")
    print(f"{'destination':<12}{'Earth: kg in LEO per kg':>26}{'Moon: kg mined per kg':>25}")
    for dest, earth, moon in table(isp, dry_frac):
        print(f"{dest:<12}{earth:>26.2f}{moon:>25.2f}")
    print(
        "\nEarth-sourced numbers exclude the Earth-to-LEO launch, which is the"
        "\ndominant cost: every kg in LEO already paid for a 9.3 to 10 km/s ascent."
    )
